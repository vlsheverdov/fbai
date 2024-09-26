import pandas as pd

def preprocess_data():
    # Загрузка данных
    df = pd.read_csv('data/combined_data.csv')

    # Обработка данных
    # Преобразование 'scheduled' матчей
    df['result'] = df['result'].apply(lambda x: 'draw' if x == 'scheduled' else x)

    # Сохранение обработанных данных
    df.to_csv('data/combined_data.csv', index=False)
