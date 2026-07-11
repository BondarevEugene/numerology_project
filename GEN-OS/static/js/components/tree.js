class Tree {
   constructor(root) {
      this.root = root;
   }
   initialize() {
      this.root
         .querySelectorAll(
            ".gen-tree-item"
         )
         .forEach(
            item => {
               item.onclick = () => {
                  this.select(item);
               };
            }
         );
   }
   select(item) {
      this.root
         .querySelectorAll(
            ".gen-tree-item"
         )
         .forEach(
            i => i.classList.remove(
               "active"
            )
         );
      item.classList.add(
         "active"
      );
   }
}


window.Tree = Tree;