

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import logging

from functions import pend
from radar_diagram import RadarDiagram

data_sol = []
logger = logging.getLogger(__name__)


def fill_diagrams(data, initial_equations, restrictions):
    radar1 = RadarDiagram()
    
    # Убираем нормализацию, только обрезаем значения
    clipped_initial = np.clip(initial_equations, 0, 1.0)
    clipped_data = np.clip(data, 0, 1.0)
    
    # Первый график - только начальные характеристики
    radar1.draw('./static/images/diagram.png', clipped_initial, clipped_data[0], u_list,
                "Характеристики системы: начальный момент времени", show_both_lines=False)
    
    # Остальные графики - обе линии
    radar1.draw('./static/images/diagram2.png', clipped_initial, clipped_data[int(len(data) / 4)], u_list,
                "Характеристики системы: 1 четверть времени", show_both_lines=True)
    radar1.draw('./static/images/diagram3.png', clipped_initial, clipped_data[int(len(data) / 2)], u_list,
                "Характеристики системы: 2 четверть времени", show_both_lines=True)
    radar1.draw('./static/images/diagram4.png', clipped_initial, clipped_data[int(len(data) / 4 * 3)], u_list,
                "Характеристики системы: 3 четверть времени", show_both_lines=True)
    radar1.draw('./static/images/diagram5.png', clipped_initial, clipped_data[-1, :], u_list,
                "Характеристики системы: конечный момент времени", show_both_lines=True)

def create_graphic(t, data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 16))
    
    labels = [
        "X1 - Численность сил",
        "X2 - Разрушенные дома", 
        "X3 - Эвакуированные",
        "X4 - Погибшие",
        "X5 - Дороги в зоне",
        "X6 - Предприятия",
        "X7 - Транспорт",
        "X8 - Население в зоне",
        "X9 - Сельхоз угодья",
        "X10 - Погибшие животные", 
        "X11 - Ущерб основным фондам",
        "X12 - Ущерб оборотным фондам"
    ]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ff1493', '#00ced1']
    
    # Первый график: характеристики 1-6
    for i in range(6):
        # Только обрезаем значения, без нормализации
        y_data = np.clip(data[:, i], 0, 1.0)
        ax1.plot(t, y_data, 
                 color=colors[i], linewidth=2.5, label=labels[i])
    
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.0])
    ax1.set_ylabel("Значения характеристик", fontsize=14, fontweight='bold')
    ax1.set_title("График 1: Характеристики системы (X1-X6)", fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=12)
    
    # Добавляем линию предела
    ax1.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1, label='Предел')
    
    # Второй график: характеристики 7-12
    for i in range(6, 12):
        # Только обрезаем значения, без нормализации
        y_data = np.clip(data[:, i], 0, 1.0)
        ax2.plot(t, y_data, 
                 color=colors[i], linewidth=2.5, label=labels[i])
    
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.0])
    ax2.set_xlabel("t, время", fontsize=14, fontweight='bold')
    ax2.set_ylabel("Значения характеристик", fontsize=14, fontweight='bold')
    ax2.set_title("График 2: Характеристики системы (X7-X12)", fontsize=16, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(axis='both', which='major', labelsize=12)
    
    # Добавляем линию предела
    ax2.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1, label='Предел')
    
    plt.tight_layout(pad=3.0)
    fig.savefig('./static/images/figure.png', bbox_inches='tight', dpi=150)
    plt.close(fig)

def cast_to_float(initial_equations, faks, equations, restrictions):
    for i in range(len(initial_equations)):
        initial_equations[i] = float(initial_equations[i])

    for i in range(len(faks)):
        for j in range(len(faks[i])):
            faks[i][j] = float(faks[i][j])

    for i in range(len(equations)):
        for j in range(len(equations[i])):
            equations[i][j] = float(equations[i][j])

    for i in range(len(restrictions)):
        restrictions[i] = float(restrictions[i])

    return initial_equations, faks, restrictions

def process(initial_equations, faks, equations, restrictions):
    global data_sol

    cast_to_float(initial_equations, faks, equations, restrictions)
    t = np.linspace(0, 1)
    data_sol = odeint(pend, initial_equations, t, args=(faks, equations, restrictions))
    create_graphic(t, data_sol)
    create_disturbances_graphic(t, faks)  
    fill_diagrams(data_sol, initial_equations, restrictions)

u_list = [
    "Численность группировки сил, участвующих в аварийно-спасательных работах",
    "Количество жилых домов, разрушенных и поврежденных в результате наводнения",
    "Численность населения, эвакуированного из зоны затопления",
    "Количество погибших",
    "Протяженность железных и автомобильных дорог, оказавшихся в зоне затопления",
    "Количество промышленных предприятий в зоне наводнения",
    "Количество транспортных средств, участвующих в аварийно-спасательных работах",
    "Численность населения в зоне затопления",
    "Площадь сельскохозяйственных угодий, охваченных наводнением",
    "Количество погибших сельскохозяйственных животных",
    "Ущерб основным производственным фондам в зоне затопления",
    "Ущерб оборотным производственным фондам в зоне затопления"
]

def f3(x, params):
    return params[0] * x ** 3 + params[1] * x ** 2 + params[2] * x + params[3]

def create_disturbances_graphic(t, faks):
    fig, axs = plt.subplots(figsize=(16, 10))
    
    disturbances_labels = [
        "S(t) - Площадь зоны затопления",
        "F(t) - Скорость течения воды", 
        "G(t) - Глубина воды",
        "T(t) - Температура воды",
        "A(t) - Плотность транспортных сетей",
        "D(t) - Плотность населения в зоне",
        "I(t) - Доля сельхоз угодий"
    ]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    # 1. Считаем все кривые заранее
    all_curves = [f3(t, faks[i]) for i in range(7)]
    
    # 2. Ищем общий максимум среди всех кривых
    global_max = max(np.max(curve) for curve in all_curves)
    if global_max == 0:
        global_max = 1
    
    # 3. Рисуем нормализованные значения
    for i in range(7):
        curve = all_curves[i] / global_max
        axs.plot(t, curve, color=colors[i], linewidth=2.5, label=disturbances_labels[i])
    
    axs.set_xlim([0, 1])
    axs.set_ylim([0, 1])
    axs.set_xlabel("t, время", fontsize=14, fontweight='bold')
    axs.set_ylabel("Значения воздействий", fontsize=14, fontweight='bold')
    axs.set_title("График внешних воздействий на систему", fontsize=16, fontweight='bold', pad=20)
    axs.legend(loc='upper right', fontsize=10, framealpha=0.9)
    axs.grid(True, alpha=0.3, linestyle='--')
    axs.tick_params(axis='both', which='major', labelsize=12)
    
    plt.tight_layout()
    fig.savefig('./static/images/disturbances.png', bbox_inches='tight', dpi=150)
    plt.close(fig)
