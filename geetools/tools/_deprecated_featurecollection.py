"""Legacy tools for ``ee.FeatureCollection``."""
from deprecated.sphinx import deprecated


@deprecated(
    version="1.0.0", reason="Use ee.FeatureCollection.aggregate_array.distinct instead"
)
def listOptions(collection, propertyName):
    """List all available values of `propertyName` in a feature collection."""
    return collection.aggregate_array(propertyName).distinct()


@deprecated(version="1.0.0", reason="Use ee.FeatureCollection.geetools.addId instead")
def addId(collection, name="id", start=1):
    """Add a unique numeric identifier, from parameter ``start``."""
    return collection.geetools.addId(name, start)


@deprecated(
    version="1.0.0", reason="Use ee.FeatureCollection.geetools.mergeGeometries instead"
)
def mergeGeometries(collection):
    """Merge the geometries of many features. Return ee.Geometry."""
    return collection.geetools.mergeGeometries()
