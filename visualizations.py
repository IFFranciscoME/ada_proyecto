
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Trading System with Genetic Programming for Feature Engineering, Multilayer Perceptron     -- #
# -- -------  Neural Network Predictive Model and Genetic Algorithms for Hyperparameter Optimization     -- #
# -- file: visualizations.py : visualization functions for the project                                   -- #
# -- author: IFFranciscoME - franciscome@iteso.mx                                                        -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/IFFranciscoME/Genetic_Net                                            -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import chart_studio

# -- ------------------------------------------------------------------------- ONLINE PLOTLY CREDENTIALS -- #
# -- --------------------------------------------------------------------------------------------------- -- #

chart_studio.tools.set_credentials_file(username='IFFranciscoME', api_key='Wv3JHvYz5h5jHGpuxvJQ')
chart_studio.tools.set_config_file(world_readable=True, sharing='public')


# -- -------------------------------------------------------- PLOT: OHLC Price Chart with Vertical Lines -- #
# -- --------------------------------------------------------------------------------------------------- -- #

def g_ohlc(p_ohlc, p_theme, p_vlines):
    """
    Timeseries Candlestick with OHLC prices and figures for trades indicator

    Requirements
    ------------
    numpy
    pandas
    plotly

    Parameters
    ----------
    p_ohlc: pd.DataFrame
        that contains the following float or int columns: 'timestamp', 'open', 'high', 'low', 'close'

    p_theme: dict
        with the theme for the visualizations

    p_vlines: list
        with the dates where to visualize the vertical lines, format = pd.to_datetime('2020-01-01 22:15:00')

    Returns
    -------
    fig_g_ohlc: plotly
        objet/dictionary to .show() and plot in the browser

    References
    ----------
    https://plotly.com/python/candlestick-charts/

    """

    # default value for lables to use in main title, and both x and y axisp_fonts
    if p_theme['p_labels'] is not None:
        p_labels = p_theme['p_labels']
    else:
        p_labels = {'title': 'Main title', 'x_title': 'x axis title', 'y_title': 'y axis title'}

    # tick values calculation for simetry in y axes
    y0_ticks_vals = np.arange(min(p_ohlc['low']), max(p_ohlc['high']),
                              (max(p_ohlc['high']) - min(p_ohlc['low'])) / 10)
    y0_ticks_vals = np.append(y0_ticks_vals, max(p_ohlc['high']))
    y0_ticks_vals = np.round(y0_ticks_vals, 5)

    # Instantiate a figure object
    fig_g_ohlc = go.Figure()

    # Add layer for OHLC candlestick chart
    fig_g_ohlc.add_trace(go.Candlestick(name='ohlc', x=p_ohlc['timestamp'], open=p_ohlc['open'],
                                        high=p_ohlc['high'], low=p_ohlc['low'], close=p_ohlc['close'],
                                        opacity=0.7))

    # Layout for margin, and both x and y axes
    fig_g_ohlc.update_layout(margin=go.layout.Margin(l=50, r=50, b=50, t=50, pad=0),
                             xaxis=dict(title_text=p_labels['x_title']),
                             yaxis=dict(title_text=p_labels['y_title']))

    # Color and font type for text in axes
    fig_g_ohlc.update_layout(xaxis=dict(titlefont=dict(color=p_theme['p_colors']['color_1']),
                                        tickfont=dict(color=p_theme['p_colors']['color_1'],
                                                      size=p_theme['p_fonts']['font_axis']), showgrid=True),
                             yaxis=dict(zeroline=False, automargin=True,
                                        titlefont=dict(color=p_theme['p_colors']['color_1']),
                                        tickfont=dict(color=p_theme['p_colors']['color_1'],
                                                      size=p_theme['p_fonts']['font_axis']),
                                        showgrid=True, gridcolor='lightgrey', gridwidth=.05))

    # If parameter vlines is used
    if p_vlines is not None:
        # Dynamically add vertical lines according to the provided list of x dates.
        shapes_list = list()
        for i in p_vlines:
            shapes_list.append({'type': 'line', 'fillcolor': p_theme['p_colors']['color_1'],
                                'line': {'color': p_theme['p_colors']['color_1'], 'dash': 'dashdot'},
                                'x0': i, 'x1': i, 'xref': 'x',
                                'y0': min(p_ohlc['low']), 'y1': max(p_ohlc['high']), 'yref': 'y'})

        # add v_lines to the layout
        fig_g_ohlc.update_layout(shapes=shapes_list)

    # Update layout for the background
    fig_g_ohlc.update_layout(
        yaxis=dict(tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis']),
                   tickvals=y0_ticks_vals),
        xaxis=dict(tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])))

    # Update layout for the y axis
    fig_g_ohlc.update_xaxes(rangebreaks=[dict(pattern="day of week", bounds=['sat', 'sun'])])

    # Update layout for the background
    fig_g_ohlc.update_layout(title_font_size=p_theme['p_fonts']['font_title'],
                             title=dict(x=0.5, text=p_labels['title']),
                             yaxis=dict(titlefont=dict(size=p_theme['p_fonts']['font_axis'])),
                             xaxis=dict(titlefont=dict(size=p_theme['p_fonts']['font_axis'])))

    # Final plot dimensions
    fig_g_ohlc.layout.autosize = True
    fig_g_ohlc.layout.width = p_theme['p_dims']['width']
    fig_g_ohlc.layout.height = p_theme['p_dims']['height']

    return fig_g_ohlc


# -- --------------------------------------------------------------------- PLOT: Stacked Horizontal Bars -- #
# -- --------------------------------------------------------------------------------------------------- -- #

def g_relative_bars(p_x, p_y0, p_y1, p_theme):
    """
    Generates a plot with two bars (two series of values) and two horizontal lines (medians of each
    series)

    Requirements
    ------------
    numpy
    pandas
    plotly

    Parameters
    ----------
    p_x : list
        lista con fechas o valores en el eje de x

    p_y0: dict
        values for upper bar plot
        {data: y0 component to plot (left axis), color: for this data, type: line/dash/dash-dot,
        size: for this data, n_ticks: number of ticks for this axis}

    p_y1: dict
        values for lower bar plot
        {data: y0 component to plot (right axis), color: for this data, type: line/dash/dash-dot,
        size: for this data, n_ticks: number of ticks for this axis}

    p_theme: dict
        colors and font sizes
        {'color_1': '#ABABAB', 'color_2': '#ABABAB', 'color_3': '#ABABAB', 'font_color_1': '#ABABAB',
        'font_size_1': 12, 'font_size_2': 16}

    Returns
    -------
    fig_relative_bars: plotly
        Object with plotly generating code for the plot

    """

    # instantiate a figure object
    fig_relative_bars = go.Figure()

    # Add lower bars
    fig_relative_bars.add_trace(go.Bar(name='Prediccion de Modelo', x=p_x, y=p_y1,
                                       marker_color='red',
                                       marker_line_color='red',
                                       marker_line_width=1, opacity=0.99))

    # Add upper bars
    fig_relative_bars.add_trace(go.Bar(name='Observacion', x=p_x, y=p_y0,
                                       marker_color='grey',
                                       marker_line_color='grey',
                                       marker_line_width=1, opacity=0.99))

    # Update layout for the background
    fig_relative_bars.update_layout(paper_bgcolor='white',
                                    yaxis=dict(tickvals=[-1, 0, 1], zeroline=True, automargin=True,
                                               tickfont=dict(color='grey',
                                                             size=p_theme['p_fonts']['font_axis'])),
                                    xaxis=dict(tickfont=dict(color='grey',
                                                             size=p_theme['p_fonts']['font_axis'])))

    # Update layout for the y axis
    fig_relative_bars.update_yaxes(showgrid=False, range=[-1, 1])

    # Legend format
    fig_relative_bars.update_layout(paper_bgcolor='white', plot_bgcolor='white', barmode='overlay',
                                    legend=go.layout.Legend(x=.41, y=-.12, orientation='h',
                                                            font=dict(size=p_theme['p_fonts']['font_axis'],
                                                                      color='grey')),
                                    margin=go.layout.Margin(l=50, r=50, b=50, t=50, pad=0))

    # Update layout for the background
    fig_relative_bars.update_layout(title_font_size=p_theme['p_fonts']['font_title'],
                                    title=dict(x=0.5,
                                               text=p_theme['p_labels']['title']),
                                    yaxis=dict(titlefont=dict(size=p_theme['p_fonts']['font_axis'])),
                                    xaxis=dict(titlefont=dict(size=p_theme['p_fonts']['font_axis'])))

    # Final plot dimensions
    fig_relative_bars.layout.autosize = True
    fig_relative_bars.layout.width = p_theme['p_dims']['width']
    fig_relative_bars.layout.height = p_theme['p_dims']['height']

    return fig_relative_bars


# -- ----------------------------------------------------------------------------------- PLOT: ROC + ACU -- #
# -- --------------------------------------------------------------------------------------------------- -- #

def g_roc_auc(p_cases, p_models, p_type, p_theme):

    # p_casos = casos
    fig_rocs = go.Figure()
    fig_rocs.update_layout(
        title=dict(x=0.5, text=p_theme['p_labels']['title']),
        xaxis=dict(title_text=p_theme['p_labels']['x_title'],
                   tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])),
        yaxis=dict(title_text=p_theme['p_labels']['y_title'],
                   tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])))

    fig_rocs.add_shape(type='line', line=dict(width=3, dash='dash', color='grey'), x0=0, x1=1, y0=0, y1=1)

    for model in p_models:
        for auc_type in ['auc_min', 'auc_max']:
            p_fpr = p_cases[model][auc_type]['data']['metrics'][p_type]['fpr']
            p_tpr = p_cases[model][auc_type]['data']['metrics'][p_type]['tpr']

            if auc_type == 'auc_min':
                fig_rocs.add_trace(go.Scatter(x=p_fpr, y=p_tpr, name=model,
                                              mode='lines+markers', line=dict(width=2, color='red')))
            elif auc_type == 'auc_max':
                fig_rocs.add_trace(go.Scatter(x=p_fpr, y=p_tpr, name=model,
                                              mode='lines+markers', line=dict(width=2, color='blue')))

    # Formato para titulo
    fig_rocs.update_layout(margin=go.layout.Margin(l=50, r=50, b=50, t=50, pad=0),
        legend=go.layout.Legend(x=.13, y=-0.25, orientation='h',
                                bordercolor='dark grey',
                                borderwidth=1,
                                font=dict(size=p_theme['p_fonts']['font_axis'])))

    # Formato de tamanos
    fig_rocs.layout.autosize = True
    fig_rocs.layout.width = p_theme['p_dims']['width']
    fig_rocs.layout.height = p_theme['p_dims']['height']

    return fig_rocs


# -- ----------------------------------------------------------------------------------- PLOT: ROC + ACU -- #
# -- --------------------------------------------------------------------------------------------------- -- #

def g_timeseries_auc(p_data_auc, p_theme):
    """
    Plot para series de tiempo de las AUC de los modelos

    Parameters
    ----------
    p_data_auc:dict
        Diccionario con datos para plot de series de tiempo AUC
        p_data_auc = minmax_auc_test

    p_theme: dict
        Diccionario con informacion de tema para plot
        p_theme = theme_plot_4

    Returns
    -------
    fig_ts_auc: plotly
        Objeto tipo plotly para utilizar con .show()

    """

    fig_ts_auc = go.Figure()
    fig_ts_auc.update_layout(
        title=dict(x=0.5, text=p_theme['p_labels']['title']),
        xaxis=dict(title_text=p_theme['p_labels']['x_title'],
                   tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])),
        yaxis=dict(title_text=p_theme['p_labels']['y_title'],
                   tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['logistic-elasticnet']['x_period'],
                                    y=p_data_auc['logistic-elasticnet']['y_mins'],

                                    line=dict(color='#004A94', width=3),
                                    marker=dict(color='#004A94', size=9),
                                    name='logistic-elasticnet (min)',
                                    mode='markers+lines'))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['logistic-elasticnet']['x_period'], fillcolor='blue',
                                    y=p_data_auc['logistic-elasticnet']['y_maxs'],

                                    line=dict(color='#004A94', width=3),
                                    marker=dict(color='#004A94', size=9),
                                    name='logistic-elasticnet (max)',
                                    mode='markers+lines'))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['ls-svm']['x_period'],
                                    y=p_data_auc['ls-svm']['y_mins'],

                                    line=dict(color='#FB5D41', width=3),
                                    marker=dict(color='#FB5D41', size=9),
                                    name='ls-svm (min)',
                                    mode='markers+lines'))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['ls-svm']['x_period'],
                                    y=p_data_auc['ls-svm']['y_maxs'],

                                    line=dict(color='#FB5D41', width=3),
                                    marker=dict(color='#FB5D41', size=9),
                                    name='ls-svm (max)',
                                    mode='markers+lines'))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['ann-mlp']['x_period'],
                                    y=p_data_auc['ann-mlp']['y_mins'],

                                    line=dict(color='#339e62', width=3),
                                    marker=dict(color='#339e62', size=9),
                                    name='ann-mlp (min)',
                                    mode='markers+lines'))

    fig_ts_auc.add_trace(go.Scatter(x=p_data_auc['ann-mlp']['x_period'],
                                    y=p_data_auc['ann-mlp']['y_maxs'],

                                    line=dict(color='#339e62', width=3),
                                    marker=dict(color='#339e62', size=9),
                                    name='ann-mlp (min)',
                                    mode='markers+lines'))

    # Formato para titulo
    fig_ts_auc.update_layout(margin=go.layout.Margin(l=50, r=50, b=50, t=50, pad=0),
        legend=go.layout.Legend(x=0.05, y=-0.35, orientation='h',
                                bordercolor='dark grey',
                                borderwidth=1,
                                font=dict(size=p_theme['p_fonts']['font_axis'])))

    # Formato de tamanos
    fig_ts_auc.layout.autosize = True
    fig_ts_auc.layout.width = p_theme['p_dims']['width']
    fig_ts_auc.layout.height = p_theme['p_dims']['height']

    return fig_ts_auc


# -- -------------------------------------------- PLOT: OHLC Candlesticks + Colored Classificator Result -- #
# -- --------------------------------------------------------------------------------------------------- -- #

def g_ohlc_class(p_ohlc, p_theme, p_data_class, p_vlines):

    # default value for lables to use in main title, and both x and y axisp_fonts
    if p_theme['p_labels'] is not None:
        p_labels = p_theme['p_labels']
    else:
        p_labels = {'title': 'Main title', 'x_title': 'x axis title', 'y_title': 'y axis title'}

    # tick values calculation for simetry in y axes
    y0_ticks_vals = np.arange(min(p_ohlc['low']), max(p_ohlc['high']),
                              (max(p_ohlc['high']) - min(p_ohlc['low'])) / 5)
    y0_ticks_vals = np.append(y0_ticks_vals, max(p_ohlc['high']))
    y0_ticks_vals = np.round(y0_ticks_vals, 4)

    # reset the index of the input data
    p_ohlc.reset_index(inplace=True, drop=True)

    # auxiliar lists
    train_error = []
    test_error = []
    test_success = []
    train_success = []

    # error and success in train
    for row in p_data_class['train_y'].index.to_list():
        if p_data_class['train_y'][row] != p_data_class['train_y_pred'][row]:
            train_error.append(row)
        else:
            train_success.append(row)

    # error and success in test
    for row in p_data_class['test_y'].index.to_list():
        if p_data_class['test_y'][row] != p_data_class['test_y_pred'][row]:
            test_error.append(row)
        else:
            test_success.append(row)

    # train and test errors in a list
    train_test_error = train_error + test_error

    # train and test success in a list
    train_test_success = train_success + test_success

    # Instantiate a figure object
    fig_g_ohlc = go.Figure()

    # Layout for margin, and both x and y axes
    fig_g_ohlc.update_layout(margin=go.layout.Margin(l=50, r=50, b=50, t=50, pad=0),
                             xaxis=dict(title_text=p_labels['x_title']),
                             yaxis=dict(title_text=p_labels['y_title']))

    # Add layer for the error based color of candles in OHLC candlestick chart
    fig_g_ohlc.add_trace(go.Candlestick(
        x=[p_ohlc['timestamp'].iloc[i] for i in train_test_error],
        open=[p_ohlc['open'].iloc[i] for i in train_test_error],
        high=[p_ohlc['high'].iloc[i] for i in train_test_error],
        low=[p_ohlc['low'].iloc[i] for i in train_test_error],
        close=[p_ohlc['close'].iloc[i] for i in train_test_error],
        increasing={'line': {'color': 'red'}},
        decreasing={'line': {'color': 'red'}},
        name='Prediction Error'))

    # Add layer for the success based color of candles in OHLC candlestick chart
    fig_g_ohlc.add_trace(go.Candlestick(
        x=[p_ohlc['timestamp'].iloc[i] for i in train_test_success],
        open=[p_ohlc['open'].iloc[i] for i in train_test_success],
        high=[p_ohlc['high'].iloc[i] for i in train_test_success],
        low=[p_ohlc['low'].iloc[i] for i in train_test_success],
        close=[p_ohlc['close'].iloc[i] for i in train_test_success],
        increasing={'line': {'color': 'skyblue'}},
        decreasing={'line': {'color': 'skyblue'}},
        name='Prediction Success'))

    # Update layout for the background
    fig_g_ohlc.update_layout(
        yaxis=dict(tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis']),
                   tickvals=y0_ticks_vals),
        xaxis=dict(tickfont=dict(color='grey', size=p_theme['p_fonts']['font_axis'])))

    # Update layout for the y axis
    fig_g_ohlc.update_xaxes(rangebreaks=[dict(pattern="day of week", bounds=['sat', 'sun'])])

    # If parameter vlines is used
    if p_vlines is not None:
        # Dynamically add vertical lines according to the provided list of x dates.
        shapes_list = list()
        for i in p_vlines:
            shapes_list.append({'type': 'line', 'fillcolor': p_theme['p_colors']['color_1'],
                                'line': {'color': p_theme['p_colors']['color_1'],
                                         'dash': 'dashdot', 'width': 3},
                                'x0': i, 'x1': i, 'xref': 'x',
                                'y0': min(p_ohlc['low']), 'y1': max(p_ohlc['high']), 'yref': 'y'})

        # add v_lines to the layout
        fig_g_ohlc.update_layout(shapes=shapes_list)

    # Update layout for the background
    fig_g_ohlc.update_layout(title_font_size=p_theme['p_fonts']['font_title'],
                             title=dict(x=0.5, text=p_theme['p_labels']['title']),
                             yaxis=dict(title=p_labels['y_title'],
                                        titlefont=dict(size=p_theme['p_fonts']['font_axis'])),
                             xaxis=dict(title=p_labels['x_title'], rangeslider=dict(visible=False),
                                        titlefont=dict(size=p_theme['p_fonts']['font_axis'])))

    # Formato para titulo
    fig_g_ohlc.update_layout(legend=go.layout.Legend(x=.35, y=-.3, orientation='h',
                                                     bordercolor='dark grey',
                                                     borderwidth=1,
                                                     font=dict(size=p_theme['p_fonts']['font_axis'])))
    # Final plot dimensions
    fig_g_ohlc.layout.autosize = True
    fig_g_ohlc.layout.width = p_theme['p_dims']['width']
    fig_g_ohlc.layout.height = p_theme['p_dims']['height']

    return fig_g_ohlc
