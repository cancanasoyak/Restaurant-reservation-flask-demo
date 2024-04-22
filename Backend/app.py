from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime, timedelta
import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "6000")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")


def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            table_id INT NOT NULL,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    return


app = Flask(__name__)

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)
create_table(conn)

@app.route('/api/reservations', methods=['GET'])
def reservations():
    today = datetime.now().date()
    
    cur = conn.cursor()
    cur.execute("""
        SELECT date, name, table_id, start_time, end_time 
        FROM reservations
        WHERE date >= %s AND date <= %s
        ORDER BY date
    """, (today, today + timedelta(days=7)))

    data = []
    for row in cur.fetchall():
        data.append({
            "date": row[0].strftime(r"%Y-%m-%d"),
            "name": row[1],
            "table_id": row[2],
            "start_time": row[3].strftime(r"%H:%M:%S"),
            "end_time": row[4].strftime(r"%H:%M:%S")
        })
    
    cur.close()
    return jsonify(data), 200


@app.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.json
    name = data.get('name')
    table_id = data.get('table_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    cur = conn.cursor()
    
    
    cur.execute("""
        INSERT INTO reservations (name, table_id, date, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, table_id, date, start_time, end_time))
    
    conn.commit()
    cur.close()
    return jsonify({"message": "Reservation successful"}), 200

@app.route('/api/check_conflict', methods=['POST'])
def check_conflict():
    data = request.json
    table_id = data.get('table_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    
    cur = conn.cursor()
    cur.execute("""
        SELECT start_time, end_time
        FROM reservations
        WHERE table_id = %s AND date = %s
    """, (table_id, date))
    
    conflict = False
    conflicting_info = {}
    start_time_dt = datetime.strptime(start_time, r"%H:%M").time()
    end_time_dt = datetime.strptime(end_time, r"%H:%M").time()
    for row in cur.fetchall():
        if (start_time_dt >= row[0] and start_time_dt < row[1]) or (end_time_dt > row[0] and end_time_dt <= row[1]):
            conflict = True
            conflicting_info = {
                "start_time": row[0].strftime(r"%H:%M:%S"),
                "end_time": row[1].strftime(r"%H:%M:%S")
            }
            break
    
    cur.close()
    return jsonify({"conflict": conflict, **conflicting_info}), 200
    
    

if __name__ == '__main__':
    app.run(debug=False, port=5000)