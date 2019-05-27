
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

    output = data.groupby(dimension_key).mean().reset_index()
    for column in data.columns:
        if column not in output.columns:
            output[column] = data[column].iloc[0]
    return output

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
        x: list,
        y: list,
        x_interp: list=[],
        step: float=1
):
    """
    Interpolates list y with respect to list x. If x_interp is given, this is
    used for the interpolation, otherwise interpolated against a series
    generated using generate_regular_monotonus_squence(x, step).

    Example:

    >>> x,y = pchip_interpolate_profile([11,13,19,25], [200,350,450,500], step=2)
    >>> x
    array([12., 14., 16., 18., 20., 22., 24.])
    >>> y
    array([289.76871469, 377.05063821, 414.5480226 , 439.11383135,
           460.84104938, 480.20833333, 494.94598765])

    """
    # check input vars are equal length
    if len(x) != len(y):
        raise Exception("x and y must be lists of same size")

    # Create interpolated list of independent variable
    if len(x_interp) == 0:
        x_interp = generate_regular_monotonus_squence(x, step)

    # Remove nans
    xx = []
    yy = []
    for x_, y_ in zip(x,y):
        if math.isnan(x_) or math.isnan(y_):
            continue
        xx.append(x_)
        yy.append(y_)

    # Sort by xx
    xx, yy = (list(x) for x in zip(*sorted(zip(xx, yy))))

    if len(yy)<2:
        # Interpolation not possible
        raise Exception("Input data has less than 2 valid elements")

    pchip = interp.PchipInterpolator(xx, yy, extrapolate=False)
    y_interp = pchip(x_interp)
    return x_interp, y_interp

def generate_regular_monotonus_squence(data: list=[], step: float=1):
    """
    Generate a regular, monotonous number sequence from data list, with
    sequence step. The sequence is garanteed to have

    max <= max(data) and min >= min(data)

    The series is also garanteed to always return the same numbers for overlapping
    data, as long as step is the same. So that eg:

    >>> x=generate_regular_monotonus_squence([7.3,17.234], 1.24)
    >>> x
    array([ 7.44,  8.68,  9.92, 11.16, 12.4 , 13.64, 14.88, 16.12])
    >>> y=generate_regular_monotonus_squence([9.7,18.75], 1.24)
    >>> y
    array([ 9.92, 11.16, 12.4 , 13.64, 14.88, 16.12, 17.36, 18.6 ])
    >>> ########## Overlaps: ##########
    >>> list(set(x) & set(y))
    [9.92, 11.16, 12.4, 13.64, 14.88, 16.12]
    """
    _min=math.ceil(min(data)/step)
    _max=math.floor(max(data)/step)
    numsteps = _max - _min + 1
    dimension = np.linspace(
        _min * step,
        _max * step,
        numsteps
    )
    return dimension

def subst_depth_profile_gaps_with_nans (
        x: list=[],
        y: list=[],
        depths: list=[],
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

    prev_index = 0
    delete_between = []
    for i, depth in enumerate(depths):
        if i == 0:
            continue
        prev_threshold = 0
        for threshold, gap in thresholds.items():
            if prev_threshold <= depth < threshold :
                if (depth - depths[prev_index]) > gap:
                    delete_between.append(
                        {
                            'min': depths[prev_index],
                            'max': depths[i],
                        }
                    )
            prev_threshold = threshold
        prev_index = i

    delete_enumerator = enumerate(delete_between)
    delete_next = next(delete_enumerator)
    xout = []
    yout = []
    no_more_gaps = True if len(delete_between) == 0 else False
    nanset = False
    for i, xx in enumerate(x):
        if no_more_gaps:
            xout.append(xx)
            yout.append(y[i])
            continue
        if xx < delete_next[1]['min']:
            xout.append(xx)
            yout.append(y[i])
            continue
        if delete_next[1]['min'] <= xx <= delete_next[1]['max']:
            if not nanset:
                nanset = True
                xout.append(xx)
                yout.append(np.nan)
            continue
        while not no_more_gaps and xx >= delete_next[1]['max']:
            nanset = False
            try:
                delete_next = next(delete_enumerator)
                if xx < delete_next[1]['min']:
                    xout.append(xx)
                    yout.append(y[i])
                    break
                if delete_next[1]['min'] <= xx <= delete_next[1]['max']:
                    if not nanset:
                        nanset = True
                        xout.append(xx)
                        yout.append(np.nan)
                    break
            except Exception as e:
                no_more_gaps = True
                xout.append(xx)
                yout.append(y[i])



    return xout, yout
