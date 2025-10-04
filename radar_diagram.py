# radar_diagram_flood.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

class RadarDiagram():
    def radar_factory(self, num_vars, frame='circle'):
        theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):
            name = 'radar'
            RESOLUTION = 1

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_theta_zero_location('N')

            def fill(self, *args, closed=True, **kwargs):
                return super().fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                if x[0] != x[-1]:
                    x = np.append(x, x[0])
                    y = np.append(y, y[0])
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                if frame == 'circle':
                    return Circle((0.5, 0.5), 0.5)
                elif frame == 'polygon':
                    return RegularPolygon((0.5, 0.5), num_vars, radius=.5, edgecolor="k")
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

            def _gen_axes_spines(self):
                if frame == 'circle':
                    return super()._gen_axes_spines()
                elif frame == 'polygon':
                    spine = Spine(axes=self, spine_type='circle',
                                path=Path.unit_regular_polygon(num_vars))
                    spine.set_transform(Affine2D().scale(.5).translate(.5, .5) + self.transAxes)
                    return {'polar': spine}
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

        register_projection(RadarAxes)
        return theta

    def draw(self, data, labels, title):
        N = len(labels)
        theta = self.radar_factory(N, frame='polygon')

        spoke_labels = labels

        fig, axs = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(wspace=1, hspace=1, top=0.85, bottom=0.05)

        colors = ['b', 'r', 'g', 'orange']
        
        # Масштабирование 
        all_data = np.concatenate(data)
        axs.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0])

        for ind, dataset in enumerate(data):
            axs.plot(theta, dataset, color=colors[ind % len(colors)], linewidth=2)
            axs.fill(theta, dataset, color=colors[ind % len(colors)], alpha=0.1)
            
        axs.set_varlabels(spoke_labels)

        legend_labels = ['Начало', '1/4 времени', '1/2 времени', '3/4 времени', 'Конец']
        axs.legend(legend_labels[:len(data)], loc=(-.13, .99), labelspacing=0.1, fontsize='medium')

        # Заголовок 
        fig.text(0.5, 0.965, title, horizontalalignment='center', 
                color='black', weight='bold', size='large')

        return fig