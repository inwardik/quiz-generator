#!/usr/bin/env python3
"""
Quiz Generator - Enhanced Version
Converts Markdown quiz files to interactive HTML pages
"""

import re
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
import random


class QuizParser:
    """Parse quiz markdown files"""

    def __init__(self, content: str, shuffle_questions: bool = True, shuffle_answers: bool = True):
        self.content = content
        self.shuffle_questions = shuffle_questions
        self.shuffle_answers = shuffle_answers
        self.title = ""
        self.questions = []

    def parse(self) -> Dict:
        """Parse markdown content into quiz structure"""
        lines = self.content.strip().split('\n')

        # Extract title (first h2 or h1)
        for line in lines:
            if line.startswith('## '):
                self.title = line[3:].strip()
                break
            elif line.startswith('# '):
                self.title = line[2:].strip()
                break

        if not self.title:
            self.title = "Quiz"

        # Parse questions
        current_question = None
        current_answers = []

        for line in lines:
            line = line.strip()

            # Question (h3 or h4)
            if line.startswith('#### ') or line.startswith('### '):
                if current_question and current_answers:
                    if self.shuffle_answers:
                        random.shuffle(current_answers)
                    self.questions.append({
                        'question': current_question,
                        'answers': current_answers
                    })

                current_question = line.lstrip('#').strip()
                current_answers = []

            # Answers
            elif line.startswith('- ['):
                is_correct = '[x]' in line.lower()
                answer_text = re.sub(r'- \[[xX ]\]\s*', '', line).strip()

                if answer_text:
                    current_answers.append({
                        'text': answer_text,
                        'correct': is_correct
                    })

        # Add last question
        if current_question and current_answers:
            if self.shuffle_answers:
                random.shuffle(current_answers)
            self.questions.append({
                'question': current_question,
                'answers': current_answers
            })

        # Shuffle questions if needed
        if self.shuffle_questions:
            random.shuffle(self.questions)

        return {
            'title': self.title,
            'questions': self.questions
        }


class HTMLGenerator:
    """Generate HTML from quiz data"""

    def __init__(self, quiz_data: Dict, dark_mode: bool = False):
        self.quiz_data = quiz_data
        self.dark_mode = dark_mode

    def generate(self) -> str:
        """Generate complete HTML page"""
        title = self.quiz_data['title']
        questions = self.quiz_data['questions']

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{self._get_css()}
    </style>
</head>
<body{' class="dark-mode"' if self.dark_mode else ''}>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
            <div class="stats">
                <span>Вопрос <span id="current-question">1</span> из <span id="total-questions">{len(questions)}</span></span>
                <span>Баллы: <span id="score">0</span></span>
            </div>
        </header>

        <main id="quiz-container">
{self._generate_questions(questions)}
        </main>

        <div id="results" class="results hidden">
            <h2>Результаты теста</h2>
            <div class="result-stats">
                <div class="stat-item">
                    <div class="stat-value" id="final-score">0</div>
                    <div class="stat-label">Итоговый балл</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="correct-answers">0</div>
                    <div class="stat-label">Правильных ответов</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="accuracy">0%</div>
                    <div class="stat-label">Точность</div>
                </div>
            </div>
            <button onclick="restartQuiz()" class="btn btn-primary">Пройти снова</button>
        </div>

        <footer>
            <button id="theme-toggle" onclick="toggleTheme()">🌙 Темная тема</button>
        </footer>
    </div>

    <script>
{self._get_javascript(len(questions))}
    </script>
</body>
</html>"""

        return html

    def _generate_questions(self, questions: List[Dict]) -> str:
        """Generate HTML for all questions"""
        html_parts = []

        for i, q in enumerate(questions):
            question_html = f"""            <div class="question-card" data-question="{i}">
                <h3 class="question-text">Q{i+1}. {q['question']}</h3>
                <div class="answers">
"""

            for j, answer in enumerate(q['answers']):
                correct = 'data-correct="true"' if answer['correct'] else ''
                question_html += f"""                    <label class="answer-option">
                        <input type="radio" name="question-{i}" value="{j}" {correct}>
                        <span class="answer-text">{answer['text']}</span>
                        <span class="answer-indicator"></span>
                    </label>
"""

            question_html += """                </div>
                <div class="feedback hidden"></div>
            </div>
"""
            html_parts.append(question_html)

        return ''.join(html_parts)

    def _get_css(self) -> str:
        """Get embedded CSS"""
        return """        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-color: #4f46e5;
            --success-color: #10b981;
            --error-color: #ef4444;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
            --hover-bg: #f1f5f9;
        }

        body.dark-mode {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #f1f5f9;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --hover-bg: #334155;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            transition: background 0.3s ease, color 0.3s ease;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            color: var(--primary-color);
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--border-color);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), #7c3aed);
            width: 0%;
            transition: width 0.3s ease;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 1.1em;
            color: var(--text-secondary);
        }

        .stats span {
            font-weight: 600;
        }

        #score {
            color: var(--primary-color);
            font-size: 1.2em;
        }

        .question-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .question-card.answered {
            opacity: 0.7;
        }

        .question-text {
            font-size: 1.3em;
            margin-bottom: 20px;
            color: var(--text-color);
        }

        .answers {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .answer-option {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            background: var(--bg-color);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }

        .answer-option:hover {
            background: var(--hover-bg);
            border-color: var(--primary-color);
        }

        .answer-option input[type="radio"] {
            margin-right: 12px;
            width: 20px;
            height: 20px;
            cursor: pointer;
        }

        .answer-text {
            flex: 1;
            font-size: 1.05em;
        }

        .answer-indicator {
            font-size: 1.5em;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .answer-option.correct {
            background: #d1fae5;
            border-color: var(--success-color);
        }

        body.dark-mode .answer-option.correct {
            background: #064e3b;
        }

        .answer-option.correct .answer-indicator {
            opacity: 1;
        }

        .answer-option.correct .answer-indicator::after {
            content: '✓';
            color: var(--success-color);
        }

        .answer-option.incorrect {
            background: #fee2e2;
            border-color: var(--error-color);
        }

        body.dark-mode .answer-option.incorrect {
            background: #7f1d1d;
        }

        .answer-option.incorrect .answer-indicator {
            opacity: 1;
        }

        .answer-option.incorrect .answer-indicator::after {
            content: '✗';
            color: var(--error-color);
        }

        .feedback {
            margin-top: 15px;
            padding: 12px 18px;
            border-radius: 6px;
            font-weight: 500;
        }

        .feedback.success {
            background: #d1fae5;
            color: #065f46;
            border-left: 4px solid var(--success-color);
        }

        body.dark-mode .feedback.success {
            background: #064e3b;
            color: #6ee7b7;
        }

        .feedback.error {
            background: #fee2e2;
            color: #991b1b;
            border-left: 4px solid var(--error-color);
        }

        body.dark-mode .feedback.error {
            background: #7f1d1d;
            color: #fca5a5;
        }

        .hidden {
            display: none !important;
        }

        .results {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .results h2 {
            font-size: 2em;
            margin-bottom: 30px;
            color: var(--primary-color);
        }

        .result-stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            gap: 20px;
        }

        .stat-item {
            flex: 1;
        }

        .stat-value {
            font-size: 3em;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 1.1em;
            color: var(--text-secondary);
        }

        .btn {
            padding: 12px 30px;
            font-size: 1.1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .btn-primary {
            background: var(--primary-color);
            color: white;
        }

        .btn-primary:hover {
            background: #4338ca;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        }

        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
        }

        #theme-toggle {
            background: var(--card-bg);
            color: var(--text-color);
            border: 2px solid var(--border-color);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.2s ease;
        }

        #theme-toggle:hover {
            background: var(--hover-bg);
            transform: scale(1.05);
        }

        @media (max-width: 600px) {
            .container {
                padding: 10px;
            }

            h1 {
                font-size: 1.8em;
            }

            .question-card {
                padding: 20px;
            }

            .result-stats {
                flex-direction: column;
            }
        }"""

    def _get_javascript(self, total_questions: int) -> str:
        """Get embedded JavaScript"""
        return f"""        let score = 0;
        let answeredQuestions = 0;
        const totalQuestions = {total_questions};
        let answers = {{}};

        document.addEventListener('DOMContentLoaded', function() {{
            const radioButtons = document.querySelectorAll('input[type="radio"]');

            radioButtons.forEach(radio => {{
                radio.addEventListener('change', function(e) {{
                    handleAnswer(e.target);
                }});
            }});

            // Restore dark mode preference
            if (localStorage.getItem('darkMode') === 'true') {{
                document.body.classList.add('dark-mode');
                document.getElementById('theme-toggle').textContent = '☀️ Светлая тема';
            }}
        }});

        function handleAnswer(radio) {{
            const questionCard = radio.closest('.question-card');
            const questionNum = questionCard.dataset.question;
            const allOptions = questionCard.querySelectorAll('.answer-option');
            const feedback = questionCard.querySelector('.feedback');

            // Prevent answering twice
            if (answers[questionNum] !== undefined) {{
                return;
            }}

            // Disable all options in this question
            allOptions.forEach(option => {{
                option.querySelector('input').disabled = true;
            }});

            const isCorrect = radio.hasAttribute('data-correct');
            const selectedOption = radio.closest('.answer-option');

            // Mark the selected answer
            if (isCorrect) {{
                selectedOption.classList.add('correct');
                feedback.textContent = '✓ Правильно!';
                feedback.classList.add('success');
                score++;
            }} else {{
                selectedOption.classList.add('incorrect');
                // Show correct answer
                allOptions.forEach(option => {{
                    if (option.querySelector('input').hasAttribute('data-correct')) {{
                        option.classList.add('correct');
                    }}
                }});
                feedback.textContent = '✗ Неправильно. Правильный ответ выделен зеленым.';
                feedback.classList.add('error');
            }}

            feedback.classList.remove('hidden');
            questionCard.classList.add('answered');
            answers[questionNum] = isCorrect;
            answeredQuestions++;

            // Update UI
            updateProgress();
            updateScore();

            // Check if quiz is complete
            if (answeredQuestions === totalQuestions) {{
                setTimeout(showResults, 500);
            }}
        }}

        function updateProgress() {{
            const progress = (answeredQuestions / totalQuestions) * 100;
            document.getElementById('progress').style.width = progress + '%';
            document.getElementById('current-question').textContent = Math.min(answeredQuestions + 1, totalQuestions);
        }}

        function updateScore() {{
            document.getElementById('score').textContent = score;
        }}

        function showResults() {{
            document.getElementById('quiz-container').classList.add('hidden');
            document.getElementById('results').classList.remove('hidden');

            const accuracy = Math.round((score / totalQuestions) * 100);

            document.getElementById('final-score').textContent = score + ' / ' + totalQuestions;
            document.getElementById('correct-answers').textContent = score;
            document.getElementById('accuracy').textContent = accuracy + '%';

            // Scroll to results
            document.getElementById('results').scrollIntoView({{ behavior: 'smooth' }});
        }}

        function restartQuiz() {{
            // Reset state
            score = 0;
            answeredQuestions = 0;
            answers = {{}};

            // Reset UI
            document.getElementById('quiz-container').classList.remove('hidden');
            document.getElementById('results').classList.add('hidden');

            // Reset all questions
            document.querySelectorAll('.question-card').forEach(card => {{
                card.classList.remove('answered');
                card.querySelectorAll('input[type="radio"]').forEach(radio => {{
                    radio.checked = false;
                    radio.disabled = false;
                }});
                card.querySelectorAll('.answer-option').forEach(option => {{
                    option.classList.remove('correct', 'incorrect');
                }});
                card.querySelector('.feedback').classList.add('hidden');
                card.querySelector('.feedback').classList.remove('success', 'error');
            }});

            updateProgress();
            updateScore();

            // Scroll to top
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function toggleTheme() {{
            const body = document.body;
            const button = document.getElementById('theme-toggle');

            body.classList.toggle('dark-mode');

            if (body.classList.contains('dark-mode')) {{
                button.textContent = '☀️ Светлая тема';
                localStorage.setItem('darkMode', 'true');
            }} else {{
                button.textContent = '🌙 Темная тема';
                localStorage.setItem('darkMode', 'false');
            }}
        }}"""


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate interactive HTML quiz from Markdown file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python to_html.py quiz.md
  python to_html.py quiz.md -o my-quiz.html
  python to_html.py quiz.md --no-shuffle-questions --dark-mode
        """
    )

    parser.add_argument('input', help='Input Markdown file (e.g., quiz.md)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: input name with .html extension)')
    parser.add_argument('--no-shuffle-questions', action='store_true', help='Do not shuffle questions')
    parser.add_argument('--no-shuffle-answers', action='store_true', help='Do not shuffle answers')
    parser.add_argument('--dark-mode', action='store_true', help='Enable dark mode by default')

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        content = input_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse quiz
    parser_obj = QuizParser(
        content,
        shuffle_questions=not args.no_shuffle_questions,
        shuffle_answers=not args.no_shuffle_answers
    )

    try:
        quiz_data = parser_obj.parse()
    except Exception as e:
        print(f"Error parsing quiz: {e}", file=sys.stderr)
        sys.exit(1)

    if not quiz_data['questions']:
        print("Error: No questions found in the file", file=sys.stderr)
        sys.exit(1)

    # Generate HTML
    generator = HTMLGenerator(quiz_data, dark_mode=args.dark_mode)
    html = generator.generate()

    # Write output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.html')

    try:
        output_path.write_text(html, encoding='utf-8')
        print(f"✓ Quiz generated successfully: {output_path}")
        print(f"  Title: {quiz_data['title']}")
        print(f"  Questions: {len(quiz_data['questions'])}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
