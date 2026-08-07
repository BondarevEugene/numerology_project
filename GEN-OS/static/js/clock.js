/*
LIVE CLOCK
*/

class Clock{
    constructor(){
        this.node=
            document.querySelector(
                "[data-clock]"
            );
        this.start();
    }
    start(){
        setInterval(
            ()=>{
                if(!this.node)return;
                this.node.innerHTML=
                    new Date()
                    .toLocaleTimeString();
            },
            1000
        );
    }
}
window.clock=

    new Clock();