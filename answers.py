import psycopg2

def count_users():
    """Count the number of distinct users.
    """
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
    """Count the number of distinct providers.
    """
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

def count_property():
    """Grab the property that occurs the most.
    """
    conn = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
    )
    cur = conn.cursor()
    query = "SELECT property, count(property) FROM Users group by property order by count(property) desc"
    cur.execute(query)
    property_name = cur.fetchone()[0]
    count = cur.fetchone()[1]
    print("iii. The property that changes the most frequently is {}, which changes {} times.".format(property_name,count))
    conn.commit()
    cur.close()
    conn.close()

def july_3_snap():
    """Count the number of distinct users that have the phone id found when provider is Snapchat and the date is july 3.
    """
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
    """Count the ads that were shown the most to users idenfied as moderates.
    """
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
count_property() #iii
july_3_snap() #iv
moderate_ads() #v
