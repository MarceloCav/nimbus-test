import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    db_up = False
    while db_up is False:
        try:
            conn = psycopg2.connect(
                dbname="nimbustest",
                user="marcelo",
                password="123marcelo",
                host="db",
                port="5432"
            )
            db_up = True
        except OperationalError:
            print("Database not ready, waiting...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()
