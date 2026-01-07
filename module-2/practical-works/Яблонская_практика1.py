import pandas as pd
import numpy as np


def load_data(filepath):
    """Загрузка данных из CSV-файла."""
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        print("Данные успешно загружены.")
        return df
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def calculate_average(df):
    """Расчёт среднего балла каждого ученика."""
    df['Средний_балл'] = df.iloc[:, 1:].mean(axis=1).round(2)
    return df


def determine_status(df):
    """Определение статуса ученика по среднему баллу."""
    conditions = [
        (df['Средний_балл'] >= 4.5),
        (df['Средний_балл'] >= 4.0) & (df['Средний_балл'] < 4.5),
        (df['Средний_балл'] >= 3.5) & (df['Средний_балл'] < 4.0),
        (df['Средний_балл'] < 3.5)
    ]
    statuses = ['Отличник', 'Хорошист', 'Троечник', 'Требуется внимание']
    df['Статус'] = np.select(conditions, statuses, default='Неизвестно')
    return df


def find_underperformers(df):
    """Выявление отстающих учеников (средний балл < 3.5)."""
    underperformers = df[df['Средний_балл'] < 3.5]
    return underperformers


def top_5_students(df):
    """Топ‑5 лучших учеников по среднему баллу."""
    top_5 = df.nlargest(5, 'Средний_балл')
    return top_5


def subject_statistics(df):
    """Статистика по предметам: средний, мин, макс."""
    stats = df.iloc[:, 1:-2].describe().T  # Т — транспонирование для удобства
    stats['средний'] = stats['mean'].round(2)
    stats['мин'] = stats['min']
    stats['макс'] = stats['max']
    return stats[['средний', 'мин', 'макс']]


def save_to_excel(df, stats, filepath):
    """Сохранение результатов в Excel с форматированием."""
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Лист с данными учеников
        df.to_excel(writer, sheet_name='Ученики', index=False)

        # Лист со статистикой по предметам
        stats.to_excel(writer, sheet_name='Статистика_по_предметам')

        # Форматирование
        workbook = writer.book
        worksheet = writer.sheets['Ученики']

        # Заголовки жирным
        for cell in worksheet[1]:
            cell.font = cell.font.copy(bold=True)

        # Выделение отстающих красным
        for row in range(2, len(df) + 2):
            if df.iloc[row - 2]['Средний_балл'] < 3.5:
                for col in range(1, len(df.columns) + 1):
                    worksheet.cell(row=row, column=col).fill = \
                        openpyxl.styles.PatternFill(start_color="FFCCCC", fill_type="solid")


def generate_report(df, underperformers, top_5, stats):
    """Создание текстового отчёта."""
    report = f"""ОТЧЁТ ПО УСПЕВАЕМОСТИ КЛАССА
============================

Общее количество учеников: {len(df)}

ТОП‑5 ЛУЧШИХ УЧЕНИКОВ:
{top_5[['Ученик', 'Средний_балл']].to_string(index=False)}

ОТСТАЮЩИЕ УЧЕНИКИ (средний балл < 3.5):
{underperformers[['Ученик', 'Средний_балл', 'Статус']].to_string(index=False) if not underperformers.empty else "Нет отстающих"}

СТАТИСТИКА ПО ПРЕДМЕТАМ:
{stats.to_string()}

СРЕДНИЙ БАЛЛ ПО КЛАССУ: {df['Средний_балл'].mean().round(2)}
"""
    return report


def main():
    input_file = 'journal.csv'
    output_file = 'отчет_по_успеваемости.xlsx'
    report_file = 'README.txt'

    # 1. Загрузка данных
    df = load_data(input_file)
    if df is None:
        return

    # 2. Расчёт среднего балла
    df = calculate_average(df)

    # 3. Определение статуса
    df = determine_status(df)

    # 4. Выявление отстающих
    underperformers = find_underperformers(df)

    # 6. Статистика по предметам
    stats = subject_statistics(df)

    # 7. Сохранение в Excel
    save_to_excel(df, stats, output_file)

    # 8. Создание отчёта
    report = generate_report(df, underperformers, stats)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("Анализ завершён. Результаты сохранены в:")
    print(f"!  - Excel: {output_file}")
    print(f"!  - Текст: {report_file}")

    if __name__ == '__main__':
        main()
