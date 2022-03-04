from bokeh.io import output_file, show
from bokeh.models.widgets import RadioButtonGroup, Div, Button, Slider
from bokeh.models import CustomJS, TextInput
from bokeh.models import CustomJS, Dropdown
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure, curdoc
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sugawara as sugawara

#output_file("layout.html")
title = Div(text="<b> SUGAWARA TANK MODEL </b>")

################################# INPUT PARAMETERS ##################################################
in_p = Div(text="<b> INPUT PARAMETERS </b>")

k1_sld = Slider(start=0, end=1.1, value=0.5, step=0.1, title="k1, Upper tank upper discharge coefficient")
k2_sld = Slider(start=0, end=1.1, value=0.2, step=0.1, title="k2, Upper tank lower discharge coefficient")
k3_sld = Slider(start=0, end=1.5, value=0.01, step=0.1, title="k3, Percolation to lower tank coefficient")
k4_sld = Slider(start=0, end=1.1, value=0.1, step=0.1, title="k4, Lower tank discharge coefficient")
d1_txt = TextInput(value="10", title="d1, Upper tank upper discharge position (m):")
d2_txt = TextInput(value="20", title="d2, Upper tank lower discharge position (m):")
rfcf_sld = Slider(start=0.8, end=1.2, value=1, step=0.1, title="Rainfall coefficient")
ecorr_sld = Slider(start=0.8, end=1.2, value=1, step=0.1, title="Error Correction")

########################################## RUN BUTTON ##################################################
run_btn  = Button(label="Run",button_type="success")

dt_txt = TextInput(value="1", title="Number of hours in time step (s):")
area_txt = TextInput(value="147", title="Catchment Area (km^2):")

################################# INITIAL WATER STATES ##################################################
s1_txt = TextInput(value="10", title="Top tank Water Level (mm):")
s2_txt = TextInput(value="10", title="Bottom tank Water Level (mm):")

###################################### SETTING THE FIGURE ###################################################
graph   = figure(plot_width=650, plot_height=500)

def sgw_model():
    graph.renderers = [] # for rendering

    ### Reading data from output file using panda   
    skip_rows = 16                  # Number of rows to skip in the output file
    output_file = 'output.asc'          # Name of the output file
            
    # Read data from the output file
    data = pd.read_csv(output_file,
    skiprows=skip_rows,
            skipinitialspace=True,
            index_col='Time')
            
    # Create vector with time stamps
    time_index = pd.date_range('1994 12 07 20:00', periods=len(data), freq='H')
            
    # Add time stamps to observations
    data.set_index(time_index, inplace=True)
                           
    #Parameters
    k1 = float(k1_sld.value)
    k2 = float(k2_sld.value)
    k3 = float(k3_sld.value)
    k4 = float(k4_sld.value)
    d1 = float(d1_txt.value)
    d2 = float(d2_txt.value)
    rfcf = float(rfcf_sld.value)
    ecorr = float(ecorr_sld.value)
    s1 = float(s1_txt.value)
    s2 = float(s2_txt.value)
    dt = float(dt_txt.value)
    area = float(area_txt.value)
            
    extra_pars = [dt, area]
    pars = [k1,k2,k3,k4,d1,d2,s1,s2]             # Set intial parameter set
    prec = np.array(data['Rainfall']) + np.array(data['Snowfall'])              # Defining precipitation array input
    evap = np.array(data['ActualET'])                                                   # defining evaptranspiration input array

    # run simulation
    q_sim, st_sim = sugawara.simulate(prec=prec[:-1], evap=evap[:-1], param=pars, extra_param=extra_pars)
                    
    # plot the results into the graph     
    graph.xaxis.axis_label = 'Time'   
    graph.yaxis.axis_label = 'Runoff ' 
                    
    x= np.linspace(0,1000,1000)
    graph.line(x,q_sim,legend_label="Simulated Runoff ")
    graph.line(x,np.array(data['Qrec']), color='red',legend_label="Observed Runoff ")       
               
run_btn.on_click(sgw_model)
curdoc().add_root(column(title, row(column(in_p, k1_sld, k2_sld, k3_sld, k4_sld, dt_txt), column(d1_txt, d2_txt, s1_txt, 
                                     s2_txt, area_txt),) ,column(graph),row(run_btn)))


# bokeh serve --show sugwara.py