import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval

from graph import *

graph_data = Graph()
graph_data.debug_create_test_data()
print(graph_data.vertexes[0].pos)

N = len(graph_data.vertexes)
node_indices = list(range(N))
color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)
print(color_list)

plot = figure(title='Graph Layout Demonstration', x_range=(0, 500), y_range=(0, 500),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Oval(height=20, width=20, fill_color='color')

graph.edge_renderer.data_source.data = dict(
    start=[0]*N,
    end=node_indices)
# start of layout code
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


def bezier(start, end, control, steps):
    return [(1-s)**2*start + 2*(1-s)*s*control + s**2*end for s in steps]


xs, ys = [], []
for vertex in graph_data.vertexes:
    for edge in vertex.edges:
        xs.extend([[vertex.pos['x'], edge.destination.pos['x']],
                   [vertex.pos['x'], edge.destination.pos['x']]])
        ys.extend([[vertex.pos['y'], edge.destination.pos['y']],
                   [vertex.pos['y'], edge.destination.pos['y']]])
graph.edge_renderer.data_source.data['xs'] = xs
graph.edge_renderer.data_source.data['ys'] = ys

print("XS:" + str(xs))
print("YS:" + str(ys))

plot.renderers.append(graph)

output_file('graph.html')
show(plot)
