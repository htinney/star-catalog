import csv
import numpy
import os
import plotly
from plotly import graph_objs
from sys import platform
import webbrowser

DEFAULT_CHART_FILE = os.path.join('star_charts', 'chart.html')
DEFAULT_CSV_FILE = os.path.join('Systems-Database', 'systems.csv')


def plot(points, edges, point_colors, labels, filename=DEFAULT_CHART_FILE):
    """
    """
    figure = graph_objs.Figure()
    edge_x, edge_y, edge_z = zip(*edges)
    point_x, point_y, point_z = zip(*points)

    trace2 = graph_objs.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode='lines',
        line=dict(color='rgb(125,125,125)', width=1),
        hoverinfo='none'
    )

    trace1 = graph_objs.Scatter3d(
        x=point_x,
        y=point_y,
        z=point_z,
        mode='markers',
        marker=dict(
            symbol='circle',
            size=6,
            color=point_colors,
            colorscale='Viridis',
            line=dict(color='rgb(50,50,50)', width=0.5)
        ),
        text=labels,
        hoverinfo='text',
    )
    
    data = [trace1, trace2]
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
            d['x'] = float(d['x'])
            d['y'] = float(d['y'])
            d['z'] = float(d['z'])
            systems.append(d)

    return sorted(systems, key=lambda d: d['distance (pc)'])

systems = get_systems()
print(systems)
points = [(s['x'], s['y'], s['z']) for s in systems]
labels = [s['proper'] for s in systems]
edges = []
for s in systems:
    target = (s['x'], s['y'], s['z'])
    origin_system = next((x for x in systems if x['proper'] == s['prev']), None)
    if origin_system is None:
        continue
    origin = (origin_system['x'], origin_system['y'], origin_system['z'])
    edges += [origin, target, (None, None, None)]

#points = list(zip(numpy.random.rand(100), numpy.random.rand(100), numpy.random.rand(100)))
#point_colors = numpy.random.rand(100)
point_colors = [0.25 if int(s['habitable']) > 0 else 0.75 for s in systems]
plot(points, edges, point_colors, labels)