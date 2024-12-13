import pandas as pd  # Для работы с DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from typing import Union, List

'''def read_excel_to_dataframe(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        df['Datetime'] = pd.to_datetime(df['Дата'], format='%y-%m-%d %H:%M:%S.%f')
        df.drop(columns=['Дата'], inplace=True)
        df.set_index('Datetime', inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return None'''

def read_excel_to_dataframe(file_paths: Union[str, List[str]]) -> pd.DataFrame:
    try:
        # Если путь один, преобразуем его в список
        if isinstance(file_paths, str):
            file_paths = [file_paths]
            
        dfs = []
        for file_path in file_paths:
            df = pd.read_excel(file_path)
            df['Datetime'] = pd.to_datetime(df['Дата'], format='%y-%m-%d %H:%M:%S.%f')
            df.drop(columns=['Дата'], inplace=True)
            df.set_index('Datetime', inplace=True)
            df.sort_index(inplace=True)
            dfs.append(df)
        
        # Объединяем все считанные DataFrame в один
        combined_df = pd.concat(dfs, sort=True)
        combined_df.sort_index(inplace=True)
        
        return combined_df
    except Exception as e:
        print(f"Ошибка при чтении Excel файла(ов): {e}")
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




def get_data_scaner(paths: Union[str, List[str]]):

    def create_general_graf(df: pd.DataFrame, name: str, date_format: str = "%d-%m", interval: int = 1) -> Figure:
        df = df.iloc[::interval]

        ax = df.plot(figsize=(12, 8))
        
        ax.set_xlabel('Дата')  # Подпись оси X
        ax.set_ylabel('Количество записей')  # Подпись оси Y
        ax.set_title('Количество записей в зависимости от даты')  # Заголовок графика
        ax.set_xticks(df.index)
        ax.set_xticklabels([date.strftime('%m-%d: %H') for date in df.index], rotation=45)

        plt.tight_layout()

        plots[f'Общий график {name}'] = plt.gcf()
        return plt.gcf()

    allGr = {}

    id_df = read_excel_to_dataframe([paths[i] for i in range(len(paths)) if i % 2 == 0])
    to_df = read_excel_to_dataframe([paths[i] for i in range(len(paths)) if i % 2 == 1])


    allGr['ID'] = count_records_by_hour_auto(id_df)
    allGr['Куда'] = count_records_by_hour_auto(to_df)

    data = dict()
    values = list(allGr.keys())
    plots = dict()

    create_general_graf(allGr['ID'], name='ID')
    create_general_graf(allGr['Куда'], name='Куда')
    

    data['plots'] = plots
    data['values'] = values

    return data