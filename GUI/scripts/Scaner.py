import pandas as pd  # Для работы с DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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

def create_general_graf(df: pd.DataFrame, interval: int = 1) -> Figure:
    df = df.iloc[::interval]

    ax = df.plot(figsize=(12, 6))

    ax.set_xlabel('Дата')  # Подпись оси X
    ax.set_ylabel('Количество записей')  # Подпись оси Y
    ax.set_title('Количество записей в зависимости от даты')  # Заголовок графика

    ax.set_xticks(df.index)
    ax.set_xticklabels([date.strftime('%m-%d: %H') for date in df.index], rotation=45)

    plt.tight_layout()

    return plt.gcf()


'''allGr = {}

id_df = read_excel_to_dataframe('LPC_Scaner_Data_ID.xlsx')
to_df = read_excel_to_dataframe('LPC_Scaner_Data_To.xlsx')


allGr['ID'] = count_records_by_hour_auto(id_df)
allGr['TO'] = count_records_by_hour_auto(to_df)'''