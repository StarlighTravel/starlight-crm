import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page config
st.set_page_config(page_title="Starlight CRM", layout="wide")

# The URL of your Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI/edit?usp=sharing"

# Initialize Connection
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Load all sheets
    deals = conn.read(spreadsheet=SHEET_URL, worksheet="Deals")
    users = conn.read(spreadsheet=SHEET_URL, worksheet="Users")
    settings = conn.read(spreadsheet=SHEET_URL, worksheet="Settings")
    tasks = conn.read(spreadsheet=SHEET_URL, worksheet="Tasks")
    return deals, users, settings, tasks

try:
    df_deals, df_users, df_settings, df_tasks = load_data()
    
    st.title("🌟 Starlight Travel - Management System")

    # Sidebar Login Simulation
    if not df_users.empty:
        user_list = df_users['Email'].tolist()
        current_user = st.sidebar.selectbox("Select User (Login):", user_list)
        
        user_data = df_users[df_users['Email'] == current_user].iloc[0]
        st.sidebar.success(f"Welcome, {user_data['Full_Name']}")
        
        # Pipeline Filter by Role
        if user_data['Role'] not in ['CEO', 'ACCOUNTANT']:
            display_deals = df_deals[df_deals['Seller_Email'] == current_user]
        else:
            display_deals = df_deals

        # Kanban Board UI
        if 'Pipeline_Stages' in df_settings.columns:
            stages = df_settings['Pipeline_Stages'].dropna().tolist()
            cols = st.columns(len(stages))

            for i, stage in enumerate(stages):
                with cols[i]:
                    st.markdown(f"### {stage}")
                    # Filter deals for this stage
                    stage_deals = display_deals[display_deals['Stage'] == stage]
                    
                    for index, row in stage_deals.iterrows():
                        with st.expander(f"👤 {row['Client_Name']}"):
                            st.write(f"📞 {row['Phone']}")
                            
                            # Display Tasks for this specific client
                            if not df_tasks.empty:
                                client_tasks = df_tasks[df_tasks['Client_Name'] == row['Client_Name']]
                                if not client_tasks.empty:
                                    st.markdown("**Tasks:**")
                                    for _, t in client_tasks.iterrows():
                                        icon = "✅" if t['Status'] == 'Done' else "⏳"
                                        st.write(f"{icon} {t['Task_Description']}")
                            
                            st.markdown("---")
                            # Notes & WhatsApp
                            st.text_area("Notes", value=row['Notes'], key=f"notes_{index}")
                            wa_link = f"https://wa.me/{str(row['Country_Code'])}{str(row['Phone'])}"
                            st.link_button("💬 WhatsApp", wa_link)
        else:
            st.error("Missing 'Pipeline_Stages' column in Settings sheet.")
            
except Exception as e:
    st.error("System is initializing or Connection error.")
    st.info("Make sure Google Sheet is shared as 'Anyone with the link can EDIT'")
    st.exception(e)
