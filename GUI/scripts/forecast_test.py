import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure  # Для работы с объектами Figure
from datetime import timedelta

# Импортируем функции из вспомогательных скриптов
from scripts.arima_forecasting import train_and_forecast_with_metrics, comparative_analysis
from scripts.arima_tuning import tune_arima_with_grid_search, find_best_seasonal_period, evaluate_arima_with_best_params
from scripts.time_series_analysis import check_stationarity, decompose_time_series, plot_acf_pacf

# Импортируем функции для чтения данных (kran15_rez, kran_15_state, Scaner, Balka)
from scripts.kran15_rez import read_excel_to_dataframe as read_kran15_rez
from scripts.kran_15_state import read_excel_to_dataframe as read_kran15_state, count_records_by_day_auto
from scripts.Scaner import read_excel_to_dataframe as read_scaner, count_records_by_hour_auto as count_scaner
from scripts.Balka import read_excel_to_dataframe as read_balka, count_records_by_hour_auto as count_balka


'''from arima_forecasting import train_and_forecast_with_metrics, comparative_analysis
from arima_tuning import tune_arima_with_grid_search, find_best_seasonal_period, evaluate_arima_with_best_params
from time_series_analysis import check_stationarity, decompose_time_series, plot_acf_pacf

from kran15_rez import read_excel_to_dataframe as read_kran15_rez
from kran_15_state import read_excel_to_dataframe as read_kran15_state, count_records_by_day_auto
from Scaner import read_excel_to_dataframe as read_scaner, count_records_by_hour_auto as count_scaner
from Balka import read_excel_to_dataframe as read_balka, count_records_by_hour_auto as count_balka'''

def arima_forecast_and_plot(data_source, column_name, paths, forecast_period=5):
    """
    Функция для прогнозирования временного ряда с помощью ARIMA и построения графика.

    Args:
        data_source (str): Источник данных ('kran15_rez', 'kran_15_state', 'Scaner', 'Balka').
        column_name (str): Название столбца для прогнозирования.
        forecast_period (int): Период прогнозирования (в днях).
        train_period_months (int): Период обучения (в месяцах).

    Returns:
        dict: Словарь с результатами, включая график и метрики.
    """

    # Чтение данных в зависимости от источника
    if data_source == 'kran_15_rez':
        df = read_kran15_rez(file_paths=paths)  # Заменить на корректный путь к файлу
        if df is not None:
            time_series = df[df['Результат'].str.startswith(column_name)]
            time_series = time_series.groupby(pd.Grouper(freq='D')).size()

    elif data_source == 'kran_15_state':
        df = read_kran15_state(file_paths=paths)  # Заменить на корректный путь к файлу
        if df is not None:
            time_series = count_records_by_day_auto(df)
            time_series = time_series[column_name]
            
    elif data_source == 'Scaner':
        df = read_scaner(file_paths=paths)  # Заменить на корректный путь к файлу
        if df is not None:
            time_series = count_scaner(df)
            time_series = time_series[column_name]

    elif data_source == 'Balka':
        df = read_balka(file_paths=paths)  # Заменить на корректный путь к файлу
        if df is not None:
            time_series = count_balka(df)
            time_series = time_series[column_name]

    else:
        return {"error": "Неверный источник данных"}

    if time_series is None or time_series.empty:
        return {"error": "Данные не найдены или некорректный столбец"}

    # Обучение и прогнозирование
    train_data = time_series[:-forecast_period]

    # Автоматический подбор параметров ARIMA
    best_order, best_metrics = tune_arima_with_grid_search(train_data)

    # Прогнозирование
    model_fit, forecast = evaluate_arima_with_best_params(train_data, order=best_order, forecast_steps=forecast_period)

    # Визуализация
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(time_series[-forecast_period * 3:], label='Реальные данные')  # 3 последних значения + прогноз
    last_date = time_series.index[-1 - forecast_period]

    # Для отрисовки данных берем последние forecast_period значений + прогноз
    forecast_index = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_period, freq='D')
    ax.plot(forecast_index, forecast, label='Прогноз', color='red')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Значение')
    ax.set_title(f'Прогноз {column_name} на {forecast_period} дней')
    ax.legend()
    ax.grid()

    # Сохраняем график в Figure объект
    figure = fig

    # Конвертируем Figure в словарь (невозможно напрямую)
    # Вместо этого сохраняем график в файл и возвращаем путь к файлу
    figure.savefig('forecast_plot.png')  # Сохраняем график как PNG

    # Возвращаем результаты в виде словаря
    results = {
        "data_source": data_source,
        "column_name": column_name,
        "forecast_period": forecast_period,
        "forecast_values": forecast.tolist(),  # Конвертируем Series в list
        "forecast_index": [date.strftime('%Y-%m-%d') for date in forecast_index],  # Конвертируем индекс в list строк
        "last_date": time_series.index[-1 - forecast_period].strftime('%Y-%m-%d'),  # Оставляем только дату
        "actual_values": time_series[-forecast_period * 3:].tolist(),
        "actual_index": [date.strftime('%Y-%m-%d') for date in time_series[-forecast_period * 3:].index],
        "plot_path": figure,  # Путь к сохраненному графику
        "metrics": best_metrics
    }
    plt.close(fig)  # Закрываем график, чтобы не отображать его на сервере

    return results


# Пример использования
#results = arima_forecast_and_plot(data_source='kran15_rez', column_name='ERR', forecast_period=5)
#print(results)
# Конвертируем результаты в JSON
#print(json.dumps(results, indent=4))
#print(arima_forecast_and_plot(data_source='kran_15_state', column_name='Статус', forecast_period=5, path='C:/Users/user/Documents/test/LPC_Kran15_Data_State_Month.xlsx'))