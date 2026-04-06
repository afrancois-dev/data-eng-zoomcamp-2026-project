import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery

st.set_page_config(
    page_title="MMA fight analytics",
    page_icon=":punch:",
    layout="wide",
)

st.markdown("""
<div style="text-align: center;">
    <h1>MMA Fight Analytics 🥊</h1>
    <p>Explore UFC results and fighter statistics since 1994.</p>
</div>
""", unsafe_allow_html=True)

# Authentication flow
if not st.user.is_logged_in:
    st.markdown("""
    <div style="text-align: center;">
        <p>Veuillez vous connecter pour accéder aux analyses.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Log in with Google", on_click=st.login, use_container_width=True)
    st.stop()

# Logout button in the sidebar
with st.sidebar:
    st.write(f"Connecté en tant que : **{st.user.name}**")
    st.button("Log out", on_click=st.logout)

# BigQuery client
@st.cache_resource
def get_bq_client():
    # Streamlit Cloud can use a Service Account JSON key for simplicity
    if "gcp_service_account" in st.secrets:
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        return bigquery.Client(credentials=credentials, project=credentials.project_id)
    
    # Fallback for local dev
    return bigquery.Client()

def run_query(query):
    client = get_bq_client()
    return client.query(query).to_dataframe()

# Load summary statistics
@st.cache_data(ttl=3600)
def load_summary():
    query = """
    SELECT 
        (SELECT COUNT(DISTINCT fighter_sk) FROM `dwh.dim_fighters` WHERE _is_current = true) as total_fighters,
        (SELECT COUNT(*) FROM `dwh.fact_bouts`) as total_bouts,
        (SELECT COUNT(DISTINCT event_sk) FROM `dwh.dim_events` WHERE _is_current = true) as total_events
    """
    return run_query(query)

try:
    summary = load_summary()
    st.markdown("<h3 style='text-align: center;'>Quick stats</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fighters 🥋", summary['total_fighters'][0])
    with col2:
        st.metric("Total Bouts ⚔️", summary['total_bouts'][0])
    with col3:
        st.metric("Events 🏟️", summary['total_events'][0])

    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        [data-testid="stMetricLabel"] {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error connecting to BigQuery: {e}")
    st.info("Check project/dataset access or environment setup.")
    st.stop()

st.divider()

# 1. Fighter search
st.markdown("<h2 style='text-align: center;'>Fighter profile</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_fighter_list():
    return run_query("SELECT DISTINCT fighter_sk, CONCAT(first_name, ' ', last_name) as full_name FROM `dwh.dim_fighters` WHERE _is_current = true ORDER BY full_name")

fighters_df = get_fighter_list()

# Add all option
fighter_options = ["All Fighters"] + fighters_df['full_name'].tolist()
_, search_col, _ = st.columns([1, 2, 1])
with search_col:
    selected_fighter_name = st.selectbox("Select a fighter", fighter_options)

if selected_fighter_name != "All Fighters":
    selected_fighter_id = fighters_df[fighters_df['full_name'] == selected_fighter_name]['fighter_sk'].values[0]
else:
    selected_fighter_id = None

@st.cache_data(ttl=3600)
def get_fighter_details(f_id):
    if f_id is None:
        return pd.DataFrame()
    return run_query(f"SELECT * FROM `dwh.dim_fighters` WHERE fighter_sk = {f_id} AND _is_current = true")

fighter_details = get_fighter_details(selected_fighter_id)

if selected_fighter_id and not fighter_details.empty:
    f = fighter_details.iloc[0]
    _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
    c1.info(f"**Nickname:** {f['nick_name'] or 'N/A'}")
    c2.info(f"**Height:** {f['height']}")
    c3.info(f"**Weight:** {f['weight']}")
    st.markdown(f"<div style='text-align: center;'><strong>Wins recorded:</strong> {f['wins']}</div>", unsafe_allow_html=True)
elif selected_fighter_name == "All Fighters":
    st.markdown("<div style='text-align: center;'><em>Showing global statistics for all fighters.</em></div>", unsafe_allow_html=True)

# bouts
if selected_fighter_id:
    st.markdown("<h3 style='text-align: center;'>Recent bouts</h3>", unsafe_allow_html=True)

    @st.cache_data(ttl=3600)
    def get_recent_bouts(f_id):
        query = f"""
        SELECT 
            b.date,
            e.name as event_name,
            b.weight_class,
            b.method,
            CASE 
                WHEN b.winner_sk = {f_id} THEN 'WIN' 
                WHEN b.winner_sk IS NULL THEN 'DRAW/NC'
                ELSE 'LOSS' 
            END as result
        FROM `dwh.fact_bouts` b
        JOIN `dwh.dim_events` e ON b.event_sk = e.event_sk
        WHERE b.fighter_1_sk = {f_id} OR b.fighter_2_sk = {f_id}
        ORDER BY b.date DESC
        LIMIT 10
        """
        return run_query(query)

    bouts = get_recent_bouts(selected_fighter_id)
    if not bouts.empty:
        st.dataframe(bouts, width="stretch")
        
        # win/loss Chart
        st.markdown("<h4 style='text-align: center;'>Win/Loss distribution</h4>", unsafe_allow_html=True)
        res_counts = bouts['result'].value_counts().reset_index()
        res_counts.columns = ['result', 'count']
        
        # Color mapping for results
        color_scale = alt.Scale(
            domain=['WIN', 'LOSS', 'DRAW/NC'],
            range=['#28a745', '#dc3545', '#ffc107']
        )
        
        wl_chart = alt.Chart(res_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="count", type="quantitative"),
            color=alt.Color(field="result", type="nominal", scale=color_scale),
            tooltip=['result', 'count']
        ).properties(height=300)
        
        st.altair_chart(wl_chart, width="stretch")
    else:
        st.write("No bouts found.")

st.divider()

# Bouts by weight class over time
st.markdown("<h2 style='text-align: center;'>Bouts by weight class over time</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_global_wc_timeline(f_id=None):
    where_clause = ""
    if f_id:
        where_clause = f"WHERE fighter_1_sk = {f_id} OR fighter_2_sk = {f_id}"
    return run_query(f"""
        SELECT 
            DATE_TRUNC(date, QUARTER) as period, 
            weight_class,
            CASE 
                WHEN LOWER(weight_class) LIKE '%women%' THEN 'Women'
                ELSE 'Men'
            END as gender_group,
            COUNT(*) as bout_count 
        FROM `dwh.fact_bouts` 
        {where_clause}
        GROUP BY period, weight_class, gender_group
        ORDER BY period
    """)

global_wc_timeline = get_global_wc_timeline(selected_fighter_id)

if not global_wc_timeline.empty:
    g_gender_filter = st.radio("Filter by gender group", ["All", "Men", "Women"], horizontal=True, key="global_gender_filter")
    
    g_plot_df = global_wc_timeline
    if g_gender_filter != "All":
        g_plot_df = global_wc_timeline[global_wc_timeline['gender_group'] == g_gender_filter]

    g_line_chart = alt.Chart(g_plot_df).mark_line(point=True).encode(
        x=alt.X('period:T', title='Quarter'),
        y=alt.Y('bout_count:Q', title='Number of Bouts'),
        color=alt.Color('weight_class:N', title='Weight class'),
        strokeDash=alt.StrokeDash('gender_group:N', title='Group'),
        tooltip=['period', 'weight_class', 'gender_group', 'bout_count']
    ).properties(height=400).interactive()
    
    st.altair_chart(g_line_chart, width="stretch")

st.divider()

# Bouts distribution (timeline)
st.markdown("<h2 style='text-align: center;'>Bouts distribution</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_timeline_stats(f_id=None):
    where_clause = ""
    if f_id:
        where_clause = f"WHERE fighter_1_sk = {f_id} OR fighter_2_sk = {f_id}"
    return run_query(f"""
        SELECT 
            DATE_TRUNC(date, MONTH) as month, 
            COUNT(*) as bout_count 
        FROM `dwh.fact_bouts` 
        {where_clause}
        GROUP BY month 
        ORDER BY month
    """)

timeline_stats = get_timeline_stats(selected_fighter_id)

# Histogram (bar chart)
hist_chart = alt.Chart(timeline_stats).mark_bar(color='#FF4B4B').encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y('bout_count:Q', title='Number of Bouts'),
    tooltip=['month', 'bout_count']
).properties(height=300)

st.altair_chart(hist_chart, width="stretch")

st.divider()

# Weight class distribution
st.markdown("<h2 style='text-align: center;'>Weight class distribution</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_wc_stats(f_id=None):
    where_clause = ""
    if f_id:
        where_clause = f"WHERE fighter_1_sk = {f_id} OR fighter_2_sk = {f_id}"
    return run_query(f"SELECT weight_class, COUNT(*) as bout_count FROM `dwh.fact_bouts` {where_clause} GROUP BY weight_class ORDER BY bout_count DESC")

wc_stats = get_wc_stats(selected_fighter_id)
chart = alt.Chart(wc_stats).mark_bar().encode(
    x=alt.X('bout_count:Q'),
    y=alt.Y('weight_class:N', sort='-x'),
    color='weight_class:N'
)
st.altair_chart(chart, width="stretch")

