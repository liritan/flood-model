# web_app_flood.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import functions as functions
import process as process
from radar_diagram import RadarDiagram

st.set_page_config(page_title="Модель последствий наводнения", layout="wide")

# Инициализация сессии
if 'data_sol' not in st.session_state:
    st.session_state.data_sol = None
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
if 'free_members' not in st.session_state:
    st.session_state.free_members = None

# Заголовок
st.title("Модель анализа последствий наводнения")

# Вкладки 
tab1, tab2, tab3, tab4 = st.tabs(["Параметры", "Графики", "Диаграмма", "Возмущение"])

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
    
    free_members = []
    selected_functions = []
    
    # Создаем 66 функций (f1-f66) согласно PDF
    for i in range(66):
        with st.expander(f"f{i+1}(x) - {process.get_function_description(i)}", expanded=False):
            func_type = process.get_function_type(i)
            default_coeffs = process.get_default_coefficients(i)
            
            col_header = st.columns([1, 3])
            with col_header[0]:
                func_select = st.selectbox(
                    f"f{i+1}(x) →",
                    options=list(range(1, 128)),
                    index=min(i, 126),
                    key=f"func_{i}_select"
                )
                selected_functions.append(func_select)
            with col_header[1]:
                st.write(f"F{func_select}(x)")
            
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

    st.markdown("---")
    
    col_status1, col_status2, col_status3 = st.columns([1, 2, 1])
    with col_status2:
        status_placeholder = st.empty()
        status_placeholder.text("Статус: Ожидание вычислений")
    
    col_calc1, col_calc2, col_calc3 = st.columns([1, 2, 1])
    with col_calc2:
        if st.button("Вычислить", use_container_width=True, key="main_calculate"):
            with st.spinner("Выполняется расчет последствий наводнения..."):
                try:
                    # Сохраняем уравнения в сессии
                    st.session_state.free_members = free_members
                    st.session_state.selected_functions = selected_functions
                    
                    # Устанавливаем параметры
                    process.free_members_of_fun_expr = free_members
                    
                    # Инициализация функций
                    process.dict_of_function_expressions.clear()
                    
                    # Применяем выбранные функции
                    for j in range(min(66, len(selected_functions))):
                        process.activatedCombox(j, str(selected_functions[j]))
                    
                    # Время моделирования
                    t = np.linspace(0, 1, 80)
                    
                    # Выполняем расчет
                    t, data_sol = process.process_calculation(start_values, free_members)
                    
                    # Сохраняем результаты
                    st.session_state.data_sol = data_sol
                    st.session_state.t = t
                    st.session_state.calculation_done = True
                    
                    status_placeholder.text("Статус: Успешно")
                    st.success("Моделирование последствий наводнения завершено успешно!")
                    
                except Exception as e:
                    status_placeholder.text("Статус: Ошибка")
                    st.error(f"Ошибка при вычислении: {str(e)}")

with tab2:
    st.header("Динамика параметров последствий наводнения")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        if st.button("Построить график"):
            t = st.session_state.t
            data_sol = st.session_state.data_sol
            labels = process.labels_array()
            
            fig, ax = plt.subplots(figsize=(15, 10))
            for i in range(14):
                ax.plot(t, data_sol[:, i], label=labels[i], linewidth=2)
            
            ax.set_xlabel('Время')
            ax.set_ylabel('Значение')
            ax.set_title('Динамика параметров последствий наводнения')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_xlim([0, 1])
            
            st.pyplot(fig)
            
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
        st.info("Выполните вычисления на вкладке 'Параметры' чтобы увидеть график")

with tab3:
    st.header("Радар-диаграммы параметров наводнения")
    
    if st.session_state.calculation_done and st.session_state.data_sol is not None:
        radar = RadarDiagram()
        diagrams = {}
        data_sol = st.session_state.data_sol
        labels = process.labels_array()
        n = len(data_sol)
        
        diagrams['initial'] = radar.draw([data_sol[0]], labels, 
                                       "Параметры в начальный момент времени")
        
        quarter_idx = n // 4
        diagrams['quarter'] = radar.draw([data_sol[0], data_sol[quarter_idx]], labels,
                                       "Параметры в 1 четверти")
        
        half_idx = n // 2
        diagrams['half'] = radar.draw([data_sol[0], data_sol[half_idx]], labels,
                                    "Параметры во 2 четверти")
        
        three_quarter_idx = 3 * n // 4
        diagrams['three_quarters'] = radar.draw([data_sol[0], data_sol[three_quarter_idx]], labels,
                                              "Параметры в 3 четверти")
        
        diagrams['final'] = radar.draw([data_sol[0], data_sol[-1]], labels,
                                     "Параметры в конечный момент времени")
        
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
    st.header("Коэффициенты возмущений")
    
    if st.session_state.calculation_done and st.session_state.free_members is not None:
        t = st.session_state.t
        fig = process.draw_third_graphic(t)
        
        fig.set_size_inches(10, 6)
        ax = fig.gca()
        ax.set_xlabel('Время')
        ax.set_ylabel('Значение')
        ax.set_title('Временные коэффициенты возмущений для функций наводнения')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        st.download_button(
            label="📥 Скачать график возмущений",
            data=buf.getvalue(),
            file_name="график_возмущений_наводнения.png",
            mime="image/png",
            use_container_width=True
        )
        
    else:
        st.info("Выполните вычисления на вкладке 'Параметры' чтобы увидеть графики возмущений")

st.markdown("---")
st.write("Модель анализа последствий наводнения - Оценка параметров чрезвычайной ситуации")