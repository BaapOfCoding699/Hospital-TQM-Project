import streamlit as st
import db
import pandas as pd
import io
import datetime

db.init_db()
# Header & Toggle
col_title, col_toggle = st.columns([4, 1])
with col_title:
    st.title("🏥 Hospital Management System")
with col_toggle:
    dark_mode = st.toggle("Dark Mode", value=True)

# Theme Palette (Slate Dark vs Clean Light)
if dark_mode:
    bg_app = "#0f172a"
    card_bg = "#1e293b"
    border = "#334155"
    text = "#f8fafc"
    accent = "#0284c7"
else:
    bg_app = "#f8fafc"
    card_bg = "#ffffff"
    border = "#cbd5e1"
    text = "#0f172a"
    accent = "#0284c7"

# Clean CSS Injection
st.markdown(
    f"""
    <style>
    /* Background & Main Typography */
    .stApp {{
        background-color: {bg_app} !important;
    }}
    .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp p, .stApp span {{
        color: {text} !important;
    }}

    /* Cards & Forms */
    div[data-testid="stMetric"], div[data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        padding: 14px !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {accent} !important;
        font-weight: 700 !important;
    }}

    /* Inputs, Selectboxes, and Steppers */
    div[data-baseweb="input"],
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stNumberInput"] button {{
        background-color: {card_bg} !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        border-radius: 6px !important;
    }}
    div[data-testid="stNumberInput"] button svg {{
        fill: {text} !important;
    }}

    /* Buttons */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {{
        background-color: {accent} !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
data = db.get_patients()
if data:
    total_Patients = len(data)
    ages = [row[2] for row in data]
    avg_age = round(sum(ages) / len(ages) , 1)
    disease = [ row[3] for row in data]
    top_disease = max(set(disease) , key = disease.count)
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.metric( label="Total Patients" , value=total_Patients)
    with col2:
        st.metric( label="Average Age" , value=f"{avg_age} yrs")
    with col3:
        st.metric( label="Most Common Disease" , value=top_disease)

tab1 , tab2 ,  tab3 , tab4 = st.tabs(["View Patient Record" , "Add Patient Record" , "Update Patient Record" , "Delete Patient Record"])

# --- Tab 1: View & Filter Records ---
with tab1:
    data = db.get_patients()
    if data:
        df = pd.DataFrame(data, columns=["Patient ID", "Name", "Age", "Disease", "Admission Date"])
        
        # ---> REPLACE FROM HERE DOWN TO st.dataframe(...) <---
        col_search, col_date = st.columns([1.5, 1])
        with col_search:
            search_query = st.text_input("🔍 Search By Patient Name or Disease")
        with col_date:
            date_range = st.date_input(
                "📅 Admission Date Range",
                value=(datetime.date.today() - datetime.timedelta(days=30), datetime.date.today())
            )

        display_df = df.copy()

        # 1. Text Search Filter
        if search_query:
            display_df = display_df[
                display_df["Name"].astype(str).str.contains(search_query, case=False, na=False) |
                display_df["Disease"].astype(str).str.contains(search_query, case=False, na=False)
            ]

        # 2. Date Range Filter
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
            admission_dates = pd.to_datetime(display_df["Admission Date"], errors="coerce").dt.date
            display_df = display_df[
                (admission_dates >= start_date) & 
                (admission_dates <= end_date)
            ]

        st.dataframe(display_df, use_container_width=True, hide_index=True)
        # ---> KEEP YOUR EXCEL EXPORT BUTTON BELOW THIS <---
        excel_data = io.BytesIO()
        with pd.ExcelWriter(excel_data , engine="openpyxl") as writer:
            display_df.to_excel(writer , index = False , sheet_name = "Patients")
        st.download_button(
            label="Download Patient Records as Excel",
            data=excel_data.getvalue(),
            file_name="Pateint Records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
            st.info("No Data Found")
    
with tab2:
    with st.form("patient_form" , clear_on_submit=True):
        patient_Name = st.text_input("Patient Name")
        patient_Age = st.number_input("Patient Age", min_value=0 , max_value=120 , step=1 )
        patient_Disease = st.text_input("Patient Disease")
        admission_date = st.date_input("Admission Date", value=datetime.date.today())
        date_str = admission_date.strftime("%Y-%m-%d")
        submit_btn = st.form_submit_button("Add Patient Details")

        if submit_btn:
            db.add_patient(patient_Name , int(patient_Age) , patient_Disease , date_str)
            st.success(f"Added {patient_Name} sucessfully!")

with tab3:
    with st.form("update_patient_form", clear_on_submit=True):
        patient_id = st.number_input("Patient ID" , min_value=1 , step=1)
        new_Name = st.text_input("Updated Name")
        new_Age = st.number_input("Updated Age" , min_value=0 , step=1)
        new_Disease = st.text_input("Updated Disease")
        update_btn = st.form_submit_button("Update Patient Details")

        if update_btn:
            db.update_patient_records(int(patient_id) , new_Name , int(new_Age) , new_Disease)
            st.success(f"Update {new_Name} sucessful!")

with tab4:
    data = db.get_patients()
    if data:
        exsisting_ids = [item[0] for item in data]
        with st.form("delete_patient_records", clear_on_submit=True):
            patient_id = st.selectbox("Patient ID to remove -", exsisting_ids)
            delete_btn = st.form_submit_button("Delete Patient Records")

            if delete_btn:
                db.delete_patient_records(patient_id)
                st.warning(f"Patient #{patient_id} has been Deleted.")
    else:
        st.info("No Patient avialiable to delete.")