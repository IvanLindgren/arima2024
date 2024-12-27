import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure  
from datetime import timedelta
import warnings
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima import auto_arima
from joblib import Parallel, delayed

# Импортируем функции для чтения данных
from scripts.Kran15_rez import read_excel_to_dataframe as read_kran15_rez
from scripts.Kran15_state import read_excel_to_dataframe as read_kran15_state, count_records_by_day_auto
from scripts.Scaner import read_excel_to_dataframe as read_scaner, count_records_by_hour_auto as count_scaner
from scripts.Balka import read_excel_to_dataframe as read_balka, count_records_by_hour_auto as count_balka


def display_metrics_dict(metrics):
    """
    Форматированный вывод метрик (для отладки).
    """
    return (f"MSE: {metrics['MSE']:.4f}, "
            f"MAE: {metrics['MAE']:.4f}, "
            f"R2: {metrics['R2']:.4f}, "
            f"MAPE: {metrics['MAPE']:.4f}")


def evaluate_arima_model(time_series, order, forecast_steps=14):
    """
    Обучает ARIMA модель с заданным order и выполняет прогноз на forecast_steps шагов.
    Возвращает предсказания и метрики, если есть достаточная история для сравнения.
    Если длина ряда меньше 2*forecast_steps, метрики могут быть неточными.
    """
    try:
        model = ARIMA(time_series, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)

        # Рассчёт метрик по последним forecast_steps точкам ряда, если они доступны
        if len(time_series) >= forecast_steps:
            actual = time_series[-forecast_steps:]
            metrics = {
                'MSE': mean_squared_error(actual, forecast),
                'MAE': mean_absolute_error(actual, forecast),
                'R2': r2_score(actual, forecast),
                'MAPE': mean_absolute_percentage_error(actual, forecast)
            }
        else:
            metrics = None

        #print(model_fit, forecast, metrics)
        return model_fit, forecast, metrics
        
    except Exception as e:
        #print(f"Ошибка при обучении и прогнозировании: {e}")
        return None, None, None


def tune_arima_with_grid_search(time_series, p_values=range(0, 4), d_values=range(0, 2), q_values=range(0, 4)):
    """
    Подбирает оптимальные параметры ARIMA через перебор по сетке параметров и оценивает модели по MSE.
    Возвращает лучшие параметры и метрики.
    """
    warnings.filterwarnings("ignore")
    best_score, best_order = float("inf"), None
    best_metrics = None

    def evaluate_single_order(order):
        """
        Вспомогательная функция для оценки одной конфигурации order.
        Прогнозируем на 14 дней вперед и считаем метрики по последним 14 данным.
        """
        try:
            model = ARIMA(time_series, order=order)
            model_fit = model.fit()
            y_pred = model_fit.forecast(steps=14)
            if len(time_series) >= 14:
                actual = time_series[-14:]
                mse = mean_squared_error(actual, y_pred)
                mae = mean_absolute_error(actual, y_pred)
                r2_val = r2_score(actual, y_pred)
                mape = mean_absolute_percentage_error(actual, y_pred)
            else:
                # Если не хватает данных для оценки, ставим метрики в inf
                mse, mae, r2_val, mape = float("inf"), None, None, None
            return mse, mae, r2_val, mape, order
        except Exception:
            return float("inf"), None, None, None, order

    # Параллельный перебор всех комбинаций
    results = Parallel(n_jobs=-1)(delayed(evaluate_single_order)((p, d, q)) 
                                   for p in p_values for d in d_values for q in q_values)

    # Находим лучшие параметры по минимальному MSE
    for mse, mae, r2_val, mape, order in results:
        if mse < best_score:
            best_score, best_order = mse, order
            best_metrics = {'MSE': mse, 'MAE': mae, 'R2': r2_val, 'MAPE': mape}

    return best_order, best_metrics


def find_best_seasonal_period(time_series, periods=[7, 14, 24, 30]):
    """
    Определяет лучший период сезонности, минимизируя AIC.
    """
    best_period = None
    best_aic = float("inf")
    for period in periods:
        try:
            model = ARIMA(time_series, seasonal_order=(1, 1, 1, period))
            model_fit = model.fit()
            if model_fit.aic < best_aic:
                best_aic = model_fit.aic
                best_period = period
        except Exception:
            continue
    return best_period


def evaluate_arima_with_best_params(time_series, order, seasonal_order=None, forecast_steps=14, freq='D'):
    """
    Обучает модель ARIMA/SARIMA с заданными параметрами и оценивает ее.
    Возвращает model_fit и предсказания.
    """
    try:
        if seasonal_order:
            model = SARIMAX(time_series, order=order, seasonal_order=seasonal_order,
                            enforce_stationarity=False, enforce_invertibility=False)
        else:
            model = ARIMA(time_series, order=order)

        model_fit = model.fit()
        predictions = model_fit.forecast(steps=forecast_steps)
        return model_fit, predictions
    except Exception as e:
        #print(f"Ошибка при обучении модели ARIMA: {e}")
        return None, None


def check_stationarity(time_series, significance_level=0.05):
    """
    Выполняет ADF и KPSS тесты на стационарность. Возвращает словарь с результатами.
    """
    result = {}
    try:
        adf_test = adfuller(time_series.dropna())
        result['ADF'] = {
            'Test Statistic': adf_test[0],
            'p-value': adf_test[1],
            'Critical Values': adf_test[4],
            'Stationary': adf_test[1] < significance_level
        }
    except Exception as e:
        result['ADF'] = {'error': str(e)}

    try:
        kpss_test = kpss(time_series.dropna(), regression='c', nlags="auto")
        result['KPSS'] = {
            'Test Statistic': kpss_test[0],
            'p-value': kpss_test[1],
            'Critical Values': kpss_test[3],
            'Stationary': kpss_test[1] > significance_level
        }
    except Exception as e:
        result['KPSS'] = {'error': str(e)}

    return result


def decompose_time_series(time_series, period=24):
    """
    Декомпозиция временного ряда. Возвращает пути к сохраненным графикам и данные декомпозиции.
    """
    try:
        decomposition = seasonal_decompose(time_series, model='additive', period=period)
        fig, axes = plt.subplots(4, 1, figsize=(12, 8))

        axes[0].plot(time_series, label='Исходный ряд')
        axes[0].legend(loc='upper left')
        axes[0].set_title('Исходный ряд')

        axes[1].plot(decomposition.trend, label='Тренд', color='orange')
        axes[1].legend(loc='upper left')
        axes[1].set_title('Тренд')

        axes[2].plot(decomposition.seasonal, label='Сезонность', color='green')
        axes[2].legend(loc='upper left')
        axes[2].set_title('Сезонность')

        axes[3].plot(decomposition.resid, label='Остаток', color='red')
        axes[3].legend(loc='upper left')
        axes[3].set_title('Остаток')

        plt.tight_layout()

        # Возвращаем сами ряды (trend, seasonal, resid) и путь к графику
        return {
            'trend': [round(i, 2) for i in decomposition.trend.dropna().tolist()],
            'seasonal': [round(i, 2) for i in decomposition.seasonal.dropna().tolist()],
            'resid': [round(i, 2) for i in decomposition.resid.dropna().tolist()],
            'plot': fig
        }
    except Exception as e:
        return {'error': str(e)}


def plot_acf_pacf(time_series, lags=31):
    """
    Строит графики ACF и PACF, возвращает путь к сохраненному файлу.
    """
    try:
        fig, axes = plt.subplots(1, 2, figsize=(12, 8))

        plot_acf(time_series, ax=axes[0], lags=lags)
        axes[0].set_title('ACF')

        plot_pacf(time_series, ax=axes[1], lags=lags, method='ywm')
        axes[1].set_title('PACF')

        plt.tight_layout()
        
        return fig
    except Exception as e:
        return {'error': str(e)}


def comparative_analysis(time_series, order, forecast_period=14):
    """
    Сравнительный анализ на основе данных за 1 месяц и 2 месяца.
    Возвращает метрики и прогнозы в словарях.
    """
    try:
        # 1 месяц (~30 дней)
        one_month_data = time_series[-30:]
        _, forecast_one_month, metrics_one_month = evaluate_arima_model(one_month_data, order, forecast_steps=forecast_period)

        # 2 месяца (~60 дней)
        two_month_data = time_series[-60:]
        _, forecast_two_months, metrics_two_months = evaluate_arima_model(two_month_data, order, forecast_steps=forecast_period)

        return {
            'one_month': {
                'data_length': len(one_month_data),
                'forecast': forecast_one_month.tolist() if forecast_one_month is not None else None,
                'metrics': metrics_one_month
            },
            'two_months': {
                'data_length': len(two_month_data),
                'forecast': forecast_two_months.tolist() if forecast_two_months is not None else None,
                'metrics': metrics_two_months
            }
        }
    except Exception as e:
        return {'error': str(e)}


def arima_forecast_and_plot(data_source, column_name, paths, custom_order: None, forecast_period=5):
    """
    Основная функция для прогнозирования и формирования итогового результата в JSON-совместимом формате.

    Args:
        data_source (str): Источник данных ('Кран Rez', 'Кран State', 'Сканер', 'Балка').
        column_name (str): Название столбца для прогнозирования.
        paths (list[str]): Пути к файлам для чтения данных.
        forecast_period (int): Период прогнозирования (в днях).

    Returns:
        dict: Словарь с результатами:
              {
                "data_source": ...,
                "column_name": ...,
                "forecast_period": ...,
                "forecast_values": ...,
                "forecast_index": ...,
                "last_date": ...,
                "actual_values": ...,
                "actual_index": ...,
                "plot_path": ...,
                "metrics": ...,
                "stationarity_tests": ...,
                "decomposition": ...,
                "acf_pacf_plot": ...
              }
    """

    # Чтение данных в зависимости от источника
    if data_source == 'Кран Rez':
        df = read_kran15_rez(file_paths=paths) 
        if df is not None:
            time_series = df[df['Результат'].str.startswith(column_name)]
            time_series = time_series.groupby(pd.Grouper(freq='D')).size()
        else:
            return {"error": "Данные kran_15_rez не прочитаны"}

    elif data_source == 'Кран State':
        df = read_kran15_state(file_paths=paths)
        if df is not None:
            day_counts = count_records_by_day_auto(df)
            print(day_counts.columns)
            if column_name in day_counts.columns:
                time_series = day_counts[column_name]
            else:
                return {"error": "Указанный столбец не найден в данных kran_15_state"}
        else:
            return {"error": "Данные kran_15_state не прочитаны"}

    elif data_source == 'Сканер':
        df = read_scaner(file_paths=paths)
        if df is not None:
            hour_counts = count_scaner(df)
            if column_name in hour_counts.columns:
                time_series = hour_counts[column_name]
            else:
                return {"error": "Указанный столбец не найден в данных Scaner"}
        else:
            return {"error": "Данные Scaner не прочитаны"}

    elif data_source == 'Балка':
        df = read_balka(file_paths=paths)
        if df is not None:
            hour_counts = count_balka(df)
            if column_name in hour_counts.columns:
                time_series = hour_counts[column_name]
            else:
                return {"error": "Указанный столбец не найден в данных Balka"}
        else:
            return {"error": "Данные Balka не прочитаны"}

    else:
        return {"error": "Неверный источник данных"}

    if time_series is None or time_series.empty:
        return {"error": "Данные не найдены или некорректный столбец"}

    # Станционарность
    stationarity_tests = check_stationarity(time_series)

    # Декомпозиция
    decomposition_results = decompose_time_series(time_series)

    # ACF/PACF
    acf_pacf_plot_path = plot_acf_pacf(time_series)

    # Делим данные на обучающую выборку
    train_data = time_series[:-forecast_period]
    if len(train_data) < forecast_period:
        return {"error": "Недостаточно данных для обучения и прогноза"}

    # Подбор параметров ARIMA
    best_order, best_metrics = tune_arima_with_grid_search(train_data)
    if custom_order is not None:
        best_order = custom_order
    # Прогноз
    model_fit, forecast = evaluate_arima_with_best_params(train_data, order=best_order, forecast_steps=forecast_period)

    if forecast is None:
        return {"error": "Не удалось выполнить прогноз"}

    # Подготовим график прогноза
    fig, ax = plt.subplots(figsize=(12, 8))
    # Показываем последние 3*forecast_period точек (исходных данных) + прогноз
    context_points = forecast_period * 3 if len(time_series) >= forecast_period * 3 else len(time_series)
    ax.plot(time_series[-context_points:], label='Реальные данные')
    last_date = time_series.index[-forecast_period - 1] if (len(time_series) > forecast_period) else time_series.index[-1]

    forecast_index = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_period, freq='D')
    ax.plot(forecast_index, forecast, label='Прогноз', color='red')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Значение')
    ax.set_title(f'Прогноз {column_name} на {forecast_period} дней')
    ax.legend()
    ax.grid()

    # Формируем итоговый словарь
    results = {
        "data_source": data_source,
        "column_name": column_name,
        "forecast_period": forecast_period,
        "forecast_values": forecast.tolist(),
        "forecast_index": [date.strftime('%Y-%m-%d') for date in forecast_index],
        "last_date": last_date.strftime('%Y-%m-%d') if hasattr(last_date, 'strftime') else str(last_date),
        "actual_values": time_series[-context_points:].tolist(),
        "actual_index": [date.strftime('%Y-%m-%d') for date in time_series[-context_points:].index],
        "plot": fig,
        "metrics": best_metrics,
        "stationarity_tests": stationarity_tests,
        "decomposition": decomposition_results,
        "acf_pacf_plot": acf_pacf_plot_path
    }

    return results


