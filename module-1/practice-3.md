# Практическая работа 3: Создание образовательной веб-игры

**Продолжительность:** 4 академических часа  
**Модуль:** Веб-технологии в образовании

---

## Цель работы

Разработать интерактивную образовательную веб-игру, которая поможет учащимся закрепить знания по выбранной теме в игровой форме. Игра должна быть увлекательной, познавательной и технически грамотно реализованной.

---

## Задание

Создать образовательную игру одного из следующих типов (на выбор):

### Варианты игр:

1. **Викторина с таймером и уровнями сложности**
2. **Мемори-игра** (карточки с парами - термин/определение, слово/перевод)
3. **Виселица** (угадай слово по теме)
4. **Математический тренажёр** (примеры на скорость)
5. **География** (угадай страну/столицу на карте)
6. **Сортировка** (распредели элементы по категориям)
7. **Своя идея** (согласовать с преподавателем)

---

## Обязательные элементы:

✅ **Игровая механика** - понятные правила и цель  
✅ **Система начисления очков** - баллы за правильные ответы  
✅ **Таймер или счётчик ходов**  
✅ **Уровни сложности** (минимум 2)  
✅ **Звуковые эффекты** или анимации (опционально)  
✅ **Таблица рекордов** (лучшие результаты)  
✅ **Возможность начать игру заново**  
✅ **Адаптивный дизайн**  
✅ **Инструкция по игре**  

---

## Технические требования:

- Использовать JavaScript для игровой логики
- Применить CSS-анимации для визуальных эффектов
- Сохранять рекорды в localStorage
- Генерировать случайные задания/вопросы
- Обрабатывать различные игровые состояния (старт, игра, конец)
- Валидировать действия игрока

---

## Пример 1: Математический тренажёр

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Математический спринт</title>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .game-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            overflow: hidden;
        }
        
        .game-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        
        .game-header h1 {
            font-size: 2.5em;
            margin-bottom: 0.5rem;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 1.5rem;
            background: #f5f5f5;
            border-bottom: 3px solid #e0e0e0;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 0.3rem;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .game-screen {
            padding: 3rem 2rem;
            min-height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .start-screen {
            text-align: center;
        }
        
        .start-screen h2 {
            color: #667eea;
            margin-bottom: 1rem;
        }
        
        .difficulty-buttons {
            display: flex;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .btn {
            padding: 1rem 2rem;
            font-size: 1.1em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .btn-easy {
            background: #4caf50;
            color: white;
        }
        
        .btn-medium {
            background: #ff9800;
            color: white;
        }
        
        .btn-hard {
            background: #f44336;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .question {
            font-size: 4em;
            font-weight: bold;
            color: #333;
            margin-bottom: 2rem;
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .answer-input {
            width: 200px;
            padding: 1rem;
            font-size: 2em;
            text-align: center;
            border: 3px solid #667eea;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .answer-input:focus {
            outline: none;
            border-color: #764ba2;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        
        .feedback {
            font-size: 1.5em;
            font-weight: bold;
            min-height: 40px;
            margin-top: 1rem;
        }
        
        .correct {
            color: #4caf50;
            animation: bounce 0.5s;
        }
        
        .incorrect {
            color: #f44336;
            animation: shake 0.5s;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .results-screen {
            text-align: center;
        }
        
        .results-screen h2 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 1rem;
        }
        
        .final-score {
            font-size: 5em;
            font-weight: bold;
            color: #667eea;
            margin: 1rem 0;
        }
        
        .results-stats {
            background: #f5f5f5;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 2rem 0;
        }
        
        .results-stats p {
            font-size: 1.2em;
            margin: 0.5rem 0;
        }
        
        .high-scores {
            margin-top: 2rem;
            text-align: left;
        }
        
        .high-scores h3 {
            color: #667eea;
            margin-bottom: 1rem;
        }
        
        .score-item {
            background: #f5f5f5;
            padding: 0.8rem;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .question {
                font-size: 2.5em;
            }
            
            .answer-input {
                width: 150px;
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h1>🧮 Математический Спринт</h1>
            <p>Решай примеры на скорость!</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Очки</div>
                <div class="stat-value" id="score">0</div>
            </div>
            <div class="stat">
                <div class="stat-label">Время</div>
                <div class="stat-value" id="timer">60</div>
            </div>
            <div class="stat">
                <div class="stat-label">Streak</div>
                <div class="stat-value" id="streak">0</div>
            </div>
        </div>
        
        <!-- Экран выбора сложности -->
        <div id="startScreen" class="game-screen start-screen">
            <h2>Выберите уровень сложности:</h2>
            <div class="difficulty-buttons">
                <button class="btn btn-easy" onclick="startGame('easy')">
                    😊 Легкий<br>
                    <small>(от 1 до 10)</small>
                </button>
                <button class="btn btn-medium" onclick="startGame('medium')">
                    🤔 Средний<br>
                    <small>(от 10 до 50)</small>
                </button>
                <button class="btn btn-hard" onclick="startGame('hard')">
                    🔥 Сложный<br>
                    <small>(от 50 до 100)</small>
                </button>
            </div>
            <div class="high-scores" id="highScoresStart"></div>
        </div>
        
        <!-- Игровой экран -->
        <div id="gameScreen" class="game-screen hidden">
            <div class="question" id="question">2 + 2 = ?</div>
            <input type="number" id="answerInput" class="answer-input" placeholder="?" autocomplete="off">
            <div class="feedback" id="feedback"></div>
        </div>
        
        <!-- Экран результатов -->
        <div id="resultsScreen" class="game-screen results-screen hidden">
            <h2>Игра окончена!</h2>
            <div class="final-score" id="finalScore">0</div>
            <div class="results-stats">
                <p>Правильных ответов: <strong id="correctAnswers">0</strong></p>
                <p>Неправильных ответов: <strong id="wrongAnswers">0</strong></p>
                <p>Точность: <strong id="accuracy">0%</strong></p>
                <p>Лучший streak: <strong id="bestStreak">0</strong></p>
            </div>
            <button class="btn btn-easy" onclick="resetGame()">🔄 Играть снова</button>
            <div class="high-scores" id="highScoresEnd"></div>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let score = 0;
        let timeLeft = 60;
        let streak = 0;
        let bestStreak = 0;
        let correctCount = 0;
        let wrongCount = 0;
        let currentQuestion = {};
        let difficulty = 'easy';
        let timerInterval;
        let isPlaying = false;

        // Настройки сложности
        const difficulties = {
            easy: { min: 1, max: 10, time: 60 },
            medium: { min: 10, max: 50, time: 60 },
            hard: { min: 50, max: 100, time: 90 }
        };

        // Операции
        const operations = ['+', '-', '*'];

        // Загрузка рекордов при старте
        window.onload = function() {
            displayHighScores('highScoresStart');
        };

        // Начало игры
        function startGame(diff) {
            difficulty = diff;
            timeLeft = difficulties[difficulty].time;
            score = 0;
            streak = 0;
            bestStreak = 0;
            correctCount = 0;
            wrongCount = 0;
            isPlaying = true;
            
            document.getElementById('startScreen').classList.add('hidden');
            document.getElementById('gameScreen').classList.remove('hidden');
            document.getElementById('resultsScreen').classList.add('hidden');
            
            updateStats();
            generateQuestion();
            startTimer();
            
            document.getElementById('answerInput').focus();
        }

        // Генерация вопроса
        function generateQuestion() {
            const config = difficulties[difficulty];
            const num1 = Math.floor(Math.random() * (config.max - config.min + 1)) + config.min;
            const num2 = Math.floor(Math.random() * (config.max - config.min + 1)) + config.min;
            const operation = operations[Math.floor(Math.random() * operations.length)];
            
            let answer;
            let questionText;
            
            switch(operation) {
                case '+':
                    answer = num1 + num2;
                    questionText = `${num1} + ${num2} = ?`;
                    break;
                case '-':
                    // Убедимся, что результат положительный
                    if (num1 >= num2) {
                        answer = num1 - num2;
                        questionText = `${num1} - ${num2} = ?`;
                    } else {
                        answer = num2 - num1;
                        questionText = `${num2} - ${num1} = ?`;
                    }
                    break;
                case '*':
                    // Для умножения используем меньшие числа
                    const mult1 = Math.floor(Math.random() * 10) + 1;
                    const mult2 = Math.floor(Math.random() * 10) + 1;
                    answer = mult1 * mult2;
                    questionText = `${mult1} × ${mult2} = ?`;
                    break;
            }
            
            currentQuestion = {
                text: questionText,
                answer: answer
            };
            
            document.getElementById('question').textContent = questionText;
            document.getElementById('answerInput').value = '';
            document.getElementById('feedback').textContent = '';
        }

        // Проверка ответа
        function checkAnswer() {
            if (!isPlaying) return;
            
            const userAnswer = parseInt(document.getElementById('answerInput').value);
            const feedback = document.getElementById('feedback');
            
            if (isNaN(userAnswer)) return;
            
            if (userAnswer === currentQuestion.answer) {
                // Правильный ответ
                correctCount++;
                streak++;
                if (streak > bestStreak) bestStreak = streak;
                
                // Бонус за streak
                const points = 10 + (streak > 1 ? (streak - 1) * 5 : 0);
                score += points;
                
                feedback.textContent = streak > 1 ? `✓ Правильно! +${points} (Streak x${streak})` : '✓ Правильно!';
                feedback.className = 'feedback correct';
                
                setTimeout(() => {
                    generateQuestion();
                }, 500);
            } else {
                // Неправильный ответ
                wrongCount++;
                streak = 0;
                
                feedback.textContent = `✗ Неправильно! Правильный ответ: ${currentQuestion.answer}`;
                feedback.className = 'feedback incorrect';
                
                setTimeout(() => {
                    generateQuestion();
                }, 1500);
            }
            
            updateStats();
        }

        // Обновление статистики
        function updateStats() {
            document.getElementById('score').textContent = score;
            document.getElementById('timer').textContent = timeLeft;
            document.getElementById('streak').textContent = streak;
        }

        // Таймер
        function startTimer() {
            timerInterval = setInterval(() => {
                timeLeft--;
                updateStats();
                
                if (timeLeft <= 10) {
                    document.getElementById('timer').style.color = '#f44336';
                }
                
                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
        }

        // Конец игры
        function endGame() {
            clearInterval(timerInterval);
            isPlaying = false;
            
            document.getElementById('gameScreen').classList.add('hidden');
            document.getElementById('resultsScreen').classList.remove('hidden');
            
            const accuracy = correctCount + wrongCount > 0 
                ? Math.round((correctCount / (correctCount + wrongCount)) * 100) 
                : 0;
            
            document.getElementById('finalScore').textContent = score;
            document.getElementById('correctAnswers').textContent = correctCount;
            document.getElementById('wrongAnswers').textContent = wrongCount;
            document.getElementById('accuracy').textContent = accuracy + '%';
            document.getElementById('bestStreak').textContent = bestStreak;
            
            saveHighScore(score, difficulty);
            displayHighScores('highScoresEnd');
        }

        // Сохранение рекорда
        function saveHighScore(newScore, diff) {
            let highScores = JSON.parse(localStorage.getItem('mathSprintScores')) || {};
            
            if (!highScores[diff]) {
                highScores[diff] = [];
            }
            
            highScores[diff].push({
                score: newScore,
                date: new Date().toLocaleDateString('ru-RU')
            });
            
            // Сортируем и оставляем топ-5
            highScores[diff].sort((a, b) => b.score - a.score);
            highScores[diff] = highScores[diff].slice(0, 5);
            
            localStorage.setItem('mathSprintScores', JSON.stringify(highScores));
        }

        // Отображение рекордов
        function displayHighScores(elementId) {
            const highScores = JSON.parse(localStorage.getItem('mathSprintScores')) || {};
            const container = document.getElementById(elementId);
            
            let html = '<h3>🏆 Таблица рекордов</h3>';
            
            ['easy', 'medium', 'hard'].forEach(diff => {
                if (highScores[diff] && highScores[diff].length > 0) {
                    const diffName = diff === 'easy' ? 'Легкий' : diff === 'medium' ? 'Средний' : 'Сложный';
                    html += `<p style="margin-top: 1rem;"><strong>${diffName}:</strong></p>`;
                    
                    highScores[diff].forEach((item, index) => {
                        html += `
                            <div class="score-item">
                                <span>${index + 1}. ${item.score} очков</span>
                                <span>${item.date}</span>
                            </div>
                        `;
                    });
                }
            });
            
            container.innerHTML = html;
        }

        // Сброс игры
        function resetGame() {
            document.getElementById('resultsScreen').classList.add('hidden');
            document.getElementById('startScreen').classList.remove('hidden');
            document.getElementById('timer').style.color = '#667eea';
            displayHighScores('highScoresStart');
        }

        // Обработка ввода ответа
        document.getElementById('answerInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });

        document.getElementById('answerInput').addEventListener('input', function() {
            if (this.value.length > 0) {
                checkAnswer();
            }
        });
    </script>
</body>
</html>
```

---

## Пример 2: Мемори-игра (Memory Game)

**Концепция:** Найти все пары карточек (термин - определение)

**Основные элементы:**
- Сетка карточек (4x4 или 6x6)
- Переворачивание карточек по клику
- Проверка совпадения пар
- Счётчик ходов
- Таймер
- Звуки при совпадении/несовпадении

---

## Пример 3: Викторина с жизнями

**Концепция:** Ответить на максимальное количество вопросов, имея 3 жизни

**Основные элементы:**
- Случайные вопросы из базы
- 3 жизни (теряется при неправильном ответе)
- Усложнение с каждым уровнем
- Бонусы за быстрые ответы
- Подсказки (50/50, пропуск вопроса)

---

## Критерии оценивания

| Критерий | Баллы |
|----------|-------|
| Работающая игровая механика | 20 |
| Система начисления очков | 10 |
| Таймер или счётчик ходов | 10 |
| Уровни сложности | 10 |
| Генерация случайных заданий | 10 |
| Сохранение рекордов (localStorage) | 10 |
| Дизайн и анимации | 15 |
| Адаптивность | 5 |
| Инструкция и понятность игры | 10 |
| **Итого** | **100** |

---

## Дополнительные задания (бонусные баллы)

1. **Звуковые эффекты** (+5 баллов)
2. **Множественные темы** (выбор темы игры) (+10 баллов)
3. **Многопользовательский режим** (по очереди) (+10 баллов)
4. **Достижения** (badges за успехи) (+5 баллов)
5. **Анимированный персонаж** или аватар (+5 баллов)
6. **Экспорт результатов** (скриншот, поделиться) (+5 баллов)

---

## Формат сдачи

1. HTML-файл с игрой
2. Название: `фамилия_практика3.html`
3. Дополнительные файлы (звуки, изображения) в отдельной папке
4. Краткая инструкция: как играть, цель игры, особенности

---

## Полезные советы

💡 **Начните с простого:** Сначала реализуйте базовую механику, затем добавляйте функции  
💡 **Тестируйте часто:** Проверяйте игру после каждого нового элемента  
💡 **Баланс сложности:** Игра не должна быть слишком простой или слишком сложной  
💡 **Обратная связь:** Игрок должен всегда понимать, что происходит  
💡 **Используйте отладку:** console.log() поможет найти ошибки  
💡 **Вдохновение:** Поиграйте в похожие игры для понимания механик  

---

## Ресурсы

- **Звуки:** [FreeSound.org](https://freesound.org/)
- **Иконки:** [Font Awesome](https://fontawesome.com/), [Icons8](https://icons8.com/)
- **Цветовые палитры:** [Coolors.co](https://coolors.co/)
- **Анимации CSS:** [Animate.css](https://animate.style/)
- **Примеры игр:** [CodePen](https://codepen.io/tag/game)

Удачи в создании увлекательной образовательной игры! 🎮🎓

