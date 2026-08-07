/*
═══════════════════════════════════════════════════════════════════════

GENESIS HR®
GENESIS REGISTRY
BUILD:0200
DESCRIPTION
Единый реестр всех модулей платформы.

═══════════════════════════════════════════════════════════════════════
*/

class Registry {
   constructor() {
      this.modules = new Map();
   }
   register(name, instance) {
      if (this.modules.has(name)) {
         console.warn(
            "[Registry] Module already exists:",
            name
         );
         return instance;
      }
      this.modules.set(name, instance);
      console.log(
         "[Registry] Registered:",
         name
      );
      return instance;
   }
   get(name) {
      return this.modules.get(name);
   }
   has(name) {
      return this.modules.has(name);
   }
   remove(name) {
      this.modules.delete(name);
   }

   clear() {
      this.modules.clear();
   }

   list() {
      return Array.from(
         this.modules.keys()
      );
   }
}

window.Registry = Registry;