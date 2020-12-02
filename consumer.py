#!/usr/bin/env python
import pika, sys, os, json, csv, os.path
from db_connect import connect

def main():
    #initiate localhost connection with pika.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    #declare queue named "leads_pipe"
    channel.queue_declare(queue='leads_pipe')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        psql_insert(message)

    #begin comsuming on channel
    channel.basic_consume(queue='leads_pipe', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def psql_insert(message):
    csv_columns = ['registration_dttm', 'id', 'first_name', 
                   'last_name', 'email','gender', 'ip_address', 
                   'cc', 'country', 'birthdate', 'salary', 'title', 
                   'comments'] #columns for csv_dump

    if message['country'] == 'United States': #if country is US
        connect(message, 'leads') #send message and determined table name to db_connect.py 
    elif message['cc'] != '': #if no cc number
       connect(message, 'high_priority') #send message and determined table name to db_connect.py 
    else:
        try:
            file_exists = os.path.isfile('leads_dump.csv') #check if file already exists
            with open('leads_dump.csv', 'a') as csvfile: #open file for dumping rest of leads
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                if not file_exists:
                    writer.writeheader()  # file doesn't exist yet, write a header
                writer.writerow(message)  # append each message to file as a new row
        except IOError:
            print("I/O error")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)