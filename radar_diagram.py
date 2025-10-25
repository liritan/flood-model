
import matplotlib
matplotlib.use('Agg')  # Важно для серверов без GUI
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


class RadarDiagram:
    def radar_factory(self, num_vars, frame='circle'):
        """
        Create a radar chart with `num_vars` axes.

        This function creates a RadarAxes projection and registers it.

        Parameters
        ----------
        num_vars : int
            Number of variables for radar chart.
        frame : {'circle', 'polygon'}
            Shape of frame surrounding axes.

        """
        # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):

            name = 'radar'
            # use 1 line segment to connect specified points
            RESOLUTION = 1

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # rotate plot such that the first axis is at the top
                self.set_theta_zero_location('N')

            def fill(self, *args, closed=True, **kwargs):
                """Override fill so that line is closed by default"""
                return super().fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                """Override plot so that line is closed by default"""
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.append(x, x[0])
                    y = np.append(y, y[0])
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
                # in axes coordinates.
                if frame == 'circle':
                    return Circle((0.5, 0.5), 0.5)
                elif frame == 'polygon':
                    return RegularPolygon((0.5, 0.5), num_vars,
                                          radius=.5, edgecolor="k")
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

            def _gen_axes_spines(self):
                if frame == 'circle':
                    return super()._gen_axes_spines()
                elif frame == 'polygon':
                    # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                    spine = Spine(axes=self,
                                  spine_type='circle',
                                  path=Path.unit_regular_polygon(num_vars))
                    # unit_regular_polygon gives a polygon of radius 1 centered at
                    # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                    # 0.5) in axes coordinates.
                    spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                        + self.transAxes)
                    return {'polar': spine}
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

        register_projection(RadarAxes)
        return theta

  
    # def draw(self, filename, initial_data, current_data, label, title, show_both_lines=True):
    #     N = 12
    #     theta = self.radar_factory(N, frame='polygon')

    #     fig, axs = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='radar'))
    #     fig.subplots_adjust(wspace=1, hspace=1, top=0.85, bottom=0.05)

    #     if show_both_lines:
    #         # Рисуем две линии: начальные условия и текущие характеристики
    #         axs.plot(theta, initial_data, color='b', linewidth=2)
    #         axs.plot(theta, current_data, color='r', linewidth=2)
    #         # Обновляем легенду для двух линий
    #         axs.legend(["Начальные характеристики", "Текущие характеристики"], 
    #                 loc=(-.13, .99), labelspacing=0.1, fontsize='medium')
    #     else:
    #         # Рисуем только одну линию (для начального момента)
    #         axs.plot(theta, initial_data, color='b', linewidth=2)
    #         # Легенда для одной линии
    #         axs.legend(["Начальные характеристики"], 
    #                 loc=(-.13, .99), labelspacing=0.1, fontsize='medium')
        
    #     axs.set_varlabels(["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12"])

    #     fig.text(0.5, 0.965, title,
    #             horizontalalignment='center', color='black', weight='bold',
    #             size='large')
    #     fig.savefig(filename)
    #     plt.close(fig)
    def draw(self, filename, initial_data, current_data, label, title, show_both_lines=True):
        N = 12
        theta = self.radar_factory(N, frame='polygon')

        fig, axs = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(wspace=1, hspace=1, top=0.85, bottom=0.05)

        # Устанавливаем пределы для радар-диаграммы
        axs.set_ylim(0, 1.0)

        if show_both_lines:
            # Рисуем две линии: начальные условия и текущие характеристики
            axs.plot(theta, initial_data, color='b', linewidth=2)
            axs.plot(theta, current_data, color='r', linewidth=2)
            # Обновляем легенду для двух линий
            axs.legend(["Начальные характеристики", "Текущие характеристики"], 
                    loc=(-.13, .99), labelspacing=0.1, fontsize='medium')
        else:
            # Рисуем только одну линию (для начального момента)
            axs.plot(theta, initial_data, color='b', linewidth=2)
            # Легенда для одной линии
            axs.legend(["Начальные характеристики"], 
                    loc=(-.13, .99), labelspacing=0.1, fontsize='medium')
        
        axs.set_varlabels(["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10", "X11", "X12"])

        fig.text(0.5, 0.965, title,
                horizontalalignment='center', color='black', weight='bold',
                size='large')
        fig.savefig(filename)
        plt.close(fig)