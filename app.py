import streamlit as st
import db
import pandas as pd

db.init_db()
st.title("🏥 Hospital Management System")

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

with tab1:
    data = db.get_patients()
    if data:
        df = pd.DataFrame(data , columns=["Patient_ID" , "Name" , "Age" , "Disease" , "Addmission Date"])
        st.dataframe(df)
    else:
        st.info("No Data Found")

with tab2:
    with st.form("patient_form" , clear_on_submit=True):
        patient_Name = st.text_input("Patient Name")
        patient_Age = st.number_input("Patient Age", min_value=0 , max_value=120 , step=1 )
        patient_Disease = st.text_input("Patient Disease")
        submit_btn = st.form_submit_button("Add Patient Details")

        if submit_btn:
            db.add_patient(patient_Name , int(patient_Age) , patient_Disease)
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