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
    radar = RadarDiagram()
    
    clipped_initial = np.clip(initial_equations, 0, 1.0)
    clipped_data = np.clip(data, 0, 1.0)
    clipped_restrictions = np.clip(restrictions, 0, 1.0)

    time_indices = [
        0,
        int(len(data) / 4),
        int(len(data) / 2),
        int(3 * len(data) / 4),
        -1
    ]
    
    titles = [
        "Характеристики системы: начальный момент времени",
        "Характеристики системы при t=0.25",
        "Характеристики системы при t=0.5",
        "Характеристики системы при t=0.75",
        "Характеристики системы при t=1"
    ]
    
    filenames = [
        './static/images/diagram.png',
        './static/images/diagram2.png',
        './static/images/diagram3.png',
        './static/images/diagram4.png',
        './static/images/diagram5.png'
    ]

    for i, (idx, title, fname) in enumerate(zip(time_indices, titles, filenames)):
        current_vals = clipped_data[idx]
        
        if i == 0:
            radar.draw(
                filename=fname,
                initial_data=clipped_initial,
                current_data=current_vals,
                label="",
                title=title,
                restrictions=clipped_restrictions,
                show_both_lines=False
            )
        else:
            radar.draw(
                filename=fname,
                initial_data=clipped_initial,
                current_data=current_vals,
                label="",
                title=title,
                restrictions=clipped_restrictions,
                show_both_lines=True
            )


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
    
    line_labels = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12"]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ff1493', '#00ced1']
    
    for i in range(6):
        y_data = np.clip(data[:, i], 0, 1.0)
        line = ax1.plot(t, y_data, color=colors[i], linewidth=2.5, label=labels[i])
        
        mid_idx = len(t) // 2
        if mid_idx > 0:
            ax1.text(t[mid_idx], y_data[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=9, va='center', ha='left',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.0])
    ax1.set_ylabel("Значения характеристик", fontsize=14, fontweight='bold')
    ax1.set_title("График 1: Характеристики системы (X1-X6)", fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=12)
    
    ax1.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1, label='Предел')
    
    for i in range(6, 12):
        y_data = np.clip(data[:, i], 0, 1.0)
        line = ax2.plot(t, y_data, color=colors[i], linewidth=2.5, label=labels[i])
        
        mid_idx = len(t) // 2
        if mid_idx > 0:
            ax2.text(t[mid_idx], y_data[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=9, va='center', ha='left',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.0])
    ax2.set_xlabel("t, время", fontsize=14, fontweight='bold')
    ax2.set_ylabel("Значения характеристик", fontsize=14, fontweight='bold')
    ax2.set_title("График 2: Характеристики системы (X7-X12)", fontsize=16, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(axis='both', which='major', labelsize=12)
    
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
    t = np.linspace(0, 1, 100)
    
    xm = np.ones(12)

    data_sol = odeint(pend, initial_equations, t, args=(faks, equations, xm))
    
    data_sol = np.clip(data_sol, 1e-3, 1.0)
    
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
        "I(t) - Доля сельхоз угодий",
        "P(t) - Осадки",
        "C(t) - Ветровые воздействия"
    ]
    
    line_labels = ["S", "F", "G", "T", "A", "D", "I", "P", "C"]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
              '#e377c2', '#7f7f7f', '#bcbd22']
    
    all_curves = [f3(t, faks[i]) for i in range(len(faks))]
    
    global_max = max(np.max(curve) for curve in all_curves)
    if global_max == 0:
        global_max = 1
    
    for i in range(len(faks)):
        curve = all_curves[i] / global_max
        line = axs.plot(t, curve, color=colors[i], linewidth=2.5, label=disturbances_labels[i])
        
        mid_idx = len(t) // 2
        if mid_idx > 0:
            axs.text(t[mid_idx], curve[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=9, va='center', ha='left',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7, edgecolor='none'))
    
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