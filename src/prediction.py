def predict_results(model, new_data):
    x_new = new_data[['home_avg_goals_scored', 'home_avg_goals_conceded', 'away_avg_goals_scored', 'away_avg_goals_conceded']]
    predictions = model.predict(x_new)
    return predictions
