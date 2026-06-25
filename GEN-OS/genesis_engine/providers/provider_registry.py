"""
═══════════════════════════════════════════════════════════════════════

Genesis Provider Registry

Contains every supported
knowledge provider.

Version

0.1

═══════════════════════════════════════════════════════════════════════
"""


class ProviderRegistry:

    _providers = {}

    @classmethod
    def register(cls, provider):

        cls._providers[
            provider.provider_name
        ] = provider

    @classmethod
    def get(cls, name):

        return cls._providers.get(name)

    @classmethod
    def all(cls):

        return cls._providers