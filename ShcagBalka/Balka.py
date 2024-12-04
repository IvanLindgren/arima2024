import pandas as pd  # Для работы с DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def read_excel_to_dataframe(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        df['Datetime'] = pd.to_datetime(df['Дата'], format='%y-%m-%d %H:%M:%S.%f')
        df.drop(columns=['Дата'], inplace=True)
        df.set_index('Datetime', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return None


def count_records_by_hour_auto(df: pd.DataFrame) -> pd.DataFrame:

    # Получаем имя первого столбца
    column_name = df.columns[0]

    # Фильтруем строки, где значение в первом столбце не равно NaN
    filtered_df = df.dropna(subset=[column_name])

    # Группируем данные по дням и считаем количество записей
    daily_counts = filtered_df.groupby(pd.Grouper(freq='h')).size()

    # Преобразуем результат в DataFrame
    counts_df = daily_counts.to_frame(name=column_name)

    return counts_df

def create_mov_avg_and_stand_dev_graf(df: pd.DataFrame, interval: int = 1) -> Figure:
    df = df.iloc[::interval]

    rolling_mean = df.rolling(window=8).mean()  # создаем скользящее среднее с окном 8
    rolling_std = df.rolling(window=8).std()  # создаем скользящее стандартное отклонение с окном 8

    fig, ax = plt.subplots(figsize=(18, 6))  # задаем размер графика
    ax.set_title('График временного ряда с скользящим средним и стандартным отклонением',
                 fontdict={'fontsize': 20, 'fontweight': 'bold'})  # подписываем график и задаем шрифт
    ax.set_xlabel('Месяца', fontsize=12)  # подписываем ось X
    ax.set_ylabel('Число продаж', fontsize=12)  # подписываем ось Y

    # Для каждого графика явным образом указываем данные для оси X и Y
    ax.plot(df.index, df.values, label='Исходные данные')  # строим график по исходным данным
    ax.plot(rolling_mean.index, rolling_mean.values, label='Скользящее среднее')  # строим график скользящего среднего
    ax.plot(rolling_std.index, rolling_std.values, label='Стандартное отклонение')  # строим график скользящего стандартного отклонения

    plt.legend()  # добавляем легенду на график

    return fig


def create_graf_for_p(df: pd.DataFrame, interval: int = 1) -> Figure:
    df = df.iloc[::interval]  # выборка данных с шагом interval

    # Создаем объект Figure и Axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Строим ACF на заданной оси
    plot_acf(df, ax=ax)  # создаем график ACF на оси ax

    plt.axis('tight')  # задаем параметры необходимые для вывода

    # Возвращаем объект Figure
    return fig

def create_graf_for_q(df: pd.DataFrame, interval: int = 1) -> Figure:
    df = df.iloc[::interval]  # выборка данных с шагом interval

    # Создаем объект Figure и Axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Строим ACF на заданной оси
    plot_pacf(df, ax=ax, method='ywm')  # создаем график ACF на оси ax

    plt.axis('tight')  # задаем параметры необходимые для вывода

    # Возвращаем объект Figure
    return fig


allGr = {}

from_df = read_excel_to_dataframe('LPC_Step_B_Data_From.xlsx')
id_df = read_excel_to_dataframe('LPC_Step_B_Data_ID.xlsx')
to_df = read_excel_to_dataframe('LPC_Step_B_Data_To.xlsx')

allGr['FROM'] = count_records_by_hour_auto(from_df)
allGr['ID'] = count_records_by_hour_auto(id_df)
allGr['TO'] = count_records_by_hour_auto(to_df)



