### This file: line-by-line translation from Algorithm 2
### in the paper "Representing higher-order dependencies in networks"
### Code written by Jian Xu, Jan 2017

### Technical questions? Please contact i[at]jianxu[dot]net
### Demo of HON: please visit http://www.HigherOrderNetwork.com
### Latest code: please visit https://github.com/xyjprc/hon

### Call BuildNetwork()
### Input: Higher-order dependency rules
### Output: HON network
### See details in README


from collections import defaultdict, Counter
from datetime import datetime
import numpy as np

Graph = defaultdict(dict)
# GraphDistribution = defaultdict(dict)
itime = datetime.now()
initial_timedelta = itime - itime
GraphDistribution = defaultdict(lambda: defaultdict(lambda: np.array([0,initial_timedelta])))
Verbose = False

def Initialize():
    Graph = defaultdict(dict)

def BuildNetwork(Rules):
    VPrint('Building network')
    # Initialize()
    Graph.clear()
    GraphDistribution.clear()
    SortedSource = sorted(Rules, key=lambda x: len(x))
    ToAdd = []
    ToRemove = []
    ToReduce = []
    for source in SortedSource:
        for target in Rules[source]:
            Graph[source][(target,)] = Rules[source][target]
            # following operations are destructive to Rules
            if len(source) > 1:
                Rewire(source, (target,), ToAdd, ToRemove, ToReduce)
    for (source, target, weight) in ToAdd:
        if weight[0] != 0:
                Graph[source][target] = weight
    for (source, target) in ToRemove:
        del (Graph[source][target])
    # for (s, t, s1, t1) in ToReduce:
    #     Graph[s][t] -= Graph[s1][t1]

    RewireTails()
    BuildDistributions()
    return Graph, GraphDistribution
    # return GraphDistribution

def Rewire(source, target, ToAdd, ToRemove, ToReduce):
    PrevSource = source[:-1]
    PrevTarget = (source[-1],)
    if not PrevSource in Graph or not source in Graph[PrevSource]:
        # Graph[PrevSource][source] = Graph[PrevSource][PrevTarget]
        if (PrevSource, source, Graph[PrevSource][PrevTarget]) not in ToAdd:
            ToAdd.append((PrevSource, source, Graph[PrevSource][PrevTarget]))
        if (PrevSource, PrevTarget) not in ToRemove:
            ToRemove.append((PrevSource, PrevTarget))
        # del(Graph[PrevSource][PrevTarget])
        # remove the counts for the wired nodes
        # e.g. if a->b has been changed as a->b|a, then count[b][*]-=count[b|a][*]
        if target in Graph[PrevTarget]:
            # ToReduce.append((PrevTarget, target, source, target))
            Graph[PrevTarget][target] -= Graph[source][target]
            if Graph[PrevTarget][target][0] == 0:
                # del(Graph[PrevTarget][target])
                if (PrevTarget, target) not in ToRemove:
                    ToRemove.append((PrevTarget, target))

def RewireTails():
    ToAdd = []
    ToRemove = []
    ToReduce = []
    for source in Graph:
        for target in Graph[source]:
            if len(target) == 1:
                NewTarget = source + target
                while len(NewTarget) > 1:
                    if NewTarget in Graph and NewTarget not in Graph[source]:
                        ToAdd.append((source, NewTarget, Graph[source][target]))
                        ToRemove.append((source, target))
                        ToReduce.append((target, NewTarget))
                        break
                    else:
                        NewTarget = NewTarget[1:]
    for (source, target, weight) in ToAdd:
        Graph[source][target] = weight
    for (source, target) in ToRemove:
        del(Graph[source][target])
    # reduce the counts for the retailed nodes
    # e.g. if a|q->b has been changed as a|q->b|a, then count[b][*]-=count[b|a][*]
    for (target, NewTarget) in ToReduce:
        for NextStep in Graph[NewTarget]:
            if NextStep in Graph[target]:
                Graph[target][NextStep] -= Graph[NewTarget][NextStep]
                if Graph[target][NextStep][0] == 0:
                    del(Graph[target][NextStep])


def BuildDistributions():
    VPrint('building distributions for network')
    for Source in Graph:
        sum_count = sum([Graph[Source][item][0] for item in Graph[Source]])
        for Target in Graph[Source]:
            if Graph[Source][Target][0] > 0:
                try:
                    GraphDistribution[Source][Target][0] = 1.0 * Graph[Source][Target][0] / sum_count
                except:
                    print('check')
                GraphDistribution[Source][Target][1] = Graph[Source][Target][1] / Graph[Source][Target][0]
    for Source in Graph:
        for Target in Graph[Source]:
            Graph[Source][Target][1] = Graph[Source][Target][1] / Graph[Source][Target][0]



###########################################
# Auxiliary functions
###########################################

def VPrint(string):
    if Verbose:
        print(string)
