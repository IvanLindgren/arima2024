import pandas as pd  # Для работы с DataFrame
import matplotlib.pyplot as plt  # Для визуализации данных
import matplotlib.dates as mdates  # Форматирование и работа с датами на графиках
from statsmodels.graphics.tsaplots import plot_acf  # График автокорреляции
from statsmodels.tsa.seasonal import seasonal_decompose  # Декомпозиция временных рядов
from matplotlib.figure import Figure
from pylab import rcParams  # Параметры графиков


# Чтение Excel-файла и преобразование в DataFrame
def read_excel_to_dataframe(file_path: str) -> pd.DataFrame:
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


# Нормализация индекса DataFrame
def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe is not None:
        dataframe.index = dataframe.index.normalize()
    return dataframe

def plots_kran_15_rez(path: str):
    
    # Построение общего графика
    def create_general_graf(dict_of_frames: dict, date_format: str = "%d-%m",
                            interval: int = 1) -> Figure:
        fig, axes = plt.subplots(figsize=(12, 8))
        date_form = mdates.DateFormatter(date_format)

        for nameG, graf in dict_of_frames.items():
            graf = graf.iloc[::interval]
            graf.plot(ax=axes, label=nameG)

        axes.set_xlabel('Дни')
        axes.xaxis.set_major_formatter(date_form)
        axes.xaxis.set_major_locator(mdates.DayLocator(interval=2*interval))
        axes.grid()
        axes.legend()
        plt.tight_layout()
        plots['Общий график'] = fig
        return fig


    # Построение сезонных графиков
    def create_seasonal_graf(dict_of_frames: dict, period: int = 6,
                            interval: int = 1) -> list[Figure]:
        rcParams['figure.figsize'] = 12, 8
        fig_list = []

        for nameG, graf in dict_of_frames.items():
            graf = graf.iloc[::interval]
            decompose = seasonal_decompose(graf, period=period)
            fig = decompose.plot()
            fig.suptitle(nameG, fontsize=25)
            plots[f'Сезонные графики {nameG}'] = fig
            fig_list.append(fig)

        return fig_list


    # Построение графика скользящего среднего
    def create_moving_average_graf(dict_of_frames: dict, window: int = 3,
                                date_format: str = "%d-%m", interval: int = 1) -> list[Figure]:
        fig_list = []
        date_form = mdates.DateFormatter(date_format)

        for nameG, graf in dict_of_frames.items():
            graf = graf.iloc[::interval]
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.xaxis.set_major_formatter(date_form)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2*interval))

            ax.plot(graf, label=nameG, color='steelblue')
            ax.plot(graf.rolling(window=window).mean(), label='Скользящее среднее', color='red')

            ax.set_xlabel('Дни', fontsize=14)
            ax.set_title(nameG, fontsize=16)
            ax.legend(title='', loc='upper left', fontsize=14)

            fig.tight_layout()
            plots[f'Построение скользящего среднего {nameG}'] = fig
            fig_list.append(fig)

        return fig_list


    # Построение графика автокорреляции
    def create_autocor_graf(dict_of_frames: dict, interval: int = 1) -> list[Figure]:
        fig_list = []

        for nameG, graf in dict_of_frames.items():
            graf = graf.iloc[::interval]
            fig, ax = plt.subplots(figsize=(12, 8))
            plot_acf(graf, ax=ax)
            ax.set_title(nameG, fontsize=16)
            plt.tight_layout()
            plots[f'График автокорелляции {nameG}'] = fig
            fig_list.append(fig)

        return fig_list



    
    # Загрузка данных из Excel
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

    data = dict()
    values = list(allGr.keys())
    plots = dict()
    create_general_graf(allGr)
    create_seasonal_graf(allGr)
    create_moving_average_graf(allGr)
    create_autocor_graf(allGr)

    data['plots'] = plots
    data['values'] = values

    return data



