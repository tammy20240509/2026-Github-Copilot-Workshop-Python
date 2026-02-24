let timerDuration = 25 * 60; // 25分
let remaining = timerDuration;
let timer = null;
let isRunning = false;

const minutesEl = document.getElementById('timer-minutes');
const secondsEl = document.getElementById('timer-seconds');
const progressBar = document.getElementById('progress-bar');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');

function updateDisplay() {
    const min = Math.floor(remaining / 60);
    const sec = remaining % 60;
    minutesEl.textContent = String(min).padStart(2, '0');
    secondsEl.textContent = String(sec).padStart(2, '0');
    const percent = 100 * (timerDuration - remaining) / timerDuration;
    progressBar.style.width = percent + '%';
}

function tick() {
    if (remaining > 0) {
        remaining--;
        updateDisplay();
    } else {
        clearInterval(timer);
        isRunning = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        // TODO: アラーム音や通知
    }
}

startBtn.onclick = function() {
    if (!isRunning) {
        timer = setInterval(tick, 1000);
        isRunning = true;
        startBtn.disabled = true;
        pauseBtn.disabled = false;
    }
};

pauseBtn.onclick = function() {
    if (isRunning) {
        clearInterval(timer);
        isRunning = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
    }
};

resetBtn.onclick = function() {
    clearInterval(timer);
    isRunning = false;
    remaining = timerDuration;
    updateDisplay();
    startBtn.disabled = false;
    pauseBtn.disabled = true;
};

// 初期状態
updateDisplay();
pauseBtn.disabled = true;
