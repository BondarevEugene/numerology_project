/*
============================================================

GENESIS LOGGER

============================================================
*/

class GenesisLogger {

    info(...args){

        console.log("[INFO]",...args);

    }

    warn(...args){

        console.warn("[WARN]",...args);

    }

    error(...args){

        console.error("[ERROR]",...args);

    }

    success(...args){

        console.log("✅",...args);

    }

}

window.logger=new GenesisLogger();