from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import output_file, show
from bokeh.models import CustomJS, TextInput, RangeSlider
from bokeh.models.widgets import RadioButtonGroup, Slider, Select, Button, Div

##### SET THE HEADER #####
main_menu        = RadioButtonGroup(labels=["Back Water Curve", "Sugawara Tank", "Free Flow Equations"], active=1)
app_title        = Div(text="<b> SUGAWARA TANK </b>")
description      = Div(text="This application helps <b>calculating and analyzing water behaviour on Sugawara Tanks. </b> All errors and the graphical result will be shown after the calculation is finished.")

##### SET THE MODEL PARAMETER ##### 
sub_div_title_1  = Div(text="<b>MODEL PARAMETER</b>")

d1_widget        = TextInput(value="5", title="d1 in mm:")
d2_widget        = TextInput(value="6", title="d2 in mm:")

s1_widget        = TextInput(value="7", title="s1 in mm:")
s2_widget        = TextInput(value="8", title="s2 in mm:")

k1_widget        = TextInput(value="9", title="k1:")
k2_widget        = TextInput(value="10", title="k2:")
k3_widget        = TextInput(value="11", title="k3:")
k4_widget        = TextInput(value="12", title="k4:")

##### SET THE OUTPUT BUTTON #####
sub_div_title_4  = Div(text="<b>===========================================================================================</b>")
output_button_1  = Button(label="Analyze Data", button_type="default")
output_button_2  = Button(label="Export Chart Result")

##### SET THE FIGURE #####
graph            = figure(plot_width=700, plot_height=500, title=None)

##### SHOW THE GUI #####
output_file("Back-Water-Curve.html")
show(column(main_menu, app_title, description,sub_div_title_1, row(column(d1_widget, d2_widget, s1_widget, s2_widget),column(k1_widget, k2_widget, k3_widget, k4_widget)),column(graph), row(column(output_button_1),column(output_button_2))))