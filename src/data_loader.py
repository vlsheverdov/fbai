import pandas as pd

def load_data():
    # Загрузка и объединение данных из разных сезонов
    seasons = [2020, 2021, 2022, 2023, 2024]
    all_seasons_data = []

    for season in seasons:
        if season in [2023, 2024]:
            file_path = f'data/season_{season}_data.csv'
        else:
            file_path = f'data/season_{season}_data.csv'

        df = pd.read_csv(file_path)
        df['season'] = season
        all_seasons_data.append(df)

    combined_df = pd.concat(all_seasons_data, ignore_index=True)
    combined_df.to_csv('data/combined_data.csv', index=False)

def load_team_statistics():
    df = pd.read_csv('data/combined_data.csv')

    home_stats, away_stats = calculate_team_statistics(df)

    # Объединение статистики команд
    team_stats = pd.merge(home_stats, away_stats, left_on='home_team', right_on='away_team', how='outer')
    team_stats.to_csv('data/team_statistics.csv', index=False)

def calculate_team_statistics(df):
    home_stats = df.groupby('home_team').agg({
        'score_home': ['mean', 'sum', 'count'],
        'score_away': 'mean'
    }).reset_index()

    away_stats = df.groupby('away_team').agg({
        'score_away': ['mean', 'sum', 'count'],
        'score_home': 'mean'
    }).reset_index()

    home_stats.columns = ['home_team', 'home_avg_goals_scored', 'home_total_goals_scored', 'home_games_played', 'home_avg_goals_conceded']
    away_stats.columns = ['away_team', 'away_avg_goals_conceded', 'away_total_goals_conceded', 'away_games_played', 'away_avg_goals_scored']

    return home_stats, away_stats
