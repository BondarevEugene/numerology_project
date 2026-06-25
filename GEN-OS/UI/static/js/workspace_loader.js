/*
═══════════════════════════════════════════════════════════════════════════════

GEN-OS®
Genesys Operating System

Workspace Loader

Version:
BUILD-0016

Description:

Главный загрузчик рабочих областей GEN-OS.

Shell никогда не знает содержимого Workspace.
Workspace никогда не знает Shell.

Все взаимодействие происходит через WorkspaceLoader.

═══════════════════════════════════════════════════════════════════════════════
*/

class WorkspaceLoader {

   constructor() {

      this.currentWorkspace = null;

      this.cache = {};

      this.container = document.getElementById("workspace-container");

   }

   async open(name) {

      if (this.currentWorkspace === name) {

         return;

      }

      this.showLoading();

      try {

         let html;

         if (this.cache[name]) {

            html = this.cache[name];

         } else {

            const response = await fetch(

               `/workspace/${name}`

            );

            html = await response.text();

            this.cache[name] = html;

         }

         this.container.innerHTML = html;

         this.currentWorkspace = name;

         this.highlightDock(name);

         this.updateTitle(name);

         this.log(

            "Workspace",

            `${name} loaded`,

            "success"

         );

         this.initializeWorkspace(name);

      } catch (e) {

         console.error(e);

         this.container.innerHTML = this.errorScreen(e);

         this.log(

            "Loader",

            e.message,

            "error"

         );

      }

   }

   initializeWorkspace(name) {

      const fn =

         window[

            `${name}WorkspaceInit`

         ];

      if (typeof fn === "function") {

         fn();

      }

   }

   highlightDock(name) {

      document

         .querySelectorAll(

            ".dock-button"

         )

         .forEach(btn => {

            btn.classList.remove("active");

            if (btn.dataset.workspace === name) {

               btn.classList.add("active");

            }

         });

   }

   updateTitle(name) {

      const title =

         document.querySelector(

            ".workspace-title h2"

         );

      const subtitle =

         document.querySelector(

            ".workspace-title span"

         );

      const names = {

         human: "Digital Twin",

         career: "Career Intelligence",

         knowledge: "Knowledge Explorer",

         import: "Knowledge Import",

         simulation: "Future Simulator",

         ai: "AI Advisor",

         platform: "Platform"

      };

      const subtitles = {

         human: "Human Intelligence",

         career: "Professional Analytics",

         knowledge: "Knowledge Graph",

         import: "Registry Import Pipeline",

         simulation: "Future Prediction",

         ai: "Genesis Neural Core",

         platform: "Configuration"

      };

      title.innerHTML =

         names[name] || name;

      subtitle.innerHTML =

         subtitles[name] || "";

   }

   showLoading() {

      this.container.innerHTML =

         `

<div class="gen-loading">

<div class="gen-spinner"></div>

<div class="gen-loading-title">

Loading Workspace...

</div>

</div>

`;

   }

   errorScreen(error) {

      return `

<div class="gen-error">

<div class="gen-error-icon">

⚠

</div>

<h2>

Workspace failed

</h2>

<p>

${error.message}

</p>

</div>

`;

   }

   log(module, message, type = "info") {

      if (

         typeof consoleLog === "function"

      ) {

         consoleLog(

            module,

            message,

            type

         );

      }

   }

}

window.loader =

   new WorkspaceLoader();

document

   .addEventListener(

      "DOMContentLoaded",

      () => {

         document

            .querySelectorAll(

               ".dock-button"

            )

            .forEach(button => {

               button.onclick = () => {

                  loader.open(

                     button.dataset.workspace

                  );

               };

            });

         loader.open(

            "human"

         );

      });