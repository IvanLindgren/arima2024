import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import matplotlib.dates as mdates
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


def adf_test(series, significance_level=0.05):
    """
    Тест Дики-Фуллера для проверки стационарности временного ряда.
    """
    adf_result = adfuller(series.dropna())
    is_stationary = adf_result[1] < significance_level
    return {
        "ADF Statistic": adf_result[0],
        "p-value": adf_result[1],
        "Critical Values": adf_result[4],
        "Stationary": is_stationary,
    }

def difference(series, order=1):
    """
    Применение дифференцирования к временному ряду.
    """
    return series.diff(order).dropna()

def get_kran_15_state_data(file_pathes: list[str]) -> dict:
    def to_dataframe(file_path: str) -> pd.DataFrame:
        try:
            if file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            else:
                raise ValueError("Поддерживаются только файлы с расширением .xlsx, .xls и .csv")
            df['Datetime'] = pd.to_datetime(df['Дата'], errors='coerce')
            #df['Datetime'] = pd.to_datetime(df['Дата'], format='%y-%m-%d %H:%M:%S.%f')
            df.drop(columns=['Дата'], inplace=True)
            df.set_index('Datetime', inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def count_records_by_day_auto(df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame()
        daily_counts = df.groupby(pd.Grouper(freq='D')).size()
        counts_df = daily_counts.to_frame(name='Count')
        return counts_df

    # Загрузка данных
    allGr = {}
    id_df = to_dataframe(file_pathes[1])
    to_df = to_dataframe(file_pathes[2])
    from_df = to_dataframe(file_pathes[3])
    state_df = to_dataframe(file_pathes[0])

    # Агрегирование данных для ID, TO и FROM
    allGr['ID'] = count_records_by_day_auto(id_df)
    allGr['TO'] = count_records_by_day_auto(to_df)
    allGr['FROM'] = count_records_by_day_auto(from_df)

    # Обработка данных по столбцу 'Статус'
    status_groups = {}
    for rez, group in state_df.groupby('Статус'):
        if rez == 'Сообщение':
            continue
        rez_counts = group.groupby(pd.Grouper(freq='D')).size()
        rez_df = rez_counts.to_frame(name='Count')
        status_groups[rez] = rez_df

    # Теперь сосредоточимся только на прогнозировании по 'Статус'
    kran_15_state_data = dict()
    forecasts = dict()

    # Обработка каждого временного ряда по 'Статус'
    for name, time_series in status_groups.items():
        name_data = dict()
        series_data = time_series['Count']

        # Проверка стационарности
        adf_result = adf_test(series_data)
        name_data['stationarity'] = adf_result
        print(f"\nТест Дики-Фуллера для {name}:")
        print(f"ADF Statistic: {adf_result['ADF Statistic']}")
        print(f"p-value: {adf_result['p-value']}")
        print(f"Critical Values: {adf_result['Critical Values']}")
        print(f"Стационарен: {adf_result['Stationary']}")

        # Если ряд нестационарен, применяем дифференцирование
        if not adf_result['Stationary']:
            series_data_diff = difference(series_data)
            print(f"Применено дифференцирование для {name}")
            d = 1
        else:
            series_data_diff = series_data
            d = 0

        # Построение графиков ACF и PACF
        fig, axes = plt.subplots(1, 2, figsize=(16, 4))
        plot_acf(series_data_diff, ax=axes[0], lags=20)
        plot_pacf(series_data_diff, ax=axes[1], lags=20, method='ywm')
        axes[0].set_title(f"ACF для {name}")
        axes[1].set_title(f"PACF для {name}")
        plt.show()

        # Ввод параметров ARIMA от пользователя
        print(f"Введите параметры ARIMA для временного ряда '{name}':")
        p = int(input("Введите порядок AR (p): "))
        q = int(input("Введите порядок MA (q): "))
        best_order = (p, d, q)
        name_data['best_order'] = best_order

        # Обучение модели и прогнозирование
        try:
            model = ARIMA(series_data, order=best_order)
            model_fit = model.fit()
            forecast_steps = 7  # Прогноз на 7 дней
            forecast = model_fit.forecast(steps=forecast_steps)
            name_data['forecast'] = forecast

            # Построение графика прогноза
            forecast_index = pd.date_range(start=series_data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
            forecast_series = pd.Series(forecast, index=forecast_index)

            # Объединяем данные для графика
            combined_series = pd.concat([series_data, forecast_series])

            plt.figure(figsize=(12, 6))
            plt.plot(combined_series.index, combined_series.values, label='Исторические данные и прогноз')
            plt.axvline(x=series_data.index[-1], color='red', linestyle='--', label='Начало прогноза')
            plt.title(f"Прогноз для {name}")
            plt.xlabel("Дата")
            plt.ylabel("Количество")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

            name_data['model'] = model_fit

        except Exception as e:
            print(f"Ошибка при обучении модели для {name}: {e}")
            name_data['error'] = str(e)

        forecasts[name] = name_data

    kran_15_state_data['forecasts'] = forecasts

    # Если нужно, можно сохранить или вывести результаты обработки по другим столбцам (ID, TO, FROM)
    # Например, построить графики без прогнозирования
    plots = dict()

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
        plt.show()

    # Построение графиков для ID, TO, FROM
    create_general_graf(allGr)

    kran_15_state_data['plots'] = plots
    return kran_15_state_data

# Путь к файлам
pathes = [
    'C:/Users/user/Documents/test/LPC_Kran15_Data_State_Month.xlsx',
    'C:/Users/user/Documents/test/LPC_Kran15_Data_ID_Month.xlsx',
    'C:/Users/user/Documents/test/LPC_Kran15_Data_To_Month.xlsx',
    'C:/Users/user/Documents/test/LPC_Kran15_Data_From_Month.xlsx'
]

# Запуск обработки
kran_15_state_data = get_kran_15_state_data(pathes)