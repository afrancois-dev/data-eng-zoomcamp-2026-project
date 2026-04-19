import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
from google.oauth2 import service_account

st.set_page_config(
    page_title="MMA fight analytics",
    page_icon=":punch:",
    layout="wide",
)

st.markdown("""
<div style="text-align: center;">
    <h1>MMA fight analytics 🥊</h1>
    <p>Explore UFC results and fighter statistics since 1994.</p>
</div>
""", unsafe_allow_html=True)

# BigQuery client
@st.cache_resource
def get_bq_client():
    # streamlit cloud can use a sa json key stored in secrets
    try:
        return bigquery.Client(
            credentials=service_account.Credentials.from_service_account_info(
                st.secrets["mma_stats_ui_sa"]
            ),
        )
    except Exception:
        # fallback for local dev (using gcloud auth)
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
        st.metric("Total bouts ⚔️", summary['total_bouts'][0])
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

# Add all option with multi-selection
fighter_options = fighters_df['full_name'].tolist()
_, search_col, _ = st.columns([1, 2, 1])
with search_col:
    selected_fighter_names = st.multiselect("Select one or more fighters", fighter_options, placeholder="Type to search...")

# Get IDs for selected fighters
if selected_fighter_names:
    selected_fighter_ids = fighters_df[fighters_df['full_name'].isin(selected_fighter_names)]['fighter_sk'].tolist()
else:
    selected_fighter_ids = []

@st.cache_data(ttl=3600)
def get_fighters_details(f_ids):
    if not f_ids:
        return pd.DataFrame()
    ids_str = ",".join(map(str, f_ids))
    return run_query(f"SELECT *, CONCAT(first_name, ' ', last_name) as full_name FROM `dwh.dim_fighters` WHERE fighter_sk IN ({ids_str}) AND _is_current = true")

fighters_details = get_fighters_details(selected_fighter_ids)

if selected_fighter_ids and not fighters_details.empty:
    for _, f in fighters_details.iterrows():
        with st.expander(f"👤 {f['full_name']}", expanded=True):
            _, c1, c2, c3, _ = st.columns([1, 2, 2, 2, 1])
            c1.info(f"**Nickname:** {f['nick_name'] or 'N/A'}")
            c2.info(f"**Height:** {f['height']}")
            c3.info(f"**Weight:** {f['weight']}")
            st.markdown(f"<div style='text-align: center;'><strong>Wins recorded:</strong> {f['wins']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center;'><em>Showing global statistics for all fighters.</em></div>", unsafe_allow_html=True)

# bouts
if selected_fighter_ids:
    st.markdown("<h3 style='text-align: center;'>Recent bouts</h3>", unsafe_allow_html=True)

    @st.cache_data(ttl=3600)
    def get_recent_bouts(f_ids):
        if not f_ids:
            return pd.DataFrame()
        ids_str = ",".join(map(str, f_ids))
        query = f"""
        WITH fighter_bouts AS (
            SELECT 
                b.date,
                e.name as event_name,
                b.weight_class,
                b.method,
                f.fighter_sk,
                CONCAT(f.first_name, ' ', f.last_name) as fighter,
                CASE 
                    WHEN b.winner_sk = f.fighter_sk THEN 'WIN' 
                    WHEN b.winner_sk IS NULL THEN 'DRAW/NC'
                    ELSE 'LOSS' 
                END as result
            FROM `dwh.fact_bouts` b
            JOIN `dwh.dim_events` e ON b.event_sk = e.event_sk
            JOIN `dwh.dim_fighters` f ON (b.fighter_1_sk = f.fighter_sk OR b.fighter_2_sk = f.fighter_sk)
            WHERE f.fighter_sk IN ({ids_str})
        )
        SELECT * FROM fighter_bouts
        ORDER BY date DESC
        LIMIT 100
        """
        return run_query(query)

    bouts = get_recent_bouts(selected_fighter_ids)
    if not bouts.empty:
        st.dataframe(bouts, width="stretch")
        
        # win/loss Chart
        st.markdown("<h4 style='text-align: center;'>Combined Win/Loss distribution</h4>", unsafe_allow_html=True)
        res_counts = bouts.groupby(['result']).size().reset_index(name='count')
        
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
        
        st.altair_chart(wl_chart, use_container_width=True)
    else:
        st.write("No bouts found.")

st.divider()

# Bouts over time
st.markdown("<h2 style='text-align: center;'>Bouts over time</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_global_bouts_timeline(f_ids=[]):
    where_clause = ""
    fighter_select = ""
    group_by = "period, weight_class, gender_group, method"
    
    if f_ids:
        ids_str = ",".join(map(str, f_ids))
        where_clause = f"""
            JOIN `dwh.dim_fighters` f ON (b.fighter_1_sk = f.fighter_sk OR b.fighter_2_sk = f.fighter_sk)
            WHERE f.fighter_sk IN ({ids_str})
        """
        fighter_select = "CONCAT(f.first_name, ' ', f.last_name) as fighter_name,"
        group_by = "fighter_name, " + group_by

    return run_query(f"""
        SELECT 
            {fighter_select}
            DATE_TRUNC(date, QUARTER) as period, 
            weight_class,
            method,
            CASE 
                WHEN LOWER(weight_class) LIKE '%women%' THEN 'Women'
                ELSE 'Men'
            END as gender_group,
            COUNT(*) as bout_count 
        FROM `dwh.fact_bouts` b
        {where_clause}
        GROUP BY {group_by}
        ORDER BY period
    """)

global_bouts_timeline = get_global_bouts_timeline(selected_fighter_ids)

if not global_bouts_timeline.empty:
    tab1, tab2 = st.tabs(["By weight class", "By method"])
    
    with tab1:
        g_gender_filter = st.radio("Filter by gender group", ["All", "Men", "Women"], horizontal=True, key="wc_gender_filter")
        
        g_plot_df = global_bouts_timeline
        if g_gender_filter != "All":
            g_plot_df = global_bouts_timeline[global_bouts_timeline['gender_group'] == g_gender_filter]

        # If fighters are selected, we separate by fighter name
        color_field = 'fighter_name:N' if selected_fighter_ids else 'weight_class:N'
        tooltip_list = ['period', 'weight_class', 'gender_group', 'bout_count']
        if selected_fighter_ids:
            tooltip_list.insert(0, 'fighter_name')

        g_line_chart = alt.Chart(g_plot_df).mark_line(point=True).encode(
            x=alt.X('period:T', title='Quarter'),
            y=alt.Y('sum(bout_count):Q', title='Number of Bouts'),
            color=alt.Color(color_field, title='Split', legend=alt.Legend(
                columns=2,
                symbolLimit=50,
                labelFontSize=10,
                titleFontSize=12
            )),
            strokeDash=alt.StrokeDash('gender_group:N', title='Group'),
            tooltip=tooltip_list
        ).properties(height=500).interactive()
        
        st.altair_chart(g_line_chart, use_container_width=True)

    with tab2:
        m_gender_filter = st.radio("Filter by gender group", ["All", "Men", "Women"], horizontal=True, key="method_gender_filter")
        
        m_plot_df = global_bouts_timeline
        if m_gender_filter != "All":
            m_plot_df = global_bouts_timeline[global_bouts_timeline['gender_group'] == m_gender_filter]

        # Color by method or fighter
        m_color_field = 'fighter_name:N' if selected_fighter_ids else 'method:N'
        m_tooltip_list = ['period', 'method', 'bout_count']
        if selected_fighter_ids:
            m_tooltip_list.insert(0, 'fighter_name')

        m_bar_chart = alt.Chart(m_plot_df).mark_bar().encode(
            x=alt.X('period:T', title='Quarter'),
            y=alt.Y('sum(bout_count):Q', title='Number of Bouts'),
            color=alt.Color(m_color_field, title='Split', legend=alt.Legend(
                columns=2,
                symbolLimit=50,
                labelFontSize=10,
                titleFontSize=12
            )),
            tooltip=m_tooltip_list
        ).properties(height=500).interactive()
        
        st.altair_chart(m_bar_chart, use_container_width=True)

st.divider()

# Bouts distribution (timeline)
st.markdown("<h2 style='text-align: center;'>Bouts distribution</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_timeline_stats(f_ids=[]):
    where_clause = ""
    fighter_select = ""
    group_by = "month"
    if f_ids:
        ids_str = ",".join(map(str, f_ids))
        where_clause = f"""
            JOIN `dwh.dim_fighters` f ON (b.fighter_1_sk = f.fighter_sk OR b.fighter_2_sk = f.fighter_sk)
            WHERE f.fighter_sk IN ({ids_str})
        """
        fighter_select = "CONCAT(f.first_name, ' ', f.last_name) as fighter_name,"
        group_by = "fighter_name, month"
    return run_query(f"""
        SELECT 
            {fighter_select}
            DATE_TRUNC(date, MONTH) as month, 
            COUNT(*) as bout_count 
        FROM `dwh.fact_bouts` b
        {where_clause}
        GROUP BY {group_by}
        ORDER BY month
    """)

timeline_stats = get_timeline_stats(selected_fighter_ids)

# Histogram (bar chart)
color_enc = alt.Color('fighter_name:N') if selected_fighter_ids else alt.value('#FF4B4B')
tooltip_list = ['month', 'bout_count']
if selected_fighter_ids:
    tooltip_list.insert(0, 'fighter_name')

hist_chart = alt.Chart(timeline_stats).mark_bar().encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y('bout_count:Q', title='Number of Bouts'),
    color=color_enc,
    tooltip=tooltip_list
).properties(height=300)

st.altair_chart(hist_chart, use_container_width=True)

st.divider()

# Weight class distribution
st.markdown("<h2 style='text-align: center;'>Weight class distribution</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_wc_stats(f_ids=[]):
    where_clause = ""
    fighter_select = ""
    group_by = "weight_class"
    if f_ids:
        ids_str = ",".join(map(str, f_ids))
        where_clause = f"""
            JOIN `dwh.dim_fighters` f ON (b.fighter_1_sk = f.fighter_sk OR b.fighter_2_sk = f.fighter_sk)
            WHERE f.fighter_sk IN ({ids_str})
        """
        fighter_select = "CONCAT(f.first_name, ' ', f.last_name) as fighter_name,"
        group_by = "fighter_name, weight_class"
    return run_query(f"""
        SELECT 
            {fighter_select}
            weight_class, 
            COUNT(*) as bout_count 
        FROM `dwh.fact_bouts` b
        {where_clause}
        GROUP BY {group_by}
        ORDER BY bout_count DESC
    """)

wc_stats = get_wc_stats(selected_fighter_ids)

color_enc = alt.Color('fighter_name:N') if selected_fighter_ids else alt.Color('weight_class:N')
x_offset = alt.XOffset('fighter_name:N') if selected_fighter_ids else alt.value(0)

chart = alt.Chart(wc_stats).mark_bar().encode(
    y=alt.Y('weight_class:N', sort='-x'),
    x=alt.X('bout_count:Q'),
    color=color_enc,
    xOffset=x_offset,
    tooltip=['weight_class', 'bout_count'] + (['fighter_name'] if selected_fighter_ids else [])
).properties(height=alt.Step(20) if not selected_fighter_ids else 400)

st.altair_chart(chart, use_container_width=True)

