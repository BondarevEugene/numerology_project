# nexus_engine.py

class NexusEngine:
    def __init__(self):
        self.registry = {}

    def register_node(self, name, func):
        """Регистрирует функцию как узел системы"""
        self.registry[name] = func

    def execute_chain(self, flow_name, input_data):
        """Запускает цепочку узлов"""
        # Здесь будет логика обхода графа, который ты нарисуешь
        pass

nexus = NexusEngine()