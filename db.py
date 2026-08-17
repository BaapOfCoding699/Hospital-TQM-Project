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

def add_patient(name , age , disease):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(" INSERT INTO patient_records (name , age , disease) VALUES (? , ?, ?)" , (name , age , disease))
    conn.commit()
    conn.close()

def get_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("select * from patient_records")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    # add_patient("Rahul" , 28, "Fever")
    # print("Test successful")
    print(get_patients())