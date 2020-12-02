#!/usr/bin/python
import psycopg2
from config import config

def connect(message, table):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        for item in message:  
            if message[item] == "":
                message[item] = None
        # create a cursor
        cur = conn.cursor()

        #insert in table depending on parameter
        if table == 'leads': 
            cur.execute("""
            INSERT INTO leads (registration_dttm,id,first_name,last_name,email,gender,ip_address,cc,country,birthdate,salary,title,comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
            """,
             (message['registration_dttm'],message['id']
            ,message['first_name'],message['last_name']
            ,message['email'],message['gender']
            ,message['ip_address'],message['cc']
            ,message['country'],message['birthdate']
            ,message['salary'],message['title']
            ,message['comments']))
        elif table == 'high_priority': 
            cur.execute("""
            INSERT INTO high_priority (registration_dttm,id,first_name,last_name,email,gender,ip_address,cc,country,birthdate,salary,title,comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
            """,
            (message['registration_dttm'],message['id']
            ,message['first_name'],message['last_name']
            ,message['email'],message['gender']
            ,message['ip_address'],message['cc']
            ,message['country'],message['birthdate']
            ,message['salary'],message['title']
            ,message['comments']))
       
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
