
import json
import boto3
import os
# from config import dbendpoint, dbname, dbuser, dbpassword
from datetime import datetime, timedelta
from numpy import size

import pymysql
import pandas as pd
from sqlalchemy import false

print('Loading function')

env_type = os.getenv("ENV_TYPE")
db_secret = os.getenv("DB_SECRET")
ec2_instance_is = os.getenv("INSTANCE_ID")
queue_url = os.getenv("QUEUE_URL")


def get_db_connection(secret_name, db):
    try:
        db_endpoint = os.getenv("DB_ENDPOINT")
        client = boto3.client('secretsmanager', 'us-east-1')
        response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = json.loads(response['SecretString'])

        username = secret['username']
        password = secret['password']

        conn = pymysql.connect(
        host=db_endpoint,
        user=username, 
        password = password,
        db=db,
        )


        return conn
    except Exception as e:
        print("Error occured:" + str(e))


def get_meters(dbConn, db):
    try:
        frame = pd.read_sql("select * from "+db+".table", dbConn)
        return frame
    except Exception as e:
        print("Error occured:" + str(e))


def get_last_meter_reading(dbConn, table, db):

    try:
        start_date = datetime.utcnow()
        end_date = start_date - timedelta(minutes=15)
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        
        query = "select * from {0}.table where date_time>='{1}' and date_time<='{2}' and table={3} order by date_time asc".format(db, end_date, start_date, table)
        frame = pd.read_sql(query, dbConn)
        return frame
    except Exception as e:
        print("Error occured:" + str(e))

def reset_ec2():
    client = boto3.client('ec2', 'us-east-1')
    client.reboot_instances(
        InstanceIds=[
            ec2_instance_is
        ]
    )

def upload_to_queue(data):
    client = boto3.client('sqs', 'us-east-1')

    client.send_message(
        QueueUrl=queue_url,
        MessageBody=data
    )

def lambda_handler(event, context):


        for meter in meters.itertuples():
            try:
                #ToDo
                pass


            except Exception as e:
                print("Error occured:" + str(e))
