# time_series_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from datetime import datetime


# Функция для загрузки данных из CSV и их предобработки
def load_and_prepare_data(file_path, date_columns=['Дата', 'Время']):
    try:
        # Загрузка данных с преобразованием столбцов даты и времени
        data = pd.read_csv(file_path, parse_dates={'Datetime': date_columns},
                           date_parser=lambda x: datetime.strptime(x, '%y-%m-%d %H:%M:%S.%f'))
        data.set_index('Datetime', inplace=True)
        # Преобразование индекса в формат "только дни"
        data.index = data.index.normalize()
        return data
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return None


# Функция для выполнения тестов на стационарность
def check_stationarity(time_series, significance_level=0.005):
    result = {}

    # Тест Дики-Фуллера (ADF)
    adf_test = adfuller(time_series.dropna())
    result['ADF Test Statistic'] = adf_test[0]
    result['ADF p-value'] = adf_test[1]
    result['ADF Critical Values'] = adf_test[4]
    result['ADF Stationary'] = adf_test[1] < significance_level

    # Тест Кэйпса (KPSS)
    kpss_test = kpss(time_series.dropna(), regression='c', nlags="auto")
    result['KPSS Test Statistic'] = kpss_test[0]
    result['KPSS p-value'] = kpss_test[1]
    result['KPSS Critical Values'] = kpss_test[3]
    result['KPSS Stationary'] = kpss_test[1] > significance_level

    return result


# Функция для визуализации тренда, сезонности и остатка
def decompose_time_series(time_series, period=6):
    decomposition = seasonal_decompose(time_series, model='additive', period=period)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    ax1.plot(decomposition.trend)
    ax1.set_title('Trend')

    ax2.plot(decomposition.seasonal)
    ax2.set_title('Seasonal')

    ax3.plot(decomposition.resid)
    ax3.set_title('Residual')

    plt.tight_layout()
    plt.show()


# Пример использования
if __name__ == "__main__":
    # Путь к файлу данных
    file_path = 'Кран/Rez/Rez_Month.csv'
    data = load_and_prepare_data(file_path)

    if data is not None:
        # Пример проверки стационарности
        for column in data.columns:
            print(f'Проверка стационарности для {column}:')
            result = check_stationarity(data[column])
            print(result)

        # Декомпозиция для первого столбца данных
        first_column = data.columns[0]
        decompose_time_series(data[first_column])
