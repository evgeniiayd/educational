import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка стиля
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# 1. Генерация примерных данных
np.random.seed(42)
students = [f'Ученик {i}' for i in range(1, 31)]
subjects = ['Математика', 'Русский', 'Физика', 'Химия', 'История']
quarters = ['I', 'II', 'III', 'IV']

# Таблица оценок: ученики × предметы × четверти
data = pd.read_csv('journal.csv')
for student in students:
    for q in quarters:
        row = {
            'Ученик': student,
            'Четверть': q,
            **{subj: np.random.randint(3, 6) for subj in subjects}
        }
        data.append(row)
df = pd.DataFrame(data)

# Агрегация для графиков
df_mean = df.groupby('Ученик')[subjects].mean().mean(axis=1)  # Средний балл ученика
df_subject_mean = df[subjects].mean()  # Средний по предметам
df_grades = df[subjects].values.flatten()
grade_counts = pd.Series(df_grades).value_counts().sort_index()

# 2. Создание фигуры с подграфиками
fig, axes = plt.subplots(3, 3, figsize=(18, 16))
axes = axes.flatten()

# 2.1 Средние баллы по предметам (столбчатая)
axes[0].bar(df_subject_mean.index, df_subject_mean.values, color='skyblue')
axes[0].set_ylabel('Средний балл')

# 2.2 Распределение оценок (круговая)
axes[1].pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Распределение оценок')

# 2.3 Топ-10 учеников (горизонтальная столбчатая)
top10 = df_mean.sort_values(ascending=False).head(10)
axes[2].barh(top10.index, top10.values, color='lightgreen')
axes[2].set_title('Топ-10 учеников по среднему баллу')
axes[2].set_xlabel('Средний балл')

# 2.4 Тепловая карта оценок
df_pivot = df.pivot_table(index='Ученик', columns='Четверть', values=subjects, aggfunc='mean')
sns.heatmap(df_pivot, ax=axes[3], cmap='RdYlBu', center=0, annot=True, fmt='.1f')
axes[3].set_title('Тепловая карта средних оценок по четвертям')

# 2.5 Динамика успеваемости по четвертям (линейный)
quarter_means = df.groupby('Четверть')[subjects].mean()
for subj in subjects:
    axes[4].plot(quarter_means.index, quarter_means[subj], label=subj, marker='o')
axes[4].set_title('Динамика успеваемости по четвертям')
axes[4].set_xlabel('Четверть')
axes[4].set_ylabel('Средний балл')
axes[4].legend()

# 2.6 Box plot для сравнения предметов
df[subjects].boxplot(ax=axes[5], patch_artist=True, boxprops=dict(facecolor='lightblue'))
axes[5].set_title('Разброс оценок по предметам')
axes[5].set_ylabel('Оценка')

# 2.7 Статистический блок (текст на графике)
stats = (
    f"Всего учеников: {len(students)}\n"
    f"Средние баллы:\n"
    + "\n".join([f"{s}: {df_subject_mean[s]:.2f}" for s in subjects]) + "\n"
    f"Общий средний балл: {df[subjects].mean().mean():.2f}\n"
    f"Стд. отклонение: {df[subjects].stack().std():.2f}"
)
axes[6].text(0.1, 0.9, stats, fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat"))
axes[6].set_title('Статистический блок')
axes[6].axis('off')

# Скрываем лишние подграфики
for i in [7, 8]:
    axes[i].axis('off')

# 3. Сохранение дашборда
plt.suptitle('Дашборд мониторинга успеваемости', fontsize=16)
plt.tight_layout()
plt.savefig('dashboard_uspevaemost.png', dpi=300, bbox_inches='tight')
plt.show()
