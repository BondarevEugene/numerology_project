import importlib
import json
from models import db, NexusNode, NexusFlow


class NexusOrchestrator:
    @staticmethod
    def execute_event(event_name, initial_data):
        """Запускает цепочку функций, связанных с событием"""
        flow = NexusFlow.query.filter_by(event_trigger=event_name).first()
        if not flow:
            return initial_data

        sequence = json.loads(flow.flow_sequence)
        current_data = initial_data

        for node_slug in sequence:
            node = NexusNode.query.filter_by(slug=node_slug, is_active=True).first()
            if node:
                # Динамический импорт функции
                module_name, func_name = node.module_path.rsplit('.', 1)
                mod = importlib.import_module(module_name)
                func = getattr(mod, func_name)

                # Выполняем и передаем результат дальше по цепочке
                current_data = func(current_data)

        return current_data


nexus = NexusOrchestrator()