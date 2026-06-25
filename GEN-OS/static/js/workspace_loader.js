/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Workspace Loader

BUILD:0135

DESCRIPTION

Управляет переключением Workspace.

Toolbar
↓
Workspace Runtime
↓
Workspace Host

═══════════════════════════════════════════════════════════════════════
*/

class WorkspaceLoader {

```
constructor() {

    this.current = null;

    this.host =
        document.querySelector(
            ".gen-workspace-body"
        );
}

open(workspaceId) {

    console.log(
        "[WORKSPACE]",
        workspaceId
    );

    this.current =
        workspaceId;

    window.location.href =
        "/workspace/" +
        workspaceId;
}

currentWorkspace() {

    return this.current;
}
```

}

window.workspaceLoader =
new WorkspaceLoader();
