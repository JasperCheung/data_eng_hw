1. What is the number of unique users?
    -  Answer: `2903`
    -  SQL Used: `SELECT COUNT(DISTINCT(user_id)) FROM Users`
2. Who are the marketing ad providers?
    - Answer: `Instagram, Facebook, Snapchat, Spotify`
    - SQL Used: `SELECT DISTINCT(provider) FROM Marketing`
3. Which user property is changed the most frequently?
    - I interpreted each property as listed in the users table as a property changed.
    - Answer: `drinking` which changes `1435` times
    - SQL Used: `SELECT property, count(property) FROM Users group by property order by count(property) desc`
4. How many users where shown a Snapchat ad on July 3rd, 2019?
    - Answer: `237`
    - SQL Used: 
    ```sql
    SELECT count(distinct(user_id)) from users 
    join marketing on marketing.phone_id = users.phone_id 
    where DATE(marketing.event_ts) = '07-03-2019' and marketing.provider = 'Snapchat'
    ```
5. Which ad was showed the most to users who identify as moderates?`
    - interpreted this as a user that has ever been moderate, because accounting for intervals where users identified as moderates seem out of my scope.
    - Answer: `ad 4` and it was shown 402 times.
    - SQL Used: 
    ```sql
     SELECT Marketing.ad_id, count(Marketing.event_id)
     from Users join Marketing on Marketing.phone_id = Users.phone_id
     WHERE Users.phone_id in (
     SELECT DISTINCT(phone_id) FROM Users WHERE property = 'politics' and value = 'Moderate')
     GROUP BY Marketing.ad_id
     ORDER BY count(Marketing.event_id) DESC
  ```
6. What are the top 5 ads? Explain how you arrived at that conclusion.  
I count an ad as sucessful when it runs and a user joins right after that.
To keep track of the intial time when a user joins, I created a table called initial and then populated that with:
```SQL
INSERT INTO initial
SELECT user_id, min(event_ts) from Users
Group By user_id  
```

Then I used:
 ```SQL
 select Marketing.ad_id
, count(distinct(Users.user_id))
FROM USERS
join marketing on marketing.phone_id = users.phone_id
join initial on initial.user_id = users.user_id
where marketing.event_ts < initial.event_ts
group by ad_id
order by count desc
;
```

This calculates the number of users that joined after a they recieved an ad

| ad_id | count        
| ---- | ---
| 4	| 198 
| 2	| 187 
| 0	| 184 
| 1	| 176 
| 3	| 176 

However, I didn't think that answered the question fully assuming that the `length` property was how long the ad ran then we should calculate the avg by dividing users joined over the total length of that ad.

SQL used: 
```SQL
 with sum_length as(select ad_id, sum(length) from marketing group by ad_id),
ad_counts as (select marketing.ad_id,count(distinct(users.user_id))
FROM USERS
join marketing on marketing.phone_id = users.phone_id
join initial on initial.user_id = users.user_id
where marketing.event_ts < initial.event_ts
group by marketing.ad_id)

select ad_counts.ad_id, CAST(ad_counts.count as float)/sum_length.sum as avg from ad_counts
join sum_length on sum_length.ad_id = ad_counts.ad_id
order by avg desc LIMIT 5
```

Answer: 

| ad_id | avg
| -- | --
|19	|0.0002912272439988599
|17	|0.0002847211512225214
|21	|0.0002805374710998036
|13	|0.00027170702894270527
|6	|0.00023551688891610418



