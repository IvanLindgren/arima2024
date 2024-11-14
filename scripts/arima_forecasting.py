# arima_forecasting.py

import pandas as pd
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from datetime import timedelta


def display_metrics(metrics):
    print(f"\nМетрики для оптимальной модели:\nMSE: {metrics['MSE']:.4f}\nMAE: {metrics['MAE']:.4f}\nR2: {metrics['R2']:.4f}\nMAPE: {metrics['MAPE']:.4f}")

# Обучение и прогнозирование с выводом метрик
def train_and_forecast_with_metrics(time_series, order, forecast_period=14, freq='D'):
    """
    Обучает ARIMA с оптимальными параметрами и выполняет прогноз на указанный период с выводом метрик.

    :param time_series: Временной ряд
    :param order: Оптимальные параметры ARIMA (p, d, q)
    :param forecast_period: Период прогноза
    :param freq: Частота прогноза
    :return: Прогноз
    """
    try:
        model = ARIMA(time_series, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_period)

        # Построение прогноза
        plt.figure(figsize=(12, 6))
        plt.plot(time_series, label="Исходные данные")
        last_date = time_series.index[-1]
        forecast_index = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_period, freq=freq)
        plt.plot(forecast_index, forecast, label=f"Прогноз на {forecast_period} периодов", color='red')
        plt.xlabel("Дата и время")
        plt.ylabel("Значение")
        plt.title(f"Прогноз с параметрами ARIMA{order}")
        plt.legend()
        plt.grid()
        plt.show()

        # Отображение метрик
        metrics = {'MSE': mean_squared_error(time_series[-forecast_period:], forecast),
                   'MAE': mean_absolute_error(time_series[-forecast_period:], forecast),
                   'R2': r2_score(time_series[-forecast_period:], forecast),
                   'MAPE': mean_absolute_percentage_error(time_series[-forecast_period:], forecast)}
        display_metrics(metrics)
        return forecast
    except Exception as e:
        print(f"Ошибка при обучении и прогнозировании: {e}")
        return None



# arima_forecasting.py

# arima_forecasting.py

def comparative_analysis(time_series, order, seasonal_order=None, forecast_period=14):
    """
    Проводит сравнительный анализ прогнозов на основе данных разного объема: 1 месяц и 2 месяца.

    :param time_series: Pandas Series с временным индексом
    :param order: Кортеж (p, d, q) для ARIMA
    :param seasonal_order: Кортеж (P, D, Q, m) для сезонной компоненты SARIMA
    :param forecast_period: Количество периодов для прогноза
    """
    try:
        # Анализ для последнего месяца данных
        one_month_data = time_series[-30:]
        print("Анализ для данных за 1 месяц:")
        forecast_one_month = train_and_forecast_with_metrics(
            one_month_data,
            order=order,
            forecast_period=forecast_period,
            freq='D'
        )

        # Анализ для последних двух месяцев данных
        two_month_data = time_series[-60:]
        print("\nАнализ для данных за 2 месяца:")
        forecast_two_months = train_and_forecast_with_metrics(
            two_month_data,
            order=order,
            forecast_period=forecast_period,
            freq='D'
        )

        return forecast_one_month, forecast_two_months
    except Exception as e:
        print(f"Ошибка при сравнительном анализе: {e}")
        return None, None
