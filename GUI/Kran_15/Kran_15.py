import pandas as pd  # Для работы с DataFrame
import matplotlib.pyplot as plt  # Для визуализации данных
import matplotlib.dates as mdates  # Форматирование и работа с датами на графиках
from statsmodels.graphics.tsaplots import plot_acf  # График автокорреляции
from statsmodels.tsa.seasonal import seasonal_decompose  # Декомпозиция временных рядов
from matplotlib.figure import Figure
from pylab import rcParams  # Параметры графиков
from pathlib import Path
from scripts.time_series_analysis import check_stationarity, decompose_time_series
from scripts.arima_tuning import tune_arima_with_grid_search
from scripts.arima_forecasting import train_and_forecast_with_metrics


def get_plots_kran_15(path: str) -> dict: 
    
    # Чтение Excel-файла и преобразование в DataFrame
    def read_excel_to_dataframe(file_path: str = None) -> pd.DataFrame:
        try:
            df = pd.read_excel(file_path)
            df['Datetime'] = pd.to_datetime(df['Дата'], format='%y-%m-%d %H:%M:%S.%f')
            df.drop(columns=['Дата'], inplace=True)
            df.set_index('Datetime', inplace=True)
            df.sort_index(inplace=True)
            if df is not None:
                df = normalize_dataframe(df)
            return df
        except Exception as e:
            print(f"Ошибка при чтении Excel файла: {e}")
            return None

    # Чтение Csv-файла и преобразование в DataFrame
    def csv_to_dataframe(file_path: str = None) -> pd.DataFrame:
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

        
    # Нормализация индекса DataFrame
    def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
        if dataframe is not None:
            dataframe.index = dataframe.index.normalize()
        return dataframe


    # Построение общего графика
    def create_general_graf(dict_of_frames: dict, date_format: str = "%d-%m") -> Figure:
        fig, axes = plt.subplots(figsize=(12, 8))
        date_form = mdates.DateFormatter(date_format)

        for nameG, graf in dict_of_frames.items():
            graf.plot(ax=axes, label=nameG)

        axes.set_xlabel('Дни')
        axes.xaxis.set_major_formatter(date_form)
        axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        axes.grid()
        axes.legend()
        plt.tight_layout()

        return fig


    # Построение сезонных графиков
    def create_seasonal_graf(dict_of_frames: dict, period: int = 6) -> list[Figure]:
        rcParams['figure.figsize'] = 11, 9
        fig_list = []

        for nameG, graf in dict_of_frames.items():
            decompose = seasonal_decompose(graf, period=period)
            fig = decompose.plot()
            fig.suptitle(nameG, fontsize=25)
            fig_list.append(fig)

        return fig_list


    # Построение графика скользящего среднего
    def create_moving_average_graf(dict_of_frames: dict, window: int = 3, date_format: str = "%d-%m") -> list[Figure]:
        fig_list = []
        date_form = mdates.DateFormatter(date_format)

        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(15, 8))
            ax.xaxis.set_major_formatter(date_form)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

            ax.plot(graf, label=nameG, color='steelblue')
            ax.plot(graf.rolling(window=window).mean(), label='Скользящее среднее', color='red')

            ax.set_xlabel('Дни', fontsize=14)
            ax.set_title(nameG, fontsize=16)
            ax.legend(title='', loc='upper left', fontsize=14)

            fig.tight_layout()
            fig_list.append(fig)

        return fig_list


    # Построение графика автокорреляции
    def create_autocor_graf(dict_of_frames: dict) -> list[Figure]:
        fig_list = []

        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_acf(graf, ax=ax)
            ax.set_title(nameG, fontsize=16)
            plt.tight_layout()
            fig_list.append(fig)

        return fig_list

    # Загрузка данных из Excel
    extensions = ['.csv', '.xlsx', '.xlsm', '.xls']
    if Path(path).suffix not in extensions:
        print('Неверный формат файла')
        return None
    elif Path(path).suffix == '.csv':
        rz = csv_to_dataframe(file_path=path)
    else:
        rz = read_excel_to_dataframe(file_path=path)

    # Устанавливаем формат даты для графиков как "день-месяц"
    date_form = "%d-%m"

    # Словарь для хранения всех графиков
    allGr = {}

    # Группировка данных по результатам и создание отдельных DataFrame для каждого статуса
    for rez, group in rz.groupby('Результат'):
        rez_counts = group.groupby(pd.Grouper(freq='D')).size()

        if ':' in rez:
            rez = rez[:rez.find(':')]

        rez_df = rez_counts.to_frame(name=rez)
        allGr[rez] = rez_df

    dict_plots_kran_15 = {}
    
    for name, time_series in allGr.items():
        
        print(time_series)
        # Проверка стационарности и декомпозиция
        #stationarity_result = check_stationarity(time_series['Counts'])
        #print(stationarity_result)

        '''# Подбор параметров модели и расчет метрик
        best_order, metrics = tune_arima_with_grid_search(time_series['Counts'])

        # Обучение модели и прогнозирование
        forecast, dict_plots_kran_15[f"Анализ для {name}"] = train_and_forecast_with_metrics(time_series['Counts'], order=best_order)'''
        

    
    dict_plots_kran_15['Общий график'] = create_general_graf(allGr)
    dict_plots_kran_15['Сезонные графики'] = create_seasonal_graf(allGr)
    dict_plots_kran_15['Построение скользящего среднего'] = create_moving_average_graf(allGr)
    dict_plots_kran_15['График автокорелляции'] = create_autocor_graf(allGr)
    

    return dict_plots_kran_15
