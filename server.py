from flask import Flask, request
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'data.db'

# Ensure DB exists and table is ready
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                col1 TEXT, col2 TEXT, col3 TEXT
            )
        ''')

@app.route('/upload', methods=['POST'])
def upload_excel():
    file = request.files['excelFile']
    if not file:
        return "No file uploaded", 400

    df = pd.read_excel(file)
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql('uploads', conn, if_exists='append', index=False)

    return f"{len(df)} rows saved to database!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)