#! /usr/bin/env bash

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

