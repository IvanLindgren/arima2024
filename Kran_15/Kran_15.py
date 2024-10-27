import pandas as pd # пандас для работы с датафреймами
import matplotlib.pyplot as plt # Библиотека для создания визуализаций данных.
import warnings # Используется для управления предупреждениями (warnings) в Python.
import matplotlib.pyplot as plt #Библиотека для создания визуализаций данных.
import matplotlib.dates as mdates #форматирование,отображение и манипуляция с датами на графиках
import numpy as np #Библиотека для численных вычислений.предоставляет поддержку многомерных массивов и матриц
from datetime import datetime# Модуль для работы с датами и временем.
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

# Код для разделения на разные файлы для REZ ////////////////////////////////////////


def csv_to_dataframe(file_path: str) -> DataFrame:
    # Считываем данные из CSV
    dataframe = pd.read_csv(file_path)

    if  not 'Datetime' in dataframe:
        # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
        dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'], format='%y-%m-%d %H:%M:%S.%f')

        # Удаляем столбцы 'Дата' и 'Время', т.к. теперь мы их объединили в один 'Datetime'
        dataframe.drop(columns=['Дата', 'Время'], inplace=True)

    else:
        dataframe['Datetime'] = pd.to_datetime(dataframe['Datetime'])

    # Устанавливаем 'Datetime' как индекс
    dataframe.set_index('Datetime', inplace=True)

    # Сортируем DataFrame по индексу (по времени)
    dataframe.sort_index(inplace=True)

    # Преобразование индекса в формат времени только по дням 11111
    dataframe.index = dataframe.index.map(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))

    return dataframe


#создаем DataFrame
rz = csv_to_dataframe('Кран/Rez/Rez_Month.csv')

# Сохранение данных в отдельные CSV файлы для каждого статуса
for rez, group in rz.groupby('Результат'):
    #По какой переменной будет подсчет(по дням = D)
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()# Группируем данные по дням и подсчитываем количество записей в столбце 'ID'
    rez_counts.to_csv(f'Кран/Rez/{rez}_Month.csv', header=[rez], index=True)#Запись файлов в папку

# Чтение данных со всех файлов ///////////////////////////////////////////

#создаем DataFrame
ID = csv_to_dataframe('Кран/ID_Month.csv')

# Группируем данные по дням и подсчитываем количество записей в столбце 'ID'
ID = ID['ID'].groupby(pd.Grouper(freq='D')).count()


WAR = csv_to_dataframe('Кран/Rez/WAR_Month.csv')  # Считываем данные из CSV-файлов

SUC = csv_to_dataframe('Кран/Rez/SUC_Month.csv') # Считываем данные из CSV-файлов

S_OK = csv_to_dataframe('Кран/Rez/S_OK_Month.csv') # Считываем данные из CSV-файлов

ERR = csv_to_dataframe('Кран/Rez/ERR_Month.csv') # Считываем данные из CSV-файлов

# Выбор кол-ва данных для прогноза в % , заполнение массивов данными ///////////////////////////////////////////

percentsize=1 #100%

#массив для всех файлов
allGr = [
    ID[:int(len(ID) * percentsize)],
    WAR[:int(len(WAR) * percentsize)],
    SUC[:int(len(SUC) * percentsize)],
    S_OK[:int(len(S_OK) * percentsize)],
    ERR[:int(len(ERR) * percentsize)]
]
#массив имен для всех файлов
nameGr=['id','WAR','SUC','S_OK','ERR']

# Выбор кол-ва данных для прогноза в % , заполнение массивов данными ///////////////////////////////////////////

date_form = mdates.DateFormatter("%d-%m") # Устанавливаем формат даты для графиков в виде "день-месяц"


fig, ax = plt.subplots(figsize=(12, 8)) # Создаем новую фигуру и ось для графиков

# Строим каждый график
for graf, nameG in zip(allGr, nameGr): #данные берутся из заданных массивов в начале
    graf.plot(ax=ax, label=nameG)


ax.set_xlabel('Дни') # Задаем название оси x как 'Дни'
ax.xaxis.set_major_formatter(date_form) # Устанавливаем основной формат даты на оси x с использованием ранее заданного формата
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))# Устанавливаем основной тип для оси x, чтобы показывать деления каждые 2 дня
plt.legend() # Добавляем легенду на график
plt.grid()# Включаем сетку на графике
plt.tight_layout()# Автоматически корректируем плотность компонентов на графике для лучшего визуального восприятия
plt.show() # Отображаем график