import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Starlight CRM", layout="wide")

# 2. Connection Settings
# Replace with your actual Google Sheet URL
URL = "https://docs.google.com/spreadsheets/d/1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI/edit?usp=sharing"

def load_data(conn):
    """Loads all required sheets with error handling."""
    try:
        deals = conn.read(spreadsheet=URL, worksheet="Deals")
        users = conn.read(spreadsheet=URL, worksheet="Users")
        settings = conn.read(spreadsheet=URL, worksheet="Settings")
        return deals, users, settings
    except Exception as e:
        st.error(f"Error loading sheets: {e}")
        return None, None, None

# 3. Main Application Logic
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_deals, df_users, df_settings = load_data(conn)

    if df_deals is not None:
        st.title("🌟 Starlight Travel Management")

        # Sidebar - User Login Simulation
        st.sidebar.header("User Access")
        if not df_users.empty:
            user_list = df_users['Email'].tolist()
            selected_user = st.sidebar.selectbox("Select Login Email:", user_list)
            
            user_info = df_users[df_users['Email'] == selected_user].iloc[0]
            st.sidebar.success(f"Welcome, {user_info['Full_Name']}")
            st.sidebar.info(f"Role: {user_info['Role']}")

            # Filter data based on Role
            if user_info['Role'] not in ['CEO', 'ACCOUNTANT']:
                mask = df_deals['Seller_Email'] == selected_user
                display_df = df_deals[mask]
            else:
                display_df = df_deals

            # 4. Kanban Pipeline Display
            if 'Pipeline_Stages' in df_settings.columns:
                stages = df_settings['Pipeline_Stages'].dropna().tolist()
                cols = st.columns(len(stages))

                for i, stage in enumerate(stages):
                    with cols[i]:
                        st.markdown(f"### {stage}")
                        # Filter deals for this specific stage
                        stage_deals = display_df[display_df['Stage'] == stage]
                        
                        for index, row in stage_deals.iterrows():
                            with st.expander(f"👤 {row['Client_Name']}"):
                                st.write(f"**Phone:** {row['Phone']}")
                                
                                # Notes management
                                st.text_area("Notes", value=row['Notes'], key=f"notes_{index}")
                                
                                # WhatsApp Button
                                wa_link = f"https://wa.me/{str(row['Country_Code'])}{str(row['Phone'])}"
                                st.link_button("💬 WhatsApp", wa_link)
            else:
                st.warning("Column 'Pipeline_Stages' not found in Settings sheet.")
        else:
            st.warning("No users found in the 'Users' sheet.")

except Exception as e:
    st.error("Global System Error")
    st.exception(e)
