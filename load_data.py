import psycopg2
import csv


def load_data():
    drop_tables()
    MARKETING_URL = './dataset/marketing_2019-07-0{}.csv'
    USERS_URL = './dataset/user_2019-07-0{}.csv'
    for day in range(1,8):
        load_marketing(clean_file(MARKETING_URL.format(day)))
        load_users(clean_file(USERS_URL.format(day)))

def load_marketing(file_path):
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    f = open(file_path)
    query = "COPY Marketing FROM STDIN WITH CSV HEADER DELIMITER as ','"
    cur.copy_expert(query, f)
    f.close()
    conn.commit()
    cur.close()
    conn.close()

def load_users(file_path):
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    f = open(file_path)
    query = "COPY Users FROM STDIN WITH CSV HEADER DELIMITER as ','"
    cur.copy_expert(query, f)
    f.close()
    conn.commit()
    cur.close()
    conn.close()

def drop_tables():
    """Drops all tables from db. Uses: pyscopg
    """
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("truncate table " + row[1] + " cascade")
    conn.commit()
    cur.close()
    conn.close()

def clean_file(file_path):
    cleaned_file =  file_path.replace("dataset","clean")
    f  = open(file_path)
    reader = csv.reader(row.replace('0x00', '').replace('\0',"") for row in f)
    NUM_COLS = len(next(reader))
    output = open(cleaned_file, "w")
    writer = csv.writer(output)
    partial = []
    for row in reader:
        if(row):
            if(partial):
                row = partial + row
                row.remove('')
                partial = []
            else:
                if(len(row) != NUM_COLS):
                    partial = row
                    continue
            writer.writerow(row)
    f.close()
    output.close()
    return cleaned_file


load_data()
