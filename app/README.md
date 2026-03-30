# MMA Stats - Bruin Data Pipeline 🥊

This project is a modern data platform for MMA (UFC) statistics analysis, built with **Bruin**, **DuckDB**, and **SCD2** principles.

## Project Architecture

The pipeline is organized into three distinct layers:

1.  **Raw (Sources)**: Python scrapers that extract raw data for bouts, events, and fighters.
2.  **Staging**: Initial cleaning and generation of deterministic **Surrogate Keys** (MD5) to ensure pipeline integrity.
3.  **DWH (Data Warehouse)**:
    *   `dim_fighters`: A **SCD2** (Slowly Changing Dimension Type 2) dimension to track fighter evolution (weight, record) over time.
    *   `dim_events`: UFC events dimension.
    *   `fact_bouts`: Central fact table gathering all bout results.

## Configuration

The project uses DuckDB as a local storage engine for local env. The configuration can be found in `.bruin.yml`.

### Quick Setup

1.  Ensure Bruin CLI is installed.
2.  Validate the project:
    ```bash
    bruin validate .
    ```

## Usage

### Run the complete pipeline
```bash
bruin run .
```

### Initialize SCD2 (Full Refresh)
For the first run of the historical fighter dimension:
```bash
bruin run --full-refresh assets/dwh/dim_fighters.sql
```

## Assets Structure

*   **Ingestion**: `assets/raw/*.py`
*   **Staging**: `assets/staging/*.sql`
*   **Analytics**: `assets/dwh/*.sql`
