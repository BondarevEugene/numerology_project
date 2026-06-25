"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Platform

FILE:launcher.py
BUILD:0023
DESCRIPTION
Главная точка входа платформы.
Запускает Kernel.
Проверяет все подсистемы.
После успешной загрузки
передает управление Workspace.

═══════════════════════════════════════════════════════════════════════════════
"""

from datetime import datetime
from genesis.kernel.bootstrap import boot


# ==========================================================
# BANNER
# ==========================================================

def banner():
    print()
    print("════════════════════════════════════════════════════════════")
    print("")
    print("                 ██████╗ ███████╗███╗   ██╗")
    print("                ██╔════╝ ██╔════╝████╗  ██║")
    print("                ██║  ███╗█████╗  ██╔██╗ ██║")
    print("                ██║   ██║██╔══╝  ██║╚██╗██║")
    print("                ╚██████╔╝███████╗██║ ╚████║")
    print("                 ╚═════╝ ╚══════╝╚═╝  ╚═══╝")
    print()
    print("                 G E N E S I S   H R ®")
    print("")
    print("               GEN-OS Enterprise Platform")
    print("")
    print("════════════════════════════════════════════════════════════")
    print()


# ==========================================================
# START
# ==========================================================

def start():
    banner()
    kernel = boot()
    print()
    print("════════════════════════════════════════════════════════════")
    print(" PLATFORM STATUS")
    print("════════════════════════════════════════════════════════════")
    print()
    print(
        f"Version ............. {kernel.VERSION}"
    )
    print(
        f"Platform ............ {kernel.PLATFORM}"
    )
    print(
        f"Started ............. {datetime.utcnow()}"
    )
    print()
    print("════════════════════════════════════════════════════════════")
    print(" MODULES")
    print("════════════════════════════════════════════════════════════")
    print()
    for module in kernel.modules.modules():
        state = "ONLINE"
        if not module.enabled:
            state = "OFFLINE"
        print(
            f"{module.title:<30} {state}"
        )
    print()
    print("════════════════════════════════════════════════════════════")
    print(" WORKSPACES")
    print("════════════════════════════════════════════════════════════")
    print()
    for workspace in kernel.workspaces.all():
        print(
            f"{workspace.icon}  "
            f"{workspace.title:<32}"
            f"{workspace.route}"
        )
    print()
    print("════════════════════════════════════════════════════════════")
    print(" SERVICES")
    print("════════════════════════════════════════════════════════════")
    print()
    if kernel.container.count == 0:
        print(
            "No services registered"
        )
    else:
        for service in kernel.container.dump():
            print(
                f"{service['name']:<25}"
                f"{service['class']}"
            )
    print()
    print("════════════════════════════════════════════════════════════")
    print(" SYSTEM READY")
    print("════════════════════════════════════════════════════════════")
    print()
    print("Genesis Platform successfully initialized.")
    print()
    return kernel


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    start()
