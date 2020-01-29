import psycopg2
import csv


def load_data():
    """Refresh the Table and then load users and marketing csvs into the respective tables
    """
    drop_tables()
    MARKETING_URL = './dataset/marketing_2019-07-0{}.csv'
    USERS_URL = './dataset/user_2019-07-0{}.csv'
    for day in range(1,8):
        load_marketing(clean_file(MARKETING_URL.format(day)))
        load_users(clean_file(USERS_URL.format(day)))
    load_inital_table()

def load_marketing(file_path):
    """given a file path load the data into the Marketing table
    """
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    f = open(file_path)
    query = "COPY Marketing FROM STDIN WITH DELIMITER as ','"
    cur.copy_expert(query, f)
    f.close()
    conn.commit()
    cur.close()
    conn.close()

def load_users(file_path):
    """given a file path load the data into the Users table
    """
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    f = open(file_path)
    query = "COPY Users FROM STDIN WITH DELIMITER as ','"
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
    """read csv file and clean the file: remove 0x00, \0, and extra newlines
    output the new file in a directory called clean.
    """
    cleaned_file =  file_path.replace("dataset","clean")
    f  = open(file_path)
    reader = csv.reader(row.replace('0x00', '').replace('\0',"") for row in f)
    NUM_COLS = len(next(reader))
    output = open(cleaned_file, "w")
    writer = csv.writer(output)
    partial = []
    # how i get around random newlines, check the number of records in a row and if its less than the columns, appends the two together and then write to new file.
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

def load_inital_table():
    """Fill the table initial with user_ids and their first ts
    """
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = '''INSERT INTO initial
    SELECT user_id, min(event_ts) from Users
    Group By user_id
    '''
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


load_data()
