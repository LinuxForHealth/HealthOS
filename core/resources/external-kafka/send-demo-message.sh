#!/usr/bin/env bash
# kafka-send-demo-message.sh
# sends the sample 270.x12 message to the "healthy-data" topic

/opt/bitnami/kafka/bin/kafka-console-producer.sh \
    --bootstrap-server localhost:9092 \
    --topic healthy-data < /opt/scripts/270.x12
