import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from scripts.time_series_analysis import check_stationarity, decompose_time_series
from scripts.arima_tuning import tune_arima_with_grid_search
from scripts.arima_forecasting import train_and_forecast_with_metrics



def get_kran_15_rez_data(file_path: str) -> dict:
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
                required_columns_datetime = {'Дата', 'Время', 'Результат'}
                required_columns_date = {'Дата', 'Результат'}
                if not required_columns_date.issubset(dataframe.columns):
                    raise ValueError("Отсутствуют необходимые столбцы: 'Дата', 'Результат'")
                
                elif not required_columns_datetime.issubset(dataframe.columns):
                    dataframe[['Дата', 'Время']] = dataframe['Дата'].str.split(' ', expand=True)
                    cols = dataframe.columns.tolist()
                    cols[1], cols[2] = cols[2], cols[1]
                    dataframe = dataframe[cols]
                    dataframe['Дата'] = pd.to_datetime(dataframe['Дата'], format='%y-%m-%d')
                
                    
                # Приведение столбцов 'Дата' и 'Время' к строковому типу
                dataframe['Дата'] = dataframe['Дата'].astype(str)
                dataframe['Время'] = dataframe['Время'].astype(str)

                # Объединяем столбцы 'Дата' и 'Время' в один столбец 'Datetime'
                dataframe['Datetime'] = pd.to_datetime(dataframe['Дата'] + ' ' + dataframe['Время'], errors='coerce')
                
                dataframe.drop(columns=['Дата', 'Время'], inplace=True)
                dataframe.dropna(subset=['Datetime'], inplace=True)
                
                dataframe['Результат'] = dataframe['Результат'].str.split(':').str[0]
                
                # Заменяем значения в 'Результат' на числовые представления
                dataframe['SmoothedResultValue'] = dataframe['Результат'].map({
                    'S_OK': 1,
                    'SUC': 0.8,
                    'ERR': 0.5,
                    'WAR': 0.2
                }).fillna(0.1)

                # Устанавливаем 'Datetime' в качестве индекса
                dataframe.set_index('Datetime', inplace=True)
                dataframe.sort_index(inplace=True)
                
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                return None

        return dataframe

    statuses = {
        1: 'S_OK',
        0.8: 'SUC',
        0.5: 'ERR',
        0.2: 'WAR',
        0.1: 'NaN'
    }
    
    # Функция для построения общего графика
    def create_general_graf(dict_of_frames: dict) -> None:
        fig, axes = plt.subplots(figsize=(12, 8))
        for nameG, graf in dict_of_frames.items():
            graf.plot(ax=axes, label=statuses[nameG])
            
        axes.set_xlabel('Дни')
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        axes.grid()
        plt.tight_layout()
        plots['Общий график'] = fig


    # Функция для построения сезонных графиков
    def create_seasonal_graf(dict_of_frames: dict) -> None:
        rcParams['figure.figsize'] = 11, 9
        for nameG, graf in dict_of_frames.items():
            decompose = seasonal_decompose(graf, period=6)
            fig = decompose.plot()
            fig.suptitle(statuses[nameG], fontsize=25)
            fig.set_size_inches(12, 8)
            plots[f'Сезонные графики {statuses[nameG]}'] = fig
            
    # Функция для построения графика скользящего среднего
    def create_moving_average_graf(dict_of_frames: dict) -> None:
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            ax.plot(graf, label=statuses[nameG], color='steelblue')
            ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')
            ax.set_xlabel('Дни', fontsize=14)
            ax.set_title(statuses[nameG], fontsize=16)
            ax.legend(title='', loc='upper left', fontsize=14)
            fig.tight_layout()
            plots[f'Построение скользящего среднего {statuses[nameG]}'] = fig
        
    # Функция для построения графика автокорреляции
    def create_autocor_graf(dict_of_frames: dict) -> None:
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(12, 8))
            plot_acf(graf, ax=ax)
            ax.set_title(statuses[nameG], fontsize=16)
            plt.tight_layout()
            plots[f'График автокорелляции {statuses[nameG]}'] = fig
       

    # Загружаем и подготавливаем данные
    data = to_dataframe(file_path)

    # Инициализация словаря для хранения временных рядов
    allGr = {}

    # Группировка данных по уникальным значениям результата и подготовка временных рядов
    for result_type, group in data.groupby('SmoothedResultValue'):
        
        # Агрегируем данные по дням и считаем количество записей за день для каждого типа результата
        daily_counts = group.resample('D').size()

        # Добавляем в словарь `allGr` сгруппированные данные по типу результата
        allGr[result_type] = daily_counts.to_frame(name=result_type)

    
    kran_15_rez_data = dict()
    
    plots = dict()
    create_general_graf(allGr)
    create_seasonal_graf(allGr)
    create_moving_average_graf(allGr)
    create_autocor_graf(allGr)
    
    forecasts = dict()
    # Далее выполняем анализ и прогноз для каждого временного ряда
    for name, time_series in allGr.items():
        
        name_data = dict()
        # Проверка стационарности и декомпозиция
        name_data['stationarity'] = f"Анализ для {name}: {check_stationarity(time_series[name])}"
        
        # Подбор параметров модели и расчет метрик
        best_order, metrics = tune_arima_with_grid_search(time_series[name])
        name_data['parametrs'] = metrics
       
        # Обучение модели и прогнозирование
        forecast, metrics, fig = train_and_forecast_with_metrics(time_series[name], order=best_order)
        name_data['plot'] = fig
        forecasts[name] = name_data

    kran_15_rez_data['forecasts'] = forecasts
    kran_15_rez_data['plots'] = plots
    return kran_15_rez_data