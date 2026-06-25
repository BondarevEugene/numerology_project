/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Toolbar Controller

BUILD:0119

DESCRIPTION

Главная панель действий платформы.

═══════════════════════════════════════════════════════════════════════
*/

class Toolbar {

   constructor() {

      this.initialize();
   }

   initialize() {

      console.log(
         "[TOOLBAR] Ready"
      );

      this.bind();

      this.bindWorkspaceTabs();
   }

   bindWorkspaceTabs() {

      document
         .querySelectorAll(
            ".gen-tab"
         )
         .forEach(
            tab => {

               tab.addEventListener(
                  "click",
                  () => {

                     const workspaceId =
                        tab.dataset.workspace;

                     console.log(
                        "[WORKSPACE TAB]",
                        workspaceId
                     );

                     if (
                        window.workspaceLoader
                     ) {

                        window
                           .workspaceLoader
                           .open(
                              workspaceId
                           );

                     }

                  }
               );

            }
         );
   }
   bind() {

      document
         .querySelectorAll(
            "[data-toolbar-action]"
         )
         .forEach(
            button => {

               button.addEventListener(
                  "click",
                  () => {

                     this.execute(
                        button.dataset.toolbarAction
                     );

                  }
               );

            }
         );
   }

   execute(action) {

      console.log(
         "[TOOLBAR]",
         action
      );

      document.dispatchEvent(
         new CustomEvent(
            "toolbar.action", {
               detail: {
                  action
               }
            }
         )
      );
   }
}

window.toolbar =
   new Toolbar();