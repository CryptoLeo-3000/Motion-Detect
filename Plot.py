from VidCapture import dataframe
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

dataframe["Start_String"] = dataframe["Start"].dt.strftime("%Y-%M-%D %H:%M:%S")
dataframe["End_String"] = dataframe["End"].dt.strftime("%Y-%M-%D %H:%M:%S")

coldata = ColumnDataSource(dataframe)

fig = figure(x_axis_type = "datetime", height = 300, width = 900, title = "Motion Graph")
fig.yaxis.minor_tick_line_color = None

hover = HoverTool(tooltips = [("Start: ", "@Start_String"), ("End: ", "@End_String")])
fig.add_tools(hover)

quadrant = fig.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "green", source = coldata)

output_file("Graph.html")
show(fig)