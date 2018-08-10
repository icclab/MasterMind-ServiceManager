# Using the Mastermind-Service Manager

## Prerequisites

- A docker engine with TLS enabled - see here for instructions on configuring a
  docker engine with TLS

## Running the Mastermind-ServiceManager

- The Mastermind-ServiceManager can be run using the `docker-compose.yml` in
  this directory:
  - `docker-compose up -d`

## Testing

### Configuration

- Ensure the `DOCKER_HOST` and `DOCKER_CERT_PATH` environment variables are set
  correctly:
  - e.g.
'''
export DOCKER_HOST='tcp://<IP_ADDR_OF_DOCKER_ENGINE>:2376'
export DOCKER_CERT_PATH <PATH_CONTAINING_CERTS>
'''

- You should be able to run standard docker commands which operate on the remote
  docker-engine
  - `docker ps -a`
  - `docker images`
- Run `validate-tls.sh` to confirm that communications with the docker-engine
  works.

### Basic Testing

- The basic tests simply create and delete networks and volumes on the docker
  engine
  - These can be run as follows:

'''
./create-network.sh
./delete-network.sh
./create-volume.sh
./delete-volume.sh
'''

### More complex testing

- The more complex tests deploy a stack to the docker engine.

