# COMP 851 Project: Option 1
## Assignment:
The first is a data integration which provides lists of users as potential leads for purchasing of Widgets. Every day a new list of leads are deposited on S3 by a marketing partner, and the leads must be processed in order to determine how they should be contacted. The existing lead integration hub is a RabbitMQ cluster, and the Office of Architecture has decreed that this integration must maintain that approach. In addition, existing marketing integrations rely on a message routing approach to ship leads to different databases which support the sales teams. 
* If a lead is in the United States: then they should be put into a PostgreSQL database table named leads. 
* If they are not and they have a known CC number, then they should go into a database table named high_priority.
* and otherwise all leads should be deposited into a text file. 

## The Plan:
![](https://i.imgur.com/gsql6QH.png)
1. The leads.csv will exist in an S3 bucket. The CSV's name will then be provided to the a message producer as an argument and read in with Boto.
2. The RabbitMQ producer will declare a message channel with Pika and begin parsing through the CSV file's rows.
3. Each Row will be mapped to a Python dictionary and sent as a message over the channel.
4. A RabbitMQ consumer will declare a queue and be consuming any incoming messages.
5. Once a message is received, the consumer will determine where to send the data by looking at the message's columns.
6. If it is determined that the message goes to a PSQL table, the consumer will send the message to a 
Psycopg2 function along with the desired table name in order to insert the data.
7. If it is determined that the message will be dumped, the consumer will either create a CSV file or append the message to an existing file.

## Installation:
#### Dependencies: Conda & PostgreSQL
1. Clone the Git repo
2. Initialize your Conda environment off the .yml file:\
```$ conda env create -n leads_project -f environment.yml```
3. Create a new PSQL db (I used project851):\
```postgres=# create database project851;```
4. Change the database.ini file to suit your PSQL database's information:
	``` 
	[postgresql]
	database=project851
	user=postgres
	```
5. Activate your Conda environment:\
  ``` $ conda activate leads_project ```
6. Run init_db.py to create your database tables or reset data:\
  ```$ python3 init_db.py```
7. Add the csv file to your S3 bucket:\
<<<<<<< HEAD
  ```aws s3 cp ./leads.csv s3://""/""/project_leads/leads.csv ```
=======
  ```$ aws s3 cp ./leads.csv s3://comp851-m1-f20/aat1006/project_leads/leads.csv ```
>>>>>>> c9b744c8d3304b49917390091c0b4c1404dd7f2d
8. Adjust the S3 bucket name in producer.py:\
  ```data = s3.get_object(Bucket='', Key=file_name)```
9. Start the consumer:\
  ``` $ python3 consumer.py ```
10. Run the producer with your S3's csv as an argument:\
<<<<<<< HEAD
  ```  $ python3 producer.py ""/project_leads/leads.csv```
11. Your database's two tables should now be populated with leads and a leads_dump.csv should reside in the directory:\
=======
  ```  $ python3 producer.py aat1006/project_leads/leads.csv```
11. Your database's two tables should now be populated with leads and a leads_dump.csv should reside in the directory:
>>>>>>> c9b744c8d3304b49917390091c0b4c1404dd7f2d
  ```
project851=# select * from leads;
....
3535101196800233 | United States | 1968-07-17 | 80552.84 | Assistant Manager |  
2016-02-03 01:02:30 | 944 | Kelly | Hanson | khansonq7@phpbb.com | | 250.78.86.48 | | United States | 1969-01-02 | | Account Executive |  
2016-02-03 03:17:13 | 969 | Terry | Robinson | trobinsonqw@amazon.com | Male | 242.98.189.30 | 491129692288238190 | United States | 1969-09-13 | 264976.12 | Information Systems Manager |  
(23 rows) 
```
```
project851=# select * from high_priority;
....
2016-02-03 02:08:01 | 994 | Earl | Butler | ebutlerrl@posterous.com | | 209.157.200.68 | 3543989857454146 | Egypt | 1981-02-02 | | Speech Patholo  
gist | ✋       
2016-02-03 00:33:54 | 998 | Stephanie | Sims | ssimsrp@newyorker.com | Female | 135.66.68.181 | 3548125808139842 | Poland | | 112275.78 |  
2016-02-03 00:53:53 | 1000 | Alice | Peterson | apetersonrr@parallels.com | Female | 244.89.94.58 | 5602227843485236 | Nigeria | | 239858.7 |  
(650 rows)
```
```
leads_dump.csv:
registration_dttm,id,first_name,last_name,email,gender,ip_address,cc,country,birthdate,salary,title,comments
2016-02-03T13:36:39Z,1,Donald,Lewis,dlewis0@clickbank.net,Male,102.22.124.20,,Indonesia,7/9/1972,140249.37,Senior Financial Analyst,
2016-02-03T18:29:04Z,3,Michelle,Henderson,mhenderson2@geocities.jp,Female,193.68.146.150,,France,1/15/1964,236219.26,Teacher,
2016-02-03T10:49:07Z,6,Frances,Adams,fadams5@123-reg.co.uk,Female,106.196.106.93,,Russia,3/27/1997,82175.77,Account Coordinator,
....
326 rows
```
## Resources
RabbitMQ/Pika:\
https://www.rabbitmq.com/tutorials/tutorial-one-python.html \
Converting Python Dictionary to JSON and Sending w/ RabbitMQ: \
https://stackoverflow.com/questions/34534178/rabbitmq-how-to-send-python-dictionary-between-python-producer-and-consumer \
Setting up PSQL:\
https://www.postgresqltutorial.com/install-postgresql-linux/ \
Inserting Python Variables into PSQL with Psycopg2:\
https://stackoverflow.com/questions/62764057/how-to-insert-variable-data-into-postgresql \
Dropping PSQL Tables with Psycopg2: \
https://stackoverflow.com/questions/435424/postgresql-how-to-create-table-only-if-it-does-not-already-exist \
Reading CSV File from S3 Bucket:\
https://dev.to/shihanng/how-to-read-csv-file-from-amazon-s3-in-python-4ee9 \
Creating CSV Dump:\
https://stackoverflow.com/questions/2363731/append-new-row-to-old-csv-file-python \
Writing CSV Header to CSV Dump:\
https://stackoverflow.com/questions/28325622/python-csv-writing-headers-only-once
