import pandas as pd
import matplotlib.pyplot as plt
import warnings
import sys
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from scripts.time_series_analysis import check_stationarity, decompose_time_series
from scripts.arima_tuning import tune_arima_with_grid_search
from scripts.arima_forecasting import train_and_forecast_with_metrics



def get_plots_kran_15(path: str) -> dict: 
    # Функция для загрузки и обработки данных из CSV/XLS файла
    def to_dataframe(file_path: str = None, dataframe: pd.DataFrame = None) -> pd.DataFrame:
        if file_path:
            try:
                # Чтение из Excel или CSV в зависимости от расширения файла
                if file_path.endswith(('.xlsx', '.xls')):
                    dataframe = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    dataframe = pd.read_csv(file_path, encoding='utf-8')
                else:
                    raise ValueError("Поддерживаются только файлы с расширением .xlsx, .xls и .csv")

                # Проверка на наличие нужных колонок
                required_columns = {'Дата', 'Время', 'Результат'}
                if not required_columns.issubset(dataframe.columns):
                    raise ValueError("Отсутствуют необходимые столбцы: 'Дата', 'Время', 'Результат'")

                # Приведение столбцов 'Дата' и 'Время' к строковому типу
                dataframe['Дата'] = dataframe['Дата'].astype(str)
                dataframe['Время'] = dataframe['Время'].astype(str)

                # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
                dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'], errors='coerce')
                dataframe.drop(columns=['Дата', 'Время'], inplace=True)
                dataframe.dropna(subset=['Datetime'], inplace=True)

                # Заменяем значения в 'Результат' на числовые представления
                dataframe['SmoothedResultValue'] = dataframe['Результат'].map({
                    'S_OK': 1,
                    'SUC:': 0.8,
                    'ERR:': 0.5,
                    'WAR:': 0.2
                }).fillna(0.1)

                # Устанавливаем 'Datetime' в качестве индекса
                dataframe.set_index('Datetime', inplace=True)
                dataframe.sort_index(inplace=True)

            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                return None

        return dataframe



    # Функция для построения общего графика
    def create_general_graf(dict_of_frames: dict) -> plt.Figure:
        fig, axes = plt.subplots(figsize=(12, 8))
        for nameG, graf in dict_of_frames.items():
            graf.plot(ax=axes, label=nameG)
        axes.set_xlabel('Дни')
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        axes.grid()
        plt.tight_layout()
        return fig


    # Функция для построения сезонных графиков
    def create_seasonal_graf(dict_of_frames: dict) -> list:
        rcParams['figure.figsize'] = 11, 9
        fig_list = []
        for nameG, graf in dict_of_frames.items():
            decompose = seasonal_decompose(graf, period=6)
            fig = decompose.plot()
            fig.suptitle(nameG, fontsize=25)
            fig_list.append(fig)
        return fig_list


    # Функция для построения графика скользящего среднего
    def create_moving_average_graf(dict_of_frames: dict) -> list:
        fig_list = []
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(15, 8))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            ax.plot(graf, label=nameG, color='steelblue')
            ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')
            ax.set_xlabel('Дни', fontsize=14)
            ax.set_title(nameG, fontsize=16)
            ax.legend(title='', loc='upper left', fontsize=14)
            fig.tight_layout()
            fig_list.append(fig)
        return fig_list


    # Функция для построения графика автокорреляции
    def create_autocor_graf(dict_of_frames: dict) -> list:
        fig_list = []
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_acf(graf, ax=ax)
            ax.set_title(nameG, fontsize=16)
            plt.tight_layout()
            fig_list.append(fig)
        return fig_list

    # Загружаем и подготавливаем данные
    file_path = path
    data = to_dataframe(file_path)

    # Инициализация словаря для хранения временных рядов
    allGr = {}
    print(data)
    
    # Группировка данных по уникальным значениям результата и подготовка временных рядов
    for result_type, group in data.groupby('SmoothedResultValue'):
        # Агрегируем данные по дням и считаем количество записей за день для каждого типа результата
        daily_counts = group.resample('D').size()

        # Добавляем в словарь `allGr` сгруппированные данные по типу результата
        allGr[result_type] = daily_counts.to_frame(name='Counts')

    dict_plots_kran_15 = {}
    dict_plots_kran_15['Общий график'] = create_general_graf(allGr)
    dict_plots_kran_15['Сезонные графики'] = create_seasonal_graf(allGr)
    dict_plots_kran_15['Построение скользящего среднего'] = create_moving_average_graf(allGr)
    dict_plots_kran_15['График автокорелляции'] = create_autocor_graf(allGr)

    # Далее выполняем анализ и прогноз для каждого временного ряда
    for name, time_series in allGr.items():
        print(f"\nАнализ для {name}:")

        # Проверка стационарности и декомпозиция
        stationarity_result = check_stationarity(time_series['Counts'])
        print(stationarity_result)

        # Подбор параметров модели и расчет метрик
        best_order, metrics = tune_arima_with_grid_search(time_series['Counts'])

        # Обучение модели и прогнозирование
        forecast = train_and_forecast_with_metrics(time_series['Counts'], order=best_order)