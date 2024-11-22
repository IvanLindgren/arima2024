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



# Словарь для хранения всех графиков
allGr = {}

id_df = read_excel_to_dataframe(file_path='Кран/State/id.xlsx')
to_df= read_excel_to_dataframe(file_path='Кран/State/to.xlsx')
from_df = read_excel_to_dataframe(file_path='Кран/State/from.xlsx')

state_df = read_excel_to_dataframe(file_path='Кран/State/state.xlsx')


# Устанавливаем формат даты для графиков как "день-месяц"
date_form = mdates.DateFormatter("%d-%m")

# Группировка данных по результатам и создание отдельных DataFrame для каждого статуса
for rez, group in state_df.groupby('Статус'):
    # Группируем данные по дням и считаем количество записей
    rez_counts = group.groupby(pd.Grouper(freq='D')).size()

    # Убираем двоеточие в конце, если оно есть
    if rez == 'Сообщение':
        continue

    # Создаем DataFrame из результатов и сохраняем его в словарь
    rez_df = rez_counts.to_frame(name=rez)
    # allGr[rez] = to_dataframe(dataframe=rez_df)
    allGr[rez] = rez_df

allGr['ID'] = count_records_by_day_auto(id_df)
allGr['TO'] = count_records_by_day_auto(to_df)
allGr['FROM'] = count_records_by_day_auto(from_df)




