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

# Функция для проверки стационарности
def check_stationarity(time_series, significance_level=0.05):
    """
    Выполняет тесты на стационарность: ADF и KPSS.

    :param time_series: Pandas Series (ожидается `SmoothedResultValue`)
    :param significance_level: Уровень значимости
    :return: Словарь с результатами тестов
    """
    result = {}
    try:
        adf_test = adfuller(time_series.dropna())
        result['ADF Test Statistic'] = adf_test[0]
        result['ADF p-value'] = adf_test[1]
        result['ADF Critical Values'] = adf_test[4]
        result['ADF Stationary'] = adf_test[1] < significance_level
    except Exception as e:
        print(f"Ошибка ADF теста: {e}")
        result['ADF'] = None

    try:
        kpss_test = kpss(time_series.dropna(), regression='c', nlags="auto")
        result['KPSS Test Statistic'] = kpss_test[0]
        result['KPSS p-value'] = kpss_test[1]
        result['KPSS Critical Values'] = kpss_test[3]
        result['KPSS Stationary'] = kpss_test[1] > significance_level
    except Exception as e:
        print(f"Ошибка KPSS теста: {e}")
        result['KPSS'] = None

    return result


# Функция для визуализации тренда, сезонности и остатка
def decompose_time_series(time_series, period=24):
    """
    Выполняет декомпозицию временного ряда и строит графики.

    :param time_series: Pandas Series
    :param period: Период сезонности
    """
    try:
        decomposition = seasonal_decompose(time_series, model='additive', period=period)
        fig, axes = plt.subplots(4, 1, figsize=(12, 10))

        axes[0].plot(time_series, label='Исходный ряд')
        axes[0].legend(loc='upper left')
        axes[0].set_title('Исходный ряд')

        axes[1].plot(decomposition.trend, label='Тренд', color='orange')
        axes[1].legend(loc='upper left')
        axes[1].set_title('Тренд')

        axes[2].plot(decomposition.seasonal, label='Сезонность', color='green')
        axes[2].legend(loc='upper left')
        axes[2].set_title('Сезонность')

        axes[3].plot(decomposition.resid, label='Остаток', color='red')
        axes[3].legend(loc='upper left')
        axes[3].set_title('Остаток')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ошибка декомпозиции временного ряда: {e}")


# Функция для построения графиков автокорреляции и частичной автокорреляции
def plot_acf_pacf(time_series, lags=40):
    """
    Строит графики ACF и PACF.

    :param time_series: Pandas Series
    :param lags: Количество лагов
    """
    try:
        fig, axes = plt.subplots(1, 2, figsize=(16, 4))

        plot_acf(time_series, ax=axes[0], lags=lags)
        axes[0].set_title('Автокорреляционная функция (ACF)')

        plot_pacf(time_series, ax=axes[1], lags=lags, method='ywm')
        axes[1].set_title('Частичная автокорреляционная функция (PACF)')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ошибка построения ACF/PACF: {e}")