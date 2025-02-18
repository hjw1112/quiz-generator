# Flask Quiz Generator

This is a simple Flask-based multiple-choice quiz application that renders a quiz using a JSON array of questions generated by gpt-4o. Uses can enter simple topics, or data file in csv, txt, pdf, doc and docx to provide data to AI and generate multiple choice questions. Users can select answers and submit the quiz, and their score is calculated.

## Features
- 📝 Dynamic rendering of multiple-choice questions.
- ✅ Client-side quiz validation and scoring using JavaScript.
- 🔥 Simple and easy-to-modify structure.



## Used framework and language

- Flask(Python)
- HTML, CSS, JS
- OpenAI API

## How It Works

- The `route.py` file contains a Flask server that passes a JSON array of quiz questions to `quiz.html`.
- The frontend dynamically loads questions and calculates the score upon submission.
- Users receive instant feedback on their scores.

## Future Enhancements
- 🎨 Improve UI with CSS and animations.
- Feedback feature after quiz using AI
---

