import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import glob
import os
from src.data_processing import combine_season_data, calculate_team_stats, calculate_team_statistics, calculate_match_results

def prepare_data(df):
    """Подготовка данных для обучения модели."""
    x = df[['home_avg_goals_scored', 'home_avg_goals_conceded', 'away_avg_goals_scored', 'away_avg_goals_conceded']]
    y = df['result']  # Целевая переменная
    return x, y

def load_model(filename):
    """Загрузка модели из файла, если она существует."""
    if os.path.exists(filename):
        return joblib.load(filename)
    else:
        return None

def save_model(model, filename):
    """Сохранение модели в файл."""
    joblib.dump(model, filename)

def train_model(df):
    x, y = prepare_data(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = load_model('model.pkl')

    if model is None:
        print("Обучение новой модели...")
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', LogisticRegression(max_iter=1000))
        ])
    else:
        print("Загрузка существующей модели...")

    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Точность модели: {accuracy:.2f}")

    save_model(model, 'model.pkl')

    return model

def predict_and_save_results(df, model):
    """Прогнозирование результатов и сохранение в файл."""
    # Прогнозирование для матчей со статусом 'scheduled'
    scheduled_matches = df[df['result'] == 'unknown']  # Предполагаем, что результат 'unknown' для новых матчей

    if not scheduled_matches.empty:
        x_scheduled = scheduled_matches[['home_avg_goals_scored', 'home_avg_goals_conceded', 'away_avg_goals_scored', 'away_avg_goals_conceded']]
        predictions = model.predict(x_scheduled)

        # Добавление предсказанных результатов в DataFrame
        scheduled_matches['predicted_result'] = predictions

        # Сохранение предсказанных результатов в файл
        file_path = 'data/predicted_matches.csv'
        scheduled_matches.to_csv(file_path, index=False)
        print(f"Предсказанные результаты сохранены в {file_path}")
    else:
        print("Нет новых матчей для предсказания")

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
    df_with_result = calculate_match_results(df)  # Используем правильную функцию
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

    # Обучение модели
    model = train_model(df_with_stats)

    # Прогнозирование и сохранение результатов
    predict_and_save_results(df_with_stats, model)

    # Прогнозирование на ручных данных
    new_data = pd.DataFrame({
        'home_avg_goals_scored': [2],
        'home_avg_goals_conceded': [1],
        'away_avg_goals_scored': [1],
        'away_avg_goals_conceded': [2]
    })

    # Прогнозирование на ручных данных
    model = load_model('model.pkl')
    if model:
        new_predictions = model.predict(new_data)
        print("Прогнозы для новых:", new_predictions)
    else:
        print("Модель не загружена.")

if __name__ == "__main__":
    main()
