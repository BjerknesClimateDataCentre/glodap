import re
import logging
import datetime
import pandas as pd
import numpy as np

@pd.api.extensions.register_dataframe_accessor("whp_exchange")
class ExchangeAccessor(object):
    """This accessor simply defines some metadata properties"""
    column_units = []
    file_signature = ''
    file_type = ''
    comments = ''

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

def excread(path):
    """Read a single, moderate-sized file defined in the WHP Exchange
    format (https://exchange-format.readthedocs.io/en/latest/)

    - path: path to exchange file to read

    Returns a pandas data frame object with the content parsed from the exc file.
    A column called EXC_DATETIME is added, holding actual date-time values for
    the file. If no times are found, time is set to 00:00
    A column EXC_CTDDEPTH is added holding sampling depth (from CTDDEP or CTDDEP)
    """

    logger = logging.getLogger('glodap.util.excread')
    try:
        with open(path, encoding="utf-8") as excfile:
            excfile.readline()
            excfile.seek(0)
            return _excread(excfile)
    except:
        try:
            with open(path, encoding="iso-8859-1") as excfile:
                excfile.readline()
                excfile.seek(0)
                logger.info(
                    'File {} character encoding is ISO-8859-1'.format(
                        path
                    )
                )
                return _excread(excfile)
        except Exception as err:
            logger.error(
                'Could not read file {}'.format(
                    path
                )
            )
            raise err

def _excread(excfile):
    """Dont call this directly, use excread() instead."""

    logger = logging.getLogger('glodap.util.excread')
    rewindto = 0
    first = True
    signature = ''
    file_type = ''
    column_headers = []
    column_units = []
    line = None
    headerlines = 0
    comments = ""
    sampl_depth_columns = [
        'CTDDEPTH',
        'CTDDEP',
	'CTDPRS',
    ]

    # Loop over the header to collect metadata and remove file type info
    while True:
        headerlines += 1
        rewindto = excfile.tell()
        line = excfile.readline().strip()
        # Get the file type and signature
        if (
                first
                and (
                    line.startswith('CTD')
                    or line.startswith('BOTTLE')
                )
        ):
            first = False
            matches = re.search('((BOTTLE)|(CTD)),(.*)$', line)
            signature = matches.group(4)
            file_type = matches.group(1)
            continue
        # ignore empty lines
        elif not line:
            continue
        # Keep comments as metadata
        elif line.startswith('#'):
            comments += line + "\n"
            continue
        else:
            # Register header lines
            if line.startswith('EXPOCODE'):
                column_headers = line.split(',')
            elif line.startswith(',,,'):
                column_units = line.split(',')
            else:
                break

    excfile.seek(rewindto)
    data_types = {
        'EXPOCODE': str,
        'SECT_ID': str,
        'DATE': str,
        'TIME': str,
    }
    dataframe = pd.read_csv(
        excfile,
        names=column_headers,
        dtype=data_types,
    )

    # Strip leading and trailing whitespaces from string columns
    df_obj = dataframe.select_dtypes(['object'])
    dataframe[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # drop lines after and including END_DATA
    drop_lines = []
    for val in reversed(range(len(dataframe))):
        drop_lines.append(val)
        if 'END_DATA' in dataframe.iloc[val, 0]:
            for line in drop_lines:
                dataframe = dataframe.drop(line, axis=0)
            break

    # Add a datetime column. If time is not present, time is set to 00:00
    if 'DATE' in dataframe.columns and 'TIME' in dataframe.columns:
        datetime = None
        for ix, d in enumerate(dataframe['DATE']):
            try:
                t = dataframe['TIME'][ix]
                date='{}-{}-{}'.format(d[:4], d[4:6], d[6:])
                time = '{}:{}'.format(t[:2], t[2:])
                datetime = pd.to_datetime('{} {}'.format(date, time), utc=True)
            except Exception as e:
                logger.error(
                    'Timer format error (date: {}) (time: {}) on line {}'
                            .format(
                            d,
                            t,
                            ix + headerlines
                    )
                )
                raise e
        dataframe['EXC_DATETIME'] = datetime

    # Try multiple sampling depth columns
    for name in sampl_depth_columns:
        if name in dataframe.columns:
            dataframe['EXC_CTDDEPTH'] = dataframe[name]
            break

    # Replace -9999, -999, -99, -9 with np.nan
    dataframe = dataframe.replace([-9999, -999, -99, -9], np.nan)

    # Add some extra metadata to the dataframe
    dataframe.whp_exchange.column_units = column_units
    dataframe.whp_exchange.signature = signature
    dataframe.whp_exchange.file_type = file_type
    dataframe.whp_exchange.comments = comments

    return dataframe
