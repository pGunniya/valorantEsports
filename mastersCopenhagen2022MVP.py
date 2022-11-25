import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def radar_factory(num_vars, frame='circle'):
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
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        PolarTransform = RadarTransform

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


def example_data():
    # The following data is from the Denver Aerosol Sources and Health study.
    # See doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase species is present...
    data = [
        ['Kills', 'ACS', 'K-D Difference', 'Assists', 'KAST%', 'ADR', 'HS%', 'First Kills', 'First Kill Difference'],
        ('Icebox', [
            [0.7,	0.803448276,	0,	1,	1,	0.79787234,	0.41, 0, 0],
            [0.95,	0.910344828,	1,	0.363636364,	0.833333333,	0.835106383,	0.52,	1,	1],
            [1	,1	,0.66	,0.545454545	,0.777777778	,1	,0.25	,1	,1],
            [0.8	,0.827586207	,0.33	,0.636363636	,0.888888889	,0.808510638	,0.29	,0.66	,1],
            [0.75	,0.686206897	,0	,0.363636364	,0.722222222	,0.760638298	,0.44,	0.66	,1]]),
        ('Fracture', [
            [0.681818182	,0.75432526	,0.666	,1	,1,	1	,.33,	0.666	,1],
            [0.681818182,	0.747404844	,0.5	,0.1	,0.8	,0.781420765	,.14	,0.666	,0],
            [0.727272727,	0.757785467,	0.333,	0.4,	0.866666667	,0.74863388	,.20,	0.166	,0],
            [1	,1,	0.833,	0.5	,1	,0.928961749	,.23	,0.166	,1],
           [0.545454545	,0.574394464	,0.166,	0.4	,0.8	,0.595628415	,.18,	0.166	,0]]),
        ('Haven', [
            [0.72,	0.740524781	,0.666,	0.5	,0.866666667	,0.792079208	,.35	,0.333,	0.5],
            [0.64,	0.67638484,	0.5,	0.375,	0.933333333,	0.742574257,	.42	,0.333,	0.166],
            [1,	1	,0.833	,0.125,	1,	1	,.18,	0.833	,0.833],
            [0.32	,0.38483965	,0.166,	1	,0.733333333	,0.52970297,	.16	,0.166	,0.5],
            [0.52,	0.56851312,	0.333	,0.625,	0.866666667,	0.643564356,	.26	,0.333	,0.166]]),
        ('Breeze', [
            [0.85,	0.843636364,	0.833	,0.857142857	,0.948051948	,0.828571429	,0.5	,0.166,	0.5],
            [0.75,	0.683636364,	0.333	,0.714285714	,1,	0.72,	0.37,	0.5	,0.5],
            [1	,1,	0.5	,0.714285714	,0.948051948	,1,	0.27,	0.833,	0.166],
            [0.95,	0.88,	0.5	,0.571428571,	0.831168831	,0.954285714	,0.45,	0.166	,0.833],
            [0.6,	0.581818182,	0.166,	1,	0.831168831	,0.605714286,	0.21,	0.5	,0.333]])
    ]
    return data


if __name__ == '__main__':
    N = 9
    theta = radar_factory(N, frame='polygon')

    data = example_data()
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    labels = ('Shao', 'Zyppan', 'Jinggg', 'SUGETSU', 'ANGE1')
    legend = axs[0, 0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')

    fig.text(0.5, 0.965, 'Top 5 players across the last 4 maps of Masters Copenhagen 2022',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()