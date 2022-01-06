import csv
import numpy
import os
import plotly
from plotly import graph_objs
from sys import platform
import webbrowser

DEFAULT_CHART_FILE = os.path.join('star_charts', 'chart.html')
DEFAULT_CSV_FILE = os.path.join('Systems-Database', 'systems.csv')


def plot(points, point_colors, filename=DEFAULT_CHART_FILE):
    """
    """
    figure = graph_objs.Figure()
    x, y, z = zip(*points)
    trace1 = graph_objs.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            symbol='circle',
            size=6,
            color=point_colors,
            colorscale='Viridis',
            line=dict(color='rgb(50,50,50)', width=0.5)
        ),
    )
    data = [trace1]
    fig = graph_objs.Figure(data=data)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    plotly.offline.plot(fig, filename=filename, auto_open=False)
    file_to_open = os.path.abspath(filename)
    if platform == 'darwin':
        file_to_open = 'file:///' + file_to_open
    print(f'Opening {file_to_open}...')
    webbrowser.get().open(file_to_open)


def get_systems(filename=DEFAULT_CSV_FILE):
    """
    """
    systems = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for d in reader:
            systems.append(d)

    return sorted(systems, key=lambda d: d['distance (pc)'])

print(get_systems())

points = list(zip(numpy.random.rand(100), numpy.random.rand(100), numpy.random.rand(100)))
point_colors = numpy.random.rand(100)
plot(points, point_colors)