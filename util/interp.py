
from typing import Tuple
import pandas as pd
import numpy as np
import scipy.interpolate as interp
import math

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
    variable. Keeps the original data, and tries to align this with the
    interpolated values.

    Dimension data are between min() and max() values, and are rounded to fit
    the step-parameter. So if step is 5, all dimesion data will be divisible by
    5. Eg if:

    depth=[11,13,19,25]
    step=2

    then:
    depth_interp=[12, 14, 16, 18, 20, 22, 24]

    """
    # Create interpolated list of independent variable
    min=math.ceil(data[dimension_key].min())
    min += step - (min % step) if min % step > 0 else 0
    max=math.floor(data[dimension_key].max())
    max -= (max - min) % step
    numsteps = (max - min) / step
    numsteps += 1
    dimension = np.linspace(
        min,
        max,
        numsteps
    )
    output = pd.DataFrame(columns=[dimension_key + suffix])

    # Raise exception if interpolated data has less points than original
    if len(dimension)<len(data):
        raise Exception(
            'Interpolated values cannot be less than actual data points'
        )
    if len(data)<2:
        raise Exception(
            'Needs at least 2 data points to interpolate'
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

def subst_depth_profile_gaps_with_nans (
        data: pd.DataFrame,
        dimension_key: str,
        dimension_keys_to_clear: list=[],
        thresholds: dict={
            500: 300,
            1500: 600,
            15000: 1100,
        }
):
    """
    For monotonic depth profile data, remove data where there are big gaps in
    the profile. The defined gap sizes are relating to the depth and can be
    changed using the thresholds - parameter. Default sets to nan if:
    * depth < 500m and gap > 300m
    * depth between 500m and 1500m and gap > 600
    * depth > 1500m and gap > 1100m

    The way it works is that all rows in the gap are removed but one, which is
    set to NaN.
    """

    drop_row = 'ROW_DELETE_MARKER'
    data[drop_row] = False

    prev_index = 0
    first = True
    for i, depth in data.loc[data[dimension_key].notnull()][dimension_key].items():
        if first:
            first = False
            prev_index = i
            continue
        last_threshold = 0
        for threshold, gap in thresholds.items():
            if last_threshold <= depth < threshold :
                if (depth - data.loc[prev_index, dimension_key]) > gap:
                    # Set values to nan before / after gap
                    if prev_index + 1 < i:
                        data.loc[prev_index+1, dimension_keys_to_clear] = np.nan
                        data.loc[i-1, dimension_keys_to_clear] = np.nan
                    # ...and delete rows in gap
                    if prev_index + 3 < i:
                        data.loc[prev_index+2:i-2, drop_row] = True
            last_threshold = threshold
        prev_index = i

    # Remove rows where ROW_DELETE_MARKER is True
    data = data.drop(data[data[drop_row]==True].index)

    # deleting the drop_row column
    del data[drop_row]

    return data
