"""
GENESIS Service Container
"""


class ServiceContainer:

    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def get(self, name):
        return self.services.get(name)

    @property
    def count(self):
        return len(self.services)

    def dump(self):
        result = []
        for name, service in self.services.items():
            result.append({
                "name": name,
                "class": service.__class__.__name__
            })
        return result


container = ServiceContainer()
