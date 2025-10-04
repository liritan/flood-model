import numpy as np
import matplotlib.pyplot as plt

class RadarDiagram:
    def draw(self, data, labels, title):
        """
        Создание радар-диаграммы
        
        Parameters:
        data - список массивов данных (каждый массив должен иметь длину как labels)
        labels - список меток параметров
        title - заголовок диаграммы
        """
        try:
            N = len(labels)
            theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
            
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            # Цвета для разных состояний
            colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
            
            for idx, dataset in enumerate(data):
                # Преобразуем в numpy array и убеждаемся в правильной длине
                dataset_array = np.array(dataset)
                
                # Если данных меньше чем меток, дополняем нулями
                if len(dataset_array) < N:
                    dataset_array = np.pad(dataset_array, (0, N - len(dataset_array)), 'constant')
                # Если данных больше, обрезаем
                elif len(dataset_array) > N:
                    dataset_array = dataset_array[:N]
                
                # Замыкаем полигон (добавляем первый элемент в конец)
                values = np.concatenate([dataset_array, [dataset_array[0]]])
                current_theta = np.concatenate([theta, [theta[0]]])
                
                # Проверяем что длины совпадают
                if len(current_theta) != len(values):
                    st.error(f"Ошибка размеров: theta={len(current_theta)}, values={len(values)}")
                    continue
                
                color = colors[idx % len(colors)]
                label = f'Состояние {idx+1}' if len(data) > 1 else 'Текущее состояние'
                
                ax.plot(current_theta, values, 'o-', linewidth=2, label=label, color=color, markersize=4)
                ax.fill(current_theta, values, alpha=0.1, color=color)
            
            # Настройка осей и меток
            ax.set_xticks(theta)
            ax.set_xticklabels(labels)
            ax.set_title(title, size=14, weight='bold')
            ax.grid(True)
            
            # Добавляем легенду если несколько состояний
            if len(data) > 1:
                ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            
            # Настраиваем пределы
            try:
                all_values = np.concatenate([np.array(d)[:N] for d in data])
                max_val = np.max(all_values)
                min_val = np.min(all_values)
                margin = (max_val - min_val) * 0.1
                ax.set_ylim(max(0, min_val - margin), max_val + margin)
            except:
                ax.set_ylim(0, 1)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            # Создаем простую диаграмму в случае ошибки
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, f'Ошибка построения диаграммы:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig