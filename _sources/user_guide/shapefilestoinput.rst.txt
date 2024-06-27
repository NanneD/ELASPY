.. _shapefilestoinput:

Shapefiles to input
===================

Shapefiles were used to create the input data :ref:`NODES_FILE<nodesfile>`. In this section, the steps are discussed to process the shapefiles. `QGIS <https://www.qgis.org/en/site/>`_ was used, but other software could also be suitable.

Data sources
++++++++++++

Two different data sets were used, both from the CBS. This is a Dutch organization that provides data sets on many subjects. A data set with `region data <https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/cbs-gebiedsindelingen>`_ and with `postal code data <https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode>`_ were used.

Loading the data
++++++++++++++++

- Create a new QGIS document.
- Load the geopackage "cbs_pc4_2021_v2.gpkg" and "cbsgebiedsindelingen2021.gpkg".
- Add layers "cbs_pc4_2021" and "provincie_gegeneraliseerd" to the map. Layer "provincie_gegeneraliseerd" should be above layer "cbs_pc4_2021" for improved visibility.

Creating a postal code layer of a province
++++++++++++++++++++++++++++++++++++++++++

- Manually select all postal codes of the province you want to consider (such as Utrecht), by selecting all postal codes of layer "cbs_pc4_2021" of that province. Note that you cannot simply create an intersection with "provincie_gegeneraliseerd" as this is cartographically simplified. 
- Save the selection by right clicking on the "cbs_pc4_2021" layer and selecting "export > save selected features as". Save it with a clear name, such as "province_pc4_2021.gpkg" with "save only selected features" selected. The new layer is then called "province_pc4_2021".

Adding centroids
++++++++++++++++

- Go to "processing toolbox > vector geometry > centroids".
- Use as input layer "province_pc4_2021.gpkg" and press "run".
- Rename the resulting layer to "Centroids".
- Save the new layer as geopackage by right clicking on the layer and selecting "make permanent". You can call it "Centroids", for example.

Adding centroid attributes
++++++++++++++++++++++++++

- Go to "processing toolbox > vector geometry > add geometry attributes" while having the "Centroids" layer selected.
- Use "Layer CRS" and call the resulting layer "Centroids_geom".
- Save the new layer as geopackage by right clicking the layer and selecting "make permanent". You can call it "Centroids_geom", for example.

Saving as CSV file
++++++++++++++++++

- Save the layer "Centroids_geom" as CSV file by right clicking on the layer and selecting "export > save features as". Select format "Comma Separated Value" [CSV] and the attributes "postcode4", "aantal inwoners" (number of inhabitants), "xcoord" and "ycoord". Select the box "add saved file to map".
