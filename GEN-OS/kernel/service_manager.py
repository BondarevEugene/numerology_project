"""
Genesis Service Manager
"""


class ServiceManager:

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

        return service

    def get(self, name):
        return self._services.get(name)

    def all(self):
        return self._services


service_manager = ServiceManager()