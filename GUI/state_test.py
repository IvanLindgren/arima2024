import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from scripts.arima_tuning import tune_arima_with_grid_search
from scripts.arima_forecasting import train_and_forecast_with_metrics


def adf_test(series, significance_level=0.05):
    """
    Тест Дики-Фуллера для проверки стационарности временного ряда.
    """
    from statsmodels.tsa.stattools import adfuller

    adf_result = adfuller(series.dropna())
    is_stationary = adf_result[1] < significance_level
    return {
        "ADF Statistic": adf_result[0],
        "p-value": adf_result[1],
        "Critical Values": adf_result[4],
        "Stationary": is_stationary,
    }


def get_kran_15_state_data(file_pathes: list[str]) -> dict:
    def to_dataframe(file_path: str) -> pd.DataFrame:
        try:
            if file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            else:
                raise ValueError("Поддерживаются только файлы с расширением .xlsx, .xls и .csv")
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

    # Нормализация индекса DataFrame
    def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
        if dataframe is not None:
            dataframe.index = dataframe.index.normalize()
        return dataframe

    def count_records_by_day_auto(df: pd.DataFrame) -> pd.DataFrame:
        # Получаем имя первого столбца
        column_name = df.columns[0]

        # Фильтруем строки, где значение в первом столбце не равно NaN
        filtered_df = df.dropna(subset=[column_name])

        # Группируем данные по дням и считаем количество записей
        daily_counts = filtered_df.groupby(pd.Grouper(freq='D')).size()

        # Преобразуем результат в DataFrame
        counts_df = daily_counts.to_frame(name=column_name)

        return counts_df

    # Функция для построения общего графика
    def create_general_graf(dict_of_frames: dict) -> None:
        fig, axes = plt.subplots(figsize=(12, 8))
        for nameG, graf in dict_of_frames.items():
            graf.plot(ax=axes, label=nameG)
        axes.set_xlabel('Дни')
        axes.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        axes.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        axes.grid()
        axes.legend(loc='upper left')
        plt.tight_layout()
        plots['Общий график'] = fig

    # Функция для построения сезонных графиков
    def create_seasonal_graf(dict_of_frames: dict) -> None:
        rcParams['figure.figsize'] = 11, 9
        for nameG, graf in dict_of_frames.items():
            decompose = seasonal_decompose(graf, period=6)
            fig = decompose.plot()
            fig.suptitle(nameG, fontsize=25)
            fig.set_size_inches(12, 8)
            plots[f'Сезонные графики {nameG}'] = fig

    # Функция для построения графика скользящего среднего
    def create_moving_average_graf(dict_of_frames: dict) -> None:
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            ax.plot(graf, label=nameG, color='steelblue')
            ax.plot(graf.rolling(window=3).mean(), label='Скользящее среднее', color='red')
            ax.set_xlabel('Дни', fontsize=14)
            ax.set_title(nameG, fontsize=16)
            ax.legend(title='', loc='upper left', fontsize=14)
            fig.tight_layout()
            plots[f'Построение скользящего среднего {nameG}'] = fig

    # Функция для построения графика автокорреляции
    def create_autocor_graf(dict_of_frames: dict) -> None:
        for nameG, graf in dict_of_frames.items():
            fig, ax = plt.subplots(figsize=(12, 8))
            plot_acf(graf, ax=ax)
            ax.set_title(nameG, fontsize=16)
            plt.tight_layout()
            plots[f'График автокорреляции {nameG}'] = fig

    # Загружаем и подготавливаем данные
    allGr = {}
    id_df = to_dataframe(file_pathes[1])
    to_df = to_dataframe(file_pathes[2])
    from_df = to_dataframe(file_pathes[3])
    state_df = to_dataframe(file_pathes[0])

    # Инициализация словаря для хранения временных рядов
    allGr['ID'] = count_records_by_day_auto(id_df)
    allGr['TO'] = count_records_by_day_auto(to_df)
    allGr['FROM'] = count_records_by_day_auto(from_df)

    for rez, group in state_df.groupby('Статус'):
        # Группируем данные по дням и считаем количество записей
        rez_counts = group.groupby(pd.Grouper(freq='D')).size()

        # Пропускаем, если статус — 'Сообщение'
        if rez == 'Сообщение':
            continue

        # Создаем DataFrame из результатов и сохраняем его в словарь
        rez_df = rez_counts.to_frame(name=rez)
        allGr[rez] = rez_df

    kran_15_state_data = dict()
    plots = dict()
    forecasts = dict()

    # Построение графиков (если требуется)
    # create_general_graf(allGr)
    # create_seasonal_graf(allGr)
    # create_moving_average_graf(allGr)
    # create_autocor_graf(allGr)

    # Далее выполняем анализ и прогноз для каждого временного ряда
    for name, time_series in allGr.items():
        name_data = dict()
        # Используем правильное название столбца
        count_column = time_series.columns[0]
        series_data = time_series[count_column]

        # Проверка стационарности
        adf_result = adf_test(series_data)
        name_data['stationarity'] = adf_result
        print(f"\nТест Дики-Фуллера для {name}: {adf_result}")

        # Подбор параметров модели и расчет метрик
        best_order, metrics = tune_arima_with_grid_search(series_data)
        name_data['parametrs'] = metrics
        print(f"Лучшие параметры ARIMA для {name}: {best_order}")

        # Обучение модели и прогнозирование
        forecast, forecast_metrics, fig = train_and_forecast_with_metrics(series_data, order=best_order)
        name_data['forecast'] = forecast
        name_data['forecast_metrics'] = forecast_metrics
        name_data['model'] = None  # Если модель возвращается, можно сохранить ее здесь
        name_data['plot'] = fig  # График прогноза
        forecasts[name] = name_data

    kran_15_state_data['forecasts'] = forecasts
    kran_15_state_data['plots'] = plots
    return kran_15_state_data


# Путь к файлам
paths = [
    r'C:\Users\denis\Downloads\Telegram Desktop\LPC_Kran15_Data_State_Month.xlsx',
    r'C:\Users\denis\Downloads\Telegram Desktop\LPC_Kran15_Data_ID_Month.xlsx',
    r'C:\Users\denis\Downloads\Telegram Desktop\LPC_Kran15_Data_To_Month.xlsx',
    r'C:\Users\denis\Downloads\Telegram Desktop\LPC_Kran15_Data_From_Month.xlsx'
]


# Запуск обработки
kran_15_state_data = get_kran_15_state_data(paths)
