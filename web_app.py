import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import process as process
from radar_diagram import RadarDiagram

st.set_page_config(
    page_title="Модель последствий наводнения", 
    layout="wide",
    page_icon="🌊"
)

# Инициализация сессии
if 'data_sol' not in st.session_state:
    st.session_state.data_sol = None
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
if 'free_members' not in st.session_state:
    st.session_state.free_members = None

st.title("🌊 Модель анализа последствий наводнения")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([" Параметры", " Графики", " Диаграмма", " Функции"])

with tab1:
    st.header("Входные параметры характеристик наводнения")
    
    start_values = []
    labels = process.labels_array()
    
    # Создаем 14 полей ввода (Z1-Z14) в 2 колонки
    cols = st.columns(2)
    for i in range(14):
        with cols[i % 2]:
            default_values = {
            0: 0.3,   # Z1 - число погибших людей
            1: 0.7,   # Z2 - продолжительность поражающего воздействия
            2: 0.8,   # Z3 - площадь зоны ЧС
            3: 0.5,   # Z4 - число людей, утративших имущество
            4: 0.6,   # Z5 - ущерб коммерческой организации
            5: 0.9,   # Z6 - объем загрязненного грунта
            6: 0.7,   # Z7 - площадь земель, исключенных из оборота
            7: 0.4,   # Z8 - снижение плодородия земель
            8: 0.6,   # Z9 - продолжительность аварийного периода
            9: 0.2,   # Z10 - продолжительность восстановительного периода
            10: 0.5,  # Z11 - число пораженных сельхоз животных
            11: 0.8,  # Z12 - величина погибшего урожая
            12: 0.4,  # Z13 - площадь уничтоженных лесных массивов
            13: 0.7   # Z14 - ущерб административной единице
        }
            value = st.number_input(
                labels[i],
                value=default_values.get(i, 0.5),
                min_value=0.0,
                max_value=1.0,
                key=f"param_{i}"
            )
            start_values.append(value)

    st.header("Система из 7 функций влияния")
    
    free_members = []
    
    # 7 основных функций системы
    function_types = [
        "Кубический полином: ax³ + bx² + cx + d",
        "Линейная функция: ax + b", 
        "Квадратный полином: ax² + bx + c",
        "Линейная функция: ax + b",
        "Квадратный полином: ax² + bx + c", 
        "Линейная функция: ax + b",
        "Квадратный полином: ax² + bx + c"
    ]
    
    function_descriptions = [
        "F1: Влияние на число погибших от продолжительности воздействия",
        "F2: Влияние на продолжительность воздействия от площади земель",
        "F3: Влияние на площадь зоны ЧС от числа погибших",
        "F4: Влияние на число людей, утративших имущество, от площади зоны ЧС",
        "F5: Влияние на ущерб организациям от объема загрязненного грунта",
        "F6: Влияние на объем загрязненного грунта от числа людей, утративших имущество",
        "F7: Влияние на площадь земель от продолжительности аварийного периода"
    ]
    
    for i in range(7):
        with st.expander(f"Функция {i+1}: {function_descriptions[i]}", expanded=i==0):
            st.write(f"**Тип:** {function_types[i]}")
            
            if i == 0:  # Кубический полином
                cols = st.columns(4)
                with cols[0]:
                    a = st.number_input("a (x³)", value=0.1, key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b (x²)", value=0.2, key=f"f{i}_b")
                with cols[2]:
                    c = st.number_input("c (x)", value=0.3, key=f"f{i}_c")
                with cols[3]:
                    d = st.number_input("d", value=0.4, key=f"f{i}_d")
                free_members.append([a, b, c, d])
                
            elif i in [1, 3, 5]:  # Линейные функции
                cols = st.columns(2)
                with cols[0]:
                    a = st.number_input("a (x)", value=0.5, key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b", value=0.1, key=f"f{i}_b")
                free_members.append([a, b])
                
            else:  # Квадратные полиномы (i in [2, 4, 6])
                cols = st.columns(3)
                with cols[0]:
                    a = st.number_input("a (x²)", value=0.1, key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b (x)", value=0.2, key=f"f{i}_b")
                with cols[2]:
                    c = st.number_input("c", value=0.3, key=f"f{i}_c")
                free_members.append([a, b, c])

    # Кнопка расчета
    st.markdown("---")
    if st.button("🚀 Выполнить расчет", use_container_width=True):
        with st.spinner("Выполняется расчет системы дифференциальных уравнений..."):
            try:
                st.session_state.free_members = free_members
                
                # Устанавливаем параметры
                process.free_members_of_fun_expr = free_members
                
                # Инициализация функций
                process.init_default_functions()
                
                # Выполняем расчет
                t, data_sol = process.process_calculation(start_values, free_members)
                
                # Сохраняем результаты
                st.session_state.data_sol = data_sol
                st.session_state.t = t
                st.session_state.calculation_done = True
                
                st.success("✅ Моделирование завершено успешно!")
                
            except Exception as e:
                st.error(f"❌ Ошибка при вычислении: {str(e)}")

with tab2:
    st.header("Динамика параметров системы")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        t = st.session_state.t
        data_sol = st.session_state.data_sol
        labels = process.labels_array()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        for i in range(14):
            ax.plot(t, data_sol[:, i], label=labels[i], linewidth=2, alpha=0.7)
        
        ax.set_xlabel('Время')
        ax.set_ylabel('Значение')
        ax.set_title('Динамика параметров системы дифференциальных уравнений')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 1])
        
        st.pyplot(fig)
        
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры'")

with tab3:
    st.header("Радар-диаграммы")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        # Создаем диаграммы
        radar = RadarDiagram()
        diagrams = {}
        data_sol = st.session_state.data_sol
        labels = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9", "Z10", "Z11", "Z12", "Z13", "Z14"]
        n = len(data_sol)
        
        # Отладочная информация - покажем реальные значения
        st.write("**Реальные значения параметров:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("Начальные:")
            for i, val in enumerate(data_sol[0]):
                st.write(f"Z{i+1}: {val:.3f}")
        
        with col2:
            quarter_idx = n // 4
            st.write(f"1/4 времени (шаг {quarter_idx}):")
            for i, val in enumerate(data_sol[quarter_idx]):
                st.write(f"Z{i+1}: {val:.3f}")
        
        with col3:
            st.write("Конечные:")
            for i, val in enumerate(data_sol[-1]):
                st.write(f"Z{i+1}: {val:.3f}")
   
        diagrams['initial'] = radar.draw([data_sol[0]], labels, 
                                       "Характеристики системы в начальный момент времени")
        
        quarter_idx = n // 4
        diagrams['quarter'] = radar.draw([data_sol[0], data_sol[quarter_idx]], labels,
                                       "Характеристики системы в 1 четверти")
        
        half_idx = n // 2
        diagrams['half'] = radar.draw([data_sol[0], data_sol[half_idx]], labels,
                                    "Характеристики системы во 2 четверти")
        
        three_quarter_idx = 3 * n // 4
        diagrams['three_quarters'] = radar.draw([data_sol[0], data_sol[three_quarter_idx]], labels,
                                              "Характеристики системы в 3 четверти")
        
        diagrams['final'] = radar.draw([data_sol[0], data_sol[-1]], labels,
                                     "Характеристики системы в последний момент времени")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Начальный момент")
            st.pyplot(diagrams['initial'])
            
            st.subheader("1/2 времени")
            st.pyplot(diagrams['half'])
            
            st.subheader("Конечный момент")
            st.pyplot(diagrams['final'])
        
        with col2:
            st.subheader("1/4 времени")
            st.pyplot(diagrams['quarter'])
            
            st.subheader("3/4 времени")
            st.pyplot(diagrams['three_quarters'])
            
    else:
        st.info("Выполните вычисления на вкладке 'Параметры' чтобы увидеть диаграммы")


with tab4:
    st.header("Графики функций системы")
    
    if st.session_state.calculation_done and st.session_state.free_members is not None:
        t = st.session_state.t
        fig = process.draw_functions_graphic(t, st.session_state.free_members)
        
        fig.set_size_inches(12, 8)
        ax = fig.gca()
        ax.set_xlabel('Время')
        ax.set_ylabel('Значение функции')
        ax.set_title('Графики 7 функций системы')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры'")

st.markdown("---")
st.markdown("**Система дифференциальных уравнений для моделирования последствий наводнения**")