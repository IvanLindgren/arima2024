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


#создаем DataFrame
rz = to_dataframe(file_path = 'Кран/Rez/Rez_Month.csv')

allGr = {}

# Сохранение данных в отдельные CSV файлы для каждого статуса
for rez, group in rz.groupby('Результат'):
    #По какой переменной будет подсчет(по дням = D)
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()# Группируем данные по дням и подсчитываем количество записей в столбце 'ID'

    if rez.endswith(':'):
        rez = rez[:-1]

    rez_df = rez_counts.to_frame(name= rez )
    allGr[rez] = to_dataframe(dataframe = rez_df)

    print(allGr[rez])


















































# #Устанавливаем процентный размер данных для анализа
#
# percentsize = 1  # 100% (берем все данные)
#
# # Создаем массив `allGr`, содержащий первые percentsize*100% данных из каждого массива (ID, WAR, SUC, S_OK, ERR)
# allGr = [arr[:int(len(arr) * percentsize)] for arr in [ID, WAR, SUC, S_OK, ERR]]
#
# # Задаем имена для каждого массива данных, которые будут использоваться в легенде графика
# nameGr = ['id', 'WAR', 'SUC', 'S_OK', 'ERR']
#
# # Настраиваем формат отображения даты на оси X и создаем фигуру и ось для графиков
# fig, ax = plt.subplots(figsize=(12, 8))  # Создаем фигуру размером 12x8 дюймов
# date_form = mdates.DateFormatter("%d-%m")  # Устанавливаем формат даты для оси X: "день-месяц"
#
# # Строим график для каждого массива данных из `allGr` и присваиваем имя из `nameGr`
# for graf, name in zip(allGr, nameGr):
#     ax.plot(graf, label=name)  # Добавляем линию для текущего массива данных с меткой `name`
#
# # Настраиваем подписи и формат оси X
# ax.set_xlabel('Дни')  # Подписываем ось X как "Дни"
# ax.xaxis.set_major_formatter(date_form)  # Применяем формат даты к основной оси X
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Устанавливаем деления по оси X каждые 2 дня
#
# # Отображаем дополнительные элементы графика
# plt.legend()  # Добавляем легенду, чтобы обозначить каждый массив данных
# plt.grid()  # Включаем сетку для лучшей читаемости графика
# plt.tight_layout()  # Автоматически регулируем компоненты графика для минимизации пустого пространства
# plt.show()  # Отображаем график
