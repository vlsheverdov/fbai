from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def prepare_data(df):
    """Подготовка данных для обучения модели."""
    # Выбираем признаки и целевую переменную
    x = df[['home_avg_goals_scored', 'home_avg_goals_conceded', 'away_avg_goals_scored', 'away_avg_goals_conceded']]
    y = df['result']  # Целевая переменная
    return x, y

def train_model(df):
    """Обучение модели."""
    x, y = prepare_data(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Создание модели с пайплайном
    model = Pipeline([
        ('scaler', StandardScaler()),  # Масштабирование признаков
        ('classifier', LogisticRegression(max_iter=1000))  # Логистическая регрессия
    ])

    # Обучение модели
    model.fit(x_train, y_train)

    # Прогнозирование и оценка модели
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Точность модели: {accuracy:.2f}")

    return model
