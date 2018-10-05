import json
from pprint import pprint

import plotly
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np


data = json.load(open('results/006/latency200_006.json'))
boxData = {}
for x in data:
    t = ''
    if x['url'] == 'https://crm.thierryve.nl':
        t = 'crm'
    else:
        continue

    if x['platform'] != 'MOBILE':
        continue

    key = '{}|{}|{}'.format(t, x['protocol'], x['platform'])
    if not key in boxData:
        boxData.update({key: []})

    boxData.get(key).append(x['duration'])

pprint(boxData)

graphData = []
for key, value in boxData.items():
    # remove first and last entry
    value.sort()
    value = value[:-1]
    value.pop(0)

    graphData.append(
        go.Box(
            y=value,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            name=key
        )
    )

plotly.offline.plot(graphData, image='png')
