#! /usr/bin/env bash
#
# A simple script to test the Mastermind-ServiceManager

STACKNAME='test-stack'
MASTERMIND_SERVER='localhost'
MASTERMIND_PORT='8081'
CERT_FILE='cert.pem'
CACERT_FILE='ca.pem'
KEY_FILE='key.pem'
STACK_BASE_DIR='../python-tests/quantum-leap'

if [ -z "$DOCKER_HOST" ]
then
  echo "DOCKER_HOST environment variable not set - exiting..."
  exit 1
fi
# Assume DOCKER_HOST is set and is in the form tcp://IP:PORT
IFS=':' fields=($DOCKER_HOST)
proto=${fields[0]}
host_with_slashes=${fields[1]}
host=${host_with_slashes:2}
port=${fields[2]}

echo "Working with docker engine on host $host, port $port using protocol $proto"

# POST /create_network
# {
#   "ca-cert": "string",
#   "cert": "string",
#   "cert-key": "string",
#   "engine-url": "string",
#   "name": "string"
# }

FULL_CERT_FILE="$DOCKER_CERT_PATH/$CERT_FILE"
FULL_CACERT_FILE="$DOCKER_CERT_PATH/$CACERT_FILE"
FULL_KEY_FILE="$DOCKER_CERT_PATH/$KEY_FILE"
FULL_COMPOSE_FILE="$STACK_BASE_DIR/docker-compose.yml"
# FULL_COMPOSE_VARS_FILE="$STACK_BASE_DIR/docker-compose.yml"
cert=$(<$FULL_CERT_FILE)
# echo $cert
cacert=$(<$FULL_CACERT_FILE)
# echo $cacert
key=$(<$FULL_KEY_FILE)
compose_file=$(<$FULL_COMPOSE_FILE)
#compose_vars=$(<$FULL_COMPOSE_VARS_FILE)
echo $compose_file

json_data=$(jq -n \
		--arg ca "$cacert" \
		--arg cert "$cert" \
		--arg key "$key" \
		--arg url "$DOCKER_HOST" \
		--arg name "$STACKNAME" \
		--arg composefile "$compose_file" \
		'{"ca-cert": $ca, "cert": $cert, "cert-key": $key, "engine-url": $url, "name": $name, "compose-file": $composefile, "compose-vars": "", "external_files": [{}] }' )
# 		.ca-cert "$ca" .cert "$cert" .cert-key "$key" .engine-url "$url" )

#     stack = swagger_client.Stack(engine_url=engine_url,
#                                  ca_cert=ca_cert, cert=cert,
#                                  cert_key=cert_key,
#                                  compose_file=compose_file,
#                                  compose_vars="",
#                                  external_files=external_files,
#                                  name=stack_name)
# # echo $json_data

echo "Creating volume $STACKNAME"
volumes_response=$(curl -X POST \
  http://$MASTERMIND_SERVER:$MASTERMIND_PORT/v1/stack \
   -H "Content-Type: Application/json" \
   --data "$json_data" )

jq <<< "$volumes_response"

