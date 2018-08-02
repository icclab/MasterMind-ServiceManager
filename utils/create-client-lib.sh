#! /usr/bin/env bash

usage() {
  echo "Usage: $0 <full path to swagger.yaml>"
}

if [ $# -ne 1 ]
then
  usage
  exit 1
fi

swagger_input=$1

cd /tmp

dt="$(date +'%Y%m%d-%H%M%S')"
echo dt = $dt
dirname="gen-swagger-client-$dt"
echo dirname = $dirname
mkdir $dirname

cd $dirname

git clone https://github.com/swagger-api/swagger-codegen.git

cd swagger-codegen

mkdir input
cp $1 input
mkdir output-client

# cd swagger-codegen
# ./run-in-docker.sh generate -i ../input/swagger.yaml -l python -o ../output-client
./run-in-docker.sh generate -i input/swagger.yaml -l python -o output-client

cd ..

mkdir output-client
cp -R swagger-codegen/output-client/* output-client

echo
echo
echo "Created new output client files...in directory /tmp/$dirname/output-client"
echo
echo 'This might work: cp -r /tmp/$dirname/output-client/* client'
echo
echo "Copy these to the client directory within this repo..."
