import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# הגדרות דף
st.set_page_config(page_title="Starlight Travel CRM", layout="wide")

# חיבור ל-Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# פונקציה לטעינת נתונים
def load_data():
    deals = conn.read(worksheet="Deals")
    users = conn.read(worksheet="Users")
    settings = conn.read(worksheet="Settings")
    return deals, users, settings

try:
    df_deals, df_users, df_settings = load_data()
    
    st.title("🌟 Starlight Travel - Pipeline")

    # בחירת משתמש (סימולציה של לוגין)
    user_list = df_users['Email'].tolist()
    current_user_email = st.sidebar.selectbox("Login as:", user_list)
    user_row = df_users[df_users['Email'] == current_user_email].iloc[0]
    user_role = user_row['Role']
    user_name = user_row['Full_Name']

    st.sidebar.write(f"Logged in as: **{user_name}** ({user_role})")

    # סינון לפי מוכר (אם לא CEO)
    if user_role not in ['CEO', 'ACCOUNTANT']:
        display_deals = df_deals[df_deals['Seller_Email'] == current_user_email]
    else:
        display_deals = df_deals

    # לוח קנבן
    stages = df_settings['Pipeline_Stages'].dropna().tolist()
    cols = st.columns(len(stages))

    for i, stage in enumerate(stages):
        with cols[i]:
            st.markdown(f"### {stage}")
            stage_deals = display_deals[display_deals['Stage'] == stage]
            
            for index, row in stage_deals.iterrows():
                with st.expander(f"👤 {row['Client_Name']}"):
                    st.write(f"📞 {row['Phone']}")
                    
                    # הצגת הערות ועדכון
                    new_notes = st.text_area("Notes", value=row['Notes'], key=f"notes_{index}")
                    
                    # אוטומציות
                    if st.button("📁 Create Folder (Seller Specific)", key=f"folder_{index}"):
                        st.info(f"Connecting to Drive... Target: Drives/{user_name}/{row['Client_Name']}")
                    
                    # אם בשלב BOOKED - הצגת משימות (סימולציה)
                    if stage == "BOOKED":
                        st.warning("📋 Tasks: Check Insurance, Visa, Hotel")

                    if st.button("Save Changes", key=f"save_{index}"):
                        st.success("Updating Spreadsheet...")
                        # כאן תבוא פונקציית העדכון לשיטס

except Exception as e:
    st.error("Please connect your Google Sheet in 'Advanced Settings' -> 'Secrets'")
    st.write(e)
