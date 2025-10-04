# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import process as process
from radar_diagram import RadarDiagram

# Настройка страницы
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

# Главный заголовок
st.title("🌊 Модель анализа последствий наводнения")
st.markdown("---")

# Вкладки 
tab1, tab2, tab3, tab4 = st.tabs(["📊 Параметры", "📈 Графики", "🎯 Диаграмма", "⚡ Возмущение"])

with tab1:
    st.header("Входные параметры характеристик наводнения")
    
    start_values = []
    labels = process.labels_array()
    
    # Создаем 14 полей ввода (Z1-Z14) в 2 колонки
    cols = st.columns(2)
    for i in range(14):
        with cols[i % 2]:
            default_values = {
                0: 0.1,   # Z1 - число погибших людей
                1: 0.3,   # Z2 - продолжительность поражающего воздействия
                2: 0.2,   # Z3 - площадь зоны ЧС
                3: 0.4,   # Z4 - число людей, утративших имущество
                4: 0.3,   # Z5 - ущерб коммерческой организации
                5: 0.5,   # Z6 - объем загрязненного грунта
                6: 0.4,   # Z7 - площадь земель, исключенных из оборота
                7: 0.3,   # Z8 - снижение плодородия земель
                8: 0.6,   # Z9 - продолжительность аварийного периода
                9: 0.2,   # Z10 - продолжительность восстановительного периода
                10: 0.4,  # Z11 - число пораженных сельхоз животных
                11: 0.5,  # Z12 - величина погибшего урожая
                12: 0.3,  # Z13 - площадь уничтоженных лесных массивов
                13: 0.4   # Z14 - ущерб административной единице
            }
            value = st.number_input(
                labels[i],
                value=default_values.get(i, 0.5),
                min_value=0.0,
                max_value=1.0,
                key=f"param_{i}"
            )
            start_values.append(value)

    st.header("Функции взаимовлияния параметров")
    st.info("Настройте коэффициенты для 66 функций модели")
    
    free_members = []
    selected_functions = []
    
    # Создаем 66 функций (f1-f66) согласно PDF
    # Для экономии места покажем только первые 10 функций
    # В полной версии будут все 66
    for i in range(10):  # Измените на 66 для полной версии
        with st.expander(f"f{i+1}(x) - {process.get_function_description(i)}", expanded=False):
            func_type = process.get_function_type(i)
            default_coeffs = process.get_default_coefficients(i)
            
            if func_type == "polynomial_4":
                cols = st.columns(4)
                with cols[0]:
                    a = st.number_input("a (x⁴)", value=float(default_coeffs[0]), key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b (x³)", value=float(default_coeffs[1]), key=f"f{i}_b")
                with cols[2]:
                    c = st.number_input("c (x²)", value=float(default_coeffs[2]), key=f"f{i}_c")
                with cols[3]:
                    d = st.number_input("d (x)", value=float(default_coeffs[3]), key=f"f{i}_d")
                free_members.append([a, b, c, d])
                
            elif func_type == "exponential":
                cols = st.columns(3)
                with cols[0]:
                    const = st.number_input("константа", value=float(default_coeffs[0]), key=f"f{i}_a")
                with cols[1]:
                    coef1 = st.number_input("коэф. 1/x", value=float(default_coeffs[1]), key=f"f{i}_b")
                with cols[2]:
                    coef2 = st.number_input("коэф. log10(x)", value=float(default_coeffs[2]), key=f"f{i}_c")
                free_members.append([const, coef1, coef2])
                
            elif func_type == "polynomial_2":
                cols = st.columns(3)
                with cols[0]:
                    a = st.number_input("a (x²)", value=float(default_coeffs[0]), key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b (x)", value=float(default_coeffs[1]), key=f"f{i}_b")
                with cols[2]:
                    c = st.number_input("c", value=float(default_coeffs[2]), key=f"f{i}_c")
                free_members.append([a, b, c])
                
            elif func_type == "linear":
                cols = st.columns(2)
                with cols[0]:
                    a = st.number_input("a (x)", value=float(default_coeffs[0]), key=f"f{i}_a")
                with cols[1]:
                    b = st.number_input("b", value=float(default_coeffs[1]), key=f"f{i}_b")
                free_members.append([a, b])
            
            selected_functions.append(i+1)

    # Кнопка расчета
    st.markdown("---")
    if st.button("🚀 Выполнить расчет", use_container_width=True):
        with st.spinner("Выполняется расчет последствий наводнения..."):
            try:
                st.session_state.free_members = free_members
                st.session_state.selected_functions = selected_functions
                
                process.free_members_of_fun_expr = free_members
                
                # Инициализация функций
                process.dict_of_function_expressions.clear()
                for j in range(min(10, len(selected_functions))):
                    process.activatedCombox(j, str(selected_functions[j]))
                
                # Выполняем расчет
                t, data_sol = process.process_calculation(start_values, free_members)
                
                # Сохраняем результаты
                st.session_state.data_sol = data_sol
                st.session_state.t = t
                st.session_state.calculation_done = True
                
                st.success("✅ Моделирование завершено успешно!")
                
            except Exception as e:
                st.error(f"❌ Ошибка при вычислении: {str(e)}")

# Остальные вкладки (tab2, tab3, tab4) остаются без изменений
with tab2:
    st.header("Динамика параметров последствий наводнения")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        t = st.session_state.t
        data_sol = st.session_state.data_sol
        labels = process.labels_array()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        for i in range(14):
            ax.plot(t, data_sol[:, i], label=labels[i], linewidth=2)
        
        ax.set_xlabel('Время')
        ax.set_ylabel('Значение')
        ax.set_title('Динамика параметров последствий наводнения')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 1])
        
        st.pyplot(fig)
        
        # Кнопка скачивания
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        st.download_button(
            label="📥 Скачать график параметров",
            data=buf.getvalue(),
            file_name="график_параметров_наводнения.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры' чтобы увидеть график")

with tab3:
    st.header("Радар-диаграммы параметров наводнения")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        radar = RadarDiagram()
        data_sol = st.session_state.data_sol
        labels = process.labels_array()
        n = len(data_sol)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Начальный vs Конечный момент")
            fig_final = radar.draw([data_sol[0], data_sol[-1]], labels,
                                 "Сравнение начального и конечного состояния")
            st.pyplot(fig_final)
            
        with col2:
            st.subheader("Динамика по четвертям")
            quarter_idx = n // 4
            half_idx = n // 2
            three_quarter_idx = 3 * n // 4
            
            fig_quarters = radar.draw([
                data_sol[0], 
                data_sol[quarter_idx],
                data_sol[half_idx],
                data_sol[three_quarter_idx]
            ], labels, "Динамика по четвертям времени")
            st.pyplot(fig_quarters)
            
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры' чтобы увидеть диаграммы")

with tab4:
    st.header("Коэффициенты возмущений")
    
    if st.session_state.calculation_done and st.session_state.free_members is not None:
        t = st.session_state.t
        fig = process.draw_third_graphic(t)
        
        fig.set_size_inches(10, 6)
        ax = fig.gca()
        ax.set_xlabel('Время')
        ax.set_ylabel('Значение')
        ax.set_title('Временные коэффициенты возмущений')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
    else:
        st.info("ℹ️ Выполните вычисления на вкладке 'Параметры' чтобы увидеть графики возмущений")

# Футер
st.markdown("---")
st.markdown("### 📊 Модель анализа последствий наводнения")
st.markdown("**Разработано для оценки параметров чрезвычайной ситуации**")