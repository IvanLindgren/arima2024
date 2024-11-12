# arima_forecasting.py

import pandas as pd
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from datetime import timedelta


# Функция для обучения и прогнозирования на 14 дней
def train_and_forecast(time_series, order, forecast_period=14):
    """
    Обучает модель ARIMA с заданными параметрами и выполняет прогноз на указанный период.
    """
    try:
        model = ARIMA(time_series, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_period)

        # Построение прогноза
        plt.figure(figsize=(10, 5))
        plt.plot(time_series, label="Исходные данные")
        forecast_index = pd.date_range(start=time_series.index[-1] + timedelta(days=1), periods=forecast_period,
                                       freq='D')
        plt.plot(forecast_index, forecast, label="Прогноз на 14 дней", color='red')
        plt.xlabel("Дата")
        plt.ylabel("Значение")
        plt.title(f"Прогноз на основе ARIMA модели {order}")
        plt.legend()
        plt.grid()
        plt.show()

        return forecast
    except Exception as e:
        print(f"Ошибка при обучении и прогнозировании: {e}")
        return None


# Функция для обработки ошибок и предупреждений
def suppress_warnings():
    """
    Подавляет предупреждения и ошибки, которые могут возникать в процессе работы модели.
    """
    warnings.filterwarnings("ignore")
    warnings.simplefilter("ignore", category=UserWarning)
    warnings.simplefilter("ignore", category=FutureWarning)


# Функция для анализа модели на данных разного объема (1 месяц и 2 месяца)
def comparative_analysis(time_series, order, forecast_period=14):
    """
    Проводит сравнительный анализ прогнозов на основе данных разного объема: 1 месяц и 2 месяца.
    """
    # Анализ для последнего месяца данных
    one_month_data = time_series[-30:]
    print("Анализ для данных за 1 месяц:")
    forecast_one_month = train_and_forecast(one_month_data, order, forecast_period)

    # Анализ для последних двух месяцев данных
    two_month_data = time_series[-60:]
    print("\nАнализ для данных за 2 месяца:")
    forecast_two_months = train_and_forecast(two_month_data, order, forecast_period)

    return forecast_one_month, forecast_two_months


# Основной код для выполнения задач 11, 12 и 13
if __name__ == "__main__":
    suppress_warnings()  # Подавляем предупреждения

    # Путь к файлу данных и загрузка
    file_path = 'Кран/Rez/Rez_Month.csv'
    data = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')

    if not data.empty:
        time_series = data[data.columns[0]]

        # Задача 10: Предполагаем, что на этом этапе уже есть оптимальные параметры, например:
        best_order = (2, 1, 2)  # пример, нужно заменить на реальные оптимальные значения

        # Задача 11: Обучение модели и прогнозирование на 14 дней
        print("Прогноз на 14 дней:")
        forecast = train_and_forecast(time_series, best_order)

        # Задача 13: Сравнительный анализ на данных за 1 месяц и за 2 месяца
        print("\nСравнительный анализ на данных разного объема:")
        comparative_analysis(time_series, best_order)
