"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Platform
FILE:kernel/platform.py
BUILD:0401

DESCRIPTION
Главное ядро Genesis Platform.
Platform объединяет все подсистемы платформы,
но не содержит бизнес-логики.
Любая новая подсистема должна подключаться
через Platform.

═══════════════════════════════════════════════════════════════════════
"""

from kernel.manifest import PLATFORM
from kernel.modules import MODULES

from kernel.shell_context import shell_context
from kernel.workspace_runtime import workspace_runtime

from services.workspace_service import workspace_service

from kernel.workspace_renderer import (workspace_renderer)

from kernel.workspace_manager import workspace_manager

from kernel.event_bus import event_bus


class Platform:
    """
    Центральный объект платформы.

    Через Platform осуществляется доступ
    ко всем сервисам, рабочим пространствам
    и системным компонентам.
    """

    def __init__(self):
        # Если вы импортировали workspace_service, убедитесь, что он доступен
        from services.workspace_service import workspace_service
        self.workspace = workspace_service  # <--- Инициализация атрибута
        self.workspaces = self.workspace  # Теперь эта строка будет работать
        # --------------------------------------------------
        # Manifest
        # --------------------------------------------------

        self.manifest = PLATFORM
        self.modules = MODULES
        self.events = event_bus
        # --------------------------------------------------
        # Core Services
        # --------------------------------------------------

        self.runtime = workspace_runtime
        self.workspace = workspace_manager
        self.workspace_service = workspace_service
        self.shell = shell_context
        self.renderer = workspace_renderer

        # --------------------------------------------------
        # Registries
        # --------------------------------------------------

        self._services = {}
        self._ui = {}
        self._plugins = {}
        self._events = {}
        self._cache = {}
        self._storage = {}
        self._settings = {}
        self._state = {}

    # ======================================================
    # PLATFORM
    # ======================================================

    def boot(self):

        print("=" * 70)
        print(">>> PLATFORM.BOOT()")
        print("=" * 70)

        from workspaces import register_workspaces

        print(">>> register_workspaces imported")

        registry = register_workspaces()

        print(">>> Registry size:", len(registry))

        print(">>> WorkspaceManager size:", len(self.workspace.all()))

        for ws in self.workspace.all():
            print("    •", ws.id)

        self.runtime.boot()

        # --------------------------------------------------
        # Core services
        # --------------------------------------------------

        self._services["runtime"] = self.runtime
        self._services["workspace"] = self.workspace
        self._services["workspace_service"] = self.workspace_service
        self._services["shell"] = self.shell
        self._services["renderer"] = self.renderer
        self._services["events"] = self.events

        print("=" * 70)
        print(">>> PLATFORM READY")
        print("=" * 70)

        return self

    # ======================================================
    # CONTEXT
    # ======================================================

    def context(self):
        context = self.shell.build()
        context["platform"] = self
        context["services"] = self.services
        if self.workspace.all():
            context["workspaces"] = self.workspace.all()
        context["current_workspace"] = self.current_workspace
        return context

    # ======================================================
    # SERVICES
    # ======================================================

    def register_service(self, name, service):
        self._services[name] = service
        return service

    def service(self, name):
        return self._services.get(name)

    @property
    def services(self):
        return self._services

    # ======================================================
    # UI
    # ======================================================

    def register_ui(self, name, component):
        self._ui[name] = component
        return component

    def ui(self, name):
        return self._ui.get(name)

    @property
    def ui_registry(self):
        return self._ui

    # ======================================================
    # PLUGINS
    # ======================================================

    def register_plugin(self, plugin):
        self._plugins[plugin.name] = plugin
        return plugin

    def plugin(self, name):
        return self._plugins.get(name)

    @property
    def plugins(self):
        return self._plugins

    # ======================================================
    # EVENTS
    # ======================================================

    def on(self, event, callback):
        self._events.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        for callback in self._events.get(event, []):
            callback(*args, **kwargs)

    # ======================================================
    # STORAGE
    # ======================================================

    def set(self, key, value):
        self._storage[key] = value

    def get(self, key, default=None):
        return self._storage.get(key, default)

    # ======================================================
    # SETTINGS
    # ======================================================

    def configure(self, **kwargs):
        self._settings.update(kwargs)

    def setting(self, key, default=None):
        return self._settings.get(key, default)

    # ======================================================
    # STATE
    # ======================================================

    @property
    def state(self):
        return self._state

    # ======================================================
    # WORKSPACE
    # ======================================================

    @property
    def current_workspace(self):
        return self.runtime.current()

    # ======================================================
    # INFO
    # ======================================================

    def statistics(self):
        return {
            "modules": len(self.modules),
            "workspaces": len(self.workspace.all()),
            "services": len(self._services),
            "plugins": len(self._plugins),
            "current_workspace":
                self.current_workspace.id
                if self.current_workspace
                else None
        }

    # ======================================================
    # DEBUG
    # ======================================================

    def __repr__(self):
        return (
            "<GenesisPlatform "
            f"modules={len(self.modules)} "
            f"workspaces={len(self.workspaces)} "
            f"services={len(self._services)} "
            f"plugins={len(self._plugins)}>"
        )

    # ======================================================
    # RENDER
    # ======================================================

    def render(self, workspace):
        return self.renderer.render(
            workspace

        )

    @property
    def version(self):
        return self.manifest["version"]


platform = Platform()
