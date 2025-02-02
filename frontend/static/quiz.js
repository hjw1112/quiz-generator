let questions = JSON.parse(document.getElementById("quiz-data").textContent.trim());
console.log("Type of questions:", typeof questions);
if (typeof questions == 'string'){
    questions = JSON.parse(questions)
    }
console.log("Type of questions:", typeof questions);

let correct = [];

function loadQuiz() {
    const quizContainer = document.getElementById('quiz-container');

    console.log(questions);


    let quizHtml = '';
    questions.forEach((q, index) => {
        quizHtml += `
            <div>
                <p><strong class="question">${index + 1}. ${q.question}</strong></p>
                <label><input type="radio" class="question" name="q${index}" value="a"> ${q.a}</label><br>
                <label><input type="radio" class="question" name="q${index}" value="b"> ${q.b}</label><br>
                <label><input type="radio" class="question" name="q${index}" value="c"> ${q.c}</label><br>
                <label><input type="radio" class="question" name="q${index}" value="d"> ${q.d}</label><br>
            </div>
            <br>
        `;
    });
    quizContainer.innerHTML = quizHtml;
}

function submitQuiz() {
    let score = 0;

    questions.forEach((q, index) => {
        const selectedAnswer = document.querySelector(`input[name="q${index}"]:checked`);
        const allOptions = document.querySelectorAll(`input[name="q${index}"]`);

        allOptions.forEach(option => {
            const parentLabel = option.parentElement;
            parentLabel.classList.remove("correct", "incorrect", "unselected-wrong", "highlight-correct");

            if (option.value === q.answer) {
                parentLabel.classList.add("correct");
            } else {
                parentLabel.classList.add("unselected-wrong");
            }
        });

        if (selectedAnswer) {
            if (selectedAnswer.value === q.answer) {
                score++;
            } else {
                selectedAnswer.parentElement.classList.add("incorrect");
                allOptions.forEach(option => {
                    if (option.value === q.answer) {
                        option.parentElement.classList.add("highlight-correct");
                    }
                });
            }
        }
    });

    const scoreElement = document.getElementById('score');
    scoreElement.style.display = "block";
    scoreElement.innerText = `Your Score: ${score}/${questions.length}`;
    alert(`You scored ${score}/${questions.length}! 🎉`);
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Quiz loaded successfully.");
    loadQuiz();
    document.getElementById('submit_button').addEventListener('click', submitQuiz);
});

