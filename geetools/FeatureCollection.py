"""Toolbox for the `ee.FeatureCollection` class."""
from __future__ import annotations

from typing import Union

import ee

from .accessors import geetools_accessor


@geetools_accessor(ee.FeatureCollection)
class FeatureCollection:
    """Toolbox for the `ee.FeatureCollection` class."""

    def __init__(self, obj: ee.FeatureCollection):
        """Initialize the FeatureCollection class."""
        self._obj = obj

    def toImage(
        self,
        color: Union[ee.String, str, ee.Number, int] = 0,
        width: Union[ee.String, str, ee.Number, int] = "",
    ) -> ee.Image:
        """Paint the current FeatureCollection to an Image.

        It's simply a wrapper on Image.paint() method

        Args:
            color: The pixel value to paint into every band of the input image, either as a number which will be used for all features, or the name of a numeric property to take from each feature in the collection.
            width: Line width, either as a number which will be the line width for all geometries, or the name of a numeric property to take from each feature in the collection. If unspecified, the geometries will be filled instead of outlined.
        """
        params = {"color": color}
        width == "" or params.update(width=width)
        return ee.Image().paint(self._obj, **params)

    def addId(
        self, name: Union[str, ee.String] = "id", start: Union[int, ee.Number] = 1
    ) -> ee.FeatureCollection:
        """Add a unique numeric identifier, starting from parameter ``start``.

        Returns:
            The parsed collection with a new id property

        Example:
            .. jupyter-execute::

                import ee
                import geetools

                ee.Initialize()

                fc = ee.FeatureCollection('FAO/GAUL/2015/level0')
                fc = fc.geetools.addId()
                print(fc.first().get('id').getInfo())
        """
        start, name = ee.Number(start).toInt(), ee.String(name)

        indexes = ee.List(self._obj.aggregate_array("system:index"))
        ids = ee.List.sequence(start, start.add(self._obj.size()).subtract(1))
        idByIndex = ee.Dictionary.fromLists(indexes, ids)
        return self._obj.map(
            lambda f: f.set(name, idByIndex.get(f.get("system:index")))
        )

    def mergeGeometries(self) -> ee.Geometry:
        """Merge the geometries the included features.

        Returns:
            the dissolved geometry

        Example:
            .. jupyter-execute::

                import ee
                import geetools

                ee.Initialize()

                fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
                fc =fc.filter(ee.Filter.inList("ADM0_CODE", [122, 237, 85]))
                geom = fc.geetools.mergeGeometries()
                print(geom.getInfo())
        """
        first = self._obj.first().geometry()
        union = self._obj.iterate(lambda f, g: f.geometry().union(g), first)
        return ee.Geometry(union).dissolve()

    def toPolygons(self) -> ee.FeatureCollection:
        """Drop any geometry that is not a Polygon or a multipolygon.

        This method is made to avoid errors when performing zonal statistics and/or other surfaces operations. These operations won't work on geometries that are Lines or points. The methods remove these geometry types from GEometryCollections and rremove features that don't have any polygon geometry

        Returns:
            The parsed collection with only polygon/MultiPolygon geometries

        Example:
            .. jupyter-execute::

                import ee
                import geetools

                ee.Initialize()

                fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
                fc =fc.filter(ee.Filter.inList("ADM0_CODE", [122, 237, 85]))
                fc = fc.geetools.toPolygon()
                print(fc.getInfo())
        """

        def filterGeom(geom):
            geom = ee.Geometry(geom)
            return ee.Algorithms.If(geom.type().compareTo("Polygon"), None, geom)

        def removeNonPoly(feat):
            filteredGeoms = feat.geometry().geometries().map(filterGeom, True)
            return feat.setGeometry(
                ee.Geometry.MultiPolygon(
                    filteredGeoms, geodesic=feat.geometry().geodesic()
                )
            )

        return self._obj.map(removeNonPoly)
