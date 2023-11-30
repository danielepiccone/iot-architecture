## Platform for ingesting data from IoT devices

### Description

The main architecture uses the following components:

- producers
- gateway
- data processing layer (event/batch)
- application

The producers connect to the MQTT broker via with TLS (TODO)

The producers generate payloads serialized in an interchange format (json, protobuf, messagepack) and connect to the gateway

The gateway receives messages and enqueues them for processing

The processing layer stores the payloads and calculates analytics

The application layer exposes an API to retrieve the sensor data

```
# To get the state of the device
$ curl localhost:5000/device/device1

# To get the readings
$ curl localhost:5000/device/device1/telemetry
```

### Dependencies

The system uses docker and localstack, to connect to localstack from the host system use these settings

```
~/.aws/config

[profile localstack]
region=us-east-1
output=json
endpoint_url = http://localhost:4566/

~/.aws/credentials

[localstack]
aws_access_key_id=test
aws_secret_access_key=test
```

Terraform versions are managed by **https://asdf-vm.com**

```
$ asdf plugin add terraform
$ asdf install terraform 1.0.0
$ asdf global terraform 1.0.0
```

The project uses a poetry workspace `https://python-poetry.org/`

The project uses pre-commit hooks `https://pre-commit.com/`

### Usage

To bring up the system

`docker compose up --build`
