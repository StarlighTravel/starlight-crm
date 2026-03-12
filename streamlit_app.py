import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Settings
st.set_page_config(page_title="Starlight CRM - Pro", layout="wide")

# 2. Spreadsheet Link
url = "https://docs.google.com/spreadsheets/d/1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI/edit?usp=sharing"

# 3. Connect (Using the simple connection)
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    deals = conn.read(spreadsheet=url, worksheet="Deals")
    users = conn.read(spreadsheet=url, worksheet="Users")
    settings = conn.read(spreadsheet=url, worksheet="Settings")
    tasks = conn.read(spreadsheet=url, worksheet="Tasks")
    return deals, users, settings, tasks

try:
    df_deals, df_users, df_settings, df_tasks = load_data()
    
    st.title("🌟 Starlight Travel Management")

    # Sidebar - Login
    user_list = df_users['Email'].tolist()
    selected_user = st.sidebar.selectbox("User Login:", user_list)
    
    # Kanban Board
    stages = df_settings['Pipeline_Stages'].dropna().tolist()
    cols = st.columns(len(stages))

    for i, stage in enumerate(stages):
        with cols[i]:
            st.markdown(f"### {stage}")
            stage_deals = df_deals[df_deals['Stage'] == stage]
            
            for index, row in stage_deals.iterrows():
                with st.expander(f"👤 {row['Client_Name']}"):
                    st.write(f"**Phone:** {row['Phone']}")
                    
                    # Show Tasks for this client
                    if not df_tasks.empty:
                        client_tasks = df_tasks[df_tasks['Client_Name'] == row['Client_Name']]
                        for _, t in client_tasks.iterrows():
                            st.write(f"Task: {t['Task_Description']} ({t['Status']})")
                    
                    # Manual Note Update (Simulated for now)
                    note = st.text_area("Update Notes", value=row['Notes'], key=f"note_{index}")
                    
                    if st.button("Save Note", key=f"btn_{index}"):
                        st.success("Note saved to logic! (Link to Sheet active)")
                        # כאן נוסיף את פקודת העדכון ברגע שהממשק יציג נתונים

except Exception as e:
    st.error("Connection Error. Please ensure the Google Sheet is shared as 'Editor'.")
    st.write(e)
