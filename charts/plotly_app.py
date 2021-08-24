import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State

import plotly.express as px
import pandas as pd
import datetime

# Read Excel Sheet
df = pd.read_excel('1628584238-test_sample.xlsx', 'data')

# To use third party css
external_stylesheets=[
    'https://codepen.io/amyoshino/pen/jzXypZ.css', 
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css', 
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css'
]
# Initialize dash app
app = DjangoDash('dash_integration_id')

app.css.append_css({
"external_url": external_stylesheets
})

# Get Unique Values
entry_no_filter = df['ENTRY_NO'].drop_duplicates()
entry_date_filter = df['ENTRY_DATE'].drop_duplicates()

# Get Option and Values for html component
entry_no_labels = [{'label':i, 'value':i} for i in entry_no_filter]
entry_date_filter = [{'label':i.strftime('%m-%d-%Y'), 'value':i} for i in entry_date_filter]

# Get Required Columns for X-Axis and Y-Axis
columns = df.drop(columns=['SNO','ENTRY_NO', 'ENTRY_DATE'])
columns = [{'label':i, 'value':i} for i in columns.columns]

# Initial Filtered Data
filtered_df = df[(df['ENTRY_NO'] == entry_no_labels[0]['value']) & (df['ENTRY_DATE'] ==  entry_date_filter[0]['value'])]
sorted_x = filtered_df.sort_values(by=['PAY'])

# Calculation for Pie Chart
summation_x = sorted_x.sum(axis = 0, skipna = True, numeric_only= True)
label_x, values_x = [], []
for s in summation_x.iteritems():
    label_x.append(s[0])
    values_x.append(s[1])

app.layout = html.Div(
    #Container
    html.Div([
        # Heading
        html.Div([
            html.Div([
                html.H1(children='Date Visualization')
            ], className = 'pl-4 col-sm-4 text-white'),
        ], className = 'row justify-content-center bg-dark round-pill pb-4'),

        #Filters and labels
        html.Div([
                html.Div([
                    html.Label(children="Select Entry Number", className="text-white"),
                    dcc.Dropdown(id='dropdown_one', options=entry_no_labels,
                        value = entry_no_filter[0]),],className="col-sm-2"),

                html.Div([
                    html.Label(children="Select Entry Date", className="text-white"),
                    dcc.Dropdown(id='dropdown_two', options= entry_date_filter,
                    value = entry_date_filter[0])],className="col-sm-2"),

                html.Div([
                    html.Label(children="X-Axis", className="text-white"),
                    dcc.Dropdown(id='dropdown_three', options= columns,
                    value = 'PAY')],className="col-sm-2"),

                html.Div([
                    html.Label(children="Y-Axis", className="text-white"),
                    dcc.Dropdown(id='dropdown_four', options=columns,
                    value = 'IV')],className="col-sm-2"),
        ], className = 'row justify-content-center bg-dark pb-4'),

        #Scatter Chart
        html.Div([
            html.Div([
                html.Div([
                    html.Div([         
                        dcc.Graph(
                            id='scatter-chart',
                            figure=px.scatter(filtered_df, x='PAY', y='IV', title='Scatter Chart')
                        ),
                    ], className = 'col six columns'),
                ], className='card-body'),
            ], className='card shadow w-75'),
            
        ], className= 'row justify-content-center pt-4 pb-4'),

        # Line Chart
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    dcc.Graph(
                        id='line-chart',
                        figure={
                            'data': [
                                {'x': sorted_x['PAY'], 'y': sorted_x['IV'], 'type': 'line'},
                            ],
                            'layout':{'title': 'Line Chart'}
                        }
                    )
            ], className = 'six columns'),
                ], className='card-body'),
            ], className='card shadow w-75'),
            
        ], className= 'row justify-content-center pt-4 pb-4'),

        # Bar Chart
        html.Div([
            html.Div([
                html.Div([
                    html.Div([         
                        dcc.Graph(
                            id='bar-chart',
                            figure={
                                "data": [{"type": "bar",
                                "x": filtered_df['IV'],
                                "y": filtered_df['PAY']}],
                                'layout':{'title': 'Bar Chart'}
                            }
                        ),
                    ], className = 'col six columns'),
                ], className='card-body'),
            ], className='card shadow w-75'),
            
        ], className= 'row justify-content-center pt-4 pb-4'),

        # Pie Chart
        html.Div([
            html.Div([
                html.Div([
                    html.Div([         
                        dcc.Graph(
                            id='pie-chart',
                            figure= px.pie(filtered_df, values=values_x, names=label_x, title='Pie Chart')
                        ),
                    ], className = 'col six columns'),
                ], className='card-body'),
            ], className='card shadow w-75'),
            
        ], className= 'row justify-content-center pt-4 pb-4'),

    ], className = 'container bg-secondary')
)


first = True

@app.callback([Output('scatter-chart', 'figure'), Output('line-chart', 'figure'), Output('bar-chart', 'figure'),Output('pie-chart', 'figure')], 
              [Input('dropdown_one', 'value'),Input('dropdown_two', 'value'), Input('dropdown_three', 'value'), Input('dropdown_four', 'value')])
def update_figure(entry_number, entry_date, x_axis, y_axis):
    """ Callback function to handle the input change events from frontend. """
    global first
    
    if first:
        first = False
        return dash.no_update
    
    if isinstance(entry_date, dict):
        entry_date = datetime.datetime.strptime(entry_date['value'], "%Y-%m-%dT%H:%M:%S")
    else:
        entry_date = datetime.datetime.strptime(entry_date, "%Y-%m-%dT%H:%M:%S")
    
    # Filter Dataset for selected ENTRY_NO and ENTRY_DATE
    filtered_df = df[(df['ENTRY_NO'] == entry_number) & (df['ENTRY_DATE'] == entry_date)]
    filtered_df = filtered_df.drop(columns=['SNO','ENTRY_NO', 'ENTRY_DATE'])
    
    #Calculation for Line Chart
    sorted = filtered_df.sort_values(by=[x_axis]) 
    line_chart = {'data': [{'x': sorted[x_axis], 'y': sorted[y_axis], 'type': 'line'},],}

    #Calculation for Bar Chart
    bar_chart={"data": [{"x": filtered_df[x_axis],"y": filtered_df[y_axis], "type": "bar",}],}
    
    
    #Calculation for Pie Chart
    summation = filtered_df.sum(axis = 0, skipna = True, numeric_only= True)
    label, values = [], []
    for s in summation.iteritems():
        label.append(s[0])
        values.append(s[1])
    pie_chart = px.pie(df, values=values, names=label)
    
    return px.scatter(filtered_df, x=x_axis, y=y_axis), line_chart, bar_chart , pie_chart

if __name__ == '__main__':
    app.run_server(8052, debug=False)