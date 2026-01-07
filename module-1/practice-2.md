# Практическая работа 2: Разработка онлайн-теста с проверкой ответов

**Продолжительность:** 4 академических часа  
**Модуль:** Веб-технологии в образовании

---

## Цель работы

Разработать интерактивный онлайн-тест по выбранной теме с автоматической проверкой ответов, подсчётом баллов и выводом результатов. Тест должен включать разные типы вопросов и обеспечивать мгновенную обратную связь учащемуся.

---

## Задание

Создать онлайн-тест, который включает:

### Обязательные элементы:

1. **Минимум 10 вопросов** по выбранной теме
2. **Разные типы вопросов:**
   - Одиночный выбор (radio buttons)
   - Множественный выбор (checkboxes)
   - Ввод текста (короткий ответ)
3. **Таймер** на прохождение теста (опционально, но желательно)
4. **Прогресс-бар** или индикатор текущего вопроса
5. **Система подсчёта баллов**
6. **Страница результатов** с:
   - Общим баллом
   - Процентом правильных ответов
   - Разбором ошибок
   - Возможностью пройти тест заново
7. **Валидация ответов** (проверка, что пользователь ответил на вопрос)
8. **Адаптивный дизайн**

### Технические требования:

✅ Использовать JavaScript для логики теста  
✅ Хранить вопросы и ответы в структурированном виде (массив объектов)  
✅ Реализовать навигацию между вопросами  
✅ Обеспечить корректную работу на мобильных устройствах  
✅ Добавить визуальную обратную связь (правильно/неправильно)  
✅ Использовать localStorage для сохранения прогресса (опционально)  

---

## Пример структуры данных

```javascript
const questions = [
    {
        id: 1,
        question: "Столица России?",
        type: "single", // single, multiple, text
        options: ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"],
        correct: 0, // индекс правильного ответа
        points: 1
    },
    {
        id: 2,
        question: "Выберите языки программирования:",
        type: "multiple",
        options: ["Python", "HTML", "JavaScript", "CSS"],
        correct: [0, 2], // индексы правильных ответов
        points: 2
    },
    {
        id: 3,
        question: "Сколько будет 2+2?",
        type: "text",
        correct: "4", // правильный ответ (строка)
        points: 1
    }
];
```

---

## Полный пример реализации

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Онлайн-тест: Основы информатики</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        header h1 {
            font-size: 2em;
            margin-bottom: 0.5rem;
        }
        
        .test-info {
            display: flex;
            justify-content: space-around;
            padding: 1rem;
            background: #f5f5f5;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .test-info div {
            text-align: center;
        }
        
        .test-info span {
            display: block;
            font-size: 0.9em;
            color: #666;
        }
        
        .test-info strong {
            font-size: 1.5em;
            color: #667eea;
        }
        
        .progress-bar {
            height: 5px;
            background: #e0e0e0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }
        
        .question-container {
            padding: 2rem;
            min-height: 400px;
        }
        
        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .question-number {
            font-size: 1.2em;
            color: #667eea;
            font-weight: bold;
        }
        
        .question-points {
            background: #e3f2fd;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9em;
            color: #1976d2;
        }
        
        .question-text {
            font-size: 1.3em;
            margin-bottom: 1.5rem;
            color: #333;
        }
        
        .options {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .option {
            padding: 1rem;
            background: #f5f5f5;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .option:hover {
            background: #e8eaf6;
            border-color: #667eea;
        }
        
        .option.selected {
            background: #e8eaf6;
            border-color: #667eea;
        }
        
        .option input[type="radio"],
        .option input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .option label {
            flex-grow: 1;
            cursor: pointer;
            font-size: 1.1em;
        }
        
        .text-input {
            width: 100%;
            padding: 1rem;
            font-size: 1.1em;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            transition: border-color 0.3s;
        }
        
        .text-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .navigation {
            padding: 1.5rem 2rem;
            background: #f5f5f5;
            display: flex;
            justify-content: space-between;
            gap: 1rem;
        }
        
        button {
            padding: 0.8rem 2rem;
            font-size: 1.1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        
        .btn-success {
            background: #4caf50;
            color: white;
        }
        
        .btn-success:hover {
            background: #45a049;
        }
        
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .results {
            padding: 2rem;
            text-align: center;
        }
        
        .results h2 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 1rem;
        }
        
        .score {
            font-size: 4em;
            font-weight: bold;
            color: #667eea;
            margin: 1rem 0;
        }
        
        .score-message {
            font-size: 1.3em;
            margin-bottom: 2rem;
            color: #666;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 2rem 0;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .stat {
            background: #f5f5f5;
            padding: 1.5rem;
            border-radius: 8px;
            min-width: 150px;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 0.5rem;
        }
        
        .review {
            text-align: left;
            margin-top: 2rem;
        }
        
        .review-item {
            background: #f5f5f5;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border-left: 5px solid #e0e0e0;
        }
        
        .review-item.correct {
            border-left-color: #4caf50;
            background: #e8f5e9;
        }
        
        .review-item.incorrect {
            border-left-color: #f44336;
            background: #ffebee;
        }
        
        .timer {
            font-size: 1.2em;
            font-weight: bold;
            color: #666;
        }
        
        .timer.warning {
            color: #f44336;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .container {
                border-radius: 0;
            }
            
            .question-container {
                padding: 1rem;
            }
            
            .navigation {
                flex-direction: column;
            }
            
            button {
                width: 100%;
            }
            
            .stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📝 Тест: Основы информатики</h1>
            <p>Проверьте свои знания!</p>
        </header>
        
        <!-- Информация о тесте -->
        <div id="testInfo" class="test-info">
            <div>
                <span>Вопросов</span>
                <strong id="totalQuestions">10</strong>
            </div>
            <div>
                <span>Текущий вопрос</span>
                <strong id="currentQuestionNum">1</strong>
            </div>
            <div class="timer" id="timer">
                <span>Времени осталось</span>
                <strong id="timeLeft">10:00</strong>
            </div>
        </div>
        
        <!-- Прогресс-бар -->
        <div class="progress-bar">
            <div class="progress-fill" id="progressBar"></div>
        </div>
        
        <!-- Контейнер для вопросов -->
        <div id="questionContainer" class="question-container">
            <!-- Вопросы будут загружаться динамически -->
        </div>
        
        <!-- Навигация -->
        <div id="navigation" class="navigation">
            <button id="prevBtn" class="btn-secondary" onclick="previousQuestion()">
                ← Назад
            </button>
            <button id="nextBtn" class="btn-primary" onclick="nextQuestion()">
                Далее →
            </button>
            <button id="submitBtn" class="btn-success hidden" onclick="submitTest()">
                ✓ Завершить тест
            </button>
        </div>
        
        <!-- Результаты -->
        <div id="results" class="results hidden">
            <!-- Результаты будут показаны здесь -->
        </div>
    </div>

    <script>
        // Данные теста
        const questions = [
            {
                id: 1,
                question: "Что такое HTML?",
                type: "single",
                options: [
                    "Язык программирования",
                    "Язык разметки",
                    "База данных",
                    "Операционная система"
                ],
                correct: 1,
                points: 1,
                explanation: "HTML (HyperText Markup Language) - язык разметки для создания веб-страниц."
            },
            {
                id: 2,
                question: "Какие из следующих являются языками программирования?",
                type: "multiple",
                options: ["Python", "HTML", "JavaScript", "CSS", "Java"],
                correct: [0, 2, 4],
                points: 2,
                explanation: "HTML и CSS - это языки разметки и стилей, а не программирования."
            },
            {
                id: 3,
                question: "Сколько байт в одном килобайте?",
                type: "text",
                correct: "1024",
                points: 1,
                explanation: "1 килобайт = 1024 байта (2^10)"
            },
            {
                id: 4,
                question: "Что означает аббревиатура CSS?",
                type: "single",
                options: [
                    "Computer Style Sheets",
                    "Cascading Style Sheets",
                    "Creative Style Sheets",
                    "Colorful Style Sheets"
                ],
                correct: 1,
                points: 1,
                explanation: "CSS расшифровывается как Cascading Style Sheets (Каскадные таблицы стилей)."
            },
            {
                id: 5,
                question: "Какой тег используется для создания ссылки в HTML?",
                type: "text",
                correct: "a",
                points: 1,
                explanation: "Тег <a> (anchor) используется для создания гиперссылок."
            },
            {
                id: 6,
                question: "Выберите все правильные операторы в JavaScript:",
                type: "multiple",
                options: ["===", "==", "=", "!==", "!="],
                correct: [0, 1, 2, 3, 4],
                points: 2,
                explanation: "Все перечисленные операторы используются в JavaScript."
            },
            {
                id: 7,
                question: "Что такое DNS?",
                type: "single",
                options: [
                    "Система доменных имён",
                    "Сетевой протокол",
                    "Тип браузера",
                    "Язык программирования"
                ],
                correct: 0,
                points: 1,
                explanation: "DNS (Domain Name System) - система доменных имён."
            },
            {
                id: 8,
                question: "В каком году был создан язык JavaScript?",
                type: "text",
                correct: "1995",
                points: 1,
                explanation: "JavaScript был создан Бренданом Айком в 1995 году."
            },
            {
                id: 9,
                question: "Какие браузеры относятся к современным?",
                type: "multiple",
                options: ["Chrome", "Internet Explorer 6", "Firefox", "Safari", "Edge"],
                correct: [0, 2, 3, 4],
                points: 2,
                explanation: "Internet Explorer 6 - устаревший браузер."
            },
            {
                id: 10,
                question: "Что такое API?",
                type: "single",
                options: [
                    "Application Programming Interface",
                    "Advanced Programming Interface",
                    "Automated Program Integration",
                    "Application Protocol Internet"
                ],
                correct: 0,
                points: 1,
                explanation: "API - Application Programming Interface (программный интерфейс приложения)."
            }
        ];

        // Глобальные переменные
        let currentQuestion = 0;
        let userAnswers = new Array(questions.length);
        let timeRemaining = 600; // 10 минут в секундах
        let timerInterval;

        // Инициализация теста
        function initTest() {
            document.getElementById('totalQuestions').textContent = questions.length;
            startTimer();
            loadQuestion();
        }

        // Загрузка вопроса
        function loadQuestion() {
            const question = questions[currentQuestion];
            const container = document.getElementById('questionContainer');
            
            let html = `
                <div class="question-header">
                    <span class="question-number">Вопрос ${currentQuestion + 1} из ${questions.length}</span>
                    <span class="question-points">${question.points} ${declension(question.points, ['балл', 'балла', 'баллов'])}</span>
                </div>
                <div class="question-text">${question.question}</div>
                <div class="options">
            `;
            
            if (question.type === 'single') {
                question.options.forEach((option, index) => {
                    const checked = userAnswers[currentQuestion] === index ? 'checked' : '';
                    html += `
                        <div class="option ${checked ? 'selected' : ''}" onclick="selectOption(${index})">
                            <input type="radio" name="answer" value="${index}" ${checked} onchange="selectOption(${index})">
                            <label>${option}</label>
                        </div>
                    `;
                });
            } else if (question.type === 'multiple') {
                question.options.forEach((option, index) => {
                    const checked = userAnswers[currentQuestion] && userAnswers[currentQuestion].includes(index) ? 'checked' : '';
                    html += `
                        <div class="option ${checked ? 'selected' : ''}" onclick="selectMultiple(${index})">
                            <input type="checkbox" value="${index}" ${checked} onchange="selectMultiple(${index})">
                            <label>${option}</label>
                        </div>
                    `;
                });
            } else if (question.type === 'text') {
                const value = userAnswers[currentQuestion] || '';
                html += `
                    <input type="text" class="text-input" id="textAnswer" 
                           placeholder="Введите ваш ответ..." value="${value}"
                           oninput="saveTextAnswer()">
                `;
            }
            
            html += '</div>';
            container.innerHTML = html;
            
            updateNavigation();
            updateProgress();
            document.getElementById('currentQuestionNum').textContent = currentQuestion + 1;
        }

        // Выбор одного варианта
        function selectOption(index) {
            userAnswers[currentQuestion] = index;
            loadQuestion();
        }

        // Выбор нескольких вариантов
        function selectMultiple(index) {
            if (!userAnswers[currentQuestion]) {
                userAnswers[currentQuestion] = [];
            }
            
            const answerIndex = userAnswers[currentQuestion].indexOf(index);
            if (answerIndex > -1) {
                userAnswers[currentQuestion].splice(answerIndex, 1);
            } else {
                userAnswers[currentQuestion].push(index);
            }
            
            loadQuestion();
        }

        // Сохранение текстового ответа
        function saveTextAnswer() {
            userAnswers[currentQuestion] = document.getElementById('textAnswer').value.trim();
        }

        // Следующий вопрос
        function nextQuestion() {
            if (currentQuestion < questions.length - 1) {
                currentQuestion++;
                loadQuestion();
            }
        }

        // Предыдущий вопрос
        function previousQuestion() {
            if (currentQuestion > 0) {
                currentQuestion--;
                loadQuestion();
            }
        }

        // Обновление навигации
        function updateNavigation() {
            document.getElementById('prevBtn').disabled = currentQuestion === 0;
            
            if (currentQuestion === questions.length - 1) {
                document.getElementById('nextBtn').classList.add('hidden');
                document.getElementById('submitBtn').classList.remove('hidden');
            } else {
                document.getElementById('nextBtn').classList.remove('hidden');
                document.getElementById('submitBtn').classList.add('hidden');
            }
        }

        // Обновление прогресс-бара
        function updateProgress() {
            const progress = ((currentQuestion + 1) / questions.length) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
        }

        // Таймер
        function startTimer() {
            timerInterval = setInterval(() => {
                timeRemaining--;
                updateTimerDisplay();
                
                if (timeRemaining <= 60) {
                    document.getElementById('timer').classList.add('warning');
                }
                
                if (timeRemaining <= 0) {
                    clearInterval(timerInterval);
                    alert('Время вышло!');
                    submitTest();
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            document.getElementById('timeLeft').textContent = 
                `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }

        // Отправка теста
        function submitTest() {
            // Проверка, все ли вопросы отвечены
            const unanswered = userAnswers.filter(a => a === undefined || a === null || a === '' || (Array.isArray(a) && a.length === 0));
            
            if (unanswered.length > 0) {
                if (!confirm(`Вы не ответили на ${unanswered.length} вопрос(ов). Завершить тест?`)) {
                    return;
                }
            }
            
            clearInterval(timerInterval);
            calculateResults();
        }

        // Расчёт результатов
        function calculateResults() {
            let score = 0;
            let maxScore = 0;
            let correctCount = 0;
            
            const reviewItems = questions.map((question, index) => {
                maxScore += question.points;
                let isCorrect = false;
                let userAnswer = userAnswers[index];
                
                if (question.type === 'single') {
                    isCorrect = userAnswer === question.correct;
                } else if (question.type === 'multiple') {
                    if (userAnswer && Array.isArray(userAnswer)) {
                        isCorrect = JSON.stringify(userAnswer.sort()) === JSON.stringify(question.correct.sort());
                    }
                } else if (question.type === 'text') {
                    isCorrect = userAnswer && userAnswer.toLowerCase() === question.correct.toLowerCase();
                }
                
                if (isCorrect) {
                    score += question.points;
                    correctCount++;
                }
                
                return {
                    question: question.question,
                    userAnswer: formatUserAnswer(question, userAnswer),
                    correctAnswer: formatCorrectAnswer(question),
                    isCorrect: isCorrect,
                    explanation: question.explanation
                };
            });
            
            showResults(score, maxScore, correctCount, reviewItems);
        }

        // Форматирование ответа пользователя
        function formatUserAnswer(question, answer) {
            if (answer === undefined || answer === null || answer === '' || (Array.isArray(answer) && answer.length === 0)) {
                return '<em>Нет ответа</em>';
            }
            
            if (question.type === 'single') {
                return question.options[answer];
            } else if (question.type === 'multiple') {
                return answer.map(i => question.options[i]).join(', ');
            } else {
                return answer;
            }
        }

        // Форматирование правильного ответа
        function formatCorrectAnswer(question) {
            if (question.type === 'single') {
                return question.options[question.correct];
            } else if (question.type === 'multiple') {
                return question.correct.map(i => question.options[i]).join(', ');
            } else {
                return question.correct;
            }
        }

        // Показ результатов
        function showResults(score, maxScore, correctCount, reviewItems) {
            document.getElementById('testInfo').classList.add('hidden');
            document.getElementById('questionContainer').classList.add('hidden');
            document.getElementById('navigation').classList.add('hidden');
            
            const percentage = Math.round((score / maxScore) * 100);
            let message = '';
            
            if (percentage >= 90) {
                message = '🎉 Отлично! Вы блестяще справились!';
            } else if (percentage >= 75) {
                message = '👍 Хорошо! Но есть куда стремиться.';
            } else if (percentage >= 60) {
                message = '😊 Неплохо, но нужно ещё поработать.';
            } else {
                message = '📚 Рекомендуем повторить материал.';
            }
            
            let reviewHtml = '';
            reviewItems.forEach((item, index) => {
                reviewHtml += `
                    <div class="review-item ${item.isCorrect ? 'correct' : 'incorrect'}">
                        <strong>Вопрос ${index + 1}:</strong> ${item.question}<br>
                        <strong>Ваш ответ:</strong> ${item.userAnswer}<br>
                        ${!item.isCorrect ? `<strong>Правильный ответ:</strong> ${item.correctAnswer}<br>` : ''}
                        <em>${item.explanation}</em>
                    </div>
                `;
            });
            
            const resultsHtml = `
                <h2>Результаты теста</h2>
                <div class="score">${percentage}%</div>
                <div class="score-message">${message}</div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">${score}/${maxScore}</div>
                        <div class="stat-label">Баллов</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${correctCount}/${questions.length}</div>
                        <div class="stat-label">Правильных ответов</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">${Math.floor((600 - timeRemaining) / 60)}:${((600 - timeRemaining) % 60).toString().padStart(2, '0')}</div>
                        <div class="stat-label">Затрачено времени</div>
                    </div>
                </div>
                
                <button class="btn-primary" onclick="location.reload()">🔄 Пройти тест заново</button>
                
                <div class="review">
                    <h3>Разбор ответов:</h3>
                    ${reviewHtml}
                </div>
            `;
            
            document.getElementById('results').innerHTML = resultsHtml;
            document.getElementById('results').classList.remove('hidden');
        }

        // Склонение числительных
        function declension(number, words) {
            const cases = [2, 0, 1, 1, 1, 2];
            return words[(number % 100 > 4 && number % 100 < 20) ? 2 : cases[Math.min(number % 10, 5)]];
        }

        // Запуск теста при загрузке страницы
        window.onload = initTest;
    </script>
</body>
</html>
```

---

## Критерии оценивания

| Критерий | Баллы |
|----------|-------|
| Наличие минимум 10 вопросов | 10 |
| Разные типы вопросов (single, multiple, text) | 15 |
| Корректная логика проверки ответов | 20 |
| Система подсчёта баллов | 10 |
| Прогресс-бар / индикатор вопроса | 5 |
| Таймер | 5 |
| Страница результатов с разбором | 15 |
| Дизайн и удобство использования | 10 |
| Адаптивность (мобильные устройства) | 10 |
| **Итого** | **100** |

---

## Дополнительные задания (бонусные баллы)

1. **Сохранение прогресса** в localStorage (+5 баллов)
2. **Категории вопросов** с фильтрацией (+5 баллов)
3. **Экспорт результатов** в PDF или текстовый файл (+10 баллов)
4. **Режим практики** (показ правильного ответа сразу) (+5 баллов)
5. **Статистика по предыдущим попыткам** (+5 баллов)
6. **Звуковые эффекты** для правильных/неправильных ответов (+3 балла)

---

## Формат сдачи

1. Один HTML-файл с встроенными CSS и JavaScript
2. Название: `фамилия_практика2.html`
3. Файл со списком вопросов (если используется отдельный JSON)
4. Краткое описание теста (тема, количество вопросов, типы)

---

## Полезные советы

💡 **Тестирование:** Проверьте все типы вопросов и варианты ответов  
💡 **Валидация:** Убедитесь, что пустые ответы обрабатываются корректно  
💡 **UX:** Добавьте визуальную обратную связь на действия пользователя  
💡 **Доступность:** Используйте контрастные цвета и читаемые шрифты  
💡 **Отладка:** Используйте `console.log()` для проверки логики  

Удачи! 🚀

