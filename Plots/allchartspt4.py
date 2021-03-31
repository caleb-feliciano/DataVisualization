import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['NOC'])['Total'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Total'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Total'])]

# Stacked bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Total': 'sum', 'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'],
ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
    marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
    marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
    marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line chart
line_df = df2
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['actual_max_temp'], mode='lines', name='actual max temp')]

# Multi line chart
multiline_df = df2
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines',
                              name='Mean')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines',
                              name='Min')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines',
                              name='Max')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
bubble_df = bubble_df.groupby(['date']).agg(
    {'actual_mean_temp': 'sum', 'average_min_temp': 'sum', 'average_max_temp': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['average_min_temp'],
               y=bubble_df['average_max_temp'],
               text=bubble_df['date'],
               mode='markers',
               marker=dict(size=bubble_df['actual_mean_temp'] / 2, color=bubble_df['actual_mean_temp'] / 2, showscale=True))]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['day'],
                   y=df2['month'],
                   z=df2['record_max_temp'].values.tolist(),
                   colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python',
             style={'textAlign': 'center'}),

    # Rio Olympic 2016
    html.Div('Rio Olympic 2016 Total medals of Gold, Silver, and Bronze.',
             style={'textAlign': 'center'}),
    html.Br(),

    # Bar Chart Layout
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the total number of olympic medals in the top 20 countries.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Rio Olympic 2016 Total Medals',
                   xaxis={'title': 'Country'},
                   yaxis={'title': 'Number of medals'})
              }
              ),

    # Stacked Bar Chart Layout
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the total gold, silver, and bronze medals for '
        'the top 20 countries.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Rio Olympic 2016 medals in the top 20 countries',
                                      xaxis={'title': 'Country'},
                                      yaxis={'title': 'Number of medals'},
                                      barmode='stack')
              }
              ),

    # Weather 2014-2015
    html.Br(),
    html.Hr(style={'color': '#7fdbff'}),
    html.Br(),
    html.Div('Weather Statistics from 2014-2015',
        style={'textAlign': 'center'}),
    html.Br(),

    # Line Chart Layout
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the average max temperature of Weather in the period from 2014-2015.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Weather Actual Max Temperature from 2014-2015',
                                      xaxis={'title': 'Date'},
                                      yaxis={'title': 'Temperature'})
              }
              ),

    # Multi Line Chart Layout
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the Actual Mean, Min, and Max temperature of Weather in the period from '
             '2014-2015.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(title='Weather Actual Mean, Min, and Max temperature from 2014-2015',
                                      xaxis={'title': 'Date'},
                                      yaxis={'title': 'Temperature'})
              }
              ),

    # Bubble Chart
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div('This bubble chart represent the Average Min and Max Temperatures for Weather in the period '
             'from 2014-2015.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Weather Average Temperatures',
                                      xaxis={'title': 'Average Min Temperature'},
                                      yaxis={'title': 'Average Max Temperature'},
                                      hovermode='closest')
              }
              ),

    # Heatmap Layout
    html.Hr(style={'color': '#7fdbff'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div('This heat map represent the Recorded Max Temperature of Weather in 2014-2015 '
             'per day of week and month of year.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Weather Recorded Max Temperature',
                                      xaxis={'title': 'Day of Week'},
                                      yaxis={'title': 'Month of Year'})
              }
              )
])

if __name__ == '__main__':
    app.run_server()