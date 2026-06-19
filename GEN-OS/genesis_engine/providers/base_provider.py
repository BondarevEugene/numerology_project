"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE

MODULE
    Base Provider

MODULE ID
    GKH-PROVIDER-001

VERSION
    1.0.0 Alpha

LAYER
    Providers

DESCRIPTION

Abstract base class for every Genesis
Knowledge Provider.

A Provider is responsible ONLY for obtaining
raw data from an external source.

Examples

    JSON Provider

    Excel Provider

    ESCO Provider

    O*NET Provider

    Wikidata Provider

    OpenLibrary Provider

Provider DOES NOT

    ✗ Parse data

    ✗ Create Entities

    ✗ Save Registry

    ✗ Build Relations

Pipeline

    Provider
        ↓
    Parser
        ↓
    Factory
        ↓
    Registry

═══════════════════════════════════════════════════════════════════════
"""

from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    NAME = "Base Provider"

    VERSION = "1.0.0"

    @abstractmethod
    def load(self):
        """
        Returns raw dataset.

        Returns
        -------
        list | dict
        """
        raise NotImplementedError
