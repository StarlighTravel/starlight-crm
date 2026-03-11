import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="Starlight Travel CRM", layout="wide")

# חיבור ישיר לגיליון (ללא תלות ב-Secrets עבור הקישור)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # קריאת הגיליונות מהקישור הישיר
    deals = conn.read(spreadsheet=spreadsheet_url, worksheet="Deals")
    users = conn.read(spreadsheet=spreadsheet_url, worksheet="Users")
    settings = conn.read(spreadsheet=spreadsheet_url, worksheet="Settings")
    return deals, users, settings

try:
    df_deals, df_users, df_settings = load_data()
    
    st.title("🌟 Starlight Travel - Management System")

    # בחירת משתמש מהרשימה בגיליון Users
    if not df_users.empty:
        user_list = df_users['Email'].tolist()
        current_user_email = st.sidebar.selectbox("Select User (Login):", user_list)
        
        user_row = df_users[df_users['Email'] == current_user_email].iloc[0]
        user_role = user_row['Role']
        user_name = user_row['Full_Name']

        st.sidebar.success(f"Connected as: {user_name}")
        st.sidebar.info(f"Role: {user_role}")

        # סינון לפי תפקיד
        if user_role not in ['CEO', 'ACCOUNTANT']:
            display_deals = df_deals[df_deals['Seller_Email'] == current_user_email]
        else:
            display_deals = df_deals

        # בניית ה-Pipeline
        stages = df_settings['Pipeline_Stages'].dropna().tolist()
        cols = st.columns(len(stages))

        for i, stage in enumerate(stages):
            with cols[i]:
                st.markdown(f"### {stage}")
                stage_deals = display_deals[display_deals['Stage'] == stage]
                
                for index, row in stage_deals.iterrows():
                    with st.expander(f"👤 {row['Client_Name']}"):
                        st.write(f"📞 {row['Phone']}")
                        st.text_area("Notes", value=row['Notes'], key=f"notes_{index}")
                        
                        # כפתור וואטסאפ
                        wa_link = f"https://wa.me/{row['Country_Code']}{row['Phone']}"
                        st.link_button("💬 WhatsApp", wa_link)
    else:
        st.warning("No users found in the Users sheet.")

except Exception as e:
    st.error("Connection Error!")
    st.write("Make sure the Google Sheet is shared as 'Anyone with the link can view'.")
    st.exception(e)
