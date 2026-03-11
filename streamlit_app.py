import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page configuration
st.set_page_config(page_title="Starlight Travel CRM", layout="wide")

# Direct Connection to Spreadsheet
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Loading sheets with exact English names
    deals = conn.read(spreadsheet=spreadsheet_url, worksheet="Deals")
    users = conn.read(spreadsheet=spreadsheet_url, worksheet="Users")
    settings = conn.read(spreadsheet=spreadsheet_url, worksheet="Settings")
    return deals, users, settings

try:
    df_deals, df_users, df_settings = load_data()
    
    st.title("🌟 Starlight Travel Management")

    # User Selection / Login Simulation
    if not df_users.empty:
        user_list = df_users['Email'].tolist()
        current_user_email = st.sidebar.selectbox("Login User:", user_list)
        
        user_row = df_users[df_users['Email'] == current_user_email].iloc[0]
        user_role = user_row['Role']
        user_name = user_row['Full_Name']

        st.sidebar.success(f"User: {user_name}")
        st.sidebar.info(f"Role: {user_role}")

        # Permissions Logic
        if user_role not in ['CEO', 'ACCOUNTANT']:
            display_deals = df_deals[df_deals['Seller_Email'] == current_user_email]
        else:
            display_deals = df_deals

        # Kanban Pipeline Construction
        stages = df_settings['Pipeline_Stages'].dropna().tolist()
        cols = st.columns(len(stages))

        for i, stage in enumerate(stages):
            with cols[i]:
                st.markdown(f"### {stage}")
                stage_deals = display_deals[display_deals['Stage'] == stage]
                
                for index, row in stage_deals.iterrows():
                    with st.expander(f"👤 {row['Client_Name']}"):
                        st.write(f"**Phone:** {row['Phone']}")
                        st.write(f"**Source:** {row['Source']}")
                        
                        # Client Notes Area
                        st.text_area("Notes", value=row['Notes'], key=f"notes_{index}")
                        
                        # WhatsApp Automation Button
                        wa_number = str(row['Country_Code']) + str(row['Phone'])
                        wa_link = f"https://wa.me/{wa_number.replace('+', '')}"
                        st.link_button("💬 Send WhatsApp", wa_link)
                        
                        # Drive Link (if exists)
                        if pd.notnull(row['Drive_Link']):
                            st.link_button("📁 Open Folder", row['Drive_Link'])
    else:
        st.warning("Data loading failed: Check Users sheet.")

except Exception as e:
    st.error("System Error")
    st.write("Ensure spreadsheet sharing is set to 'Anyone with the link can view'")
    st.exception(e)
