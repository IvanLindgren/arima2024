# arima_tuning.py

import pandas as pd
import warnings
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from joblib import Parallel, delayed

# Подбор гиперпараметров с использованием сетки поиска
def tune_arima_with_grid_search(time_series, p_values=range(0, 4), d_values=range(0, 2), q_values=range(0, 4), seasonal_period=None):
    """
    Подбирает оптимальные параметры ARIMA через перебор по сетке параметров и оценивает модель по MSE.

    :param time_series: Временной ряд
    :param p_values: Диапазон значений p
    :param d_values: Диапазон значений d
    :param q_values: Диапазон значений q
    :param seasonal_period: Период сезонности
    :return: Словарь с лучшими параметрами и метриками
    """
    warnings.filterwarnings("ignore")
    best_score, best_order = float("inf"), None
    best_metrics = None

    def evaluate_arima_model(order):
        try:
            model = ARIMA(time_series, order=order)
            model_fit = model.fit()
            y_pred = model_fit.forecast(steps=14)  # Прогноз на 14 шагов
            mse = mean_squared_error(time_series[-14:], y_pred)
            mae = mean_absolute_error(time_series[-14:], y_pred)
            r2 = r2_score(time_series[-14:], y_pred)
            mape = mean_absolute_percentage_error(time_series[-14:], y_pred)
            return mse, mae, r2, mape, order
        except Exception as e:
            return float("inf"), None, None, None, order

    # Перебор всех комбинаций значений p, d и q
    results = Parallel(n_jobs=-1)(delayed(evaluate_arima_model)((p, d, q)) for p in p_values for d in d_values for q in q_values)

    # Поиск лучших параметров по MSE
    for mse, mae, r2, mape, order in results:
        if mse < best_score:
            best_score, best_order = mse, order
            best_metrics = {'MSE': mse, 'MAE': mae, 'R2': r2, 'MAPE': mape}

    #return f"Лучшие параметры: ARIMA{best_order} с метриками: {best_metrics}"
    return best_order, best_metrics

# Функция для расчета и отображения метрик
def display_metrics(metrics):
    print(f"\nМетрики для оптимальной модели:\nMSE: {metrics['MSE']:.4f}\nMAE: {metrics['MAE']:.4f}\nR2: {metrics['R2']:.4f}\nMAPE: {metrics['MAPE']:.4f}")

def find_best_seasonal_period(time_series, periods=[7, 14, 24, 30]):
    """
    Определяет лучший период сезонности, минимизируя AIC.
    :param time_series: Временной ряд
    :param periods: Список возможных периодов для тестирования
    :return: Лучший период сезонности
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
        except Exception as e:
            print(f"Ошибка при проверке периода {period}: {e}")
            continue
    print(f"Лучший период сезонности: {best_period} с AIC: {best_aic}")
    return best_period


# Функция для оценки модели с оптимизированными гиперпараметрами
def evaluate_arima_with_best_params(time_series, order, seasonal_order=None, forecast_steps=14, freq='D'):
    """
    Обучает модель ARIMA/SARIMA с заданными параметрами и оценивает ее на основе метрик.

    :param time_series: Pandas Series с временным индексом
    :param order: Кортеж (p, d, q) для ARIMA
    :param seasonal_order: Кортеж (P, D, Q, m) для сезонной компоненты SARIMA
    :param forecast_steps: Количество шагов для прогноза
    :param freq: Частота временного ряда
    :return: Кортеж (model_fit, predictions)
    """
    try:
        if seasonal_order:
            model = SARIMAX(time_series, order=order, seasonal_order=seasonal_order, enforce_stationarity=False,
                            enforce_invertibility=False)
        else:
            model = ARIMA(time_series, order=order)

        model_fit = model.fit()
        predictions = model_fit.forecast(steps=forecast_steps)

        # Если есть истинные значения для оценки, можно их добавить здесь
        # Например, разделение на тренировочную и тестовую выборки

        # Метрики оценки (требуют наличия истинных значений, что в данном случае не всегда применимо)
        # Здесь можно использовать только предсказанные значения без метрик, если нет тестовой выборки

        print(f"Модель обучена. Прогноз на {forecast_steps} периодов:")
        print(predictions.head())

        return model_fit, predictions
    except Exception as e:
        print(f"Ошибка при обучении модели ARIMA: {e}")
        return None, None