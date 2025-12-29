from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import json
import snowflake.connector

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'kafka_to_snowflake',
    default_args=default_args,
    schedule_interval='@once'
)

def consume_kafka_to_snowflake():
    consumer = KafkaConsumer(
        'orders',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    ctx = snowflake.connector.connect(
        user='',
        password='',
        account='',
        warehouse='COMPUTE_WH',
        database='DEMO_DB',
        schema='PUBLIC'
    )

    cs = ctx.cursor()
    for message in consumer:
        order = message.value
        cs.execute(
            "INSERT INTO DEMO_DB.PUBLIC.RAW_ORDERS (ORDER_ID, CUSTOMER, AMOUNT, EVENT_TIME) VALUES (%s, %s, %s, %s)",
            (order['order_id'], order['customer'], order['amount'], order['event_time'])
        )
        print("Inserted:", order)
    cs.close()
    ctx.close()

t1 = PythonOperator(
    task_id='consume_kafka',
    python_callable=consume_kafka_to_snowflake,
    dag=dag
)


