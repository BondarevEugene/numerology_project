"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Registry Service
BUILD:0067
DESCRIPTION
Центральный сервис доступа
ко всем Registry платформы.

═══════════════════════════════════════════════════════════════════════
"""

from services.entity_service import entity_service
from services.profession_service import profession_service
from services.competency_service import competency_service
from services.relation_service import relation_service


class RegistryService:

    def entities(self):
        return entity_service.all()

    def professions(self):
        return profession_service.all()

    def competencies(self):
        return competency_service.all()

    def relations(self):
        return relation_service.all()

    def statistics(self):

        return {

            "entities":
                entity_service.count(),

            "professions":
                profession_service.count(),

            "competencies":
                competency_service.count(),

            "relations":
                relation_service.count()

        }


registry_service = RegistryService()