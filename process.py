import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from radar_diagram import RadarDiagram
import functions as functions
import streamlit as st
import gc

dict_of_function_expressions = dict()
free_members_of_fun_expr = []
data_sol = []


def init():
    """Инициализация функций"""
    dict_of_function_expressions[1] = function_0
    dict_of_function_expressions[2] = function_1
    dict_of_function_expressions[3] = function_2
    dict_of_function_expressions[4] = function_3
    dict_of_function_expressions[5] = function_4
    dict_of_function_expressions[6] = function_5
    dict_of_function_expressions[7] = function_6


def init_default_functions():
    """Инициализация функций по умолчанию"""
    global dict_of_function_expressions
    dict_of_function_expressions.clear()
    dict_of_function_expressions[1] = function_0
    dict_of_function_expressions[2] = function_1  
    dict_of_function_expressions[3] = function_2
    dict_of_function_expressions[4] = function_3
    dict_of_function_expressions[5] = function_4
    dict_of_function_expressions[6] = function_5
    dict_of_function_expressions[7] = function_6


def activatedCombox(index, text):
    try:
        func_num = int(text)
        if index == 0:
            dict_of_function_expressions[func_num] = function_0
        elif index == 1:
            dict_of_function_expressions[func_num] = function_1
        elif index == 2:
            dict_of_function_expressions[func_num] = function_2
        elif index == 3:
            dict_of_function_expressions[func_num] = function_3
        elif index == 4:
            dict_of_function_expressions[func_num] = function_4
        elif index == 5:
            dict_of_function_expressions[func_num] = function_5
        elif index == 6:
            dict_of_function_expressions[func_num] = function_6
    except ValueError:
        st.error(f"Ошибка: неверный номер функции '{text}'")


def function_0(u):
    if len(free_members_of_fun_expr) > 0:
        return (free_members_of_fun_expr[0][0] * u ** 3 + 
                free_members_of_fun_expr[0][1] * u ** 2 + 
                free_members_of_fun_expr[0][2] * u + 
                free_members_of_fun_expr[0][3])
    return u


def function_1(u):
    if len(free_members_of_fun_expr) > 1:
        return (free_members_of_fun_expr[1][0] * u + 
                free_members_of_fun_expr[1][1])
    return u


def function_2(u):
    if len(free_members_of_fun_expr) > 2:
        return (free_members_of_fun_expr[2][0] * u ** 2 + 
                free_members_of_fun_expr[2][1] * u + 
                free_members_of_fun_expr[2][2])
    return u


def function_3(u):
    if len(free_members_of_fun_expr) > 3:
        return (free_members_of_fun_expr[3][0] * u + 
                free_members_of_fun_expr[3][1])
    return u


def function_4(u):
    if len(free_members_of_fun_expr) > 4:
        return (free_members_of_fun_expr[4][0] * u ** 2 + 
                free_members_of_fun_expr[4][1] * u + 
                free_members_of_fun_expr[4][2])
    return u


def function_5(u):
    if len(free_members_of_fun_expr) > 5:
        return (free_members_of_fun_expr[5][0] * u + 
                free_members_of_fun_expr[5][1])
    return u


def function_6(u):
    if len(free_members_of_fun_expr) > 6:
        return (free_members_of_fun_expr[6][0] * u ** 2 + 
                free_members_of_fun_expr[6][1] * u + 
                free_members_of_fun_expr[6][2])
    return u


def draw_third_graphic(t):
    """График возмущений"""
    global free_members_of_fun_expr
    fig = plt.figure(figsize=(15, 10))
    plt.subplot(1, 1, 1)
    
    if len(free_members_of_fun_expr) >= 6:
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        y6 = []
        for i in t:
            y1.append(free_members_of_fun_expr[0][0] * i**3 +
                     free_members_of_fun_expr[0][1] * i**2 +
                     free_members_of_fun_expr[0][2] * i +
                     free_members_of_fun_expr[0][3])
            y2.append(free_members_of_fun_expr[1][0] * i +
                     free_members_of_fun_expr[1][1])
            y3.append(free_members_of_fun_expr[2][0] * i**2 +
                     free_members_of_fun_expr[2][1] * i +
                     free_members_of_fun_expr[2][2])
            y4.append(free_members_of_fun_expr[3][0] * i +
                     free_members_of_fun_expr[3][1])
            y5.append(free_members_of_fun_expr[4][0] * i**2 +
                     free_members_of_fun_expr[4][1] * i +
                     free_members_of_fun_expr[4][2])
            y6.append(free_members_of_fun_expr[5][0] * i +
                     free_members_of_fun_expr[5][1])
        plt.plot(t, y1, label='F1')
        plt.plot(t, y2, label='F2')
        plt.plot(t, y3, label='F3')
        plt.plot(t, y4, label='F4')
        plt.plot(t, y5, label='F5')
        plt.plot(t, y6, label='F6')
    
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.ylabel('F(t)')
    plt.title('Графики функций системы')
    plt.grid()
    return fig


def create_radar_diagrams(data, labels):
    radar = RadarDiagram()
    diagrams = []
    
    n = len(data)
    moments = [
        ([data[0]], "Характеристики системы в начальный момент времени"),
        ([data[0], data[n // 4]], "Характеристики системы в 1 четверти"),
        ([data[0], data[n // 2]], "Характеристики системы во 2 четверти"),
        ([data[0], data[n - 1]], "Характеристики системы в последний момент времени")
    ]
    
    for data_moment, title in moments:
        fig = radar.draw(data_moment, labels, title)
        diagrams.append((fig, title))
    
    return diagrams


def process_function_list(num_functions):
    new_function_list = []
    for ind, expression in enumerate(functions.function_list):
        new_expression = []
        for ind2, part in enumerate(expression):
            if isinstance(part, dict):
                new_expression.append(np.intersect1d(list(part.keys()), num_functions))
                functions.function_list[ind][ind2] = recreate(new_expression[ind2], part)
            else:
                new_expression.append(part)
    
    return new_function_list


def recreate(new_expression, part):
    new_part = {}
    for ind in new_expression:
        new_part[ind] = part[ind]
    return new_part


def create_graphic(t, data):
    """График характеристик"""
    fig, ax = plt.subplots(figsize=(15, 10))
    labels = labels_array()
    for i in range(14):
        plt.plot(t, data[:, i], label=labels[i])
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.ylabel('Значение')
    plt.title('Динамика параметров системы')
    ax.legend(labels, loc=(.75, .64), labelspacing=0.1, fontsize='small')
    plt.grid()
    plt.xlim([0, 1])
    return fig


def labels_array():
    return [
        "Z1 - Число погибших людей",
        "Z2 - Продолжительность поражающего воздействия", 
        "Z3 - Площадь зоны ЧС",
        "Z4 - Число людей, утративших имущество",
        "Z5 - Ущерб коммерческой организации",
        "Z6 - Объем загрязненного грунта",
        "Z7 - Площадь земель, исключенных из оборота",
        "Z8 - Снижение плодородия земель",
        "Z9 - Продолжительность аварийного периода",
        "Z10 - Продолжительность восстановительного периода",
        "Z11 - Число пораженных сельхоз животных", 
        "Z12 - Величина погибшего урожая",
        "Z13 - Площадь уничтоженных лесных массивов",
        "Z14 - Ущерб административной единице"
    ]


def process_calculation(start_values, free_members):
    """Основная функция расчета"""
    global data_sol
    global free_members_of_fun_expr
    
    plt.close('all')
    gc.collect()

    free_members_of_fun_expr = free_members
    t = np.linspace(0, 1, 80)
    
    # Инициализация функций
    init_default_functions()
    
    # Обрабатываем список функций
    process_function_list(list(dict_of_function_expressions.keys()))

    # Решаем систему уравнений
    data_sol = odeint(functions.pend, start_values, t, 
                     args=(dict_of_function_expressions, functions.function_list))
    
    # Гарантируем, что значения не нулевые
    data_sol = np.clip(data_sol, 0.01, 1.0)
    
    gc.collect()
    
    return t, data_sol


def draw_third_graphic(t):
    """График временных возмущений системы"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Вычисляем значения временных возмущений
    y1 = []  # fak_1: t² + 1
    y2 = []  # fak_2: cos²(1.5πt - π/6)/4 + 0.2
    y3 = []  # fak_3: sin(πt - π/6)/2.5 + 0.3
    y4 = []  # fak_4: 2t - 1
    y5 = []  # fak_5: cos²(1.5πt - π/6)/4
    y6 = []  # fak_6: sin²(πt - π/6)/2.5 + 0.3
    
    for time_val in t:
        # fak_1: t² + 1
        y1.append(time_val**2 + 1)
        
        # fak_2: cos²(1.5πt - π/6)/4 + 0.2
        y2.append(np.cos(1.5 * time_val * np.pi - np.pi / 6) ** 2 / 4 + 0.2)
        
        # fak_3: sin(πt - π/6)/2.5 + 0.3
        y3.append(np.sin(time_val * np.pi - np.pi / 6) / 2.5 + 0.3)
        
        # fak_4: 2t - 1
        y4.append(2 * time_val - 1)
        
        # fak_5: cos²(1.5πt - π/6)/4
        y5.append(np.cos(1.5 * time_val * np.pi - np.pi / 6) ** 2 / 4)
        
        # fak_6: sin²(πt - π/6)/2.5 + 0.3
        y6.append(np.sin(time_val * np.pi - np.pi / 6) ** 2 / 2.5 + 0.3)
    
    # Рисуем все возмущения на одном графике
    ax.plot(t, y1, label='fak₁(t) = t² + 1', linewidth=2, color='blue')
    ax.plot(t, y2, label='fak₂(t) = cos²(1.5πt - π/6)/4 + 0.2', linewidth=2, color='red')
    ax.plot(t, y3, label='fak₃(t) = sin(πt - π/6)/2.5 + 0.3', linewidth=2, color='green')
    ax.plot(t, y4, label='fak₄(t) = 2t - 1', linewidth=2, color='orange')
    ax.plot(t, y5, label='fak₅(t) = cos²(1.5πt - π/6)/4', linewidth=2, color='purple')
    ax.plot(t, y6, label='fak₆(t) = sin²(πt - π/6)/2.5 + 0.3', linewidth=2, color='brown')
    
    # Настройка графика
    ax.set_xlabel('Время (t)')
    ax.set_ylabel('Значение возмущения')
    ax.set_title('Временные возмущения системы', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    
    # Добавляем описание возмущений
    ax.text(0.02, 0.02, 
            'Возмущения fak₁-fak₆ используются в системе уравнений\nдля моделирования временных изменений параметров',
            transform=ax.transAxes, fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8),
            verticalalignment='bottom')
    
    plt.tight_layout()
    return fig