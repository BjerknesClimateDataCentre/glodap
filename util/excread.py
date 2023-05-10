import re
import logging
import datetime
import pandas as pd
import numpy as np
from file_read_backwards import FileReadBackwards
import dateutil.parser as parser


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
        encoding = "utf-8"
        with open(path, encoding=encoding) as excfile:
            excfile.readline()
    except:
        try:
            encoding = "iso-8859-1"
            with open(path, encoding=encoding) as excfile:
                excfile.readline()
                logger.info(
                    'File {} character encoding is ISO-8859-1'.format(
                        path
                    )
                )
        except Exception as err:
            logger.error(
                'Could not read file {}'.format(
                    path
                )
            )
            raise err
    return _excread(path, encoding=encoding)

   ## logger = logging.getLogger('glodap.util.excread')
########
   ## encodingup = [
   ##         'ascii',
   ##         'utf-8',
   ##         'iso-8859-1',
   ##         'latin-1'
##]
  ##  info =None
  ##  for encoding in encodingup:
  ##      try:
  ##          with open(path, encoding=encoding) as excfile:
  ##              excfile.readline()
  ##      except: 
  ##          continue
  ##      else:
########            
    #try:
       # encoding = "utf-8"
      #  with open(path, encoding=encoding) as excfile:
     #       excfile.readline()
    #except Exception:
        #try: 
            #encoding = "iso-8859-1"
           # with open(path, encoding=encoding) as excfile:
             #   excfile.readline()            
            #    logger.info(
           #         'File {} character encoding is ISO-8859-1'.format(
          #              path
         #           )
        #        )
        #except Exception:
            #try:
                #encoding = "latin-1"
                #with open(path, encoding=encoding) as excfile:
               #     excfile.readline()
              #      logger.info(
             #           'File {} character encoding is latin-1'.format(
            #                path
           #             )
          #          )
         #   except Exception as err:
        #        logger.error(
       #             'Could not read file {}'.format(
      #                  path
     #                )   
     #            )
    #        raise err
    #     return _excread(path, encoding=encoding)


def _excread(path, encoding="utf-8"):
    """Dont call this directly, use excread() instead."""
    logger = logging.getLogger('glodap.util.excread')
    skipfooter = 0
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
    with open(path, encoding=encoding) as excfile:
        while True:
            headerlines += 1
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
                matches = re.search('((BOTTLE)|(CTD))[, ](.*)$', line)
                signature = matches.group(4)
                file_type = matches.group(1)
                continue
            # ignore empty lines
            elif not line.strip():
                continue
            # Keep comments as metadata
            elif line.startswith('#'):
                comments += line + "\n"
                continue
            else:
                # Register header lines
                if line.startswith('EXPOCODE'):
                    column_headers = [s.strip() for s in line.split(',')]
                elif line.startswith(',,,'):
                    column_units =  [s.strip() for s in line.split(',')]
                else:
                    break

   ## with FileReadBackwards(path, encoding=encoding) as fin:
   ##     for line in fin:
   ##         skipfooter += 1
   ##         if line.strip() == 'END_DATA':
   ##             break
##############
    #try:
        ##encoding = "utf-8"    
        ##with FileReadBackwards(path, encoding=encoding) as fin:
        ##    for line in fin:
        ##        skipfooter += 1
        ##        if line.strip() == 'END_DATA': 
        ##            break

        encoding_list = ['ascii','latin-1','iso-8859-1']
        ##encoding_list = ['ascii','latin-1','iso-8859-1','ISO8601']
        for encoding in encoding_list:
            worked = True
        try:
            with FileReadBackwards(path, encoding=encoding) as fin:
                for line in fin:
                    skipfooter += 1
                    if line.strip() == 'END_DATA':
                        continue
        except:
            worked = False
        if worked:
            print(encoding_list)

   #except: 
    ##   try:
    ##        encoding = "iso-8859-1"
    ##    with FileReadBackwards(path, encoding=encoding) as fin:
    ##        for line in fin:
    ##            skipfooter += 1
    ##            if line.strip() == 'END_DATA':                    
    ##    except:
    ##        pass
    ##        try:
    ##    encoding = "latin-1"
    ##    with FileReadBackwards(path, encoding=encoding) as fin:
    ##        for line in fin:
    ##            skipfooter += 1
    ##            if line.strip() == 'END_DATA':                    
    ##        except:
    ##            pass

##################

    data_types = {
        'EXPOCODE': str,
        'SECT_ID': str,
        'DATE': str,
        'TIME': str,
    }
    
    ##dataframe = pd.read_csv(
    ##    path,
    ##    names=column_headers,
    ##    dtype=data_types,
    ##    skiprows=headerlines,
    ##    skipfooter=skipfooter,
    ##    engine='python',
    ##    encoding=encoding,
   ## )
          
   ## dataframe = pd.read_csv(
   ##     path,
   ##     names=column_headers,
   ##     dtype=data_types,
   ##     skiprows=headerlines,
   ##     nrows=1000,
   ##     engine='python',
   ##     encoding=encoding,
   ##     index_col=False,
   ##     warn_bad_lines=True,
   ##     error_bad_lines=False,
   ## )
    
    dataframe = pd.read_csv(
        path,
        names=column_headers,
        dtype=data_types,
        skiprows=headerlines,
        nrows=1500,
        engine='python',
        encoding=encoding,
        index_col=False,
        warn_bad_lines=True,
        error_bad_lines=False,
        sep = ',',
    )
    #keep_default_na =False,

    dataframe=dataframe.dropna(axis=0, how='any')
    dataframe = dataframe.replace(to_replace='None', value=np.nan).dropna()

    #dataframe = dataframe.fillna(0, inplace =True)
    #dataframe = dataframe.astype('float',errors='ignore')
    




    


    # Strip leading and trailing whitespaces from string columns
    df_obj = dataframe.select_dtypes(['object'])
    dataframe[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    #dataframe[df_obj.columns] = df_obj.dropna()
    ##dataframe[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # If 'TIME' not present but 'HOUR' and 'MINUTE' is, then make time :)
    ##if (not 'TIME' in dataframe.columns
    ##        and 'HOUR' in dataframe.columns
    ##        and 'MINUTE' in dataframe.columns):
    ##    dataframe['TIME'] = [
    ##        f'{d.HOUR:02}{d.MINUTE:02}' for i, d in dataframe.iterrows()
    ##    ]

    #if ('CASTNO' in dataframe.columns):
    #    dataframe['CASTNO']=dataframe['CASTNO']
    #elif ( not 'CASTNO' in dataframe.columns):
    #    dataframe['CASTNO']=1
    #else:
    # print(STNNBR)



    FilterCondition=dataframe['CASTNO'].between(59,200).values
    dataframe.loc[FilterCondition, 'CASTNO']=0
    


    #FilterCondition=dataframe['DATE'].between(100209,100220).values
    #dataframe.loc[FilterCondition, 'DATE']=20100209

    if (not 'TIME' in dataframe.columns
            and 'HOUR' in dataframe.columns
            and 'MINUTE' in dataframe.columns):
        dataframe['TIME'] = [
            f'{d.HOUR:02}{d.MINUTE:02}' for i, d in dataframe.iterrows()
        ]
    elif (not 'TIME' in dataframe.columns):
         dataframe['TIME'] = [
                f'{d.CASTNO:06}' for i, d in dataframe.iterrows()
        ]
    elif ('TIME' in dataframe.columns):
        dataframe['TIME'] = [
                f'{d.CASTNO:06}' for i, d in dataframe.iterrows()
        ]
    else:
        print(df_obj)


        #if (not 'TIME' in dataframe.columns):
        # dataframe['TIME'] = [
        #        f'{d.STNNBR:06}' for i, d in dataframe.iterrows()
        #]
        

    
    
    # Add a datetime column
    if 'DATE' in dataframe.columns and 'TIME' in dataframe.columns:
        datetime = []
        
        for ix, d in enumerate(dataframe['DATE'],start=0):
            try:
                t = dataframe['TIME'][ix]
                print (ix,d)
                date='{}-{}-{}'.format(d[:4], d[4:6], d[6:])
                #date= dataframe['DATE'].apply(lambda d:.format(d[:4], d[4:6], d[6:]
                #date = filter(lambda d: d is not None,'{}-{}-{}'.format(d[:4], d[4:6], d[6:]))
                
                #print(date)
                #date='{}-{}-{}'.format(d[:4], d[4:6], d[6:])
                #print(d)
                #date='{}-{}-{}'.format(d[:4], d[4:6], d[6:])
                #print(date)
                time = '{}:{}'.format(t[:2], t[2:])               
                datetime.append(pd.to_datetime('{} {}'.format(date,time), utc=True))
                #datetime.append(pd.to_datetime(str(dataframe['DATE'])))
            except Exception as e:
                logger.error(
                        'Time format error (date: {} time: {} )) on line {}'
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
    #dataframe = dataframe.replace(np.nan, 0)
    # Add some extra metadata to the dataframe
    dataframe.whp_exchange.column_units = column_units
    dataframe.whp_exchange.signature = signature
    dataframe.whp_exchange.file_type = file_type
    dataframe.whp_exchange.comments = comments

    return dataframe
