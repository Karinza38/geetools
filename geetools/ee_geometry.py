"""Toolbox for the :py:class:`ee.Geometry` class."""
from __future__ import annotations

import ee

from .accessors import register_class_accessor


@register_class_accessor(ee.Geometry, "geetools")
class GeometryAccessor:
    """Toolbox for the :py:class:`ee.Geometry` class."""

    def __init__(self, obj: ee.Geometry):
        """Initialize the Geometry class."""
        self._obj = obj

    def keepType(self, type: str) -> ee.Geometry:
        """Only keep the geometries of the given type from a GeometryCollection.

        Args:
            type: The type of geometries to keep. Can be one of: Point, LineString, LineRing Polygon.

        Returns:
            The geometries of the given type.

        Examples:
            .. jupyter-execute::

                import ee, geetools
                from geetools.utils import initialize_documentation

                initialize_documentation()

                # generate multiple geometries of different types
                point0 = ee.Geometry.Point([0,0], proj="EPSG:4326")
                point1 = ee.Geometry.Point([0,1], proj="EPSG:4326")
                poly0 = point0.buffer(1, proj="EPSG:4326")
                poly1 = point1.buffer(1, proj="EPSG:4326").bounds(proj="EPSG:4326")
                line = ee.Geometry.LineString([point1, point0], proj="EPSG:4326")
                multiPoly = ee.Geometry.MultiPolygon([poly0, poly1], proj="EPSG:4326")

                # create a geometry collection from them
                geometryCollection = ee.Algorithms.GeometryConstructors.MultiGeometry(
                    [multiPoly, poly0, poly1, point0, line],
                    crs="EPSG:4326",
                    geodesic=True,
                    maxError=1
                )

                # extract only the LineString geometries from the collection
                geom = geometryCollection.geetools.keepType('LineString')
                geom.getInfo()
        """
        # will raise an error if self is not a GeometryCollection
        error_msg = "This method can only be used with GeometryCollections"
        assert self._obj.type().getInfo() == "GeometryCollection", error_msg

        def filterType(geom):
            geom = ee.Geometry(geom)
            return ee.Algorithms.If(geom.type().compareTo(type), None, geom)

        geometries = self._obj.geometries().map(filterType, True)
        return getattr(ee.Geometry, "Multi" + type)(geometries, self._obj.projection())
