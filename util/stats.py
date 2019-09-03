import pandas as pd
import numpy as np
import statistics as stat
from operator import itemgetter

def _get_matching_dimensions_for_station(
        data1: pd.DataFrame,
        data2: pd.DataFrame,
        dimension_key: str
):
    """
    Return DataFrames with only the matching values
    """

    output1 = data1[data1[dimension_key].isin(data2[dimension_key])]
    output2 = data2[data2[dimension_key].isin(data1[dimension_key])]
    return output1, output2

def _get_matching_indices(x1: list=[], x2: list=[]):
    """
    Return matching indices
    """
    x = set(x1) & set(x2)
    index_1 = [x1.index(_x) for _x in x]
    index_2 = [x2.index(_x) for _x in x]
    index_1.sort()
    index_2.sort()
    return index_1, index_2

def calculate_offset(
        array1: list,
        array2: list,
        additive: bool = False,
):
    """
    Calculate the multiplicative or additive offset for variables in two
    stations. Returns the offset:

    columns = ['dimension', 'station1', 'station2', 'offset']
    """
    output = []
    if additive:
        output = [a-b for a,b in zip(array1, array2)]
    else: # multiplicative
        output = [a/b for a,b in zip(array1, array2)]
    return output

def stats_and_offset(
        input: pd.DataFrame,
        reference: pd.DataFrame,
        dimension_key: str,
        dependent_key: str,
        use_additive_offset: bool = False,
):
    """
    Calculate stats for variables in two stations. Returns a
    pandas.DataFrame with the following columns:

    columns = ['dimension', 'station1', 'station1_mean', 'station1_stdev',
    'station2', 'station2_mean',  'station2_stdev', 'offset',
    ]
    """
    input, reference = _get_matching_dimensions_for_station(
        input,
        reference,
        dimension_key,
    )
    if len(input) < 2:
        return input
    offset = calculate_offset(
        input[dependent_key],
        reference[dependent_key],
        use_additive_offset,
    )
    input['offset'] = offset
    input[dependent_key + '_mean'] = stat.mean(input[dependent_key])
    input[dependent_key + '_stdev'] = stat.stdev(input[dependent_key])

    return input

def linear_fit(x, y):
    """
    Calculates linear regression for x and y. First removing all elemets
    where either x or y is None or NaN.

    Return a tuple (slope, intercept)
    """
    xx = []
    yy = []
    for ix, val in enumerate(x):
        if pd.notnull(val) and pd.notnull(y[ix]):
            xx.append(x[ix])
            yy.append(y[ix])
    return np.polyfit(xx, yy, 1)
