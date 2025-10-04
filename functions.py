# functions_flood.py
import numpy as np
import math

# Полная структура взаимовлияний согласно PDF
function_list = np.array([
    # Z1: Число погибших людей
    [
        {1: 1},  # положительное влияние от f1(Z2)
        {2: 8, 3: 13}  # положительное от f2(Z9), отрицательное от f3(Z14)
    ],
    # Z2: Продолжительность поражающего воздействия
    [
        {4: 6},  # положительное от f4(Z7)
        {5: 3, 6: 10}  # отрицательное от f5(Z4), f6(Z11)
    ],
    # Z3: Площадь зоны ЧС
    [
        {7: 0, 8: 6, 9: 8},  # положительное от f7(Z1), f8(Z7), f9(Z9)
        {10: 1, 11: 9}  # отрицательное от f10(Z2), f11(Z10)
    ],
    # Z4: Число людей, утративших имущество
    [
        {12: 0, 13: 2, 14: 6, 15: 6, 16: 13},  # положительное влияние
        {}  # отрицательное влияние
    ],
    # Z5: Ущерб коммерческой организации
    [
        {17: 5, 18: 7, 19: 11},  # положительное
        {20: 1, 21: 11}  # отрицательное
    ],
    # Z6: Объем загрязненного грунта
    [
        {22: 3, 23: 6, 24: 8, 25: 12},  # положительное
        {26: 9, 27: 10, 28: 11}  # отрицательное
    ],
    # Z7: Площадь земель, исключенных из оборота
    [
        {29: 8},  # положительное
        {}  # отрицательное
    ],
    # Z8: Снижение плодородия земель
    [
        {30: 5, 31: 10},  # положительное
        {32: 3, 33: 9, 34: 12}  # отрицательное
    ],
    # Z9: Продолжительность аварийного периода
    [
        {35: 3},  # положительное
        {36: 1, 37: 4, 38: 9}  # отрицательное
    ],
    # Z10: Продолжительность восстановительного периода
    [
        {39: 1, 40: 3, 41: 10, 42: 11, 43: 13},  # положительное
        {}  # отрицательное
    ],
    # Z11: Число пораженных сельхоз животных
    [
        {44: 2, 45: 6, 46: 8},  # положительное
        {47: 3, 48: 12}  # отрицательное
    ],
    # Z12: Величина погибшего урожая
    [
        {49: 5, 50: 7, 51: 12},  # положительное
        {52: 0, 53: 6, 54: 10}  # отрицательное
    ],
    # Z13: Площадь уничтоженных лесных массивов
    [
        {55: 6},  # положительное
        {56: 2, 57: 8}  # отрицательное
    ],
    # Z14: Ущерб административной единице
    [
        {58: 1, 59: 2, 60: 4, 61: 7, 62: 10, 63: 11, 64: 12},  # положительное
        {65: 6, 66: 8}  # отрицательное
    ]
], dtype=object)

# Функции возмущений времени
def fak_1(t):
    return t**2 + 1

def fak_2(t):
    return np.cos(1.5 * t * np.pi - np.pi / 6) ** 2 / 4 + 0.2

def fak_3(t):
    return np.sin(t * np.pi - np.pi / 6) / 2.5 + 0.3

def fak_4(t):
    return 2*t - 1

def fak_5(t):
    return np.cos(1.5 * t * np.pi - np.pi / 6) ** 2 / 4

def fak_6(t):
    return np.sin(t * np.pi - np.pi / 6) ** 2 / 2.5 + 0.3

def process_part_of_expression(u, fak_list, t, dict_of_function_expressions, new_function_list, index_expression, index_side):
    """Обработка части выражения для системы дифференциальных уравнений"""
    result = 1
    result_fak = 0

    for num_function in new_function_list[index_expression][index_side]:
        result *= dict_of_function_expressions[num_function](u[new_function_list[index_expression][index_side][num_function]])
    for fak in fak_list:
        result_fak += fak(t)
    return result * result_fak

def pend(u, t, dict_of_function_expressions, new_function_list):
    """Полная система дифференциальных уравнений для модели наводнения"""
    dudt = [
        # Z1: Число погибших людей
        (process_part_of_expression(u, [fak_1, fak_2, fak_6], t, dict_of_function_expressions, new_function_list, 0, 0)
         - process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 0, 1)),

        # Z2: Продолжительность поражающего воздействия
        (process_part_of_expression(u, [fak_1, fak_5], t, dict_of_function_expressions, new_function_list, 1, 0)
         - process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 1, 1)),

        # Z3: Площадь зоны ЧС
        (process_part_of_expression(u, [fak_1, fak_5], t, dict_of_function_expressions, new_function_list, 2, 0)
         - process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 2, 1)),

        # Z4: Число людей, утративших имущество
        (process_part_of_expression(u, [fak_1, fak_2, fak_5, fak_6], t, dict_of_function_expressions, new_function_list, 3, 0)
         - process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 3, 1)),

        # Z5: Ущерб коммерческой организации
        (process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 4, 0)
         - process_part_of_expression(u, [fak_3], t, dict_of_function_expressions, new_function_list, 4, 1)),

        # Z6: Объем загрязненного грунта
        (process_part_of_expression(u, [fak_1, fak_2], t, dict_of_function_expressions, new_function_list, 5, 0)
         - process_part_of_expression(u, [fak_3], t, dict_of_function_expressions, new_function_list, 5, 1)),

        # Z7: Площадь земель, исключенных из оборота
        (process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 6, 0)
         - process_part_of_expression(u, [fak_1, fak_2], t, dict_of_function_expressions, new_function_list, 6, 1)),

        # Z8: Снижение плодородия земель
        (process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 7, 0)
         - process_part_of_expression(u, [fak_1, fak_2], t, dict_of_function_expressions, new_function_list, 7, 1)),

        # Z9: Продолжительность аварийного периода
        (process_part_of_expression(u, [fak_4], t, dict_of_function_expressions, new_function_list, 8, 0)
         - process_part_of_expression(u, [fak_5, fak_6], t, dict_of_function_expressions, new_function_list, 8, 1)),

        # Z10: Продолжительность восстановительного периода
        (process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 9, 0)
         - process_part_of_expression(u, [fak_1], t, dict_of_function_expressions, new_function_list, 9, 1)),

        # Z11: Число пораженных сельхоз животных
        (process_part_of_expression(u, [fak_3], t, dict_of_function_expressions, new_function_list, 10, 0)
         - process_part_of_expression(u, [fak_1], t, dict_of_function_expressions, new_function_list, 10, 1)),

        # Z12: Величина погибшего урожая
        (process_part_of_expression(u, [fak_3], t, dict_of_function_expressions, new_function_list, 11, 0)
         - process_part_of_expression(u, [fak_1, fak_5], t, dict_of_function_expressions, new_function_list, 11, 1)),

        # Z13: Площадь уничтоженных лесных массивов
        (process_part_of_expression(u, [], t, dict_of_function_expressions, new_function_list, 12, 0)
         - process_part_of_expression(u, [fak_1], t, dict_of_function_expressions, new_function_list, 12, 1)),

        # Z14: Ущерб административной единице
        (process_part_of_expression(u, [fak_3], t, dict_of_function_expressions, new_function_list, 13, 0)
         - process_part_of_expression(u, [fak_1], t, dict_of_function_expressions, new_function_list, 13, 1))
    ]
    return dudt