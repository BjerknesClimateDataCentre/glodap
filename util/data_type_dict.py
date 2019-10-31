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

    """
    reference_types={
        'tco2'         : 'SDN:P01::PCO2XXXX',
        'talk'         : 'SDN:P01::ALKYZZXX',
        'oxygen'       : 'SDN:P01::DOKGWITX',
        'nitrate'      : 'SDN:P01::MDMAP005',
        'phosphate'    : 'SDN:P01::PHOSZZXX',
        'silicate'     : 'SDN:P01::SLCAZZXX',
        'salinity'     : 'SDN:P01::PSALST01',
        'phts25p0'     : 'SDN:P01::PHTLSX25',
        'theta'        : 'SDN:P01::SIGTEQ01',
        'doc'          : 'SDN:P01::CORGZZZX',
        'cfc11'        : 'SDN:P01::MDMAP001',
        'cfc12'        : 'SDN:P01::MDMAP002',
        'aou'          : 'SDN:P01::AOUXXXXX',
        'tdn'          : 'SDN:P01::MDMAP013',
        'pcfc11'       : 'SDN:P01::PF11GCTX',
        'pressure'     : 'SDN:P01::PRESPR01',
        'gamma'        : 'SDN:P01::NEUTDENS',
        'he3err'       : 'SDN:P01::S3HHMXTX',
        'sigma1'       : 'SDN:P01::POTDENS1',
        'cfc113'       : 'SDN:P01::MDMAP003',
        'pcfc12'       : 'SDN:P01::PF12GCTX',
        'sigma3'       : 'SDN:P01::POTDENS3',
        'c14'          : 'SDN:P01::D14CMIXX',
        'psf6'         : 'SDN:P01::PSF6XXXX',
        'he3'          : 'SDN:P01::DHE3XX01',
        'c14err'       : 'SDN:P01::D14CMIER',
        'neon'         : 'SDN:P01::NECNMASS',
        'neonerr'      : 'SDN:P01::NECNMAER',
        'pcfc113'      : 'SDN:P01::P113GCTX',
        'sf6'          : 'SDN:P01::PSF6XXXX',
        'pccl4'        : 'SDN:P01::PCCL4XXX',
        'sigma2'       : 'SDN:P01::POTDENS2',
        'sigma4'       : 'SDN:P01::POTDENS4',
        'ccl4'         : 'SDN:P01::CCL4AFX1',
        'toc'          : 'SDN:P01::MDMAP011',
        'temperature'  : 'SDN:P01::TEMPPR01',
        'he'           : 'SDN:P01::HECNMASS',
        'c13'          : 'SDN:P01::D13COPXX',
        'nitrite'      : 'SDN:P01::NTRIZZXX',
        'o18'          : 'SDN:P01::D18OSDWT', # Alt:  D18OMXDG (in dissolved O2)
        'sigma0'       : 'SDN:P01::POTDENS0',
        'don'          : 'SDN:P01::MDMAP008',
        'h3'           : 'SDN:P01::ACTVM012',
        'heerr'        : 'SDN:P01::HECNMAER',
        'h3err'        : 'SDN:P01::DHE3XXER',
        'phtsinsitutp' : 'SDN:P01::PHFRSXXX',
        'chla'         : 'SDN:P01::CPHLZZXX',
    }

    exchange_types={
        'TCARBN'       : 'SDN:P01::PCO2XXXX',
        'ALKALI'       : 'SDN:P01::ALKYZZXX',
        'OXYGEN'       : 'SDN:P01::DOXMZZXX',
        'NITRAT'       : 'SDN:P01::NTRAZZXX',
        'PHSPHT'       : 'SDN:P01::PHOSZZXX',
        'SILCAT'       : 'SDN:P01::SLCAZZXX',
        'SALNTY'       : 'SDN:P01::PSALST01', # absolute salinity SDN:P01::ASLTZZ01
        'CTDSAL'       : 'SDN:P01::PSALST01',
        'CTDOXY'       : 'SDN:P01::DOXMZZXX',
        'PH_TOT'       : 'SDN:P01::PHFRSXXX',
        'THETA'        : 'SDN:P01::POTMCV01',
        'DOC'          : 'SDN:P01::CORGZZZX',
        'CFC_11'       : 'SDN:P01::MDMAP001',
        'CFC_12'       : 'SDN:P01::MDMAP002',
        'CTDTMP'       : 'SDN:P01::TEMPPR01',
        'NO2+NO3'      : 'SDN:P01::NTRZYYDZ',
        'NITRIT'       : 'SDN:P01::NTRIZZXX',
        'CTDPRS'       : 'SDN:P01::PRESPR01',
        'CFC-11'       : 'SDN:P01::MDMAP001',
        'CFC-12'       : 'SDN:P01::MDMAP002',
        'SF6'          : 'SDN:P01::PSF6XXXX',
        'CHLORA'       : 'SDN:P01::CPHLZZXX',
        'PHAEO'        : 'SDN:P01::PTAXZZXX',
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
