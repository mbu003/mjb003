# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:19:22 2022

@author: amo023
"""

from bokeh.io import show
from bokeh.models import CustomJS, TextInput
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import RadioButtonGroup, Button
from bokeh.io import show
from bokeh.models import CustomJS, RadioButtonGroup
from bokeh.layouts import gridplot
from bokeh.layouts import column,row 
from bokeh.plotting import figure
from bokeh.models import Panel, Tabs
from bokeh.plotting import curdoc 
from bokeh.models.widgets import PreText
import pandas as pd
import sugawara as sugawara
import numpy as np


# =============================================================================
# #Sugawara layout 
# =============================================================================
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.io import output_file, show
from bokeh.models import CustomJS, TextInput, RangeSlider
from bokeh.models.widgets import RadioButtonGroup, Slider, Select, Button, Div

##### SET THE HEADER #####
#main_menu        = RadioButtonGroup(labels=["Back Water Curve", "Sugawara Tank", "Free Flow Equations"], active=1)
#app_title        = Div(text="<b> SUGAWARA TANK </b>")
#description      = Div(text="This application helps <b>calculating and analyzing water behaviour on Sugawara Tanks. </b> All errors and the graphical result will be shown after the calculation is finished.")

##### SET THE MODEL PARAMETER ##### 
sub_div_title_1  = PreText(text="See summary here .... ")

d1_widget        = TextInput(value="10", title="d1 (mm):")
d2_widget        = TextInput(value="20", title="d2 (mm):")

s1_widget        = TextInput(value="1", title="s1 (mm)")
s2_widget        = TextInput(value="1", title="s2 (mm)")

k1_widget        = TextInput(value="0.5", title="k1:")
k2_widget        = TextInput(value="0.2", title="k2:")
k3_widget        = TextInput(value="0.01", title="k3:")
k4_widget        = TextInput(value="0.1", title="k4:")

##### SET THE OUTPUT BUTTON #####
sub_div_title_4  = Div(text="<b>===========================================================================================</b>")
btn_export  = Button(label="Export Chart Result", button_type="success")
btn_run_sugw  = Button(label="Run",button_type="success")

##### SET THE FIGURE #####
graph_sugw      = figure(plot_width=650, plot_height=300)

##### SHOW THE GUI #####

Sugawara_layout= column(  row(column(d1_widget, d2_widget, s1_widget, 
                                     s2_widget),column(k1_widget, k2_widget, k3_widget, k4_widget)),column(sub_div_title_1) ,column(graph_sugw),row(column(btn_export),column(btn_run_sugw)))

####



# =============================================================================
# ###################
# =============================================================================


# =============================================================================
# # for back water curve 
# =============================================================================

#input boxes
input_q = TextInput(value="50", title="Channel Discharge (Q m3/s)")
input_L = TextInput(value="6000", title="Channel Length (L m)")
input_B = TextInput(value="50", title="Channel Width (B m)")
input_slope = TextInput(value="0.001", title="Bed Slope (S0)")
input_chezy= TextInput(value="45", title="Chezy Coefficient (C)")
DS_depth = TextInput(value="3", title="Water Level Dwonstream (h_d/s)")
dx_explict = TextInput(value="100", title="Computational Step (dx)")

tollerance = TextInput(value="0.01", title="Tollerance for Iteration (Error)")
max_itr =   TextInput(value="350", title="Maximum number of iterations")
########### Disable some input at the  begining ##
tollerance.disabled= True
max_itr.disabled= True
dx_explict.disabled= False




################ Button s#########3
btn_run = Button(label="RUN", button_type="success")
btn_close = Button(label="CLOSE", button_type="success")
btn_csv = Button(label="Export csv",width=200)
btn_png = Button(label="Export png",width=200)
btn_tabular = Button(label="Tabular results",width=200)



##### figures################
graph_BWC= figure(plot_width=650, plot_height=300)



### text##########

texto = PreText(text="See summary here .... ")

####### rdio buttons #####
LABELS = ["Explicit", "Implicit"]
solution_mthd = RadioButtonGroup(labels=LABELS,active=0)




         


basic_input = column(input_q, input_L, input_B,input_slope, input_chezy,DS_depth)
numerical_input = column(solution_mthd, dx_explict,tollerance,max_itr)



# =============================================================================
# # coding part 
# =============================================================================

def on_run_btn_sugw_clicked():
    try:
            graph_sugw.renderers=[] # for rendering
            sub_div_title_1.text=  'Reading the data from the file and simulating.....'
            # go and read form the file #######
            ### Read the output.asc file
            
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
                
            
            # read the parameters from input boxes 
            
            
            k1=  float(k1_widget.value)
            k2=  float(k2_widget.value)
            k3=  float(k3_widget.value)
            k4=  float(k4_widget.value)
            d1=  float(d1_widget.value)
            d2=  float(d2_widget.value)
            s1=  float(s1_widget.value)
            s2=  float(s2_widget.value)
            
            extra_pars = [1, 147.0]
            pars = [k1,k2,k3,k4,d1,d2,s1,s2] # Set intial parameter set
            prec = np.array(data['Rainfall']) + np.array(data['Snowfall']) # Define the precipitation input
            evap = np.array(data['ActualET'])  # get the actual evapotranspiration
        
            
        
            
            
            # run the sugawara simulateioh nwith defa
            sub_div_title_1.text='Simulating.....'
            q_sim, st_sim = sugawara.simulate(prec=prec[:-1], evap=evap[:-1], param=pars, extra_param=extra_pars)  # Run the model
            
            # plot the results into the graph 
            #texto.text= '{}'.format(q_sim)
            sub_div_title_1.text='Plotting.....'
            graph_sugw.xaxis.axis_label = 'Time'   
            graph_sugw.yaxis.axis_label = 'Runoff ' 
            
            x= np.linspace(0,1000,1000)
            graph_sugw.line(x,q_sim,legend_label="Simulated Runoff ")
            graph_sugw.line(x,np.array(data['Qrec']), color='red',legend_label="Observed Runoff ")
            
            sub_div_title_1.text=  '|||SUCCESSFUL||| Used parameters:k1={}, k2={}, k3={}, k4={}, d1={}mm, d2={}mm, s1={}mm, s2={}mm'.format(k1,k2,k3,k4,d1,d2,s1,s2)
    
    
    except Exception as e:
       
     sub_div_title_1.text=  '|||Error|||   Error Message: {}'.format(e)
     
    
    
def on_run_btn_bwc_clicked():
     #sub_div_title_1.text= 'i am the button being clicked '
     try:       
            graph_BWC.renderers=[] # for rendering
            
            #some inputs for calculation 
            b  = float(input_B.value)
            hd = float(DS_depth.value)
            Q  = float(input_q.value)
            c  = float(input_chezy.value)
            s  = float(input_slope.value)
            dx = float(dx_explict.value)
            x_total= float(input_L.value)
            
            
            maxcomp = int(x_total/dx)+1            # mximum numer of computations 
            h = [hd]                           # h using the implicit scheme        
            hg    = [0]                            # to store the bed level values
            x     = [0]                            # to store the values of x                    
            wl  = [hd]                        # to store the value of the water level
            
            
            
            # chosing the solution methods 
            if solution_mthd.active==0:
                # explicit solution \
                    
                    
                  sol= 'Explicit'
                  
                  for j in range(1,maxcomp):            # looping through the steps 
                      
                      
                      texto.text    = 'calculating at x={}m'.format(j*dx)    
                      h_calc=0                      # to keep track of the iteration number
                      x.append(j*dx)
                      hg.append(j*dx*s)
                      h.append(h[j-1] + dx * (((Q**2 / (c**2 * h[j-1]**3 * b**2))-s)))                 # if the erorr is acceptable, append the needed values
                      wl.append(hg[j]+h[j])
                                 
            else:
                    
                    # implementation of the implicit scheme-------------------
                    
                    sol= 'Implicit'
                    tol=  float(tollerance.value)
                    itr_max =  float(max_itr.value)
                    itr_list = [float("NaN")]                    # to store the number of iterations
                    
                   # texto.text = 'implicit solution: L={}m, dx={}m, tol={}m, max_iterations={}'.format(x_total, dx,tol, itr_max)
                    
                    for j in range(1,maxcomp):            # looping through the steps 
                        h_assumed=h[-1]               # start with assumed 
                        itr = 0 
                        erorr=1     
                        h_calc=0                      # to keep track of the iteration number
                        
                        while erorr >tol and itr<itr_max: #checking for the error and if the value is close enough to the normal depth                 
                            texto.text    = 'calculating iteration number {itr},at x={x}m '.format(x=j*dx,itr=itr) 
                                     
                            RHS = Q**2/(c**2*b**2*h_assumed**3)-s   # Right hand side of the equation
                            h_calc= (RHS*dx)+h[j-1]              # calculate h as function of RHS 
                            erorr= abs(h_assumed-h_calc)
                            h_assumed = h_calc 
                            itr = itr + 1
                            
                            
                            
                            
                            
                            
                        x.append(j*dx)
                        hg.append(j*dx*s)
                        h.append(h_assumed)                 # if the erorr is acceptable, append the needed values
                        wl.append(hg[j]+h[j])
                        itr_list.append(itr)           
            texto.text    = 'plotting....'            
            graph_BWC.xaxis.axis_label = 'Space (m)'   
            graph_BWC.yaxis.axis_label = 'level (m)' 
            graph_BWC.circle(x,wl ,size=3,legend_label="Water Level " ,color='red')
            graph_BWC.line(x,hg ,legend_label=" Bed Level ")
            texto.text    = '|||SUCCESSFUL|||{} solution: L={}m, dx={}m'.format(sol, x_total, dx)
                       
           
                    
                        
                        
                        
                        
                
                
     except Exception as e:
        
        texto.text= '|||Error|||   Error Message: {}'.format(e)
            
                




def disappearing(active):
          if active==0:
                graph_BWC.renderers=[] # for rendering
                texto.text    = 'See summary here..'
                max_itr.disabled= True              
                tollerance.disabled= True
                dx_explict.disabled= False
               
                 
          elif  active==1:
              graph_BWC.renderers=[] # for rendering
              texto.text    = 'See summary here..'
              max_itr.disabled= False
              tollerance.disabled= False
              dx_explict.disabled= False
            
            
  # solution_mthd.on_change('active',disappearing)  


solution_mthd.on_click(disappearing)
         


               
btn_run.on_click(on_run_btn_bwc_clicked)
btn_run_sugw.on_click(on_run_btn_sugw_clicked)

btns_row_1= row(btn_close,btn_run)
btns_row_0= row(btn_tabular,btn_csv,btn_png)



c=column( row(basic_input,numerical_input),texto,graph_BWC,btns_row_0, btns_row_1)






#tabs


tab_BWC = Panel(child=c, title="Back Water Curve ")
tab_sugawara = Panel(child=Sugawara_layout,title="Sugawara Tank Model")
tab_composed= Tabs(tabs=[tab_BWC, tab_sugawara],)

curdoc().add_root(Tabs(tabs=[tab_BWC,tab_sugawara],width=2000))

