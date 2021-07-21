import psycopg2
import os
import datetime
from datetime import timezone
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

def update_job(status, id_job):
    """ update job status  """
    sql = """ UPDATE job_job
                SET status = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = psycopg2.connect(host=os.getenv('DB_HOST'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute(sql, (status, id_job))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def get_jobs():
    conn = None
    now_time = datetime.datetime.now().replace(tzinfo=timezone.utc)
    try:
        conn = psycopg2.connect(host=os.getenv('DB_HOST'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM job_job ORDER BY id")
        row = cur.fetchone()

        while row is not None:
            start_time = row[4]
            end_time = row[3]
            id_job = row[0]
            print("Start time: {0}, End time: {1}".format(start_time,end_time))
            if start_time <= now_time and now_time <= end_time:
                update_job(True, id_job)
            else:
                update_job(False, id_job)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    get_jobs()