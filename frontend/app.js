const API_BASE = 'http://localhost:8000';

const courseIcons = {
    'Introduction to Deep Learning': '🤖',
    'Quantum Machine Learning': '⚛️',
    'Data Science Foundations': '📊',
    'Agile Software Engineering': '💻',
    'Advanced Natural Language Processing': '🧠',
    'Cybersecurity & AI': '🔐'
};

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        const container = document.getElementById('courses-container');
        const mlSelect = document.getElementById('ml-course-select');
        const dlSelect = document.getElementById('dl-course-select');
        const qmlSelect = document.getElementById('qml-course-select');

        container.innerHTML = '';
        mlSelect.innerHTML = '';
        dlSelect.innerHTML = '';
        qmlSelect.innerHTML = '';

        data.courses.forEach(course => {
            // Add to dropdowns
            const optionHTML = `<option value="${course.course_name}">${course.course_name}</option>`;
            mlSelect.innerHTML += optionHTML;
            dlSelect.innerHTML += optionHTML;
            qmlSelect.innerHTML += optionHTML;

            // Render Course Card
            const icon = courseIcons[course.course_name] || '📚';
            const cardHTML = `
                <div class="course-card glass">
                    <div class="course-icon">${icon}</div>
                    <h3>${course.course_name}</h3>
                    <div class="progress-bar"><div class="fill" style="width: ${course.progress_percent}%;"></div></div>
                    <p class="progress-text">${course.progress_percent}% Completed</p>
                    <button class="btn accent" onclick="scrollToAnalytics('${course.course_name}')">Analyze Course Performance</button>
                </div>
            `;
            container.innerHTML += cardHTML;
        });
    } catch (error) {
        console.error("Failed to load dashboard from DB", error);
        document.getElementById('courses-container').innerHTML = '<p style="color:red">Error: Ensure FastAPI Backend is running with the Database active.</p>';
    }
}

function scrollToAnalytics(courseName) {
    document.getElementById('analytics').scrollIntoView({ behavior: 'smooth' });
    document.getElementById('ml-course-select').value = courseName;
    document.getElementById('dl-course-select').value = courseName;
    document.getElementById('qml-course-select').value = courseName;
}

async function predictML() {
    const course = document.getElementById('ml-course-select').value;
    const resultDiv = document.getElementById('ml-result');
    
    resultDiv.innerHTML = 'Fetching stats from DB & Predicting...';
    resultDiv.classList.add('show');

    try {
        const response = await fetch(`${API_BASE}/predict/ml`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course_name: course })
        });
        
        if(!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        resultDiv.innerHTML = `
            <strong>${course}</strong><br>
            <small style="color:var(--text-secondary)">DB Stats: ${data.data_used_from_db.hours_studied} hrs studied | Prev Score: ${data.data_used_from_db.previous_score}</small><br>
            <span style="font-size: 1.2rem">Predicted Score: ${data.predicted_score}%</span>
        `;
        resultDiv.style.color = '#3b82f6';

        // Generate Study Tips
        generateStudyTips(course, data.predicted_score, 'ML');
    } catch (error) {
        resultDiv.textContent = 'Error: Ensure Backend is running.';
        resultDiv.style.color = '#ef4444';
    }
}

async function predictDL() {
    const course = document.getElementById('dl-course-select').value;
    const feedback = document.getElementById('feedback').value;
    const resultDiv = document.getElementById('dl-result');
    
    resultDiv.innerHTML = 'Analyzing...';
    resultDiv.classList.add('show');

    try {
        const response = await fetch(`${API_BASE}/predict/dl`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course_name: course, feedback: feedback })
        });
        
        if(!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        resultDiv.innerHTML = `<strong>${course}</strong><br>Sentiment: ${data.sentiment}`;
        resultDiv.style.color = data.sentiment === 'POSITIVE' ? '#22c55e' : (data.sentiment === 'NEGATIVE' ? '#ef4444' : '#eab308');
    } catch (error) {
        resultDiv.textContent = 'Error: Ensure Backend is running.';
        resultDiv.style.color = '#ef4444';
    }
}

async function predictQML() {
    const course = document.getElementById('qml-course-select').value;
    const resultDiv = document.getElementById('qml-result');
    
    resultDiv.innerHTML = 'Fetching stats from DB & Running Quantum Circuit...';
    resultDiv.classList.add('show');

    try {
        const response = await fetch(`${API_BASE}/predict/qml`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course_name: course })
        });
        
        if(!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        resultDiv.innerHTML = `
            <strong>${course}</strong><br>
            <small style="color:var(--text-secondary)">DB Stats: Login Freq ${data.data_used_from_db.login_frequency} | Vid Completion ${data.data_used_from_db.video_completion_rate}</small><br>
            <span style="font-size: 1.1rem">${data.classification_result}</span>
        `;
        resultDiv.style.color = '#ec4899';

        // Generate Study Tips based on QML pattern
        const isHighEngagement = data.classification_result.includes("High Engagement");
        generateStudyTips(course, isHighEngagement ? 90 : 40, 'QML');
    } catch (error) {
        resultDiv.textContent = 'Error: Ensure Backend is running.';
        resultDiv.style.color = '#ef4444';
    }
}

// Load data automatically when the page loads
window.onload = loadDashboard;

function generateStudyTips(course, score, source) {
    const container = document.getElementById('tips-container');
    let tips = [];

    if (score < 50) {
        tips = [
            `Critically low prediction for <strong>${course}</strong>. We recommend starting with the "Foundations" module.`,
            `Schedule a 1-on-1 session with a mentor to clarify core concepts.`,
            `AI Suggestion: Increase study time by at least 5 hours per week.`
        ];
    } else if (score < 80) {
        tips = [
            `Solid progress in <strong>${course}</strong>, but there's room for improvement.`,
            `Focus on practical exercises and previous test papers to boost your score.`,
            `AI Suggestion: Review the last 3 video lectures to reinforce learning.`
        ];
    } else {
        tips = [
            `Outstanding prediction for <strong>${course}</strong>! You are performing at an Advanced level.`,
            `Try the "Challenge Exercises" to push your boundaries further.`,
            `AI Suggestion: Consider becoming a peer mentor for this course.`
        ];
    }

    container.innerHTML = `
        <div class="tip-card glass" style="grid-column: 1 / -1; border-left-color: var(--primary-color)">
            <span class="tip-badge">${source} Prediction Insight</span>
            <p>Based on your <strong>${score}%</strong> predicted performance in <strong>${course}</strong>, the AI recommends:</p>
        </div>
    `;

    tips.forEach(tip => {
        container.innerHTML += `
            <div class="tip-card glass">
                <p>${tip}</p>
            </div>
        `;
    });
}
