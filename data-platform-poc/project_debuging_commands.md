🔹 1. DOCKER LEVEL COMMANDS (FOUNDATION)
Check all running containers
docker ps

Check all containers (including stopped)
docker ps -a

Start full platform
docker-compose up -d

Stop full platform
docker-compose down

Rebuild images (after code/config changes)
docker-compose up -d --build

Restart a single container
docker restart data-platform-poc-airflow

View container logs
docker logs data-platform-poc-airflow
docker logs data-platform-poc-kafka-1

Follow logs live
docker logs -f data-platform-poc-airflow

🔹 2. ENTER CONTAINERS (CRITICAL SKILL)
Enter Airflow container
docker exec -it data-platform-poc-airflow bash

Enter Kafka container
docker exec -it data-platform-poc-kafka-1 bash

Exit container
exit

🔹 3. VERIFY VOLUMES & FILES (DEBUGGING)
Check project mounted in Airflow
ls /opt/project

Verify Kafka producer exists
ls /opt/project/kafka

Verify DAGs exist
ls /opt/airflow/dags

🔹 4. KAFKA LEVEL COMMANDS
Kafka Console Producer (manual test)
kafka-console-producer \
  --bootstrap-server localhost:9092 \
  --topic orders

Kafka Console Consumer (debugging)
kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --from-beginning

List Kafka topics
kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

Describe a topic
kafka-topics \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic orders

🔹 5. PYTHON KAFKA PRODUCER (REAL DATA)
Run producer inside Airflow container
cd /opt/project
python kafka/producer.py

🔹 6. AIRFLOW LEVEL COMMANDS (CORE)
List all DAGs
airflow dags list

Trigger a DAG manually
airflow dags trigger kafka_to_snowflake

List DAG runs
airflow dags list-runs -d kafka_to_snowflake

Pause a DAG
airflow dags pause kafka_to_snowflake

Unpause a DAG
airflow dags unpause kafka_to_snowflake

🔹 7. AIRFLOW TASK DEBUGGING
List tasks in a DAG
airflow tasks list kafka_to_snowflake

Run a task manually (debug mode)
airflow tasks test kafka_to_snowflake consume_kafka 2025-01-01

View task logs (filesystem)
ls /opt/airflow/logs

🔹 8. COMMON AIRFLOW DEBUGGING COMMANDS
Check Airflow DB
airflow db check

Reset Airflow DB (dangerous – dev only)
airflow db reset

Restart scheduler
airflow scheduler

🔹 9. SNOWFLAKE DEBUGGING (MOST IMPORTANT)
Check if data exists
SELECT * FROM DEMO_DB.PUBLIC.RAW_ORDERS;

Check insert count
SELECT COUNT(*) FROM DEMO_DB.PUBLIC.RAW_ORDERS;

Check Snowflake query history
SELECT
  query_text,
  execution_status,
  error_message,
  start_time
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_text ILIKE '%RAW_ORDERS%'
ORDER BY start_time DESC;

Validate context
SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA();

🔹 10. SNOWFLAKE CONNECTIVITY TEST (PYTHON)
python

import snowflake.connector

conn = snowflake.connector.connect(
    user='YOUR_USER',
    password='YOUR_PASSWORD',
    account='ACCOUNT_ID',
    warehouse='COMPUTE_WH',
    database='DEMO_DB',
    schema='PUBLIC'
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_TIMESTAMP")
print(cur.fetchall())

🔹 11. NETWORK DEBUGGING (EXPERT LEVEL)
Test Kafka connectivity from Airflow container
ping data-platform-poc-kafka-1

Check exposed ports
netstat -tulpn

🔹 12. FULL PIPELINE RUN (MEMORIZE THIS)
docker-compose up -d --build
docker exec -it data-platform-poc-airflow bash
cd /opt/project
python kafka/producer.py
airflow dags trigger kafka_to_snowflake


Then in Snowflake:

SELECT * FROM DEMO_DB.PUBLIC.RAW_ORDERS;

🧠 DEBUGGING MINDSET (THIS IS GOLD)

When data is missing, always check in this order:

1️⃣ Producer → Kafka
2️⃣ Kafka → Consumer
3️⃣ Consumer → Airflow logs
4️⃣ Airflow → Snowflake inserts
5️⃣ Snowflake query history