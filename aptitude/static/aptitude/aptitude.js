let cheatedCount = 0;
const cheatLimit = 3;
const totalTestDuration = 40 * 60; // 40 minutes
let remainingTime = totalTestDuration;
let timerInterval;
let isLoggingOut = false;

// Debouncing variables
let lastBlurTime = 0;
let lastKeyTime = 0;
const DEBOUNCE_TIME = 300; // 300ms debounce

function showWarning(msg) {
  // Non-blocking DOM update
  setTimeout(() => {
    const banner = document.getElementById("warningBanner");
    if (banner) {
      banner.innerText = msg;
      banner.style.display = "block";
    }
  }, 0);
}

function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === 'csrftoken') return value;
  }
  return '';
}

function logCheating() {
  if (isLoggingOut) return;

  cheatedCount++;
  
  // Non-blocking fetch request
  setTimeout(() => {
    fetch('/aptitude/log-cheating/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    }).catch(() => {}); // Silent fail to prevent blocking
  }, 0);

  if (cheatedCount >= cheatLimit) {
    isLoggingOut = true;
    // Non-blocking alert and redirect
    setTimeout(() => {
      alert("🚫 You have violated the rules multiple times. You will be logged out.");
      window.location.href = "/logout/";
    }, 0);
  }
}

function initCheatingPrevention() {
  // Optimized blur handler with debouncing
  window.addEventListener("blur", () => {
    if (isLoggingOut) return;
    
    const now = Date.now();
    if (now - lastBlurTime < DEBOUNCE_TIME) return;
    lastBlurTime = now;
    
    // Non-blocking execution
    setTimeout(() => {
      showWarning("⚠️ Tab switching is not allowed!");
      logCheating();
    }, 0);
  }, { passive: true });

  // Optimized keydown handler with debouncing
  document.addEventListener("keydown", (e) => {
    if (isLoggingOut) return;
    
    const isBlocked = ["F5", "Alt", "Control"].includes(e.key) || e.ctrlKey || e.altKey;
    
    if (isBlocked) {
      e.preventDefault(); // Prevent immediately
      
      const now = Date.now();
      if (now - lastKeyTime < DEBOUNCE_TIME) return;
      lastKeyTime = now;
      
      // Non-blocking execution
      setTimeout(() => {
        showWarning("⚠️ Shortcut keys are blocked!");
        logCheating();
      }, 0);
    }
  }, { passive: false });
}

function initWebcam() {
  const camera = document.getElementById('userCamera');
  if (!camera) return;

  if (!window.webcamStream) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        camera.srcObject = stream;
        window.webcamStream = stream; // store globally
      })
      .catch(err => {
        console.error("Webcam blocked:", err);
        if (!isLoggingOut) {
          setTimeout(() => logCheating(), 0);
        }
      });
  } else {
    camera.srcObject = window.webcamStream;
  }
}

function formatTime(sec) {
  const m = Math.floor(sec / 60).toString().padStart(2, '0');
  const s = (sec % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function initTimer() {
  const timerBox = document.getElementById("timer-box");
  if (!timerBox) return;

  timerBox.innerText = formatTime(remainingTime);
  timerInterval = setInterval(() => {
    if (isLoggingOut) {
      clearInterval(timerInterval);
      return;
    }
    
    remainingTime--;
    timerBox.innerText = formatTime(remainingTime);

    if (remainingTime <= 0) {
      clearInterval(timerInterval);
      alert("⏱️ Time is over! Your test will be submitted.");
      const form = document.querySelector("form");
      if (form) {
        form.submit();
      }
    }
  }, 1000);
}

function initInstructionCountdown() {
  const timerEl = document.getElementById("instruction-timer");
  const startBtn = document.getElementById("start-test-btn");
  const startUrl = startBtn?.getAttribute("data-url");

  if (!timerEl || !startBtn || !startUrl) return;

  let count = 2 * 60; // 2 mins

  timerEl.innerText = formatTime(count);
  const countdown = setInterval(() => {
    if (isLoggingOut) {
      clearInterval(countdown);
      return;
    }
    
    count--;
    timerEl.innerText = formatTime(count);

    if (count <= 0) {
      clearInterval(countdown);
      startBtn.classList.remove("disabled");
      startBtn.removeAttribute("tabindex");
      startBtn.removeAttribute("aria-disabled");
      startBtn.innerText = "✅ Starting Test...";
      setTimeout(() => {
        window.location.href = startUrl;
      }, 1000);
    }
  }, 1000);
}

document.addEventListener('DOMContentLoaded', () => {
  initCheatingPrevention();
  initWebcam();
  initTimer();
  initInstructionCountdown();
});
