async function analyze() {

    const progress = document.getElementById("progressBar");
    const progressContainer = document.getElementById("progressContainer");
    const progressText = document.getElementById("progressText");

    progressContainer.style.display = "block";

    let percent = 0;

    const timer = setInterval(() => {
        if (percent < 90) {
            percent += 10;
            progress.style.width = percent + "%";
            progressText.innerHTML = "Analyzing... " + percent + "%";
        }
    }, 300);

    const resume = document.getElementById("resumeFile").files[0];
    const job = document.getElementById("jobFile").files[0];

    if (!resume || !job) {
        alert("Please upload both PDF files.");

        clearInterval(timer);
        progressContainer.style.display = "none";

        return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job", job);

    document.getElementById("result").innerHTML = `
        <div class="card score-card">
            <h2>🤖 AI is analyzing your resume...</h2>

            <div class="loader"></div>

            <p>Please wait 10–30 seconds...</p>
        </div>
    `;

    const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        alert("Error while analyzing resume.");
        return;
    }

    const data = await response.json();

    let html = `
<div class="dashboard">

    <div class="card score-card">
        <h2>📊 ATS Resume Score</h2>

        <div class="chart-container">
            <canvas id="scoreChart"></canvas>
        </div>

        <h2 class="score-text">${data.score}%</h2>

        <p class="time-text">
    Generated on: ${new Date().toLocaleString()}
    </p>
    </div>

    <div class="card">
        <h2>✅ Matched Skills</h2>
        <ul>
            ${data.matched.map(skill => `<li>🟢 ${skill}</li>`).join("")}
        </ul>
    </div>

    <div class="card">
        <h2>❌ Missing Skills</h2>
        <ul>
            ${data.missing.map(skill => `<li>🔴 ${skill}</li>`).join("")}
        </ul>
    </div>

    <div class="card">
        <h2>📄 AI Resume Summary</h2>
        <pre>${data.summary}</pre>
    </div>

    <div class="card">
        <h2>💡 AI Resume Suggestions</h2>
        <ul>
            ${data.suggestions.map(item => `<li>✅ ${item}</li>`).join("")}
        </ul>
    </div>

    <div class="card">
        <h2>📄 AI Cover Letter</h2>
        <pre>${data.cover_letter}</pre>
    </div>

    <div class="card">
        <h2>🎤 AI Interview Questions</h2>
        <pre>${data.interview_questions}</pre>
    </div>

</div>
`;
clearInterval(timer);

progress.style.width = "100%";
progressText.innerHTML = "";
progressText.style.display = "none";
progressContainer.style.display = "none";

document.getElementById("result").innerHTML = html;
const scoreText = document.querySelector(".score-text");

if (scoreText) {

    if (data.score >= 80) {
        scoreText.style.color = "#16a34a";
    }
    else if (data.score >= 60) {
        scoreText.style.color = "#f59e0b";
    }
    else {
        scoreText.style.color = "#dc2626";
    }

}

const downloadBtn = document.getElementById("downloadReport");

if (downloadBtn) {
    downloadBtn.onclick = function () {
        window.print();
    };
}

const ctx = document.getElementById("scoreChart");

new Chart(ctx, {
    type: "doughnut",
    data: {
        datasets: [{
            data: [data.score, 100 - data.score],
            backgroundColor: [
                "#4CAF50",
                "#E5E7EB"
            ],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        cutout: "75%",
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false
            }
        }
    }
});
}
const toggle = document.getElementById("themeToggle");

if (toggle) {
    toggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            toggle.innerText = "☀️ Light Mode";
        } else {
            toggle.innerText = "🌙 Dark Mode";
        }
    });
}