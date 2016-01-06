import plotly.plotly as plt
import plotly.graph_objs as graphobjs


class Plotter(object):
	def __init__(self, *traces):
		self.traces = traces

	def plot(self):
		for trace in traces:
