"""A package to use with Google Earth Engine Python API."""
from ._version import __version__  # noqa: F401

__title__ = "geetools"
__summary__ = "A set of useful tools to use with Google Earth Engine Python" "API"
__uri__ = "http://geetools.readthedocs.io"

__author__ = "Rodrigo E. Principe"
__email__ = "fitoprincipe82@gmail.com"

__license__ = "MIT"
__copyright__ = "2017 Rodrigo E. Principe"

# from geetools import (
# bitreader,
# cloud_mask,
# expressions,
# decision_tree,
# indices,
# batch,
# algorithms,
# composite,
# manager,
# utils,
# collection,
# oauth,
# visualization,
# classification
# )
# from geetools.tools import (
# array,
# date,
# dictionary,
# ee_list,
# featurecollection,
# geometry,
# image,
# imagecollection,
# string
# )
# from geetools.ui import eprint
# from geetools.batch import Export, Import, Convert, Download
# from geetools.oauth import Initialize
# from geetools.utils import evaluate

from . import _deprecated_filters as filters  # noqa: F401
from .Array import Array  # noqa: F401
from .Filter import Filter  # noqa: F401
from .List import List  # noqa: F401
from .Number import Number  # noqa: F401
from .String import String  # noqa: F401

# reproduce older structure of the lib (deprecated)
# will be removed along the deprecation cycle
from .tools import (
    array,  # noqa: F401
    number,  # noqa: F401
    string,  # noqa: F401
)
