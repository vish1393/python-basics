# kafka-basics

# [1] Setup and Cluster Lifecycle

# Initialize project directory
mkdir -p ~/kafka-learning && cd ~/kafka-learning

# Spin up cluster in background
docker compose up -d

# Verify container status
docker ps

# Stop containers (preserves messages and topic data)
docker compose stop

# Destroy containers (preserves data volumes)
docker compose down

# Destroy containers AND delete all volumes/data (full reset)
docker compose down -v


# [2] Topic Management:
# Create main events topic
docker exec -it local-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic order-events --partitions 3 --replication-factor 1

# Create Dead Letter Queue (DLQ) topic
docker exec -it local-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic order-events-dlq --partitions 3 --replication-factor 1

# List active topics
docker exec -it local-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list

# Delete a topic
docker exec -it local-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --delete --topic sample


# [3] CLI testing
# Produce messages interactively
docker exec -it local-kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 --topic order-events

# Consume main topic from beginning
docker exec -it local-kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic order-events --from-beginning

# Inspect Dead Letter Queue (DLQ) messages
docker exec -it local-kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic order-events-dlq --from-beginning


# [4] Consumer Group Operations:
# Inspect consumer group status, lags, and partition offsets
docker exec -it local-kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group order-processing-group

# Reset consumer group offsets to beginning
docker exec -it local-kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group order-processing-group \
  --reset-offsets --to-earliest --execute --topic order-events