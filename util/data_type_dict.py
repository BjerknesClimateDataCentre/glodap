class DataType:
    """
    DataType simply has a name and a BODC identifier. It can be linked to
    a parent data type, which would be the datatype from the glodap data set.
    Glodap data types has is_ref_type = True, and should not have parent types.
    """
    name = None
    identifier = None
    parent_ref_type = None
    is_ref_type = False
    def __init__(
            self,
            name,
            identifier = None,
            parent_ref_type = None,
            is_ref_type = False,
    ):
        self.name = name
        self.identifier = identifier
        self.parent_ref_type = parent_ref_type
        self.is_ref_type = is_ref_type

    def set_parent_reference_type(self, parent_ref_type):
        self.parent_ref_type = parent_ref_type

    def __str__(self):
        return self.name

class DataTypeDict():
    """This class is a simple mapping of variable names in glodap, to bodc
    vocabularies. It is implemented as an iterable class. Usage:

    >>> a = DataTypeDict()
    >>> a['OXYGEN']
    <glodap.util.data_type_dict.DataTypeDict.DataType object at 0x7f11d0230d30>

    >>> for key in a:
            print("{}".format(a[key]))
    G2cfc11
    salinity
    G2oxygen
    ...

    Vocabularies are available from the bodc vocabulary search at:
    https://www.bodc.ac.uk/resources/vocabularies/vocabulary_search/
    https://www.bodc.ac.uk/resources/vocabularies/vocabulary_search/P01/

    Data types updated from
    https://git.geomar.de/patrick-michaelis/python-for-glodap/blob/master/glodap.py
    """
    reference_types={
        'aou'          : 'SDN:P01::AOUXXXXX',
        'c13'          : 'SDN:P01::D13COPXX',
        'c14'          : 'SDN:P01::D14CMIXX',
        'c14err'       : 'SDN:P01::D14CMIER',
        'ccl4'         : 'SDN:P01::CCL4AFX1',
        'cfc11'        : 'SDN:P01::MDMAP001',
        'cfc113'       : 'SDN:P01::MDMAP003',
        'cfc12'        : 'SDN:P01::MDMAP002',
        'chla'         : 'SDN:P01::CPHLZZXX',
        'doc'          : 'SDN:P01::CORGZZZX',
        'don'          : 'SDN:P01::MDMAP008',
        'gamma'        : 'SDN:P01::NEUTDENS',
        'h3'           : 'SDN:P01::ACTVM012',
        'h3err'        : 'SDN:P01::DHE3XXER',
        'he'           : 'SDN:P01::HECNMASS',
        'he3'          : 'SDN:P01::DHE3XX01',
        'he3err'       : 'SDN:P01::S3HHMXTX',
        'heerr'        : 'SDN:P01::HECNMAER',
        'neon'         : 'SDN:P01::NECNMASS',
        'neonerr'      : 'SDN:P01::NECNMAER',
        'nitrate'      : 'SDN:P01::NTRAZZXX',
        'nitrite'      : 'SDN:P01::NTRIZZXX',
        'o18'          : 'SDN:P01::D18OSDWT', # Alt:  D18OMXDG (in dissolved O2)
        'oxygen'       : 'SDN:P01::DOXMZZXX',
        'pccl4'        : 'SDN:P01::PCCL4XXX',
        'pcfc11'       : 'SDN:P01::PF11GCTX',
        'pcfc113'      : 'SDN:P01::P113GCTX',
        'pcfc12'       : 'SDN:P01::PF12GCTX',
        'phosphate'    : 'SDN:P01::PHOSZZXX',
        'phts25p0'     : 'SDN:P01::PHTLSX25',
        'phtsinsitutp' : 'SDN:P01::PHFRSXXX',
        'pressure'     : 'SDN:P01::PRESPR01',
        'psf6'         : 'SDN:P01::PSF6XXXX',
        'salinity'     : 'SDN:P01::PSALST01',
        'sf6'          : 'SDN:P01::PSF6XXXX',
        'sigma0'       : 'SDN:P01::POTDENS0',
        'sigma1'       : 'SDN:P01::POTDENS1',
        'sigma2'       : 'SDN:P01::POTDENS2',
        'sigma3'       : 'SDN:P01::POTDENS3',
        'sigma4'       : 'SDN:P01::POTDENS4',
        'silicate'     : 'SDN:P01::SLCAZZXX',
        'talk'         : 'SDN:P01::ALKYZZXX',
        'tco2'         : 'SDN:P01::PCO2XXXX',
        'tdn'          : 'SDN:P01::MDMAP013',
        'temperature'  : 'SDN:P01::TEMPPR01',
        'theta'        : 'SDN:P01::SIGTEQ01',
        'toc'          : 'SDN:P01::MDMAP011',
    }

    exchange_types={
        'ALKALI'       : 'SDN:P01::ALKYZZXX',
        'C14ERR'       : 'SDN:P01::D14CMIER',
        'CCL4'         : 'SDN:P01::CCL4AFX1',
        'CFC_11'       : 'SDN:P01::MDMAP001',
        'CFC_12'       : 'SDN:P01::MDMAP002',
        'CFC-11'       : 'SDN:P01::MDMAP001',
        'CFC-12'       : 'SDN:P01::MDMAP002',
        'CFC113'       : 'SDN:P01::MDMAP003',
        'CHLORA'       : 'SDN:P01::CPHLZZXX',
        'CHLORA'       : 'SDN:P01::CPHLZZXX',
        'CTDOXY'       : 'SDN:P01::DOXMZZXX',
        'CTDPRS'       : 'SDN:P01::PRESPR01',
        'CTDSAL'       : 'SDN:P01::PSALST01',
        'CTDTMP'       : 'SDN:P01::TEMPPR01',
        'DELC13'       : 'SDN:P01::D13COPXX',
        'DELC14'       : '',
        'DELHE3'       : '',
        'DELHER'       : '',
        'DELO18'       : '',
        'DOC'          : 'SDN:P01::CORGZZZX',
        'DON'          : 'SDN:P01::MDMAP008',
        'HELIER'       : 'SDN:P01::DHE3XXER',
        'HELIUM'       : 'SDN:P01::HECNMASS',
        'NEON'         : 'SDN:P01::NECNMASS',
        'NEONER'       : 'SDN:P01::NECNMAER',
        'NITRAT'       : 'SDN:P01::NTRAZZXX',
        'NITRIT'       : 'SDN:P01::NTRIZZXX',
        'NO2+NO3'      : 'SDN:P01::NTRAZZXX',
        'NO2NO3'       : 'SDN:P01::NTRAZZXX',
        'OXYGEN'       : 'SDN:P01::DOXMZZXX',
        'PH_SWS'       : 'SDN:P01::PHFRSXXX',
        'PH_TMP'       : 'SDN:P01::PHFRSXXX',
        'PH_TOT'       : 'SDN:P01::PHFRSXXX',
        'PH_TS'        : 'SDN:P01::PHFRSXXX',
        'PH'           : 'SDN:P01::PHFRSXXX',
        'PHAEO'        : 'SDN:P01::PTAXZZXX',
        'PHSPHT'       : 'SDN:P01::PHOSZZXX',
        'SALNTY'       : 'SDN:P01::PSALST01', # absolute salinity SDN:P01::ASLTZZ01
        'SF6'          : 'SDN:P01::PSF6XXXX',
        'SILCAT'       : 'SDN:P01::SLCAZZXX',
        'TCARBN'       : 'SDN:P01::PCO2XXXX',
        'TDN'          : 'SDN:P01::MDMAP013',
        'THETA'        : 'SDN:P01::POTMCV01',
        'TOC'          : 'SDN:P01::MDMAP011',
        'TRITER'       : 'SDN:P01::DHE3XXER',
        'TRITUM'       : 'SDN:P01::ACTVM012',
    }

    typelist = {}



    def __init__(self):
        for name in self.reference_types:
            self.typelist[name] = DataType(
                name,
                is_ref_type = True,
                identifier = self.reference_types[name]
            )
        for name in self.exchange_types:
            self.typelist[name] = DataType(
                name,
                parent_ref_type = self.typelist.get(
                    self.get_ref_type(self.exchange_types[name])
                ),
                identifier = self.exchange_types[name],
            )

    def getIdentifier(self, var_name):
        return self.typelist.get(var_name).identifier

    def get_ref_type(self, identifier):
        for k,v in self.reference_types.items():
            if v == identifier:
                return k
        return None

    def __iter__(self):
        return iter(self.typelist)

    def __getitem__(self, key):
        return self.typelist[key]

    def __len__(self):
        return len(self.typelist)

    def items(self):
        return self.typelist.items()
