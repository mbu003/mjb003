# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 08:31:08 2015

@author: chaco3

Tank Model

Implemented By Juan Chacon
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column, row
from bokeh.models import Slider, Button, TextInput
from bokeh.plotting import curdoc, figure
from bokeh.models.widgets import PreText
import pandas as pd
#%%
# Initial States
s1_0 = TextInput(value="2", title="Level of the Top Tank [mm]")
s2_0 = TextInput(value="2", title="Level of the Bottom Tank [mm]")
Q_0 = TextInput(value="5", title="Initial Discharge (m3/sec)")

# Initial Parameters
slider_k1 = Slider(start=0.0, end=5.0, step=0.1, value=0.5, title='Upper Tank Upper Discharge Coefficient')
slider_k2 = Slider(start=0.0, end=5.0, step=0.1, value=0.2, title='Upper Tank Lower Discharge Coefficient')
slider_k3 = Slider(start=0.00, end=5.00, step=0.01, value=0.01, title='Percolation to Lower Tank Coefficient')
slider_k4 = Slider(start=0.0, end=5.0, step=0.1, value=0.1, title='Lower Tank Discharge Coefficient')
slider_d1 = Slider(start=1, end=30, step=1, value=10, title='Upper Tank Upper Discharge Position')
slider_d2 = Slider(start=0.1, end=30, step=1, value=20, title='Upper Tank Lower Discharge Position')
slider_rfcf = Slider(start=0.0, end=5.0, step=0.1, value=1.0, title='Rainfall Coefficient Factor')
slider_ecorr = Slider(start=0.0, end=5.0, step=0.1, value=1.0, title='Evaporation Coefficient Factor')

# Extra Parameters
slider_dt = Slider(start=5, end=100, step=5, value=10, title='Time Step [s]')
slider_area = Slider(start=0, end=4000, step=5, value=100, title='Catchment area [km²]')


# Pre Text
texto = PreText(text="""Please click to Run the Model""",width=500, height=100)

# Run Button
run_button = Button(label="Run Model", button_type="success")

# Plotting Figures
fig_1 = figure(width=400, height=400, title="Sugawara - Discharge Plot",x_axis_label='Date',y_axis_label='Discharge (m3/sec)')
fig_2 = figure(width=400, height=400, title="Sugawara - Upper Tank Water Level Plot",x_axis_label='Date',y_axis_label='Water Level (mm)')
fig_3 = figure(width=400, height=400, title="Sugawara - Lower Tank Water Level Plot",x_axis_label='Date',y_axis_label='Water Level (mm)')


#INITIAL_STATES = [float(s1_0.value), float(s2_0.value)]
#INITIAL_Q = float(Q_0.value)
#INITIAL_PARAM = [float(slider_k1.value), float(slider_k2.value), float(slider_k3.value), float(slider_k4.value), float(slider_d1.value), float(slider_d2.value), float(slider_rfcf.value), float(slider_ecorr.value)]
#INITIAL_PARAM = [0.1819, 0.0412, 0.3348, 0.0448, 3.2259, 0.3800]


PARAM_BND = ((0.0, 1.1),
             (0.0, 1.1),
             (0.0, 1.5),
             (0.0, 1.1),
             (1.0, 15.0),
             (0.1, 1.0),
             (0.8, 1.2),
			 (0.8, 1.2))


def _step(prec, evap, st, param, extra_param):
    '''
    #this function takes the following arguments
    #I -> inputs(2)[prec, evap]
    #    I(1) prec: Precipitation [mm]
    #    I(2) evap: Evaporation [mm]
    #
    #S -> System states(2)[S1, S2]
    #    S(1) S1: Level of the top tank [mm]
    #    S(2) S2: Level of the bottom tank [mm]
    #
    #P -> Parameter vector(6)
    #    P(1) k1: Upper tank upper discharge coefficient
    #    P(2) k2: Upper tank lower discharge coefficient
    #    P(3) k3: Percolation to lower tank coefficient
    #    P(4) k4: Lower tank discharge coefficient
    #    P(5) d1: Upper tank upper discharge position
    #    P(6) d2: Upper tank lower discharge position
    #
    #EP -> Extra parameters(2)
    #    EP(1) DT: Number of hours in the time step [s]
    #    EP(2) AREA: Catchment area [km²]
    #
    #Outputs
    #Q -> Flow [m³/s]
    #S -> Updated system states(2)[S1, S2] mm
    '''

    # Old states
    S1Old = st[0]
    S2Old = st[1]

    #Parameters
    k1 = param[0]
    k2 = param[1]
    k3 = param[2]
    k4 = param[3]
    d1 = param[4]
    d2 = param[5]
    rfcf = param[6]
    ecorr = param[7]
    
    # Extra Parameters
    DT = extra_param[0]
    Area = extra_param[1]

    ## Top tank
    H1 = np.max([S1Old + prec*rfcf - evap*ecorr, 0])

    if H1 > 0:
        #direct runoff
        if H1 > d1:
            q1 = k1*(H1-d1)
        else:
            q1 = 0

        #Fast response component
        if H1 > d2:
            q2 = k2*(H1-d2)
        else:
            q2 = 0

        #Percolation to bottom tank
        q3 = k3 * H1
        #Check for availability of water in upper tank
        q123 = q1+q2+q3
        if q123 > H1:
            q1 = (q1/q123)*H1
            q2 = (q2/q123)*H1
            q3 = (q3/q123)*H1
    else:
        q1 = 0
        q2 = 0
        q3 = 0

    Q1 = q1+q2
    #State update top tank
    S1New = max(H1 - (q1+q2+q3), 0.0)
    
    ## Bottom tank
    H2 = S2Old+q3
    Q2 = k4* H2

    #check if there is enough water
    if Q2 > H2:
        Q2 = H2

    #Bottom tank update
    S2New = H2 - Q2

    ## Total Flow
    # DT = 86400 #number of seconds in a day
    # Area = 2100# Area km²
    if (Q1 + Q2) >= 0:
        Q = (Q1+Q2)*Area/(3.6*DT)
    else:
        Q = 0

    S = [S1New, S2New]
#    if S1New < 0:
#        print('s1 below zero')
    return Q, S

def simulate():
    '''

    '''
    fig_1.renderers = []
    fig_2.renderers = []
    fig_3.renderers = []

    skip_rows = 16  # Number of rows to skip in the output file
    output_file = 'output.asc' # Name of the output file

    # Read data from the output file
    data = pd.read_csv(output_file,
                    skiprows=skip_rows,
                    skipinitialspace=True,
                    index_col='Time')

    # Create vector with time stamps
    time_index = pd.date_range('1994 12 07 20:00', periods=len(data), freq='H')

    # Add time stamps to observations
    data.set_index(time_index, inplace=True)

    prec = np.array(data['Rainfall']) + np.array(data['Snowfall']) # Define the precipitation input
    evap = np.array(data['ActualET'])  # get the actual evapotranspiration
    Q_Rec = np.array(data['Qrec'])
    INITIAL_STATES = [float(s1_0.value), float(s2_0.value)]
    INITIAL_PARAM = [float(slider_k1.value), float(slider_k2.value), float(slider_k3.value), float(slider_k4.value), float(slider_d1.value), float(slider_d2.value), float(slider_rfcf.value), float(slider_ecorr.value)]
    INITIAL_Q = float(Q_0.value)
    param = INITIAL_PARAM
    extra_param = [slider_dt.value, slider_area.value]
    st = [INITIAL_STATES,]
    q = [INITIAL_Q,]
    for i in range(len(prec)-1):
        step_res = _step(prec[i], evap[i], st[i], param, extra_param)
        q.append(step_res[0])
        st.append(step_res[1])
    y2=[]
    y3=[]
    for j in range(len(prec)):
        y2.append(st[j][0])
        y3.append(st[j][1])

    fig_1.line(x=time_index,y=q,width=1.5,legend_label='Simulated Q')
    fig_1.line(x=time_index,y=Q_Rec,color='black',width=1.5,legend_label='Recorded Q')
    fig_2.line(x=time_index,y=y2,width=1.5)
    fig_3.line(x=time_index,y=y3,width=1.5)
    texto.text=(' Final Discharge ='+ str(q[-1])+' m3/sec\n'+
    ' Final Level of the Top Tank ='+ str(st[-1][0])+' mm\n'+
    ' Final Level of the Bottom Tank ='+str(st[-1][1])+' mm') 





# the model calculates qt+1, therefore to make it compatible with the observations, we have to
# get rid of the last simulation result by reducing the input size

run_button.on_click(simulate)
curdoc().add_root(column(s1_0, s2_0, Q_0, slider_dt, slider_area, slider_k1, slider_k2, slider_k3, slider_k4,
slider_d1, slider_d2, slider_rfcf, slider_ecorr, run_button, texto, row(fig_1,fig_2,fig_3)))

# bokeh serve --show sugawara.py


'''
TEsting function    
'''