#!/usr/bin/python

"""Command line tools for doing Exploratory Data Analysis for csv data


"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots


# draw_data: value_counts data
# enumerate_map: the name to display
def eda_graph(draw_data, enumerate_map, title='title', x_label='x_label', y_label='y_label'):
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    # Add traces
    fig.add_trace(go.Bar(
        x = [enumerate_map[str(e)] if str(e) in enumerate_map else str(e) for e in draw_data.index],
        y = draw_data.values,
        name='',
        text=draw_data.values,
        textposition='auto', # ['inside', 'outside', 'auto', 'none']
        texttemplate='%{text:.4s}'
    ))


    fig.update_layout(
        title = dict(
            text=title,
            y=1,
            x=0.5,
        ),
        xaxis = dict(
            title=x_label,
            tickmode = 'linear',
            # tick0 = 0,   # スタート
            dtick = 1  # 間隔
        ),
        yaxis = dict(
            title=y_label
        ),
        legend = dict(
            y=1.2,
            x=0.,
        )
    )

    fig.show()
    # plotly.offline.plot(fig)


# series: pd.Series, source data
# data_type: 'auto': judge by data.type   'discrete': value count directly   'continuous': binning at first, then value count
# max_bins: max bins
def calculate_draw_data(series:pd.Series, data_type='auto', max_bins=12, bins=[]):
    if len(series.value_counts()) < max_bins:
        max_bins = len(series.value_counts())
    if data_type != 'discrete' and data_type != 'continuous':
        if series.dtype == pd.Series(['1']).dtype:
            data_type = 'discrete'
        else:
            data_type = 'continuous'

    if data_type == 'discrete':
        draw_data = series.value_counts()[:max_bins] # Only return the largest max_bins bins
    if data_type == 'continuous':
        if bins:
            bin_info = pd.cut(series, bins=bins) # specified bins
        else:
            bin_info = pd.cut(series, bins=max_bins) # 等間隔ビン
        draw_data = bin_info.value_counts().sort_index()

    return draw_data


# df: pd.DataFrame, source data
# feature_list: features to show, if feature_list is null then show all the features
# exclude_list: features that will not show
# labels_map: labels to show   {'feature':{'enumerate': 'show label'}}
# data_type_map: specify if the feature is discrete or continuous , {'feature':'discrete'}
#         'discrete': value count directly   'continuous': binning at first, then value count
# bins_map: specify bins by bin list     {'feature': [1,2,3]}
def eda(df: pd.DataFrame, feature_list=[], exclude_list=[], max_bins=12, labels_map={}, data_type_map={}, bins_map={}):

    if not feature_list:
        feature_list = list(df.columns)

    for feature in feature_list:

        if feature not in exclude_list:
            data_type = data_type_map[feature] if feature in data_type_map else {}
            bins = bins_map[feature] if feature in bins_map else {}
            draw_data = calculate_draw_data(df[feature], data_type=data_type, max_bins=max_bins, bins=bins)
            enumerate_map = labels_map[feature] if feature in labels_map else {}
            eda_graph(draw_data, enumerate_map, title=feature, x_label=feature, y_label='counts')
