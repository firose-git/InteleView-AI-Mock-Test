let recognition;
let timerInterval;
let currentIndex = 0;
let fullTranscript = [];

const startBtn = document.getElementById("start-btn");
const skipBtn = document.getElementById("skip-btn");
const stopBtn = document.getElementById("stop-btn");
const timerDisplay = document.getElementById("timer");
const transcriptBox = document.getElementById("transcription");
const topicBox = document.getElementById("topic-box");
const topicNumber = document.getElementById("topic-number");

const allResults = [];
// const topics = ["Topic 1", "Topic 2", "Topic 3"]; // Replace with your actual topics

function showTopic(index) {
    if (index >= topics.length) {
        console.warn("No more topics.");
        sendResultsToBackend();
        return;
    }

    topicBox.textContent = topics[index];
    topicNumber.textContent = index + 1;
    transcriptBox.value = '';
    startBtn.disabled = false;
    stopBtn.classList.add("d-none");
}


function startTimer(duration) {
    let time = duration;
    timerInterval = setInterval(() => {
        const min = String(Math.floor(time / 60)).padStart(2, '0');
        const sec = String(time % 60).padStart(2, '0');
        timerDisplay.textContent = `${min}:${sec}`;
        if (--time < 0) stopRecognition();
    }, 1000);
}

function startRecognition() {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;

    let full = '';
    recognition.onresult = (event) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            const text = event.results[i][0].transcript;
            interim += text + ' ';
            if (event.results[i].isFinal) full += text + ' ';
        }
        transcriptBox.value = full + interim;
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        stopRecognition();
    };

    recognition.onend = () => stopRecognition();

    recognition.start();
}

function stopRecognition() {
    clearInterval(timerInterval);
    if (recognition) recognition.stop();

    stopBtn.classList.add("d-none");

    const transcript = transcriptBox.value.trim();
    const topic = topics[currentIndex];

    if (currentIndex < topics.length) {
        allResults.push({
            topic,
            transcript,
            feedback: null
        });
    }

    currentIndex++;
    showTopic(currentIndex);  // This will call sendResultsToBackend if out of range
}
    
function sendResultsToBackend() {
    const csrftoken = getCookie('csrftoken');
    // Remove this line: const resultsURL = "{% url 'GD:gd_results' %}";

    fetch(submitResultsURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ results: allResults })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === "success") {
            window.location.href = resultsURL; // ✅ Now uses the variable from HTML
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error submitting results:", error);
        alert("Submission failed. Please try again.");
    });
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

startBtn.addEventListener("click", () => {
    startBtn.disabled = true;
    stopBtn.classList.remove("d-none");
    transcriptBox.value = "";
    startTimer(180);
    startRecognition();
});

stopBtn.addEventListener("click", stopRecognition);

skipBtn.addEventListener("click", () => {
    currentIndex++;
    if (currentIndex < topics.length) showTopic(currentIndex);
    else sendResultsToBackend();
});

showTopic(currentIndex);
