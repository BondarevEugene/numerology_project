class KernelModule:

    NAME = "Base"

    VERSION = "1.0"

    BUILD = "0157"

    def register_services(self, kernel):
        pass

    def register_events(self, kernel):
        pass

    def register_workspaces(self, kernel):
        pass

    def initialize(self):
        pass

    def shutdown(self):
        pass

MODULES = {
    "career": {
        "version": "1.0",
        "status": "ACTIVE",
        "coverage": 18,
        "priority": 1
    },
    "psychology": {
        "version": "0.9",
        "status": "ACTIVE",
        "coverage": 42
    },
    "health": {
        "status": "PLANNED"
    }
}