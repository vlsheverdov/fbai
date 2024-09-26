import pandas as pd
import os

# Назначает результат матча на основе счёта
def assign_result(row):
    if row['score_home'] > row['score_away']:
        return 'home_win'
    elif row['score_home'] < row['score_away']:
        return 'away_win'
    else:
        return 'draw'

# Объединяет данные матчей за разные сезоны в один файл
def combine_season_data(season_files, output_file):
    all_data = []
    for file in season_files:
        if os.path.exists(file):
            print(f"Загрузка данных из {file}")
            df = pd.read_csv(file)
            # Проверка наличия необходимых столбцов
            if 'score_home' in df.columns and 'score_away' in df.columns:
                # Добавляем 'result'
                df['result'] = df.apply(assign_result, axis=1)
                all_data.append(df)
            else:
                print(f"Файл {file} не содержит требуемых столбцов.")
        else:
            print(f"Файл не найден: {file}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Данные сезонов объединены в {output_file}")
    else:
        print("Нет данных для объединения")

if __name__ == "__main__":
    # Список файлов сезонов
    season_files = [
        'data/season_2020_data.csv',
        'data/season_2021_data.csv',
        'data/season_2022_data.csv',
        'data/season_2023_data.csv',
        'data/season_2024_data.csv'
    ]

    # Путь к итоговому файлу
    output_file = 'data/combined_data.csv'
    combine_season_data(season_files, output_file)
