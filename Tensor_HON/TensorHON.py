import pandas as pd

import BuildRulesFastParameterFree
import BuildRulesFastParameterFreeFreq
import BuildNetwork
import itertools
import random
import matplotlib.pyplot as plt
import glob
import copy
import numpy as np
import os
import shutil
import pickle
from datetime import datetime, timedelta
import re

###########################################
# Functions
###########################################

def ReadSequentialData(InputFileName):
    if Verbose:
        print('Reading raw sequential data')
    RawTrajectories = []
    df_data = pd.read_csv(InputFileName, index_col=False)
    # global num_anomaly
    # num_anomaly = df_data[df_data['counts']<200]['counts'].sum()
    for i, row in df_data.iterrows():
        ship = row['ID']
        movements = row['sequence'].split(', ')
        timestamp = row['timestamp'].split(', ')
        movements.append('END')
        timestamp.append(timestamp[-1])
        count = 1
        RawTrajectories += [[ship, movements, timestamp]] * count
        if i % 1000 == 0:
            VPrint(i)
    return RawTrajectories


def BuildTrainingAndTesting(RawTrajectories):
    VPrint('Building training and testing')
    Training = []
    Testing = []
    for trajectory in RawTrajectories:
        ship, movement = trajectory
        movement = [key for key,grp in itertools.groupby(movement)] # remove adjacent duplications
        if LastStepsHoldOutForTesting > 0:
            Training.append([ship, movement[:-LastStepsHoldOutForTesting]])
            Testing.append([ship, movement[-LastStepsHoldOutForTesting]])
        else:
            Training.append([ship, movement])
    return Training, Testing

def DumpRules(Rules, OutputRulesFile):
    VPrint('Dumping rules to file')
    with open(OutputRulesFile, 'w') as f:
        for Source in Rules:
            for Target in Rules[Source]:
                f.write(' '.join([' '.join([str(x) for x in Source]), '=>', Target, str(Rules[Source][Target][0]), str(Rules[Source][Target][1])]) + '\n')

def DumpNetwork(Network, OutputNetworkFile):
    VPrint('Dumping network to file')
    LineCount = 0
    with open(OutputNetworkFile, 'w') as f:
        for source in Network:
            for target in Network[source]:
                f.write(','.join([SequenceToNode(source), SequenceToNode(target), str(Network[source][target][0]), str(Network[source][target][1]).replace(',', '')]) + '\n')
                LineCount += 1
    VPrint(str(LineCount) + ' lines written.')

def SequenceToNode(seq):
    curr = seq[-1]
    node = curr + '|'
    seq = seq[:-1]
    while len(seq) > 0:
        curr = seq[-1]
        node = node + curr + '.'
        seq = seq[:-1]
    if node[-1] == '.':
        return node[:-1]
    else:
        return node

def VPrint(string):
    if Verbose:
        print(string)


def BuildHON(InputFileName, OutputNetworkFile):
    RawTrajectories = ReadSequentialData(InputFileName)
    TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    VPrint(len(TrainingTrajectory))
    Rules = BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    # DumpRules(Rules, OutputRulesFile)
    Network = BuildNetwork.BuildNetwork(Rules)
    DumpNetwork(Network, OutputNetworkFile)
    VPrint('Done: '+InputFileName)

def BuildHONfreq(InputFileName, OutputNetworkFile):
    print('FREQ mode!!!!!!')
    RawTrajectories = ReadSequentialData(InputFileName)
    TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    VPrint(len(TrainingTrajectory))
    Rules = BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    # DumpRules(Rules, OutputRulesFile)
    Network = BuildNetwork.BuildNetwork(Rules)
    DumpNetwork(Network, OutputNetworkFile)
    VPrint('Done: '+InputFileName)

def ParseTimedelta(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]* (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    t = {key: float(val) for key, val in m.groupdict().items()}
    return timedelta(**t)


def GenerateWholeGraph():
    ###
    # generate network with freq or possibility as edge weight
    ###
    OutputNetworkFileFreq = path_data + 'network-freq.csv'
    OutputNetworkFile = path_data + 'network.csv'
    OutputRulesFile = path_data + 'rules.csv'
    # print(OutputRulesFile, OutputNetworkFile)
    # TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    # VPrint(len(TrainingTrajectory))
    TrainingTrajectory = RawTrajectories
    Rules_Freq = BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    # DumpRules(Rules_Freq, OutputRulesFile)
    # print(len(Rules_Freq))
    Network_Freq, Network = BuildNetwork.BuildNetwork(Rules_Freq)
    print(len(Network))
    DumpNetwork(Network_Freq, OutputNetworkFileFreq)
    DumpNetwork(Network, OutputNetworkFile)



###########################################
# User parameters
###########################################
## Initialize algorithm parameters
MaxOrder = 1
MinSupport = 0
InputFolder = './data/'
InputFileName = InputFolder + 'sample.csv'
path_results = './results/'
path_data = path_results + 'data/'
path_network = path_results + 'network/'
os.makedirs(path_results, exist_ok=True)
os.makedirs(path_data, exist_ok=True)
os.makedirs(path_network, exist_ok=True)

# copy normal data to data folder
shutil.copy(InputFileName, path_data)

LastStepsHoldOutForTesting = 0
MinimumLengthForTraining = 1
InputFileDeliminator = ' '
Verbose = False

if __name__ == "__main__":
    print('FREQ mode!!!!!!')
    RawTrajectories = ReadSequentialData(InputFileName)
    num_Raw = len(RawTrajectories)
    GenerateWholeGraph()

    print('test finished!!!')
