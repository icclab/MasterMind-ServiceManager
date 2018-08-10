#! /usr/bin/env bash
#
# A simple script to test the Mastermind-ServiceManager

NETWORKNAME='test-network'
MASTERMIND_SERVER='localhost'
MASTERMIND_PORT='8081'
CERT_FILE='cert.pem'
CACERT_FILE='ca.pem'
KEY_FILE='key.pem'

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
cert=$(<$FULL_CERT_FILE)
# echo $cert
cacert=$(<$FULL_CACERT_FILE)
# echo $cacert
key=$(<$FULL_KEY_FILE)
# echo $key

json_data=$(jq -n \
		--arg ca "$cacert" \
		--arg cert "$cert" \
		--arg key "$key" \
		--arg url "$DOCKER_HOST" \
		--arg name "$NETWORKNAME" \
		'{"ca-cert": $ca, "cert": $cert, "cert-key": $key, "engine-url": $url, "name": $name}' )
# 		.ca-cert "$ca" .cert "$cert" .cert-key "$key" .engine-url "$url" )

# echo $json_data

echo "Creating network $NETWORKNAME"
networks_response=$(curl -X DELETE \
  http://$MASTERMIND_SERVER:$MASTERMIND_PORT/v1/network/delete \
   -H "Content-Type: Application/json" \
   --data "$json_data" )

echo $networks_response

