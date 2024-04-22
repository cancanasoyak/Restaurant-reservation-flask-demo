import psycopg2
from datetime import datetime, timedelta

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="9000",
    database="postgres",
    user="postgres",
    password="postgres"
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Create a table
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

today = datetime.now().date()
cur.execute("""
        SELECT date, name, table_id, start_time, end_time 
        FROM reservations
        WHERE date >= %s AND date <= %s
        ORDER BY date
    """, (today, today + timedelta(days=7)))

for row in cur.fetchall():
    print(row)


conn.commit()
cur.close()
conn.close()
# Close the cursor and connection
