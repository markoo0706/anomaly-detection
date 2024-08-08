import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import dash_dangerously_set_inner_html

df = pd.read_csv("data1.csv")

bonds = {}

for col in df.columns[1:10]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    IQR = q3 - q1
    upper_bound = q3 + 1.5 * IQR
    lower_bound = q1 - 1.5 * IQR
    df[f'{col}_上界'] = pd.Series(upper_bound, index = range(len(df)))
    df[f'{col}_下界'] = pd.Series(lower_bound, index = range(len(df)))
    bonds[col] = (lower_bound, upper_bound)

x_line = px.line(df, x = "時間", y = ["x", "x_上界", "x_下界"], title= "x軸數值")
y_line = px.line(df, x = "時間", y = ["y", "y_上界", "y_下界"], title= "y軸數值")
z_line = px.line(df, x = "時間", y = ["z", "z_上界", "z_下界"], title= "z軸數值")
xyz_line = px.line(df, x = "時間", y = ["x", "y", "z"], title= "xyz軸數值")
xyz_line.update_layout(title_text = "xyz軸數值", title_font_size = 30)
voltage_line = px.line(df, x = "時間", y = ["voltage(V)", "voltage(V)_上界", "voltage(V)_下界"], title= "電壓 (voltage(V))")
current_line = px.line(df, x = "時間", y = ["current(A)", "current(A)_上界", "current(A)_下界"], title= "電流 (current(A))")
power_line = px.line(df, x = "時間", y = ["power(W)", "power(W)_上界", "power(W)_下界"], title= "功率 (power(W))")
energy_line = px.line(df, x = "時間", y = ["energy(Wh)", "energy(Wh)_上界", "energy(Wh)_下界"], title= "能量 (energy(Wh))")
frequency_line = px.line(df, x = "時間", y = ["frequency(Hz)", "frequency(Hz)_上界", "frequency(Hz)_下界"], title= "頻率 (frequency(Hz))")
powerfactor_line = px.line(df, x = "時間", y = ["powerfactor", "powerfactor_上界", "powerfactor_下界"], title= "功率因子 (powerfactor)")
anmoly_line = px.line(df, x = "時間", y = ["異常分數"], title= "異常分數")

anmoly_indicator = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = df["異常分數"][0],
    title = {'text': "異常程度"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [0, 100]}}
))

error_messages_html = [
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
        df["錯誤訊息"][0].replace(", ", ",<br>")
    )]


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(figure=anmoly_indicator, style={'width': '20vw', 'height': '30vh'}, id = "anmoly_indicator"),
        dcc.Graph(figure=anmoly_line, id = "anmoly_line", style={'width': '65vw', 'height': '30vh'}),
        html.Div(error_messages_html, id = "error-message-div",  className = "error_message")
    ], className= "rowElement"),

    html.Div([
        dcc.Graph(figure=x_line, className= "smallplot", id = "x_line"),
        dcc.Graph(figure= y_line, className="smallplot", id = "y_line"),
        dcc.Graph(figure= z_line, className="smallplot", id = "z_line")
    ], className= "rowElement"),


    html.Div([
        dcc.Graph(figure=voltage_line, className= "smallplot", id = "voltage_line"),
        dcc.Graph(figure=current_line, className= "smallplot", id = "current_line"),
        dcc.Graph(figure=power_line, className= "smallplot", id = "power_line")
    ], className= "rowElement"),

    html.Div([
        dcc.Graph(figure=energy_line, className= "smallplot", id = "energy_line"),
        dcc.Graph(figure=frequency_line, className= "smallplot", id = "frequency_line"),
        dcc.Graph(figure=powerfactor_line, className= "smallplot", id = "powerfactor_line")
    ], className= "rowElement"),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, 
        n_intervals=0
    )
], className= "container")

@app.callback([
           Output('error-message-div', 'children'),
           Output('anmoly_line', 'figure'),
           Output('x_line', 'figure'),
           Output('y_line', 'figure'),
           Output('z_line', 'figure'),
           Output('voltage_line', 'figure'),
           Output('current_line', 'figure'),
           Output('power_line', 'figure'),
           Output('energy_line', 'figure'),
           Output('frequency_line', 'figure'),
           Output('powerfactor_line', 'figure'),
           Output('anmoly_indicator', 'figure')],
          [Input('interval-component', 'n_intervals')])
def update_graph_live(n_intervals):
    
    start_row = max(n_intervals - 50, 0)
    end_row = min(n_intervals + 50, len(df))

    sliced_df = df.iloc[start_row:end_row]

    error_messages_html = [
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
        df["錯誤訊息"][n_intervals].replace(", ", ",<br>")
    )]
    anamoly_line = px.line(sliced_df, x = "時間", y = ["異常分數"], title= "異常分數")
    x_line = px.line(sliced_df, x = "時間", y = ["x", "x_上界", "x_下界"], title= "x軸數值")
    y_line = px.line(sliced_df, x = "時間", y = ["y", "y_上界", "y_下界"], title= "y軸數值")
    z_line = px.line(sliced_df, x = "時間", y = ["z", "z_上界", "z_下界"], title= "z軸數值")
    voltage_line = px.line(sliced_df, x = "時間", y = ["voltage(V)", "voltage(V)_上界", "voltage(V)_下界"], title= "電壓 (voltage(V))")
    current_line = px.line(sliced_df, x = "時間", y = ["current(A)", "current(A)_上界", "current(A)_下界"], title= "電流 (current(A))")
    power_line = px.line(sliced_df, x = "時間", y = ["power(W)", "power(W)_上界", "power(W)_下界"], title= "功率 (power(W))")
    energy_line = px.line(sliced_df, x = "時間", y = ["energy(Wh)", "energy(Wh)_上界", "energy(Wh)_下界"], title= "能量 (energy(Wh))")
    frequency_line = px.line(sliced_df, x = "時間", y = ["frequency(Hz)", "frequency(Hz)_上界", "frequency(Hz)_下界"], title= "頻率 (frequency(Hz))")
    powerfactor_line = px.line(sliced_df, x = "時間", y = ["powerfactor", "powerfactor_上界", "powerfactor_下界"], title= "功率因子 (powerfactor)")

    indicator = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = df["異常分數"][n_intervals],
        title = {'text': "異常程度"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 100]}}
    ))

    return error_messages_html, anamoly_line, x_line, y_line, z_line, voltage_line, current_line, power_line, energy_line, frequency_line, powerfactor_line, indicator

if __name__ == '__main__':
    app.run_server(debug=True)
