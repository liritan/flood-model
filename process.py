import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import functions as functions
import streamlit as st

dict_of_function_expressions = {}
free_members_of_fun_expr = []
data_sol = []

def init_default_functions():
    """Инициализация 7 функций по умолчанию"""
    global dict_of_function_expressions
    dict_of_function_expressions.clear()
    dict_of_function_expressions[1] = function_0
    dict_of_function_expressions[2] = function_1  
    dict_of_function_expressions[3] = function_2
    dict_of_function_expressions[4] = function_3
    dict_of_function_expressions[5] = function_4
    dict_of_function_expressions[6] = function_5
    dict_of_function_expressions[7] = function_6

def function_0(u):
    """Кубический полином: ax³ + bx² + cx + d"""
    if len(free_members_of_fun_expr) > 0:
        coeffs = free_members_of_fun_expr[0]
        return coeffs[0] * u**3 + coeffs[1] * u**2 + coeffs[2] * u + coeffs[3]
    return u

def function_1(u):
    """Линейная функция: ax + b"""
    if len(free_members_of_fun_expr) > 1:
        coeffs = free_members_of_fun_expr[1]
        return coeffs[0] * u + coeffs[1]
    return u

def function_2(u):
    """Квадратный полином: ax² + bx + c"""
    if len(free_members_of_fun_expr) > 2:
        coeffs = free_members_of_fun_expr[2]
        return coeffs[0] * u**2 + coeffs[1] * u + coeffs[2]
    return u

def function_3(u):
    """Линейная функция: ax + b"""
    if len(free_members_of_fun_expr) > 3:
        coeffs = free_members_of_fun_expr[3]
        return coeffs[0] * u + coeffs[1]
    return u

def function_4(u):
    """Квадратный полином: ax² + bx + c"""
    if len(free_members_of_fun_expr) > 4:
        coeffs = free_members_of_fun_expr[4]
        return coeffs[0] * u**2 + coeffs[1] * u + coeffs[2]
    return u

def function_5(u):
    """Линейная функция: ax + b"""
    if len(free_members_of_fun_expr) > 5:
        coeffs = free_members_of_fun_expr[5]
        return coeffs[0] * u + coeffs[1]
    return u

def function_6(u):
    """Квадратный полином: ax² + bx + c"""
    if len(free_members_of_fun_expr) > 6:
        coeffs = free_members_of_fun_expr[6]
        return coeffs[0] * u**2 + coeffs[1] * u + coeffs[2]
    return u

def draw_functions_graphic(t, free_members):
    """График 7 функций системы"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Тестовые значения x для построения графиков функций
    x = np.linspace(0, 1, 100)
    
    # Строим графики для каждой функции
    for i in range(min(7, len(free_members))):
        coeffs = free_members[i]
        if i == 0:  # Кубический полином
            y = coeffs[0] * x**3 + coeffs[1] * x**2 + coeffs[2] * x + coeffs[3]
            label = f'F{i+1}: Кубический полином'
        elif i in [1, 3, 5]:  # Линейные функции
            y = coeffs[0] * x + coeffs[1]
            label = f'F{i+1}: Линейная функция'
        else:  # Квадратные полиномы
            y = coeffs[0] * x**2 + coeffs[1] * x + coeffs[2]
            label = f'F{i+1}: Квадратный полином'
        
        ax.plot(x, y, label=label, linewidth=2)
    
    ax.set_xlabel('x')
    ax.set_ylabel('F(x)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def labels_array():
    """Метки 14 параметров системы"""
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
    """Основная функция расчета системы дифференциальных уравнений"""
    global data_sol
    global free_members_of_fun_expr
    
    plt.close('all')

    free_members_of_fun_expr = free_members
    t = np.linspace(0, 1, 80)
    
    # Инициализация функций
    init_default_functions()
    
    # Упрощенная система дифференциальных уравнений
    def flood_model(u, t):
        dudt = []
        for i in range(14):
            # Базовая динамика системы с взаимовлиянием
            change = -0.1 * u[i] + 0.015 * np.sum(u) / 14
            
            # Добавляем влияние функций согласно системе уравнений
            if i == 0:  # Z1 зависит от F1 (Z2)
                if 1 in dict_of_function_expressions:
                    change += 0.05 * dict_of_function_expressions[1](u[1])
                    
            elif i == 1:  # Z2 зависит от F2 (Z7) и F1 (Z4)
                if 2 in dict_of_function_expressions:
                    change += 0.03 * dict_of_function_expressions[2](u[6])
                if 1 in dict_of_function_expressions:
                    change -= 0.02 * dict_of_function_expressions[1](u[3])
                    
            elif i == 3:  # Z4 зависит от F4 (Z3)
                if 4 in dict_of_function_expressions:
                    change += 0.04 * dict_of_function_expressions[4](u[2])
                    
            elif i == 5:  # Z6 зависит от F6 (Z4)
                if 6 in dict_of_function_expressions:
                    change += 0.03 * dict_of_function_expressions[6](u[3])
                    
            elif i == 6:  # Z7 зависит от F7 (Z9)
                if 7 in dict_of_function_expressions:
                    change += 0.02 * dict_of_function_expressions[7](u[8])
            
            dudt.append(change)
        return dudt
    
    data_sol = odeint(flood_model, start_values, t)
    
    return t, data_sol