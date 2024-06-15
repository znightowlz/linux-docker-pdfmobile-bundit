import psycopg2
import cornetto

def connect_db():
    conn = psycopg2.connect(
        dbname=cornetto.corndog.DB_NAME,
        user=cornetto.corndog.DB_USER,
        password=cornetto.corndog.DB_PASSWORD,
        host=cornetto.corndog.DB_HOST,
        port=cornetto.corndog.DB_PORT,
    )
    return conn


