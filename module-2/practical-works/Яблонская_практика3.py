# test_analyzer.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from jinja2 import Template
import weasyprint
import textwrap

# ---------- 1. НАСТРОЙКИ ----------
DATA_DIR   = Path('.')
RESULTS_CSV = DATA_DIR / 'test_results.csv'
INFO_CSV    = DATA_DIR / 'test_info.csv'
FIG_DIR     = DATA_DIR / 'figures'
EXCEL_OUT   = DATA_DIR / 'test_report.xlsx'
PDF_OUT     = DATA_DIR / 'test_report.pdf'

FIG_DIR.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid')

# ---------- 2. ЧТЕНИЕ ----------
results = pd.read_csv(RESULTS_CSV, index_col=0)   # строки = ученики
tasks   = pd.read_csv(INFO_CSV,    index_col=0)   # строки = задания

# ---------- 3. СТАТИСТИКА ----------
total  = results.shape[0]                  # сколько учеников
right  = results.sum()                     # сколько верных ответов по задаче
pct    = (right / total * 100).round(1)  # проценты

stats = pd.DataFrame({'Верно': right, 'Всего': total, 'Процент_верных': pct})
stats = stats.join(tasks[['Тема','Сложность']])

# сложные задания (<60 %)
hard_tasks = stats[stats['Процент_верных'] < 60].index.tolist()

# слабые ученики (<60 % верных)
personal = results.sum(axis=1)
weak_st  = personal[personal < results.shape[1]*0.6].index.tolist()

# успеваемость по темам
theme_stat = stats.groupby('Тема')['Процент_верных'].mean().sort_values()

# ---------- 4. ВИЗУАЛИЗАЦИЯ ----------
plt.figure(figsize=(12,5))
sns.barplot(x=stats.index, y=stats['Процент_верных'], palette='viridis')
plt.xticks(rotation=45)
plt.title('Успеваемость по заданиям')
for i,v in enumerate(stats['Процент_верных']):
    plt.text(i, v+1, f'{v}%', ha='center')
plt.tight_layout()
plt.savefig(FIG_DIR / 'tasks.png', dpi=300)
plt.close()

plt.figure(figsize=(8,6))
sns.heatmap(results, cmap='RdYlGn', cbar_kws={'label':'Верно?'}, linewidths=.5)
plt.title('Матрица ответов (зелёное = верно)')
plt.tight_layout()
plt.savefig(FIG_DIR / 'heatmap.png', dpi=300)
plt.close()

plt.figure(figsize=(8,4))
sns.barplot(x=theme_stat.index, y=theme_stat.values, palette='coolwarm')
plt.title('Средняя успеваемость по темам')
plt.xticks(rotation=45)
plt.ylabel('% верных')
plt.tight_layout()
plt.savefig(FIG_DIR / 'themes.png', dpi=300)
plt.close()

# ---------- 5. ГЕНЕРАЦИЯ HTML-ШАБЛОНА ----------
html_tpl = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Отчёт по тестированию</title>
  <style>
    body{font-family:Arial;margin:40px}
    h1,h2{color:#2E86AB}
    table{border-collapse:collapse;width:100%;margin:15px 0}
    th,td{border:1px solid #ccc;padding:6px;text-align:center}
    th{background:#f3f3f3}
    .red{background:#ffe6e6}
  </style>
</head>
<body>
  <h1>Отчёт по результатам тестирования</h1>
  <p><strong>Количество учеников:</strong> {{total}}</p>
  <h2>Сводная таблица по заданиям</h2>
  {{stats_html}}
  <h2>Проблемные задания (<60 %)</h2>
  <ul>
  {% for t in hard_tasks %}
    <li>{{t}} – {{stats.loc[t,'Процент_верных']}}% верных</li>
  {% endfor %}
  </ul>
  <h2>Слабые ученики (<60 % верных)</h2>
  <ul>
  {% for s in weak_st %}
    <li>{{s}} – {{pers.loc[s]}} из {{cols}} верных</li>
  {% endfor %}
  </ul>
  <h2>Графики</h2>
  <p><img src="figures/tasks.png" width="700"></p>
  <p><img src="figures/heatmap.png" width="600"></p>
  <p><img src="figures/themes.png" width="600"></p>

  <h2>Рекомендации для учителя</h2>
  <ul>
    <li>Повторите темы: {{theme_rec}}</li>
    <li>Дайте дополнительные задачи по заданиям: {{hard_tasks|join(', ')}}</li>
    <li>Отработайте индивидуально с: {{weak_st|join(', ')}}</li>
  </ul>
</body>
</html>
"""

pers = personal
cols = results.shape[1]
html = Template(html_tpl).render(
    total=total,
    stats_html=stats.to_html(classes='table'),
    hard_tasks=hard_tasks,
    weak_st=weak_st,
    theme_rec=', '.join(theme_stat[theme_stat<60].index),
    pers=pers,
    cols=cols
)

# ---------- 6. PDF ----------
weasyprint.HTML(string=html).write_pdf(PDF_OUT)

# ---------- 7. EXCEL ----------
with pd.ExcelWriter(EXCEL_OUT, engine='openpyxl') as w:
    results.to_excel(w, sheet_name='Матрица_ответов')
    stats.to_excel(w, sheet_name='Статистика_заданий')
    theme_stat.to_frame('Средний_процент').to_excel(w, sheet_name='Темы')
    personal.to_frame('Верных_ответов').to_excel(w, sheet_name='Ученики')

print('✅ Отчёты готовы:')
print(f'   Excel -> {EXCEL_OUT.resolve()}')
print(f'   PDF   -> {PDF_OUT.resolve()}')
