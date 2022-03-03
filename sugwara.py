from bokeh.io import output_file, show
from bokeh.models.widgets import RadioButtonGroup, Div, Button, Slider
from bokeh.models import CustomJS, TextInput
from bokeh.models import CustomJS, Dropdown
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure, curdoc
from __future__ import division
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
import scipy.optimize as opt
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
