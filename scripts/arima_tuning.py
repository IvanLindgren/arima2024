# arima_tuning.py

import pandas as pd
import warnings
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error


# Подбор гиперпараметров с помощью auto_arima
def tune_arima_model(time_series, seasonal=False, max_p=5, max_d=2, max_q=5, m=1, max_order=20):
    """
    Подбирает оптимальные параметры ARIMA с помощью pmdarima.auto_arima.
    """
    warnings.filterwarnings("ignore")

    # Используем auto_arima для подбора параметров
    model = auto_arima(time_series,
                       start_p=1, start_q=1,
                       max_p=max_p, max_d=max_d, max_q=max_q,
                       seasonal=seasonal, m=m,
                       trace=True,  # Убираем False, если нужно видеть шаги подбора параметров
                       error_action='ignore',
                       suppress_warnings=True,
                       stepwise=True,
                       max_order=max_order)

    print(f"Оптимальные параметры для ARIMA: {model.order}")
    return model.order


# Функция для оценки модели с оптимизированными гиперпараметрами
def evaluate_arima_with_best_params(time_series, order, forecast_steps=14):
    """
    Обучает модель ARIMA с заданными параметрами и оценивает ее на основе метрик.
    """
    try:
        model = ARIMA(time_series, order=order)
        model_fit = model.fit()
        predictions = model_fit.forecast(steps=forecast_steps)

        # Метрики оценки
        mse = mean_squared_error(time_series[-forecast_steps:], predictions)
        mae = mean_absolute_error(time_series[-forecast_steps:], predictions)
        r2 = r2_score(time_series[-forecast_steps:], predictions)
        mape = mean_absolute_percentage_error(time_series[-forecast_steps:], predictions)

        print(f"Метрики для модели ARIMA {order}:")
        print(f"MSE: {mse}, MAE: {mae}, R2: {r2}, MAPE: {mape}")

        return model_fit, predictions
    except Exception as e:
        print(f"Ошибка при обучении модели ARIMA: {e}")
        return None, None


# Пример использования
if __name__ == "__main__":
    # Загрузка данных
    file_path = 'Кран/Rez/Rez_Month.csv'
    data = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')

    # Пример подбора гиперпараметров для первого столбца данных
    if not data.empty:
        time_series = data[data.columns[0]]

        # Подбор параметров ARIMA
        best_order = tune_arima_model(time_series)

        # Оценка модели с подобранными параметрами
        evaluate_arima_with_best_params(time_series, best_order)
