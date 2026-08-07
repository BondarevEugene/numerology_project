/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
SHELL ENGINE
BUILD:0120
═══════════════════════════════════════════════════════════════════════
*/

class Shell {
   constructor() {
      this.state = {
         workspace: "human",
         loading: false,
         explorer: true,
         inspector: true,
         console: true
      };

      this.initialize();
   }

   initialize() {
      console.log(
         "[GEN-OS] Shell Booting..."
      );
      this.bind();
      this.restore();
      this.broadcast();
   }

   bind() {
      document.addEventListener(
         "toolbar.action",
         (event) => {
            this.handleToolbar(
               event.detail.action
            );
         }
      );

      document.addEventListener(
         "workspace.change",
         (event) => {
            this.loadWorkspace(
               event.detail.workspace
            );
         }
      );
   }

   handleToolbar(action) {
      console.log(
         "[Toolbar]",
         action
      );

      switch (action) {
         case "toggleExplorer":
            this.toggleExplorer();
            break;
         case "toggleInspector":
            this.toggleInspector();
            break;
         case "toggleConsole":
            this.toggleConsole();

            break;

      }

   }

   toggleExplorer() {

      const explorer =

         document.querySelector(

            ".shell-explorer"

         );

      explorer.classList.toggle(

         "hidden"

      );

   }

   toggleInspector() {

      document.querySelector(

         ".shell-inspector"

      ).classList.toggle(

         "hidden"

      );

   }

   toggleConsole() {

      document.querySelector(

         ".shell-console"

      ).classList.toggle(

         "hidden"

      );

   }

   loadWorkspace(id) {

      console.log(

         "[Workspace]",

         id

      );

      window.location =

         "/workspace/" + id;

   }

   restore() {

      console.log(

         "[Shell] Restoring session"

      );

   }

   broadcast() {

      document.dispatchEvent(

         new CustomEvent(

            "shell.ready"

         )

      );

   }

}

window.shell =

   new Shell();