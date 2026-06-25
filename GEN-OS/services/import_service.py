"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
Import Service
BUILD:0034

DESCRIPTION
-----------
Главный сервис импорта платформы.

Через него будут работать:

• Excel
• CSV
• JSON
• ESCO
• O*NET
• API
• AI Import

═══════════════════════════════════════════════════════════════════════
"""

from typing import Dict


class ImportService:

    def __init__(self):
        self.providers = {}

    def register(
        self,
        name,
        provider
    ):
        self.providers[name] = provider

    def providers_list(self):
        return sorted(
            self.providers.keys()
        )

    def exists(
        self,
        provider
    ):
        return provider in self.providers

    def import_file(
        self,
        provider,
        filename
    ):
        if provider not in self.providers:
            raise Exception(
                f"Provider '{provider}' not registered."
            )
        return self.providers[
            provider
        ].import_file(
            filename
        )

    def statistics(self):
        return {
            "providers":
                len(self.providers)
        }


import_service = ImportService()