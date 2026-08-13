import os
import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load secure enterprise environment configurations
load_dotenv()

st.set_page_config(
    page_title="DataPulse-AI | Compliance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and Status Badges
st.title("📊 DataPulse-AI Workforce Insights")
st.subheader("Enterprise Operations & Compliance Monitoring Console")
st.markdown("---")

def get_db_connection():
    # Establish link directly to the localized PostgreSQL container
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "datapulse_admin"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "datapulse_warehouse")
    )

try:
    conn = get_db_connection()
    
    # Ingest historical database logs into a structured Pandas DataFrame
    query = "SELECT log_id, employee_name, department, assigned_hours, shift_notes FROM raw_workforce_logs;"
    df = pd.read_sql(query, conn)
    conn.close()

    # Upper Summary KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Logged Personnel", value=len(df))
    with col2:
        total_hours = int(df['assigned_hours'].sum())
        st.metric(label="Total Tracked Operational Hours", value=f"{total_hours} hrs")
    with col3:
        overtime_incidents = len(df[df['assigned_hours'] > 40])
        st.metric(label="High Burnout Flagged Roles (>40h)", value=overtime_incidents)

    st.markdown("### 📋 Active Workforce Database Staging Rows")
    # Display an interactive, clean data grid representing our dbt/warehouse layer
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Unable to query local database warehouse instance: {str(e)}")
    st.info("Ensure your container environment is running via: 'docker compose up -d'")
