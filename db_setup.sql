-- in terminal:
-- cd /Users/claudiauribe/Desktop/Geovis2/_Q_A2/static
-- psql geovis2 < plz.sql --username=postgres
CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS regions;

CREATE TABLE regions (
    gid integer NOT NULL PRIMARY KEY,
    name varchar NOT NULL,
    geom geometry
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    type varchar,
    talent_type varchar,
    child_type varchar,
    name varchar,
    pt geometry,
    date date,
    t_0 time,
    t_1 time,
    pay_opt varchar,
    description varchar,
    email varchar NOT NULL,
    geom_id integer REFERENCES regions(gid),
    __date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indices -------------------------------------------------------

--CREATE UNIQUE INDEX evenements_pkey ON evenements(id int4_ops);


-- empty all table entries
DELETE from posts;

-- restart id count
ALTER SEQUENCE posts_id_seq RESTART;

-- delete table, bye bye
drop table posts;
