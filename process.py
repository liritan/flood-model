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
    """График всех функций системы на одном изображении"""
    global free_members_of_fun_expr
    
    # Создаем одну большую картинку со всеми графиками
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(15, 12))
    axes = [ax1, ax2, ax3, ax4, ax5, ax6]
    
    function_names = [
        "F1: Кубический полином (ax³ + bx² + cx + d)",
        "F2: Линейная функция (ax + b)", 
        "F3: Квадратный полином (ax² + bx + c)",
        "F4: Линейная функция (ax + b)",
        "F5: Квадратный полином (ax² + bx + c)",
        "F6: Линейная функция (ax + b)"
    ]
    
    # Цвета для графиков
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    for i in range(6):
        ax = axes[i]
        
        if i < len(free_members_of_fun_expr) and free_members_of_fun_expr[i]:
            coeffs = free_members_of_fun_expr[i]
            y = []
            
            # Вычисляем значения функции
            for time_val in t:
                if i == 0:  # Кубический полином
                    if len(coeffs) >= 4:
                        value = coeffs[0] * time_val**3 + coeffs[1] * time_val**2 + coeffs[2] * time_val + coeffs[3]
                    else:
                        value = time_val
                elif i in [1, 3, 5]:  # Линейные функции
                    if len(coeffs) >= 2:
                        value = coeffs[0] * time_val + coeffs[1]
                    else:
                        value = time_val
                else:  # Квадратные полиномы
                    if len(coeffs) >= 3:
                        value = coeffs[0] * time_val**2 + coeffs[1] * time_val + coeffs[2]
                    else:
                        value = time_val
                y.append(value)
            
            # Рисуем график
            ax.plot(t, y, color=colors[i], linewidth=3, label=function_names[i])
            
            # Добавляем информацию о коэффициентах
            coeff_text = "Коэффициенты:\n"
            for j, coeff in enumerate(coeffs):
                coeff_text += f"  {coeff:.4f}\n"
            
            ax.text(0.02, 0.98, coeff_text, transform=ax.transAxes, 
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
            
        else:
            # Демо-график если нет данных
            if i == 0:
                y = t**3
            elif i == 1:
                y = 2*t + 0.5
            elif i == 2:
                y = t**2 + 0.3*t
            elif i == 3:
                y = 0.5*t + 0.2
            elif i == 4:
                y = 1.5*t**2 - 0.2*t
            else:
                y = 0.8*t + 0.1
                
            ax.plot(t, y, color=colors[i], linewidth=3, label=function_names[i] + " (демо)")
            ax.text(0.02, 0.98, "Демонстрационные\nкоэффициенты", transform=ax.transAxes, 
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
        
        # Настройка внешнего вида
        ax.set_xlabel('Время')
        ax.set_ylabel('F(x)')
        ax.set_title(function_names[i], fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='lower right', fontsize=8)
        
        # Устанавливаем одинаковые пределы для сравнения
        ax.set_xlim(0, 1)
    
    # Общий заголовок
    plt.suptitle('Графики всех функций системы', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    
    return fig