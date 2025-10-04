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

tab1, tab2, tab3, tab4 = st.tabs(["📊 Параметры", "📈 Графики", "🎯 Диаграмма", "⚡ Функции"])

with tab1:
    st.header("Входные параметры характеристик наводнения")
    
    start_values = []
    labels = process.labels_array()
    
    # Создаем 14 полей ввода (Z1-Z14) в 2 колонки
    cols = st.columns(2)
    for i in range(14):
        with cols[i % 2]:
            default_values = {
                0: 0.1, 1: 0.3, 2: 0.2, 3: 0.4, 4: 0.3, 
                5: 0.5, 6: 0.4, 7: 0.3, 8: 0.6, 9: 0.2,
                10: 0.4, 11: 0.5, 12: 0.3, 13: 0.4
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
    st.header("Радар-диаграммы параметров")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        radar = RadarDiagram()
        data_sol = st.session_state.data_sol
        labels = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9", "Z10", "Z11", "Z12", "Z13", "Z14"]
        n = len(data_sol)
        
        # Вычисляем индексы для промежуточных состояний
        indices = {
            'Начальный момент': 0,
            '1/8 времени': n // 8,
            '1/4 времени': n // 4, 
            '3/8 времени': 3 * n // 8,
            '1/2 времени': n // 2,
            '5/8 времени': 5 * n // 8,
            '3/4 времени': 3 * n // 4,
            '7/8 времени': 7 * n // 8,
            'Конечный момент': n - 1
        }
        
        st.subheader("📊 Все состояния системы")
        
        # Создаем диаграмму со всеми состояниями
        all_data = [data_sol[idx] for idx in indices.values()]
        fig_all = radar.draw(all_data, labels, "Динамика системы во времени")
        st.pyplot(fig_all)
        
        st.subheader("🔍 Детальный анализ по состояниям")
        
        # Показываем отдельные диаграммы для ключевых моментов
        key_moments = {
            'Начальный момент': 0,
            '1/4 времени': n // 4,
            '1/2 времени': n // 2,
            '3/4 времени': 3 * n // 4,
            'Конечный момент': n - 1
        }
        
        cols = st.columns(3)
        col_idx = 0
        
        for moment_name, idx in key_moments.items():
            with cols[col_idx]:
                st.write(f"**{moment_name}**")
                fig_moment = radar.draw([data_sol[idx]], labels, f"t = {idx}/{n}")
                st.pyplot(fig_moment)
                
                # Показываем значения параметров
                with st.expander("Значения параметров"):
                    for i, value in enumerate(data_sol[idx]):
                        st.write(f"{labels[i]}: {value:.3f}")
            
            col_idx = (col_idx + 1) % 3
            
        st.subheader("📈 Сравнительный анализ")
        
        # Сравнение начального и конечного состояния
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Начальное vs Конечное состояние**")
            fig_comparison = radar.draw([data_sol[0], data_sol[-1]], labels, 
                                      "Сравнение начального и конечного состояния")
            st.pyplot(fig_comparison)
            
        with col2:
            st.write("**Изменения параметров**")
            changes = data_sol[-1] - data_sol[0]
            
            # График изменений
            fig_changes, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(range(14), changes, color=['red' if x < 0 else 'green' for x in changes])
            ax.set_xlabel('Параметры')
            ax.set_ylabel('Изменение')
            ax.set_title('Изменение параметров от начального до конечного состояния')
            ax.set_xticks(range(14))
            ax.set_xticklabels([f'Z{i+1}' for i in range(14)], rotation=45)
            ax.grid(True, alpha=0.3)
            
            # Добавляем значения на столбцы
            for bar, change in zip(bars, changes):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{change:+.3f}', ha='center', va='bottom' if height >= 0 else 'top')
            
            st.pyplot(fig_changes)
            
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры' чтобы увидеть диаграммы")

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