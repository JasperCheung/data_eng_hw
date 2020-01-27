import psycopg2

def count_users():
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = "SELECT COUNT(DISTINCT(user_id)) FROM Users"
    cur.execute(query)
    print("i. There are {} unique users".format(cur.fetchone()[0]))
    conn.commit()
    cur.close()
    conn.close()

def count_providers():
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = "SELECT DISTINCT(provider) FROM Marketing"
    cur.execute(query)
    providers = ''.join(x[0] + ', ' for x in cur.fetchall())[0:-2]
    print("ii. The marketing ad providers are {}.".format(providers))
    conn.commit()
    cur.close()
    conn.close()

def july_3_snap():
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = '''SELECT count(distinct(user_id)) from users join marketing on marketing.phone_id = users.phone_id where DATE(marketing.event_ts) = '07-03-2019' and marketing.provider = 'Snapchat'
    '''
    cur.execute(query)
    num_users = cur.fetchone()[0]
    print("iv. {} users were shown a Snapchat ad on July 3rd, 2019.".format(num_users))
    conn.commit()
    cur.close()
    conn.close()


def moderate_ads():
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = '''
    SELECT Marketing.ad_id, count(Marketing.event_id)
from Users join Marketing on Marketing.phone_id = Users.phone_id
WHERE Users.phone_id in (
SELECT DISTINCT(phone_id) FROM Users WHERE property = 'politics' and value = 'Moderate')
GROUP BY Marketing.ad_id
ORDER BY count(Marketing.event_id) DESC
    '''
    cur.execute(query)
    ad_id = cur.fetchone()[0]
    ad_count = cur.fetchone()[1]
    print("v. The ad that was shown the most to users that identified as moderates is ad {ad_id} and it was shown {ad_count} times.".format( ad_id = ad_id, ad_count = ad_count))
    conn.commit()
    cur.close()
    conn.close()


count_users() #i
count_providers() #ii
july_3_snap() #iv
moderate_ads() #v
