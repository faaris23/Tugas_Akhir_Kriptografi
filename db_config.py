import mysql.connector

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=8501,
        user="root",
        password="",  # Ganti sesuai dengan konfigurasi Anda
        database="db_penilangan"
    )

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create encrypted_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image LONGBLOB NOT NULL,
            text TEXT,
            encrypted_text TEXT,
            encrypted_image TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database if not exists
initialize_database()
