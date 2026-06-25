function updateClock() {

    const clock = document.getElementById('clock');

    if (!clock) return;

    const now = new Date();

    clock.innerText = now.toLocaleTimeString(
        'ru-RU',
        {
            hour12: false
        }
    );
}

setInterval(updateClock, 1000);

updateClock();