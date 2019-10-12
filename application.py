
import numpy as np
from math import *
from numexpr import evaluate

import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
pio.templates.default = "plotly_white"

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
application = app.server

app.layout= html.Div(children=[

                html.Div([                          
                    html.H1(children='3D Plotter',style={'textAlign': 'center'}),                   
                    html.H3(children='3D Plotting Tool for f(x,y)',style={'textAlign': 'center'}),
                    
                    html.Div([                       
                        html.Label('X-Values',style={'display':'table-cell','font-weight':'bold'}),                   
                        dcc.Input(id='xmin',value=0,type='number',placeholder='x minimum',style=dict(display='table-cell')),
                        
                        html.Div(id="xmin-val"),
                        dcc.Input(id='xmax',value=10,type='number',placeholder="x maximim",style=dict(display='table-cell')),
                        
                        html.Div(id="xmax-val"),
                        dcc.Input(id='xi',value=1,type='number',placeholder='x increment',style=dict(display='table-cell')),                              
                    ],        
                    style={'display':'inline-block','font-family':'Trebuchet MS, sans-serif'}
                    ),    
                    
                    html.Div([
                        html.Label('Y-Values',style={'display':'table-cell','font-weight':'bold'}),
                        dcc.Input(id='ymin',value=0, type='number',placeholder='y minimum',style=dict(display='table-cell')),
                        
                        html.Div(id="ymin_val"),
                        dcc.Input(id='ymax',value=10,type='number',placeholder='y maximum',style=dict(display='table-cell')),
                        
                        html.Div(id="ymax_val"),
                        dcc.Input(id='yi',value=1,type='number',placeholder='y increment',style=dict(display='table-cell')),        
                    ],        
                    style={'display':'inline-block','padding-left': '20px','font-family':'Trebuchet MS, sans-serif'}
                    ),
                    
                    html.Div([
                        html.Label('Z-Values for Colorbar',style={'display':'table-cell','font-weight':'bold'}),
                        dcc.Input(id='zmin',value=0, type='number',placeholder='z minimum',style=dict(display='table-cell')),
                        
                        html.Div(id="zmin_val"),
                        dcc.Input(id='zmax',value=10,type='number',placeholder='z maximum',style=dict(display='table-cell')),
                        
                        html.Div(id="zmax_val")       
                    ],        
                    style={'display':'inline-block','padding-left': '20px','font-family':'Trebuchet MS, sans-serif'}
                    ),
                    
                    html.Div([
                        html.Label('Enter an equation in the form of z = f(x,y)',style={'display':'table-cell','font-weight':'bold'}),
                        dcc.Input(id='equation',value='',type='string',placeholder='Example: sin(x**2)*cos(y)',size=50),
                        
                        html.Div(id="equation-val"),

                    ],        
                    style={'display':'inline-block','padding-left': '20px','padding-top': '0px','font-family':'Trebuchet MS, sans-serif'}
                    ),

                    html.Div([
                        html.Label('Select Type of Graph to Plot',style={'font-weight': 'bold'}),
                        dcc.RadioItems(id='radio',value='surface',
                            options=[
                                {'label': 'Surface Plot', 'value': 'surface'},
                                {'label': 'Heatmap', 'value': 'heatmap'},
                            ]
                        )
                    ],        
                    style={'display':'inline-block','padding-left': '20px','font-family':'Trebuchet MS, sans-serif'}    
                    )
                ],
                style={'font-family':'Trebuchet MS, sans-serif','border':'3px outset','padding':'10px','background-color':'#f5f5f5',}                         
                ),
                
                html.Div(id="graph-val",style={'border':'3px outset','margin-top': '10px','background-color':'#f5f5f5'})    
            ])

@app.callback(
    Output(component_id='graph-val',component_property='children'),
    [Input(component_id='xmin',component_property='value'),
     Input(component_id='xmax',component_property='value'),
     Input(component_id='xi',component_property='value'),
     Input(component_id='ymin',component_property='value'),
     Input(component_id='ymax',component_property='value'),
     Input(component_id='yi',component_property='value'),
     Input(component_id='zmin',component_property='value'),
     Input(component_id='zmax',component_property='value'),
     Input(component_id='radio',component_property='value'),
     Input(component_id='equation',component_property='value')     
    ]    
)
    
def update_data(xminval,xmaxval,xival,yminval,ymaxval,yival,zminval,zmaxval,radio,equation): 
    
    xr = np.arange(xminval,xmaxval,xival) 
    yr = np.arange(yminval,ymaxval,yival)
    x,y = np.meshgrid(xr,yr)  
    
    zz = evaluate(equation)
    
    if radio=='surface':
    
        return  dcc.Graph(
                    figure=go.Figure(
                        data=[go.Surface(z=zz,x=x,y=y,colorscale='jet',cmin=zminval,cmax=zmaxval)]
                    )
                )
        
    elif radio=='heatmap':
        
        return  dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Heatmap(z=zz,x=xr,y=yr,colorscale='jet',zmin=zminval,zmax=zmaxval)]
                    )
                )
    

if __name__ == '__main__':
    app.run_server(port=8080)




