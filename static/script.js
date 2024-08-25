const textToType = document.getElementById('text-to-type');
const typingArea = document.getElementById('typing-area');
const timerElement = document.getElementById('timer');
const wpmElement = document.getElementById('wpm');
const restartBtn = document.getElementById('restart-btn');

let timer, startTime;
let isPlaying = false;

const sampleText = "Szybkie pisanie na klawiaturze to ważna umiejętność.";

function startGame() {
    textToType.innerText = sampleText;
    typingArea.value = '';
    typingArea.disabled = false;
    typingArea.focus();
    startTime = new Date();
    timer = setInterval(updateTimer, 1000);
    isPlaying = true;
}

function updateTimer() {
    const currentTime = new Date();
    const timeElapsed = Math.floor((currentTime - startTime) / 1000);
    timerElement.innerText = timeElapsed;
    calculateWPM(timeElapsed);
}

function calculateWPM(timeElapsed) {
    const wordsTyped = typingArea.value.trim().split(/\s+/).length;
    const wpm = Math.floor((wordsTyped / timeElapsed) * 60);
    wpmElement.innerText = isNaN(wpm) ? 0 : wpm;
}

function checkCompletion() {
    if (typingArea.value.trim() === sampleText) {
        clearInterval(timer);
        typingArea.disabled = true;
        isPlaying = false;
    }
}

function restartGame() {
    clearInterval(timer);
    timerElement.innerText = '0';
    wpmElement.innerText = '0';
    startGame();
}

typingArea.addEventListener('input', () => {
    if (!isPlaying) startGame();
    checkCompletion();
});

restartBtn.addEventListener('click', restartGame);
