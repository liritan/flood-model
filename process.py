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
    
    # Сбалансированная система дифференциальных уравнений
    def flood_model(u, t):
        dudt = []
        for i in range(14):
            # Слабое затухание вместо сильного
            base_change = -0.01 * u[i]  # Уменьшили затухание в 10 раз
            
            # Взаимовлияния между параметрами - больше положительных влияний
            influence = 0
            
            # Z1 (погибшие) - медленно растет от воздействия
            if i == 0:  # Z1
                influence += 0.08 * u[1]  # растет от продолжительности воздействия
                influence += 0.05 * u[2]  # растет от площади ЧС
                if 1 in dict_of_function_expressions:
                    influence += 0.03 * dict_of_function_expressions[1](u[1])
                    
            # Z2 (продолжительность) - стабилизируется
            elif i == 1:  # Z2
                influence += 0.06 * u[2]  # зависит от площади
                influence += 0.04 * u[6]  # зависит от исключенных земель
                influence -= 0.02 * u[9]  # уменьшается при восстановлении
                if 2 in dict_of_function_expressions:
                    influence += 0.02 * dict_of_function_expressions[2](u[6])
                    
            # Z3 (площадь) - медленно растет
            elif i == 2:  # Z3
                influence += 0.07 * u[1]  # растет от продолжительности
                influence += 0.03 * u[5]  # растет от загрязнения
                if 3 in dict_of_function_expressions:
                    influence += 0.02 * dict_of_function_expressions[3](u[0])
                    
            # Z4 (утратившие имущество) - растет
            elif i == 3:  # Z4
                influence += 0.09 * u[2]  # сильно зависит от площади
                influence += 0.04 * u[0]  # зависит от погибших
                if 4 in dict_of_function_expressions:
                    influence += 0.03 * dict_of_function_expressions[4](u[2])
                    
            # Z5 (ущерб организациям) - растет
            elif i == 4:  # Z5
                influence += 0.08 * u[3]  # зависит от утративших имущество
                influence += 0.05 * u[6]  # зависит от исключенных земель
                if 5 in dict_of_function_expressions:
                    influence += 0.02 * dict_of_function_expressions[5](u[5])
                    
            # Z6 (загрязнение) - растет
            elif i == 5:  # Z6
                influence += 0.1 * u[2]   # сильно зависит от площади
                influence += 0.04 * u[8]  # зависит от аварийного периода
                if 6 in dict_of_function_expressions:
                    influence += 0.03 * dict_of_function_expressions[6](u[3])
                    
            # Z7 (исключенные земли) - растет
            elif i == 6:  # Z7
                influence += 0.07 * u[5]  # зависит от загрязнения
                influence += 0.05 * u[2]  # зависит от площади
                    
            # Z8 (снижение плодородия) - медленно растет
            elif i == 7:  # Z8
                influence += 0.06 * u[5]  # зависит от загрязнения
                influence += 0.03 * u[6]  # зависит от исключенных земель
                    
            # Z9 (аварийный период) - стабилизируется
            elif i == 8:  # Z9
                influence += 0.05 * u[2]  # зависит от площади
                influence += 0.04 * u[3]  # зависит от утративших имущество
                influence -= 0.03 * u[9]  # переходит в восстановление
                    
            # Z10 (восстановительный период) - растет со временем
            elif i == 9:  # Z10
                influence += 0.02 * t     # растет со временем
                influence += 0.03 * u[2]  # зависит от масштаба ЧС
                influence += 0.02 * u[3]  # зависит от числа пострадавших
                    
            # Z11 (пораженные животные) - растет
            elif i == 10:  # Z11
                influence += 0.08 * u[2]  # зависит от площади
                influence += 0.04 * u[6]  # зависит от исключенных земель
                    
            # Z12 (погибший урожай) - растет
            elif i == 11:  # Z12
                influence += 0.09 * u[2]  # сильно зависит от площади
                influence += 0.05 * u[7]  # зависит от снижения плодородия
                influence += 0.04 * u[5]  # зависит от загрязнения
                    
            # Z13 (лесные массивы) - медленно растет
            elif i == 12:  # Z13
                influence += 0.07 * u[2]  # зависит от площади
                influence += 0.03 * u[5]  # зависит от загрязнения
                    
            # Z14 (ущерб администрации) - растет
            elif i == 13:  # Z14
                influence += 0.04 * np.sum(u[:13]) / 13  # зависит от всех параметров
                influence += 0.03 * u[4]  # зависит от ущерба организациям
            
            # Балансируем систему - добавляем небольшие положительные смещения
            balance = 0.01 * (1 - u[i])  # Стремление к значению 1
            
            dudt.append(base_change + influence + balance)
        
        return dudt
    
    # Решаем систему
    data_sol = odeint(flood_model, start_values, t)
    
    # Нормализуем значения чтобы они не уходили в ноль
    data_sol = np.clip(data_sol, 0.001, 1.0)
    
    return t, data_sol