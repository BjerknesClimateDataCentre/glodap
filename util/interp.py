
from typing import Tuple
import pandas as pd
import numpy as np
import scipy.interpolate as interp

def average_values_for_duplicate_dimension(
        data: pd.DataFrame,
        dimension_key: str
):
    """
    Useful for making data monotonic. If you have measurements for e.g
    different depths, whereever the same depth is reported twice, you average
    the values for that particular depth.

    Return your modified DataFrame
    """


    return data.groupby(dimension_key).mean().reset_index()

def sort_data_set_on_dimension(
    data: pd.DataFrame,
    dimension_key: str
):
    """
    Sort the dataframe by the given key
    """
    return data.sort_values(dimension_key)

def remove_nans(
    data: pd.DataFrame,
    dimension_keys: str or []
):
    """
    Remove any row with NaN-values in the column(s) given by dimension_keys

    return the modified dataframe input
    """
    if isinstance(dimension_keys, str):
        dimension_keys = [ dimension_keys ]

    for key in dimension_keys:
        data = data[pd.notnull(data[key])]
    return data

def pchip_interpolate_profile(
        data: pd.DataFrame,
        dimension_key: str,
        step: float=1,
        suffix: str='_interp'
):
    """
    Interpolates all variables in the data with respect to the dimension_key -
    variable.
    """
    # Make sure data are sorted and monotonic
    data = average_values_for_duplicate_dimension(data, dimension_key)
    data = sort_data_set_on_dimension(data, dimension_key)

    # Create interpolated list of independent variable
    numsteps = (data[dimension_key].max() - data[dimension_key].min()) / step
    numsteps += 1
    dimension = np.linspace(
        data[dimension_key].min(),
        data[dimension_key].max(),
        numsteps
    )

    output = pd.DataFrame(columns=[dimension_key + suffix])

    # Raise exception if interpolated data has less points than original
    if len(dimension)<len(data):
        raise Exception(
            'Interpolated values cannot be less than actual data points'
        )

    output[dimension_key + suffix] = dimension
    output[dimension_key] = np.nan
    for var in data:
        if var == dimension_key:
            continue
        pchip = interp.PchipInterpolator(data[dimension_key], data[var])
        output[var + suffix] = pchip(dimension)
        output[var] = np.nan
    prev = 0
    orig_index = 0
    for i, dim in output[dimension_key + suffix].items():
        if dim == data.loc[orig_index, dimension_key]:
            for key in data:
                output.loc[i, key] = data.loc[orig_index, key]
            orig_index += 1
        elif dim > data.loc[orig_index, dimension_key] and prev > 0:
            for key in data:
                output.loc[prev, key] = data.loc[orig_index, key]
            orig_index += 1
        prev = i

    return output
