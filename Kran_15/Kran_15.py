import pandas as pd # пандас для работы с датафреймами
import matplotlib.pyplot as plt # Библиотека для создания визуализаций данных.
import warnings # Используется для управления предупреждениями (warnings) в Python.
import matplotlib.pyplot as plt #Библиотека для создания визуализаций данных.
import matplotlib.dates as mdates #форматирование,отображение и манипуляция с датами на графиках
import numpy as np #Библиотека для численных вычислений.предоставляет поддержку многомерных массивов и матриц
from datetime import datetime# Модуль для работы с датами и временем.
from matplotlib.figure import Figure
from pandas.core.interchange.dataframe_protocol import DataFrame
from statsmodels.graphics.tsaplots import plot_acf   # Функция для построения графика автокорреляционной функции (ACF).
from statsmodels.graphics.tsaplots import plot_pacf   # Функция для построения графика частичной автокорреляционной функции (PACF).
from sklearn.model_selection import ParameterGrid # Используется для создания сетки параметров для перебора при настройке моделей.
from statsmodels.tools.sm_exceptions import ConvergenceWarning #Предупреждение о сходимости.
from joblib import Parallel, delayed #для параллельного выполнения кода.
from statsmodels.tsa.seasonal import seasonal_decompose #функция для декомпозиции временных рядов, сезонную составляющую и остаток
from pylab import rcParams #параметры для графиков
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from tqdm import tqdm #Библиотека для отображения индикатора прогресса при выполнении итераций в циклах
from statsmodels.tsa.arima.model import ARIMA #Библиотека для статистического анализа и построения временных рядов.



def to_dataframe(file_path: str = None, dataframe: DataFrame = None) -> DataFrame:
    if file_path:
        try:
            # Считываем данные из CSV
            dataframe = pd.read_csv(file_path)

            # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
            dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'],
                                                   format='%y-%m-%d %H:%M:%S.%f')

            # Удаляем столбцы 'Дата' и 'Время', так как они больше не нужны
            dataframe.drop(columns=['Дата', 'Время'], inplace=True)

        except Exception:
            print(f"Ошибка при чтении CSV файла")
            return None

    # Если столбец 'Datetime' существует в предоставленном DataFrame

    if dataframe is not None and 'Datetime' in dataframe.columns:
        # Преобразуем столбец 'Datetime' в формат datetime
        dataframe['Datetime'] = pd.to_datetime(dataframe['Datetime'])
        dataframe.set_index('Datetime', inplace=True)

    # Сортируем DataFrame по индексу (времени)
    dataframe.sort_index(inplace=True)

    # Изменяем индекс, чтобы он содержал только дату
    if dataframe is not None:
        dataframe.index = dataframe.index.normalize()

    return dataframe

def create_general_graf(dict_of_frames: dict) -> Figure:
    # Устанавливаем формат даты и параметры отображения
    fig, axes = plt.subplots(figsize=(12, 8))

    # Построение графиков
    for nameG, graf in dict_of_frames.items():
        graf.plot(ax=axes, label=nameG)

    # Настройки осей и оформления
    axes.set_xlabel('Дни')
    axes.xaxis.set_major_formatter(date_form)
    axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    axes.grid()

    # Отображаем график с плотной компоновкой
    plt.tight_layout()

    return fig


def create_seasonal_graf(dict_of_frames: dict) -> list[Figure]:
    rcParams['figure.figsize'] = 11, 9  # Устанавливаем размер графика
    fig_list = []

    for nameG, graf in dict_of_frames.items():  # данные берутся из заданных массивов в начале

        decompose = seasonal_decompose(graf, period=6)  # Выполняем сезонное разложение временного ряда graf с периодом 6
        fig = decompose.plot()  # Создаем графическое представление разложения и сохраняем его в fig
        fig.suptitle(nameG, fontsize=25)  # Устанавливаем заголовок
        fig_list.append(fig)

    return fig_list



def create_moving_average_graf(dict_of_frames: dict) -> list[Figure]:
    fig_list = []
    for nameG, graf in dict_of_frames.items():

        fig, ax = plt.subplots(figsize=(15, 8))

        ax.xaxis.set_major_formatter(date_form)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

        ax.plot(graf, label=nameG, color='steelblue')
        ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')

        # Настройки графика
        ax.set_xlabel('Дни', fontsize=14)
        ax.set_title(nameG, fontsize=16)
        ax.legend(title='', loc='upper left', fontsize=14)

        # выведем обе кривые на одном график
        fig.tight_layout()
        fig.show()
        fig_list.append(fig)

    return fig_list


def create_autocor_graf(dict_of_frames: dict) -> list[Figure]:

    fig_list = []
    for nameG, graf in dict_of_frames.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        # Строим автокорреляционный график на заданных осях
        plot_acf(graf, ax=ax)

        # Устанавливаем заголовок графика
        ax.set_title(nameG, fontsize=16)

        # Плотная компоновка
        plt.tight_layout()

        # Возвращаем объект Figure
        fig_list.append(fig)

    return fig_list


#создаем DataFrame
rz = to_dataframe(file_path = 'Кран/Rez/Rez_Month.csv')

allGr = {}
date_form = mdates.DateFormatter("%d-%m")  # Устанавливаем формат даты для  графиков как "день-месяц"

# Сохранение данных в отдельные CSV файлы для каждого статуса
for rez, group in rz.groupby('Результат'):
    #По какой переменной будет подсчет(по дням = D)
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()# Группируем данные по дням и подсчитываем количество записей

    if rez.endswith(':'):
        rez = rez[:-1]

    rez_df = rez_counts.to_frame(name=rez )
    allGr[rez] = to_dataframe(dataframe = rez_df)
