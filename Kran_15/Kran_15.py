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

#             Функция для загрузки и обработки данных из CSV файла

def to_dataframe(file_path: str = None, dataframe: DataFrame = None) -> DataFrame:
    if file_path:
        try:
            # Считываем данные из CSV файла
            dataframe = pd.read_csv(file_path)

            # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
            dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'], format='%y-%m-%d %H:%M:%S.%f')

            # Удаляем ненужные столбцы 'Дата' и 'Время'
            dataframe.drop(columns=['Дата', 'Время'], inplace=True)
        except Exception:
            print("Ошибка при чтении CSV файла")
            return None

    # Если DataFrame уже передан и содержит столбец 'Datetime'
    if dataframe is not None and 'Datetime' in dataframe.columns:
        # Преобразуем столбец 'Datetime' в тип datetime и устанавливаем его в качестве индекса
        dataframe['Datetime'] = pd.to_datetime(dataframe['Datetime'])
        dataframe.set_index('Datetime', inplace=True)

    # Сортируем DataFrame по индексу (дате)
    dataframe.sort_index(inplace=True)

    # Нормализуем индекс, оставляя только дату (без времени)
    if dataframe is not None:
        dataframe.index = dataframe.index.normalize()

    return dataframe

#             Функция для построения общего графика

def create_general_graf(dict_of_frames: dict) -> Figure:
    # Создаем фигуру и оси для построения графика
    fig, axes = plt.subplots(figsize=(12, 8))

    # Построение графиков для каждого элемента из словаря
    for nameG, graf in dict_of_frames.items():
        graf.plot(ax=axes, label=nameG)  # Строим график

    # Настройки осей и форматирования
    axes.set_xlabel('Дни')
    axes.xaxis.set_major_formatter(date_form)
    axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    axes.grid()

    # Плотная компоновка
    plt.tight_layout()

    return fig

#             Функция для построения сезонных графиков

def create_seasonal_graf(dict_of_frames: dict) -> list[Figure]:
    rcParams['figure.figsize'] = 11, 9  # Устанавливаем размер графика
    fig_list = []

    # Разложение временного ряда на тренд, сезонность и остатки
    for nameG, graf in dict_of_frames.items():
        decompose = seasonal_decompose(graf, period=6)
        fig = decompose.plot()  # Построение графика
        fig.suptitle(nameG, fontsize=25)
        fig_list.append(fig)  # Сохраняем фигуру в список

    return fig_list

#             Функция для построения графика скользящего среднего

def create_moving_average_graf(dict_of_frames: dict) -> list[Figure]:
    fig_list = []

    # Построение графика для каждого временного ряда
    for nameG, graf in dict_of_frames.items():
        fig, ax = plt.subplots(figsize=(15, 8))

        # Форматирование осей
        ax.xaxis.set_major_formatter(date_form)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

        # Построение исходного графика и графика скользящего среднего
        ax.plot(graf, label=nameG, color='steelblue')
        ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')

        # Настройки графика
        ax.set_xlabel('Дни', fontsize=14)
        ax.set_title(nameG, fontsize=16)
        ax.legend(title='', loc='upper left', fontsize=14)

        fig.tight_layout()
        fig_list.append(fig)

    return fig_list

#             Функция для построения графика автокорреляции

def create_autocor_graf(dict_of_frames: dict) -> list[Figure]:
    fig_list = []

    # Построение автокорреляционного графика для каждого временного ряда
    for nameG, graf in dict_of_frames.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_acf(graf, ax=ax)

        # Настройки заголовка и компоновки
        ax.set_title(nameG, fontsize=16)
        plt.tight_layout()

        fig_list.append(fig)

    return fig_list

#             Создание DataFrame из CSV файла

# Загрузка данных из CSV файла
rz = to_dataframe(file_path='Кран/Rez/Rez_Month.csv')

# Словарь для хранения всех графиков
allGr = {}import pandas as pd # пандас для работы с датафреймами
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

#             Функция для загрузки и обработки данных из CSV файла

def to_dataframe(file_path: str = None, dataframe: DataFrame = None) -> DataFrame:
    if file_path:
        try:
            # Считываем данные из CSV файла
            dataframe = pd.read_csv(file_path)

            # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
            dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'], format='%y-%m-%d %H:%M:%S.%f')

            # Удаляем ненужные столбцы 'Дата' и 'Время'
            dataframe.drop(columns=['Дата', 'Время'], inplace=True)
        except Exception:
            print("Ошибка при чтении CSV файла")
            return None

    # Если DataFrame уже передан и содержит столбец 'Datetime'
    if dataframe is not None and 'Datetime' in dataframe.columns:
        # Преобразуем столбец 'Datetime' в тип datetime и устанавливаем его в качестве индекса
        dataframe['Datetime'] = pd.to_datetime(dataframe['Datetime'])
        dataframe.set_index('Datetime', inplace=True)

    # Сортируем DataFrame по индексу (дате)
    dataframe.sort_index(inplace=True)

    # Нормализуем индекс, оставляя только дату (без времени)
    if dataframe is not None:
        dataframe.index = dataframe.index.normalize()

    return dataframe

#             Функция для построения общего графика

def create_general_graf(dict_of_frames: dict) -> Figure:
    # Создаем фигуру и оси для построения графика
    fig, axes = plt.subplots(figsize=(12, 8))

    # Построение графиков для каждого элемента из словаря
    for nameG, graf in dict_of_frames.items():
        graf.plot(ax=axes, label=nameG)  # Строим график

    # Настройки осей и форматирования
    axes.set_xlabel('Дни')
    axes.xaxis.set_major_formatter(date_form)
    axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    axes.grid()

    # Плотная компоновка
    plt.tight_layout()

    return fig

#             Функция для построения сезонных графиков

def create_seasonal_graf(dict_of_frames: dict) -> list[Figure]:
    rcParams['figure.figsize'] = 11, 9  # Устанавливаем размер графика
    fig_list = []

    # Разложение временного ряда на тренд, сезонность и остатки
    for nameG, graf in dict_of_frames.items():
        decompose = seasonal_decompose(graf, period=6)
        fig = decompose.plot()  # Построение графика
        fig.suptitle(nameG, fontsize=25)
        fig_list.append(fig)  # Сохраняем фигуру в список

    return fig_list

#             Функция для построения графика скользящего среднего

def create_moving_average_graf(dict_of_frames: dict) -> list[Figure]:
    fig_list = []

    # Построение графика для каждого временного ряда
    for nameG, graf in dict_of_frames.items():
        fig, ax = plt.subplots(figsize=(15, 8))

        # Форматирование осей
        ax.xaxis.set_major_formatter(date_form)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

        # Построение исходного графика и графика скользящего среднего
        ax.plot(graf, label=nameG, color='steelblue')
        ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')

        # Настройки графика
        ax.set_xlabel('Дни', fontsize=14)
        ax.set_title(nameG, fontsize=16)
        ax.legend(title='', loc='upper left', fontsize=14)

        fig.tight_layout()
        fig_list.append(fig)

    return fig_list

#             Функция для построения графика автокорреляции

def create_autocor_graf(dict_of_frames: dict) -> list[Figure]:
    fig_list = []

    # Построение автокорреляционного графика для каждого временного ряда
    for nameG, graf in dict_of_frames.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_acf(graf, ax=ax)

        # Настройки заголовка и компоновки
        ax.set_title(nameG, fontsize=16)
        plt.tight_layout()

        fig_list.append(fig)

    return fig_list

#             Создание DataFrame из CSV файла

# Загрузка данных из CSV файла
rz = to_dataframe(file_path='Кран/Rez/Rez_Month.csv')

# Словарь для хранения всех графиков
allGr = {}

# Устанавливаем формат даты для графиков как "день-месяц"
date_form = mdates.DateFormatter("%d-%m")

# Группировка данных по результатам и создание отдельных DataFrame для каждого статуса
for rez, group in rz.groupby('Результат'):
    # Группируем данные по дням и считаем количество записей
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()

    # Убираем двоеточие в конце, если оно есть
    if rez.endswith(':'):
        rez = rez[:-1]

    # Создаем DataFrame из результатов и сохраняем его в словарь
    rez_df = rez_counts.to_frame(name=rez)
    allGr[rez] = to_dataframe(dataframe=rez_df)


# Устанавливаем формат даты для графиков как "день-месяц"
date_form = mdates.DateFormatter("%d-%m")

# Группировка данных по результатам и создание отдельных DataFrame для каждого статуса
for rez, group in rz.groupby('Результат'):
    # Группируем данные по дням и считаем количество записей
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()

    # Убираем двоеточие в конце, если оно есть
    if rez.endswith(':'):
        rez = rez[:-1]

    # Создаем DataFrame из результатов и сохраняем его в словарь
    rez_df = rez_counts.to_frame(name=rez)
    allGr[rez] = to_dataframe(dataframe=rez_df)
