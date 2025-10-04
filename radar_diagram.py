import numpy as np
import matplotlib.pyplot as plt

class RadarDiagram:
    def draw(self, data, labels, title):
        N = len(labels)
        theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Цвета для разных состояний
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
        
        for idx, dataset in enumerate(data):
            # Убеждаемся, что данные имеют правильную длину
            if len(dataset) != N:
                # Если длина не совпадает, берем первые N элементов или дополняем нулями
                if len(dataset) > N:
                    values = dataset[:N].tolist()
                else:
                    values = dataset.tolist() + [0] * (N - len(dataset))
            else:
                values = dataset.tolist()
            
            # Замыкаем полигон
            values += values[:1]
            current_theta = theta.tolist() + theta[:1]
            
            color = colors[idx % len(colors)]
            label = f'Состояние {idx+1}' if len(data) > 1 else 'Текущее состояние'
            
            ax.plot(current_theta, values, 'o-', linewidth=2, label=label, color=color, markersize=4)
            ax.fill(current_theta, values, alpha=0.1, color=color)
        
        ax.set_xticks(theta)
        ax.set_xticklabels(labels)
        ax.set_title(title, size=14, weight='bold')
        ax.grid(True)
        
        # Добавляем легенду если несколько состояний
        if len(data) > 1:
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        # Настраиваем пределы для лучшего отображения
        try:
            max_val = max([max(dataset) for dataset in data])
            ax.set_ylim(0, max_val * 1.1)
        except:
            ax.set_ylim(0, 1)
        
        return fig