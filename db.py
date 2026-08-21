import sqlite3

def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_records(
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            disease TEXT,
            admission_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Datebase ready!")

def add_patient(name , age , disease , admission_date):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(" INSERT INTO patient_records (name , age , disease , admission_date) VALUES (? , ?, ?, ?)" , (name , age , disease , admission_date))
    conn.commit()
    conn.close()

def get_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("select * from patient_records")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_patient_records(patient_id , name , age , disease):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient_records SET name = ? , age = ? , disease = ?
        WHERE patient_id = ?
    """, (name , age , disease , patient_id))
    conn.commit()
    conn.close()

def delete_patient_records(patient_id):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM patient_records
        WHERE patient_id = ?
    """ , (patient_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()