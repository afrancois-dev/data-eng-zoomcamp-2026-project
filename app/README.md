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


## Development Journey
- first day 
    - set up everything
        - linting, formating, typing
        - install
    - devex
    - bruin : only fighters, and just getting bouts and events raw data.
        - raw/
            - staging/
                - dwh/ (just thinking about the structure with the minimum fiels i.e first_name, last_name, nick_name and wins for fighters to have an end to end pipeline already)
    - 


- second day
    - data modeling
        - modeling events, bouts, fighters
            - identifying fact and dim
            - finding suitable surrogate_key candidates
            - use scd2 whenever possible
            - use macros
