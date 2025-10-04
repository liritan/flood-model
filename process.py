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
    t = np.linspace(0, 2, 100)  # Увеличиваем время для большего разнообразия
    
    # Инициализация функций
    init_default_functions()
    
    # Более сложная система дифференциальных уравнений с реальными взаимовлияниями
    def flood_model(u, t):
        dudt = []
        for i in range(14):
            # Базовое затухание разное для каждого параметра
            base_decay = -0.05 * u[i] * (1 + i * 0.02)
            
            # Взаимовлияния между параметрами
            influence = 0
            
            # Z1 (погибшие) зависит от многих факторов
            if i == 0:  # Z1
                influence += 0.1 * u[1] * u[2]  # зависит от Z2 и Z3
                influence -= 0.05 * u[9]        # уменьшается при восстановлении (Z10)
                if 1 in dict_of_function_expressions:
                    influence += 0.08 * dict_of_function_expressions[1](u[1])
                    
            # Z2 (продолжительность) зависит от площади и ущерба
            elif i == 1:  # Z2
                influence += 0.07 * u[2] * u[6]  # зависит от Z3 и Z7
                influence -= 0.03 * u[9]         # уменьшается при восстановлении
                if 2 in dict_of_function_expressions:
                    influence += 0.06 * dict_of_function_expressions[2](u[6])
                    
            # Z3 (площадь) растет от воздействия и уменьшается от мер
            elif i == 2:  # Z3
                influence += 0.08 * u[1]        # зависит от продолжительности
                influence -= 0.04 * u[9] * u[10] # уменьшается от восстановления и помощи
                if 3 in dict_of_function_expressions:
                    influence += 0.05 * dict_of_function_expressions[3](u[0])
                    
            # Z4 (утратившие имущество) зависит от площади и погибших
            elif i == 3:  # Z4
                influence += 0.09 * u[2] * u[0]  # зависит от Z3 и Z1
                influence -= 0.03 * u[9]         # уменьшается при восстановлении
                if 4 in dict_of_function_expressions:
                    influence += 0.07 * dict_of_function_expressions[4](u[2])
                    
            # Z5 (ущерб организациям) зависит от многих факторов
            elif i == 4:  # Z5
                influence += 0.06 * u[3] * u[6]  # зависит от Z4 и Z7
                influence += 0.04 * u[5]         # зависит от загрязнения (Z6)
                if 5 in dict_of_function_expressions:
                    influence += 0.05 * dict_of_function_expressions[5](u[5])
                    
            # Z6 (загрязнение) зависит от площади и времени
            elif i == 5:  # Z6
                influence += 0.08 * u[2] * u[8]  # зависит от Z3 и Z9
                influence -= 0.02 * u[9]         # уменьшается при восстановлении
                if 6 in dict_of_function_expressions:
                    influence += 0.06 * dict_of_function_expressions[6](u[3])
                    
            # Z7 (исключенные земли) зависит от загрязнения и площади
            elif i == 6:  # Z7
                influence += 0.07 * u[5] * u[2]  # зависит от Z6 и Z3
                influence -= 0.03 * u[9]         # уменьшается при восстановлении
                    
            # Z8 (снижение плодородия) зависит от загрязнения
            elif i == 7:  # Z8
                influence += 0.09 * u[5]        # зависит от Z6
                influence -= 0.02 * u[9]        # медленно восстанавливается
                    
            # Z9 (аварийный период) зависит от масштаба
            elif i == 8:  # Z9
                influence += 0.05 * u[2] * u[3]  # зависит от Z3 и Z4
                influence -= 0.04 * u[9]         # переходит в восстановление
                    
            # Z10 (восстановительный период) растет со временем
            elif i == 9:  # Z10
                influence += 0.03 * t           # растет со временем
                influence += 0.02 * (u[2] + u[3]) # зависит от масштаба ЧС
                    
            # Z11 (пораженные животные) зависит от площади
            elif i == 10:  # Z11
                influence += 0.08 * u[2]        # зависит от Z3
                influence -= 0.03 * u[9]        # уменьшается при восстановлении
                    
            # Z12 (погибший урожай) зависит от многих факторов
            elif i == 11:  # Z12
                influence += 0.07 * u[2] * u[7]  # зависит от Z3 и Z8
                influence -= 0.02 * u[9]         # уменьшается при восстановлении
                    
            # Z13 (лесные массивы) зависит от площади ЧС
            elif i == 12:  # Z13
                influence += 0.06 * u[2]        # зависит от Z3
                influence -= 0.01 * u[9]        # очень медленно восстанавливается
                    
            # Z14 (ущерб администрации) зависит от всего
            elif i == 13:  # Z14
                influence += 0.04 * np.sum(u[:13]) / 13  # зависит от всех параметров
                influence -= 0.02 * u[9]         # уменьшается при восстановлении
            
            # Случайные флуктуации для разнообразия
            random_fluctuation = 0.01 * np.random.normal(0, 0.1)
            
            dudt.append(base_decay + influence + random_fluctuation)
        
        return dudt
    
    # Решаем систему с разными начальными условиями
    data_sol = odeint(flood_model, start_values, t)
    
    return t, data_sol