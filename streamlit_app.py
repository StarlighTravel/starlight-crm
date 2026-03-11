import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Starlight CRM", layout="wide")

# Correct Export URL for Google Sheets
# This format ensures pandas can read the sheet directly
SHEET_ID = "1sACSy-IQY6rl3mw8A6l1JgyPCpFShRN326-_-KcVEJI"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60)
def load_data(sheet_name):
    url = f"{BASE_URL}&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {e}")
        return pd.DataFrame()

# Main App
st.title("🌟 Starlight Travel Management")

df_deals = load_data("Deals")
df_users = load_data("Users")
df_settings = load_data("Settings")

if not df_deals.empty and not df_users.empty:
    # Sidebar Login
    user_list = df_users['Email'].tolist()
    selected_user = st.sidebar.selectbox("Login Email:", user_list)
    
    user_info = df_users[df_users['Email'] == selected_user].iloc[0]
    st.sidebar.success(f"Welcome, {user_info['Full_Name']}")

    # Dashboard Logic
    if 'Pipeline_Stages' in df_settings.columns:
        stages = df_settings['Pipeline_Stages'].dropna().tolist()
        cols = st.columns(len(stages))

        for i, stage in enumerate(stages):
            with cols[i]:
                st.markdown(f"### {stage}")
                stage_deals = df_deals[df_deals['Stage'] == stage]
                
                for _, row in stage_deals.iterrows():
                    with st.expander(f"👤 {row['Client_Name']}"):
                        st.write(f"Phone: {row['Phone']}")
                        st.text_area("Notes", value=row['Notes'], key=f"n_{row.name}")
                        
                        wa_link = f"https://wa.me/{str(row['Country_Code'])}{str(row['Phone'])}"
                        st.link_button("💬 WhatsApp", wa_link)
else:
    st.warning("Please check if Sheet Tabs are named exactly: Deals, Users, Settings")
