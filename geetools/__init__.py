"""A toolbox to use with Google Earth Engine Python API.

The ``geetools`` package extends the Google Earth Engine Python API with pre-processing and processing tools for the most used satellite platforms by adding utility methods for different Earth Engine Objects that are friendly with the Python method chaining using the geetools namespace.

.. jupyter-kernel:: python3
    :id: reference_kernel

.. jupyter-execute::

    import ee, geetools, os, re, httplib2

    if "EARTHENGINE_SERVICE_ACCOUNT" in os.environ:
        private_key = os.environ["EARTHENGINE_SERVICE_ACCOUNT"]
        private_key = private_key[1:-1] if re.compile(r"^'[^']*'$").match(private_key) else private_key
        ee.Initialize.geetools.from_service_account(private_key)

    elif "EARTHENGINE_PROJECT" in os.environ:
        ee.Initialize(project=os.environ["EARTHENGINE_PROJECT"], http_transport=httplib2.Http())

    else:
        raise ValueError("EARTHENGINE_SERVICE_ACCOUNT or EARTHENGINE_PROJECT environment variable is missing")
"""
import ee

# import the accessor namespace
from .accessors import geetools

# it needs to be imported first as it's the mother class
from .ee_computed_object import *

# reproduce older structure of the lib (deprecated)
# will be removed along the deprecation cycle
from . import _deprecated_algorithms as algorithms
from . import _deprecated_composite as composite
from .tools import imagecollection

# then we extend all the other classes
from .ee_asset import Asset
from .ee_date import DateAccessor
from .ee_dictionary import DictionaryAccessor
from .ee_feature import FeatureAccessor
from .ee_feature_collection import FeatureCollectionAccessor
from .ee_filter import FilterAccessor
from .ee_geometry import GeometryAccessor
from .ee_image import ImageAccessor
from .ee_join import JoinAccessor
from .ee_list import ListAccessor
from .ee_number import NumberAccessor
from .ee_string import StringAccessor
from .ee_image_collection import ImageCollectionAccessor
from .ee_initialize import InitializeAccessor
from .ee_authenticate import AuthenticateAccessor
from .ee_array import ArrayAccessor
from .ee_date_range import DateRangeAccessor
from .ee_export import ExportAccessor
from .ee_profiler import Profiler

__title__ = "geetools"
__summary__ = "A set of useful tools to use with Google Earth Engine Python" "API"
__uri__ = "http://geetools.readthedocs.io"
__version__ = "1.9.1"

__author__ = "Rodrigo E. Principe"
__email__ = "fitoprincipe82@gmail.com"

__license__ = "MIT"
__copyright__ = "2017 Rodrigo E. Principe"
