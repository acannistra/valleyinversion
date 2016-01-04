# coding=utf8


from bs4 import BeautifulSoup
import requests
import plotly.plotly as plt
import plotly.graph_objs as graphobjs
from numpy import array
from scipy.stats import linregress

def is_number(x):
	try:
		int(x)
		return True
	except ValueError:
		return False

WEATHER_URL = "http://avalanche.state.co.us/caic/obs_stns/zones.php"
REGION      = "Aspen"

weather_raw = requests.get(WEATHER_URL)

parser = BeautifulSoup(weather_raw.text, "html.parser")

## Parse CAIC data
weather_table_raw = parser.find("h4", text=REGION).find_next("table").find_all("tr")
table_header      = [head.text for head in weather_table_raw[0].find_all("th")]
weather_stations  = [dict(zip(table_header, [cell.text for cell in row.find_all("td")])) for row in weather_table_raw[1:-1]]

## massage data into usable format
### get rows with actual temperature information
weather_stations  = [(int(row["Elev"]), int(row["Temp"]), row["Station"]) for row in weather_stations if is_number(row["Temp"])]
print weather_stations[0]
weather_stations  = sorted(weather_stations, lambda e,t: e[0], reverse=True)

## calculate line of best fit
elevs, temps, labels = zip(*weather_stations)
slope, intercept, r_value, p_value, std_err = linregress(elevs, temps)
fit_line = slope*array(elevs)+intercept

## plot traces
temp_trace = graphobjs.Scatter(x = elevs,
							   y = temps,
							   mode = 'markers',
							   text = labels,
							   name = "Temperature")
best_fit_trace = graphobjs.Scatter(x = elevs,
								  y = fit_line,
								  mode = "lines",
								  name = "Best Fit Line (r-value: "+str(r_value)+")",
								  text = "Slope: "+str(slope)+" degrees/ft")

## make plot
data = [temp_trace, best_fit_trace]
layout = graphobjs.Layout(title = "Valley Inversion", 
						 yaxis = graphobjs.YAxis(title="Temperature (°F)"),
						 xaxis = graphobjs.XAxis(title="Elevation (ft.)"))
figure = graphobjs.Figure(data=data, layout=layout)
plot = plt.iplot(figure, filename="Valley Inversion")

print plot.resource

