"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 MODULE
-----------------------------------------------------------------------------
 Platform Bootstrap

 FILE
-----------------------------------------------------------------------------
 bootstrap.py

 BUILD
-----------------------------------------------------------------------------
 0156

 DESCRIPTION
-----------------------------------------------------------------------------

 Bootstrap собирает GEN-OS из отдельных модулей.

 Именно здесь происходит регистрация всех Runtime-компонентов.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging

from kernel.kernel import kernel

from core.runtime import runtime
from core.platform_context import platform_context
from core.service_registry import service_registry
from core.event_bus import event_bus
from core.lifecycle import lifecycle

from kernel.module_loader import module_loader
import modules

LOGGER = logging.getLogger("GEN-OS.Bootstrap")

def bootstrap():
    """
    Assemble platform.
    """

    #
    # Load platform modules
    #
    module_loader.load_all(
        modules
    )
    module_loader.initialize(
        kernel
    )

    LOGGER.info("Bootstrapping GEN-OS...")
    #
    # Runtime
    #
    runtime.register_service(
        "kernel",
        kernel
    )

    runtime.register_service(
        "event_bus",
        event_bus
    )

    runtime.register_service(
        "service_registry",
        service_registry
    )

    runtime.register_service(
        "platform_context",
        platform_context
    )

    runtime.register_service(
        "lifecycle",
        lifecycle
    )

    #
    # Platform Context
    #

    platform_context.register(
        "runtime",
        runtime
    )

    platform_context.register(
        "registry",
        service_registry
    )

    platform_context.register(
        "event_bus",
        event_bus
    )

    platform_context.register(
        "lifecycle",
        lifecycle
    )

    #
    # Kernel Lifecycle
    #

    lifecycle.register(kernel)

    LOGGER.info(
        "GEN-OS successfully bootstrapped."
    )

    return kernel

