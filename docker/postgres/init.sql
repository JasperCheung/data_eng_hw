CREATE TABLE IF NOT EXISTS Marketing (
    event_id varchar(255),
    phone_id varchar(255),
    ad_id INTEGER,
    provider varchar(255),
    placement varchar(255),
    length INTEGER,
    event_ts timestamp,
    PRIMARY KEY(event_id)
);

CREATE TABLE IF NOT EXISTS Users (
    event_id varchar(255),
    user_id varchar(255),
    phone_id varchar(255),
    property varchar(255),
    value varchar(255),
    event_ts timestamp,
    PRIMARY KEY(event_id)
);

CREATE TABLE IF NOT EXISTS initial(
       user_id varchar(255),
       event_ts timestamp,
       PRIMARY KEY(user_id)
);
