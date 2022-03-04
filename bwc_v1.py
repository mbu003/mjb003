from bokeh.io import output_file, show
from bokeh.models.widgets import RadioButtonGroup, Div, Button, Slider
from bokeh.models import CustomJS, TextInput
from bokeh.models import CustomJS, Dropdown
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure, curdoc
import numpy as np
import matplotlib.pyplot as plt

output_file("layout.html")
title = Div(text="<b> BACK WATER CURVE </b>")

################################# INPUT PARAMETERS ##################################################
in_p = Div(text="<b> INPUT PARAMETERS </b>")

length = TextInput(value="6000", title="Channel Length (m):")
width = TextInput(value="50", title="Width of Channel (m):")
h_ds = TextInput(value="3", title="Water depth downstream (m):")
friction = TextInput(value="15", title="Chezy's Coefficient (m^(1/2)/s):")
slope = TextInput(value="0.0001", title="Channel Bed Slope")

xsec = [("Rectangular", "item_1"), ("Trapezoidal", "item_2"), ("Circular", "item_3")]
xsec_dd = Dropdown(label="Select a cross section", button_type="warning", menu=xsec)

################################# FLOW PARAMETERS ##################################################
flow_p = Div(text="<b> FLOW PARAMETERS </b>")
flow_p = Div(text="<b> FLOW PARAMETERS </b>")
depth = TextInput(value="5", title="Depth of flow (m):")
dis = TextInput(value="50", title="Discharge (m^3/s):")
cd = Slider(start=0.1, end=5, value=1, step=.1, title="Coefficient of Discharge (Cd)")

################################# FLOW CHARACTERISTICS ##################################################
flow_c = Div(text="<b> FLOW CHARACTERISTICS </b>")

a_f = TextInput(value="50", title="Area of flow (m^2):")
wp = TextInput(value="50", title="Wetted Perimeter (m):")
h_r = TextInput(value="10", title="Hydraulic Radius (m):")
v_f = TextInput(value="50", title="Velocity of flow (m/s):")
sp_d = TextInput(value="50", title="Specific Discharge (m^3/s/m):")
fr_no = TextInput(value="10", title="Froud Number (m):")
hn = TextInput(value="50", title="Normal Depth (m):")
hc = TextInput(value="50", title="Critical Depth (m):")

################################# CALCULATIONS ##################################################
cal = Div(text="<b> CALCULATIONS </b>")
cal_sch = Div(text="<b> SELECT A SCHEME </b>")
delx = TextInput(value="50", title="Space Interval (m):")
delt = TextInput(value="50", title="Time Step (sec):")
sch= RadioButtonGroup(labels=["Explicit", "Implicit"], active=0)

us_bd = [("water depth", "item_1"), ("Discharge", "item_2")]
us_bd = Dropdown(label="Upstream Boundary Condition", button_type="warning", menu=us_bd)

ds_bd = [("water depth", "item_1"), ("Discharge", "item_2")]
ds_bd = Dropdown(label="Downstream Boundary Condition", button_type="warning", menu=ds_bd)

i_c = [("water depth", "item_1"), ("Discharge", "item_2")]
i_c = Dropdown(label="Initial Condition", button_type="warning", menu=i_c)

################################# OUTPUTS ##################################################
out = Div(text="<b> OUTPUTS </b>")
out_sel= RadioButtonGroup(labels=["Table (Length vs Depth)", "Water Surface Profile"], active=0)

button = Button(label="Draw Back water curve", button_type="success")

graph = figure(width = 500, height= 500, title = 'Back water curve',
 x_axis_label="Length", y_axis_label="height")

def bwc():
    # Initializing variables
    graph.renderers = []
    h0 = float(h_ds.value)         # Water depth at downstream end in meters
    b = float(width.value)         # Breadth of the rectangular open flow channel in meters
    Q = float(dis.value)           # Flow rate or discharge in m^3/s
    C = float(friction.value)      # Chezy's coefficient in m^(1/2)/s
    S0 = float(slope.value)        # bed slope of channel
    X = float(length.value)        # Total distance for which calculation is required, in meters
    dx = float(delx.value)         # step interval or space step
   
    # Initializing variables using Boundary Conditions
    x1 = [0]
    h = [h0]
    gl = [0]
    wl = [h0]
    h_ratio = []

    # Euler Numerical Scheme Solution (Explicit method)
    max_range = int(X/dx)+1
    for i in range(1,max_range):
        x1.append(i*dx)
        gl.append(i*dx*S0)
        h.append(h[i-1]+dx*(Q*Q/(C*C*h[i-1]**3*b*b)-S0))
        wl.append(gl[i]+h[i])
        h_ratio.append(h[i]/h[i-1])

    graph.varea(x = x1, y1 = gl, y2 = wl)


button.on_click(bwc)
curdoc().add_root(column(title, row(column(in_p, length, width, h_ds, friction, slope, xsec_dd), 
    column(cal, sch, delx, button, graph))))

# bokeh serve --show bwc_v1.py
