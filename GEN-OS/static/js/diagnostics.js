/*
============================================================

GENESIS DIAGNOSTICS

============================================================
*/

class Diagnostics{

    check(){

        console.group("Diagnostics");

        [

            "Registry",

            "StateManager",

            "Genesis",

            "workspaceLoader",

            "toolbar",

            "explorer"

        ].forEach(name=>{

            console.log(

                name,

                window[name]?"OK":"MISSING"

            );

        });

        console.groupEnd();

    }

}

window.diagnostics=new Diagnostics();