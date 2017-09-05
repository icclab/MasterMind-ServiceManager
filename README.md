# MasterMind-ServiceManager

# Installing the MasterMind API 

run: 
 * `virtualenv .mm`
 * `python setup.py install`

# Example usage of the API

see: `src/api/controllers/default_controller.py`

# Running the MasterMind API

```
pip install -r src/requirements.txt
cd src/api
python app.py
```

# MasterMind Swagger generated server

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

To run the server, please execute the following:

```
sudo pip3 install -U connexion # install Connexion from PyPI
python3 app.py
```

and open your browser to here:

```
http://localhost:8080/v1/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/v1/swagger.json
```

