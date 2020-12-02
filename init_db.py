#!/usr/bin/python
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()

        #drop existing tables ane make new ones.
        cur.execute("""DROP TABLE leads""")
        cur.execute("""DROP TABLE high_priority""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            registration_dttm timestamp NOT NULL,
            id INTEGER PRIMARY KEY NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            gender VARCHAR(255),
            ip_address VARCHAR(255),
            cc BIGINT,
            country VARCHAR(255),
            birthdate DATE,
            salary NUMERIC,
            title VARCHAR(255),
            comments VARCHAR(255)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS high_priority (
            registration_dttm timestamp NOT NULL,
            id INTEGER PRIMARY KEY NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            gender VARCHAR(255),
            ip_address VARCHAR(255),
            cc BIGINT,
            country VARCHAR(255),
            birthdate DATE,
            salary NUMERIC,
            title VARCHAR(255),
            comments VARCHAR(255)
        )
        """)
       
	    # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def main():
    connect()

if __name__ == '__main__':
    connect()
