import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, GraphRenderer, StaticLayoutProvider, Oval, LabelSet
from bokeh.colors.groups import *

from graph import *

WIDTH = 500
HEIGHT = 500

graph_data = Graph()
graph_data.debug_create_test_data()
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes)
node_indices = list(range(N))
color_list = []
# color_list = cyan._colors[0:N]
value_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)
    value_list.append(vertex.value)


plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.data_source.add(value_list, 'value')

graph.node_renderer.glyph = Oval(height=30, width=30, fill_color='color')


graph.edge_renderer.data_source.data = dict(
    start=[0]*N,
    end=node_indices)
# start of layout code
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]
values = [v.value for v in graph_data.vertexes]


labelData = ColumnDataSource(data=dict(x=x, y=y, values=values))

labels = LabelSet(x='x', y='y', text='values', level='glyph', text_align='center',
                  text_baseline='middle', source=labelData, render_mode='canvas')
graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


xs, ys = [], []
for vertex in graph_data.vertexes:
    xpoints, ypoints = [], []
    for edge in vertex.edges:
        xpoints.extend([vertex.pos['x'], edge.destination.pos['x']])
        ypoints.extend([vertex.pos['y'], edge.destination.pos['y']])
    xs.append(xpoints)
    ys.append(ypoints)


graph.edge_renderer.data_source.data['xs'] = xs
graph.edge_renderer.data_source.data['ys'] = ys


plot.renderers.append(graph)
plot.add_layout(labels)

output_file('graph.html')
show(plot)
