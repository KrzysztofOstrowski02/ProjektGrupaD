import sqlite3

def connect_db(db_path):
    return sqlite3.connect(db_path)

def get_column_names(db_path, table):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns

def add_record(db_path, table, columns, data):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    column_names = ', '.join(columns)
    placeholders = ', '.join(['?' for _ in columns])
    cursor.execute(f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})", data)
    conn.commit()
    conn.close()

def get_records(db_path, table):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()
    conn.close()
    return records

def update_record(db_path, table, record_id, columns, data):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    set_clause = ', '.join([f"{col} = ?" for col in columns])
    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE rowid = ?", (*data, record_id))
    conn.commit()
    conn.close()

def delete_record(db_path, table, record_id):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE rowid = ?", (record_id,))
    conn.commit()
    conn.close()

def get_sorted_records(db_path, table, column, order):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} ORDER BY {column} {order}")
    records = cursor.fetchall()
    conn.close()
    return records

def get_filtered_records(db_path, table, filter_column, filter_value):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {filter_column} LIKE ?", (f'%{filter_value}%',))
    records = cursor.fetchall()
    conn.close()
    return records

def get_joined_records(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT Sprzedaze.rowid, Klienci.Imie, Klienci.Nazwisko, Samochody.Marka, Samochody.Model, Sprzedawcy.Imie, Sprzedawcy.Nazwisko, Sprzedaze.DataSprzedazy 
                      FROM Sprzedaze 
                      JOIN Klienci ON Sprzedaze.KlientID = Klienci.rowid
                      JOIN Samochody ON Sprzedaze.SamochodID = Samochody.rowid
                      JOIN Sprzedawcy ON Sprzedaze.SprzedawcaID = Sprzedawcy.rowid''')
    records = cursor.fetchall()
    conn.close()
    return records
