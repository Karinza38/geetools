"""Toolbox for the ``ee.ImageCollection`` class."""
from __future__ import annotations

import uuid
from typing import Optional, Union

import ee
import ee_extra

from geetools.accessors import geetools_accessor
from geetools.types import ee_list, number


@geetools_accessor(ee.ImageCollection)
class ImageCollection:
    """Toolbox for the ``ee.ImageCollection`` class."""

    def __init__(self, obj: ee.ImageCollection):
        """Instantiate the class."""
        self._obj = obj

    # -- ee-extra wrapper ------------------------------------------------------
    def maskClouds(
        self,
        method: str = "cloud_prob",
        prob: int = 60,
        maskCirrus: bool = True,
        maskShadows: bool = True,
        scaledImage: bool = False,
        dark: float = 0.15,
        cloudDist: int = 1000,
        buffer: int = 250,
        cdi: Optional[int] = None,
    ) -> ee.ImageCollection:
        """Masks clouds and shadows in each image of an ImageCollection (valid just for Surface Reflectance products).

        Parameters:
            self: ImageCollection to mask.
            method: Method used to mask clouds. This parameter is ignored for Landsat products.
                Available options:
                    - 'cloud_prob' : Use cloud probability.
                    - 'qa' : Use Quality Assessment band.
            prob: Cloud probability threshold. Valid just for method = 'cloud_prob'. This parameter is ignored for Landsat products.
            maskCirrus: Whether to mask cirrus clouds. Default to ``True``. Valid just for method = 'qa'. This parameter is ignored for Landsat products.
            maskShadows: Whether to mask cloud shadows. Default to ``True`` This parameter is ignored for Landsat products.
            scaledImage: Whether the pixel values are scaled to the range [0,1] (reflectance values). This parameter is ignored for Landsat products.
            dark: NIR threshold. NIR values below this threshold are potential cloud shadows. This parameter is ignored for Landsat products.
            cloudDist: Maximum distance in meters (m) to look for cloud shadows from cloud edges. This parameter is ignored for Landsat products.
            buffer: Distance in meters (m) to dilate cloud and cloud shadows objects. This parameter is ignored for Landsat products.
            cdi: Cloud Displacement Index threshold. Values below this threshold are considered potential clouds. A cdi = None means that the index is not used. This parameter is ignored for Landsat products.

        Returns:
            Cloud-shadow masked image.

        Notes:
            This method may mask water as well as clouds for the Sentinel-3 Radiance product.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()
                S2 = (
                    ee.ImageCollection('COPERNICUS/S2_SR')
                    .maskClouds(prob = 75,buffer = 300,cdi = -0.5)
                    .first()
                )

        """
        return ee_extra.QA.clouds.maskClouds(
            self._obj,
            method,
            prob,
            maskCirrus,
            maskShadows,
            scaledImage,
            dark,
            cloudDist,
            buffer,
            cdi,
        )

    def closest(
        self, date: Union[ee.Date, str], tolerance: int = 1, unit: str = "month"
    ) -> ee.ImageCollection:
        """Gets the closest image (or set of images if the collection intersects a region that requires multiple scenes) to the specified date.

        Parameters:
            date: Date of interest. The method will look for images closest to this date.
            tolerance: Filter the collection to [date - tolerance, date + tolerance) before searching the closest image. This speeds up the searching process for collections with a high temporal resolution.
            unit: Units for tolerance. Available units: 'year', 'month', 'week', 'day', 'hour', 'minute' or 'second'.

        Returns:
            Closest images to the specified date.

        Examples:
            .. code-block:: python

                import ee
                import geetools

                s2 = ee.ImageCollection('COPERNICUS/S2_SR').closest('2020-10-15')
                s2.size().getInfo()
        """
        return ee_extra.ImageCollection.core.closest(self._obj, date, tolerance, unit)

    def spectralIndices(
        self,
        index: str = "NDVI",
        G: number = 2.5,
        C1: number = 6.0,
        C2: number = 7.5,
        L: number = 1.0,
        cexp: number = 1.16,
        nexp: number = 2.0,
        alpha: number = 0.1,
        slope: number = 1.0,
        intercept: number = 0.0,
        gamma: number = 1.0,
        omega: number = 2.0,
        beta: number = 0.05,
        k: number = 0.0,
        fdelta: number = 0.581,
        kernel: str = "RBF",
        sigma: str = "0.5 * (a + b)",
        p: number = 2.0,
        c: number = 1.0,
        lambdaN: number = 858.5,
        lambdaR: number = 645.0,
        lambdaG: number = 555.0,
        online: number = False,
    ) -> ee.ImageCollection:
        """Computes one or more spectral indices (indices are added as bands) for an image from the Awesome List of Spectral Indices.

        Parameters:
            self: Image to compute indices on. Must be scaled to [0,1].
            index: Index or list of indices to compute, default = 'NDVI'
                Available options:
                    - 'vegetation' : Compute all vegetation indices.
                    - 'burn' : Compute all burn indices.
                    - 'water' : Compute all water indices.
                    - 'snow' : Compute all snow indices.
                    - 'urban' : Compute all urban (built-up) indices.
                    - 'kernel' : Compute all kernel indices.
                    - 'all' : Compute all indices listed below.
                    - Awesome Spectral Indices for GEE: Check the complete list of indices `here <https://awesome-ee-spectral-indices.readthedocs.io/en/latest/list.html>`_.
            G: Gain factor. Used just for index = 'EVI', default = 2.5
            C1: Coefficient 1 for the aerosol resistance term. Used just for index = 'EVI', default = 6.0
            C2: Coefficient 2 for the aerosol resistance term. Used just for index = 'EVI', default = 7.5
            L: Canopy background adjustment. Used just for index = ['EVI','SAVI'], default = 1.0
            cexp: Exponent used for OCVI, default = 1.16
            nexp: Exponent used for GDVI, default = 2.0
            alpha: Weighting coefficient used for WDRVI, default = 0.1
            slope: Soil line slope, default = 1.0
            intercept: Soil line intercept, default = 0.0
            gamma: Weighting coefficient used for ARVI, default = 1.0
            omega: Weighting coefficient  used for MBWI, default = 2.0
            beta: Calibration parameter used for NDSIns, default = 0.05
            k: Slope parameter by soil used for NIRvH2, default = 0.0
            fdelta: Adjustment factor used for SEVI, default = 0.581
            kernel: Kernel used for kernel indices, default = 'RBF'
                Available options:
                    - 'linear' : Linear Kernel.
                    - 'RBF' : Radial Basis Function (RBF) Kernel.
                    - 'poly' : Polynomial Kernel.
            sigma: Length-scale parameter. Used for kernel = 'RBF', default = '0.5 * (a + b)'. If str, this must be an expression including 'a' and 'b'. If numeric, this must be positive.
            p: Kernel degree. Used for kernel = 'poly', default = 2.0
            c: Free parameter that trades off the influence of higher-order versus lower-order terms in the polynomial kernel. Used for kernel = 'poly', default = 1.0. This must be greater than or equal to 0.
            lambdaN: NIR wavelength used for NIRvH2 and NDGI, default = 858.5
            lambdaR: Red wavelength used for NIRvH2 and NDGI, default = 645.0
            lambdaG: Green wavelength used for NDGI, default = 555.0
            drop: Whether to drop all bands except the new spectral indices, default = False

        Returns:
            Image with the computed spectral index, or indices, as new bands.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()
                image = ee.Image('COPERNICUS/S2_SR/20190828T151811_20190828T151809_T18GYT')
                image = image.geetools.specralIndices(["NDVI", "NDFI"])
        """
        # fmt: off
        return ee_extra.Spectral.core.spectralIndices(
            self._obj, index, G, C1, C2, L, cexp, nexp, alpha, slope, intercept, gamma, omega,
            beta, k, fdelta, kernel, sigma, p, c, lambdaN, lambdaR, lambdaG, online,
            drop=False,
        )
        # fmt: on

    def getScaleParams(self) -> dict:
        """Gets the scale parameters for each band of the image.

        Returns:
            Dictionary with the scale parameters for each band.


        Examples:
            .. code-block:: python

                import ee
                import geetools

                ee.Initialize()

                ee.ImageCollection('MODIS/006/MOD11A2').geetools.getScaleParams()
        """
        return ee_extra.STAC.core.getScaleParams(self._obj)

    def getOffsetParams(self) -> dict:
        """Gets the offset parameters for each band of the image.

        Returns:
            Dictionary with the offset parameters for each band.

        Examples:
            .. code-block:: python

            import ee
            import geetools

            ee.Initialize()

            ee.ImageCollection('MODIS/006/MOD11A2').getOffsetParams()
        """
        return ee_extra.STAC.core.getOffsetParams(self._obj)

    def scaleAndOffset(self) -> ee.ImageCollection:
        """Scales bands on an image according to their scale and offset parameters.

        Returns:
            Scaled image.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                S2 = ee.ImageCollection('COPERNICUS/S2_SR').scaleAndOffset()
        """
        return ee_extra.STAC.core.scaleAndOffset(self._obj)

    def preprocess(self, **kwargs) -> ee.ImageCollection:
        """Pre-processes the image: masks clouds and shadows, and scales and offsets the image.

        Parameters:
            **kwargs: Keywords arguments for ``maskClouds`` method.

        Returns:
            Pre-processed image.

        Examples:
            .. code-block:: python

            import ee
            import geetools

            ee.Initialize()
            S2 = ee.ImageCollection('COPERNICUS/S2_SR').preprocess()
        """
        return ee_extra.QA.pipelines.preprocess(self._obj, **kwargs)

    def getSTAC(self) -> dict:
        """Gets the STAC of the image.

        Returns:
            STAC of the image.

        Examples:
            .. code-block:: python

            import ee
            import geetools

            ee.Initialize()

            ee.ImageCollection('COPERNICUS/S2_SR').getSTAC()
        """
        return ee_extra.STAC.core.getSTAC(self._obj)

    def getDOI(self) -> str:
        """Gets the DOI of the image, if available.

        Returns:
            DOI of the ee.Image dataset.

        Examples:
            .. code-block:: python

                import ee
                import geetools

                ee.Initialize()

                ee.ImageCollection('NASA/GPM_L3/IMERG_V06').getDOI()
        """
        return ee_extra.STAC.core.getDOI(self._obj)

    def getCitation(self) -> str:
        """Gets the citation of the image, if available.

        Returns:
            Citation of the ee.Image dataset.

        Examples:
            .. code-block:: python

                import ee
                import geetools

                ee.Initialize()

                ee.ImageCollection('NASA/GPM_L3/IMERG_V06').getCitation()
        """
        return ee_extra.STAC.core.getCitation(self._obj)

    def panSharpen(self, method: str = "SFIM", qa: str = "", **kwargs) -> ee.ImageCollection:
        """Apply panchromatic sharpening to the ImageCollection images.

        Optionally, run quality assessments between the original and sharpened Image to
        measure spectral distortion and set results as properties of the sharpened Image.

        Parameters:
            method: The sharpening algorithm to apply. Current options are "SFIM" (Smoothing Filter-based Intensity Modulation), "HPFA" (High Pass Filter Addition), "PCS" (Principal Component Substitution), and "SM" (simple mean). Different sharpening methods will produce different quality sharpening results in different scenarios.
            qa: One or more optional quality assessment names to apply after sharpening. Results will be stored as image properties with the pattern `geetools:metric`, e.g. `geetools:RMSE`.
            **kwargs: Keyword arguments passed to ee.Image.reduceRegion() such as "geometry", "maxPixels", "bestEffort", etc. These arguments are only used for PCS sharpening and quality assessments.

        Returns:
            The ImageCollections with all sharpenable bands sharpened to the panchromatic resolution and quality assessments run and set as properties.

        Examples:
            .. code-block:: python

                import ee
                import geetools

                ee.Initialize()

                source = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_047027_20160819")
                sharp = source.panSharpen(method="HPFA", qa=["MSE", "RMSE"], maxPixels=1e13)
        """
        return ee_extra.Algorithms.core.panSharpen(
            img=self._obj, method=method, qa=qa or None, prefix="geetools", **kwargs
        )

    def tasseledCap(self) -> ee.ImageCollection:
        """Calculates tasseled cap brightness, wetness, and greenness components.

        Tasseled cap transformations are applied using coefficients published for these
        supported platforms:

        * Sentinel-2 MSI Level 1C
        * Landsat 9 OLI-2 SR
        * Landsat 9 OLI-2 TOA
        * Landsat 8 OLI SR
        * Landsat 8 OLI TOA
        * Landsat 7 ETM+ TOA
        * Landsat 5 TM Raw DN
        * Landsat 4 TM Raw DN
        * Landsat 4 TM Surface Reflectance
        * MODIS NBAR

        Parameters:
            self: ee.ImageCollection to calculate tasseled cap components for. Must belong to a supported platform.

        Returns:
            ImageCollections with the tasseled cap components as new bands.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                image = ee.Image('COPERNICUS/S2_SR')
                img = img.tasseledCap()
        """
        return ee_extra.Spectral.core.tasseledCap(self._obj)

    def append(self, image: ee.Image) -> ee.ImageCollection:
        """Append an image to the existing image collection.

        Args:
            image: Image to append to the collection.

        Returns:
            ImageCollection with the new image appended.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                ic = ee.ImageCollection('COPERNICUS/S2_SR');

                geom = ee.Geometry.Point(-122.196, 41.411);
                ic2018 = ic.filterBounds(geom).filterDate('2019-07-01', '2019-10-01')
                ic2021 = ic.filterBounds(geom).filterDate('2021-07-01', '2021-10-01')

                ic = ic2018.append(ic2021.first())
                ic.getInfo()
        """
        return self._obj.merge(ee.ImageCollection([image]))

    def collectionMask(self) -> ee.Image:
        """A binary ee.Image where only pixels that are masked in all images of the collection get masked.

        Returns:
            ee.Image of the mask. 1 where at least 1 pixel is valid 0 elswere

        Examples:
            .. code-block::

                import ee, geetools

                ee.Initialize()

                ic = ee.ImageCollection('COPERNICUS/S2_SR');

                geom = ee.Geometry.Point(-122.196, 41.411);
                ic2018 = ic.filterBounds(geom).filterDate('2019-07-01', '2019-10-01')
                ic = ic2018.geetools.collectionMask()
                ic.getInfo()
        """
        masks = self._obj.map(lambda i: i.mask())
        return ee.Image(masks.sum().gt(0))

    def iloc(self, index: int) -> ee.Image:
        """Get Image from the ImageCollection by index.

        Args:
            index: Index of the image to get.

        Returns:
            ee.Image at the specified index.

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                ic = ee.ImageCollection('COPERNICUS/S2_SR');

                geom = ee.Geometry.Point(-122.196, 41.411);
                ic2018 = ic.filterBounds(geom).filterDate('2019-07-01', '2019-10-01')
                ic2018.geetools.iloc(0).getInfo()
        """
        return ee.Image(self._obj.toList(self._obj.size()).get(index))

    def integral(self, band: str, time: str = "system:time_start", unit: str = "") -> ee.Image:
        """Compute the integral of a band over time or a specified property.

        Args:
            band: the name of the band to integrate
            time: the name of the property to use as time. It must be a date property of the images.
            unit: the time unit use to compute the integral. It can be one of the following: ["year", "month", "day", "hour", "minute", "second"]. If non is set, the time will be normalized on the integral length.

        Returns:
            An Image object with the integrated band for each pixel

        Examples:
            .. code-block:: python

                import ee, LDCGEETools

                collection = (
                    ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
                    .filterBounds(ee.Geometry.Point(-122.262, 37.8719))
                    .filterDate("2014-01-01", "2014-12-31")
                )

                integral = collection.ldc.integral("B1")
                print(integral.getInfo())
        """
        # compute the intervals along the x axis
        # the GEE time is stored as a milliseconds timestamp. If the time unit is not set,
        # the integral is normalized on the total time length of the time series
        minTime = self._obj.aggregate_min(time)
        maxTime = self._obj.aggregate_max(time)
        intervals = {
            "year": ee.Number(1000 * 60 * 60 * 24 * 365),  # 1 year in milliseconds
            "month": ee.Number(1000 * 60 * 60 * 24 * 30),  # 1 month in milliseconds
            "day": ee.Number(1000 * 60 * 60 * 24),  # 1 day in milliseconds
            "hour": ee.Number(1000 * 60 * 60),  # 1 hour in milliseconds
            "minute": ee.Number(1000 * 60),  # 1 minute in milliseconds
            "second": ee.Number(1000),  # 1 second in milliseconds
            "": ee.Number(maxTime).subtract(ee.Number(minTime)),
        }
        interval = intervals[unit]

        # initialize the sum with a 0 value initial item
        # all the properties of the first image of the collection are copied
        first = self._obj.first()
        zero = ee.Image.constant(0).copyProperties(first, first.propertyNames())
        s = ee.Image(zero).rename("integral").set("last", zero)

        # compute the approximation of the integral using the trapezoidal method
        # each local interval is aproximated by the corresponding trapez and the
        # sum is updated
        def computeIntegral(image, integral):
            image = ee.Image(image).select(band)
            integral = ee.Image(integral)
            last = ee.Image(integral.get("last"))
            locMinTime = ee.Number(last.get(time))
            locMaxTime = ee.Number(image.get(time))
            locInterval = locMaxTime.subtract(locMinTime).divide(interval)
            locIntegral = last.add(image).multiply(locInterval).divide(2)
            return integral.add(locIntegral).set("last", image)

        return ee.Image(self._obj.iterate(computeIntegral, s))

    def containsBandNames(self, bandNames: ee_list, filter: str) -> ee.ImageCollection:
        """Filter the ImageCollection by band names using the provided filter.

        Args:
            bandNames: list of band names to filter
            filter: type of filter to apply. To keep images that contains all the specified bands use "ALL". To get the images including at least one of the specified band use "ANY".

        Returns:
            A filtered ImageCollection

        Examples:
            .. code-block:: python

                import ee, LDCGEETools

                collection = (
                    ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
                    .filterBounds(ee.Geometry.Point(-122.262, 37.8719))
                    .filterDate("2014-01-01", "2014-12-31")
                )

                filtered = collection.ldc.containsBandNames(["B1", "B2"], "ALL")
                print(filtered.getInfo())
        """
        # cast parameters
        filter = {"ALL": "Filter.and", "ANY": "Filter.or"}[filter]
        bandNames = ee.List(bandNames)

        # add bands as metadata in a temporary property
        band_name = uuid.uuid4().hex
        ic = self._obj.map(lambda i: i.set(band_name, i.bandNames()))

        # create a filter by combining a listContain filter over all the band names from the
        # user list. Combine them with a "Or" to get a "any" filter and "And" to get a "all".
        # We use a workaround until this is solved: https://issuetracker.google.com/issues/322838709
        filterList = bandNames.map(lambda b: ee.Filter.listContains(band_name, b))
        filterCombination = ee.ApiFunction._call(filter, ee.List(filterList))

        # apply this filter and remove the temporary property. Exclude parameter is additive so
        # we do a blank multiplication to remove all the properties beforhand
        ic = ee.imageCollection(ic.filter(filterCombination))
        ic = ic.map(lambda i: ee.image(i.multiply(1).copyProperties(i, exclude=[band_name])))

        return ee.ImageCollection(ic)

    def containsAllBands(self, bandNames: ee_list) -> ee.ImageCollection:
        """Filter the ImageCollection keeping only the images with all the provided bands.

        Args:
            bandNames: list of band names to filter

        Returns:
            A filtered ImageCollection

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                collection = (
                    ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
                    .filterBounds(ee.Geometry.Point(-122.262, 37.8719))
                    .filterDate("2014-01-01", "2014-12-31")
                )

                filtered = collection.ldc.containsAllBands(["B1", "B2"])
                print(filtered.getInfo())
        """
        return self.containsBandNames(bandNames, "ALL")

    def containsAnyBand(self, bandNames: ee_list) -> ee.ImageCollection:
        """Filter the ImageCollection keeping only the images with any of the provided bands.

        Args:
            bandNames: list of band names to filter

        Returns:
            A filtered ImageCollection

        Examples:
            .. code-block:: python

                import ee, geetools

                ee.Initialize()

                collection = (
                    ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
                    .filterBounds(ee.Geometry.Point(-122.262, 37.8719))
                    .filterDate("2014-01-01", "2014-12-31")
                )

                filtered = collection.ldc.containsAnyBand(["B1", "B2"])
                print(filtered.getInfo())
        """
        return self.containsBandNames(bandNames, "ANY")
