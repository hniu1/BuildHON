'''
1. split normal and abnormal data
2. build networks for them separately
3. draw sankey diagram or network for them
'''

import json
import os
import re
import pandas as pd
from graphviz import Digraph
from datetime import datetime, timedelta


def ReadTensorNetwork(ntkfile):
    dict_ntk = {} # key: id, value: [action, action]
    with open(ntkfile, 'r') as nf:
        for line in nf:
            # source = line.split(',')[0].split('|')[0]
            # target = line.split(',')[1].split('|')[0]
            source = line.split(',')[0]
            target = line.split(',')[1]
            source_action = ReadHONode(source)
            target_action = ReadHONode(target)
            tp = float(line.split('\n')[0].split(',')[-2])
            duration = line.split('\n')[0].split(',')[-1]
            duration = duration.split('.')[0]
            # source_action = source
            # target_action = target
            tran = source_action + '-->' +target_action
            dict_ntk[tran] = (tp,duration)
    return dict_ntk

def ParseTimedelta(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]* (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    t = {key: float(val) for key, val in m.groupdict().items()}
    return timedelta(**t)

def ReadTensorNetworkFreq(ntkfile):
    dict_ntk = {} # key: id, value: [action, action]
    with open(ntkfile, 'r') as nf:
        for line in nf:
            source = line.split(',')[0]
            target = line.split(',')[1]
            source_action = ReadHONode(source)
            target_action = ReadHONode(target)
            tp = int(line.split('\n')[0].split(',')[-2])
            duration = line.split('\n')[0].split(',')[-1]
            try:
                duration_ave = ParseTimedelta(duration)/tp
                duration_ave = str(duration_ave).replace(',', '')
            except:
                continue
            tran = source_action + '-->' +target_action
            dict_ntk[tran] = (tp,duration_ave)
    return dict_ntk

def VisualTensorNetwork(dict_tran, SaveName):
    g = Digraph('G', filename= SaveName, graph_attr={'rankdir':'LR'})
    # g.graph_attr['rankdir'] = 'LR'
    g.attr('node', fontsize='100', BORDER='255')
    g.attr('edge', fontsize='100')
    g.node('Created', shape='Mdiamond', style='filled', color='green')
    g.node('END', shape='Msquare', style='filled', color='red')
    for tran in dict_tran:
        (tp, duration) = dict_tran[tran]
        action_0 = tran.split('-->')[0]
        action_1 = tran.split('-->')[1]
        # tp = int(tp)
        if tp > 10:
            if tp/800.0 > 2:
                g.edge(action_0, action_1, str(round(tp,3))+', '+duration, penwidth= str(tp/200.0),
                       color='blue')
            else:
                g.edge(action_0, action_1, str(round(tp, 3)) + ', ' + duration, penwidth=str(3),
                       color='blue')
        else:
            g.edge(action_0, action_1, str(round(tp,3))+', '+duration, penwidth= str(tp*15),
                   color='blue')
    g.view()
    print('DFA')

def ViewTensorNetwork(network_file, graph_file):

    dict_normal = ReadTensorNetwork(path_data + network_file)

    VisualTensorNetwork(dict_normal, path_visual + graph_file)

    print('view network finished!!!')

def ViewTensorNetworkFreq(network_file, graph_file):

    dict_normal = ReadTensorNetworkFreq(path_data + network_file)

    VisualTensorNetwork(dict_normal, path_visual + graph_file)

    print('view network finished!!!')

def ReadHONode(hon):
    root = hon.split('|')[0]
    # node = dict_actid[int(root)]
    node = root
    list_prenodes = hon.split('|')[1].split('.')
    if not list_prenodes==['']:
        node += '|'
        for ix, prenode in enumerate(list_prenodes):
            # node += dict_actid[int(prenode)]
            node += prenode

            if ix < len(list_prenodes)-1:
                node += '.'
    # node += '(' + hon + ')'
    return node


if __name__ == '__main__':
    path_results_FON = '../05092022/results/network/'
    # path_results_HON = '../../results/hon_tensor/OASIS/ConShortEnd_10k/'

    path_results = path_results_FON
    path_data = path_results + 'data/'
    path_visual = path_results + 'visual/'
    os.makedirs(path_visual, exist_ok=True)

    ViewTensorNetwork('network.csv', 'TensorNetwork')


    print('test finished!!!')

