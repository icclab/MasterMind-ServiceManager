import docker


def get_client(host=None, version="1.26", tls=False):
    return docker.DockerClient(base_url=host, version=version, tls=tls)
