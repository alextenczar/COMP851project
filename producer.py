#!/usr/bin/env python
import pika, json, csv, sys, boto3, codecs

def send_leads(file_name):
    #initiate localhost connection with pika.
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #declare queue named "leads_pipe"
    channel.queue_declare(queue='leads_pipe')

    #retrieve leads file from s3 bucket with file parameter
    s3 = boto3.client('s3')
    data = s3.get_object(Bucket='comp851-m1-f20', Key=file_name)

    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        #create message dictionary and link with csv colums
        lead = {'registration_dttm': row['registration_dttm'], 'id': row['id'],'first_name': row['first_name'], 
                'last_name': row['last_name'], 'email': row['email'], 'gender': row['gender'], 
                'ip_address': row['ip_address'], 'cc': row['cc'], 'country': row['country'], 
                'birthdate': row['birthdate'], 'salary': row['salary'], 'title': row['title'], 'comments': row['comments']
                }
        #send message
        channel.basic_publish(exchange='', routing_key='leads_pipe', body=json.dumps(lead))

    connection.close()

def main():
    send_leads(sys.argv[1])
    
if __name__=="__main__":
    main()
