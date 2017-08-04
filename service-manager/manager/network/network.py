NETWORK_KEYS = [
    "driver",
    "options",
    "ipam",
    "internal",
    "labels",
    "external"
]


class Network(object):
    def __init__(self,
                 name,
                 client=None,
                 driver=None,
                 external=False,
                 options=None,
                 ipam=None,
                 check_duplicate=True,
                 internal=False,
                 labels=None,
                 enable_ipv6=False,
                 stack_name=None):
        self.client = client
        self.name = name
        self.driver = driver
        self.external = external
        self.options = options
        self.ipam = ipam
        self.check_duplicate = check_duplicate
        self.internal = internal
        self.labels = labels or {}
        self.enable_ipv6 = enable_ipv6
        self.stack_name = stack_name

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self):
        if self.external:
            self.check_external_network()
        self.client.networks.create(name=self.name,
                                    driver=self.driver,
                                    options=self.options,
                                    ipam=self.ipam,
                                    check_duplicate=self.check_duplicate,
                                    internal=self.internal,
                                    labels=self.labels)

    def check_external_network(self):
        if not self.client.networks.list(names=self.name):
            raise NotImplementedError
