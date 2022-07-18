# Core 

The HealthOS core module supports data related features such as data acquisition, validation, transmission, and 
distribution.

External data sources integrate with the HealthOS using connectors. Connectors may be either inbound, for data
acquisition, or outbound for data transmission. Support is currently limited to the following inbound data connectors:

- Kafka Consumer
- NATS Client
- Rest Endpoint

## Quickstart

```shell
cd core
# start default services
docker-compose up -d

# verify that the healthos-core-jetstream service is running and "healthy"
docker-compose ps

# launch the HealthOS core application
poetry run healthos core -f ./resources/service-config/quickstart-config.yml 
```

Browse to http://localhost:8080/docs and use the OpenAPI UI to submit the sample `/healthos/core/ingress` request.

The expected result is a 200 status code with response and terminal output similar to

```json
{
  "status": "received",
  "content_type": "application/EDI-X12",
  "data_id": "a0443ab3-21cd-4946-aa65-2b6b34aa2df2"
}
```

```shell
2022-07-18 15:26:47,623 - linuxforhealth.healthos.core.connector.rest - DEBUG - Generated a0443ab3-21cd-4946-aa65-2b6b34aa2df2 for incoming payload
2022-07-18 15:26:47,796 - linuxforhealth.healthos.core.connector.processor - DEBUG - publishing to NATS healthos:ingress
2022-07-18 15:26:47,796 - linuxforhealth.healthos.core.connector.processor - DEBUG - received NATS Ack PubAck(stream='healthos', seq=1, domain=None, duplicate=None)
2022-07-18 15:26:47,796 - linuxforhealth.healthos.core.connector.processor - DEBUG - returning status = received, id = c3ed5ff1-c156-4e46-aae2-86e3be1d8075
2022-07-18 15:26:47,796 - uvicorn.access - INFO - ::1:55681 - "POST /healthos/core/ingress HTTP/1.1" 200
```

This demonstrates that the data message was validated, identified, and received by the HealthOS Core module's internal
messaging system.

### Demo Profile
The HealthOS Core project's [docker-compose.yml](./docker-compose.yml) includes a demo profile which supports
testing external Kafka and NATS systems.

```shell
# start default and "demo" services
docker-compose --profile demo up -d

# view service status
# Note: "configure-external-jetstream" is a "job" container which will exit after configuring NATS
docker-compose ps

# start the HealthOS Core application
poetry run healthos core -f ./resources/service-config/demo-config.yml
```

#### Kafka Consumer

#### NATS Client

The NATS Client demo requires the [NATS CLI tool](https://github.com/nats-io/natscli#readme). Please install the
CLI within your environment before running the demo.

In a separate terminal, execute the following command:
```shell
cat ./tests/resources/sample-data/270.x12 | nats pub --server localhost:4224 healthy-data
```

The output will look similar to
```shell
15:59:00 Reading payload from STDIN
15:59:00 Published 493 bytes to "healthy-data"
```

The HealthOS core module output will look similar to 
```shell
2022-07-18 16:00:01,771 - linuxforhealth.healthos.core.connector.processor - DEBUG - publishing to NATS healthos:ingress
2022-07-18 16:00:01,772 - linuxforhealth.healthos.core.connector.processor - DEBUG - received NATS Ack PubAck(stream='healthos', seq=9, domain=None, duplicate=None)
2022-07-18 16:00:01,772 - linuxforhealth.healthos.core.connector.processor - DEBUG - returning status = received, id = dda5f4f1-b0bb-4aa1-a65c-78682b563e2a
2022-07-18 16:00:01,772 - linuxforhealth.healthos.core.connector.nats - DEBUG - published message to ingress
2022-07-18 16:00:01,772 - linuxforhealth.healthos.core.connector.nats - DEBUG - message metadata {'data_id': UUID('dda5f4f1-b0bb-4aa1-a65c-78682b563e2a'), 'data': 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~', 'content_type': <ContentType.ASC_X12: 'application/EDI-X12'>}
```








