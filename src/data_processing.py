import pandas as pd
import glob
import os

def combine_season_data(season_files, output_file):
    """Объединяет данные матчей за разные сезоны в один файл."""
    all_data = []
    for file in season_files:
        if os.path.exists(file):
            print(f"Загрузка данных из {file}")
            df = pd.read_csv(file)
            all_data.append(df)
        else:
            print(f"Файл не найден: {file}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Данные сезонов объединены в {output_file}")
    else:
        print("Нет данных для объединения")

def calculate_team_stats(df):
    """Расчитывает статистику для каждой команды и добавляет в DataFrame."""
    df['home_avg_goals_scored'] = df.groupby('home_team')['score_home'].transform('mean')
    df['home_avg_goals_conceded'] = df.groupby('home_team')['score_away'].transform('mean')
    df['away_avg_goals_scored'] = df.groupby('away_team')['score_away'].transform('mean')
    df['away_avg_goals_conceded'] = df.groupby('away_team')['score_home'].transform('mean')

    return df

def calculate_team_statistics(df):
    """Расчитывает общую статистику по командам и сохраняет в файл."""
    teams = pd.concat([df['home_team'], df['away_team']]).unique()

    stats = []
    for team in teams:
        team_data = df[(df['home_team'] == team) | (df['away_team'] == team)]

        avg_goals_scored = (team_data['score_home'][team_data['home_team'] == team].sum() +
                            team_data['score_away'][team_data['away_team'] == team].sum()) / len(team_data)
        avg_goals_conceded = (team_data['score_away'][team_data['home_team'] == team].sum() +
                              team_data['score_home'][team_data['away_team'] == team].sum()) / len(team_data)

        stats.append({'team': team, 'avg_goals_scored': avg_goals_scored, 'avg_goals_conceded': avg_goals_conceded})

    return pd.DataFrame(stats)

def calculate_match_results(df):
    """Заполняет колонку 'result' на основе счетов или оставляет 'unknown' для матчей со статусом 'scheduled'."""
    def get_result(row):
        if pd.isna(row['score_home']) or pd.isna(row['score_away']):
            return 'unknown'  # Используем 'unknown' для матчей, которые еще не сыграны
        elif row['score_home'] > row['score_away']:
            return 'home_win'
        elif row['score_home'] < row['score_away']:
            return 'away_win'
        else:
            return 'draw'

    df['result'] = df.apply(get_result, axis=1)

    return df

def main():
    # Объединение данных сезонов
    season_files = glob.glob('data/season_*_data.csv')
    if not season_files:
        print("Не найдено файлов для объединения. Проверьте папку 'data'.")
        return

    combine_season_data(season_files, 'data/combined_data.csv')

    # Загрузка объединенных данных
    df = pd.read_csv('data/combined_data.csv')

    # Добавление столбца 'result'
    df_with_result = calculate_match_results(df)
    df_with_result.to_csv('data/combined_data_with_result.csv', index=False)
    print("Столбец 'result' добавлен в combined_data_with_result.csv")

    # Добавление статистики команд
    df_with_stats = calculate_team_stats(df_with_result)
    df_with_stats.to_csv('data/combined_data_with_stats.csv', index=False)
    print("Статистика команд добавлена в combined_data_with_stats.csv")

    # Расчет общей статистики по командам
    team_stats = calculate_team_statistics(df_with_result)
    team_stats.to_csv('data/team_statistics.csv', index=False)
    print("Общая статистика по командам сохранена в team_statistics.csv")

if __name__ == "__main__":
    main()
