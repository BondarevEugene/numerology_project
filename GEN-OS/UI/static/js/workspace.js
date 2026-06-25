/*
═══════════════════════════════════════════════

GENESIS HR®

Workspace Engine

═══════════════════════════════════════════════
*/

class Workspace{

constructor(){

this.widgets=[];

this.events=[];

}

boot(){

console.log("GENOS Workspace started");

}

register(widget){

this.widgets.push(widget);

}

}

window.GENOS=new Workspace();

window.onload=()=>{

GENOS.boot();

}