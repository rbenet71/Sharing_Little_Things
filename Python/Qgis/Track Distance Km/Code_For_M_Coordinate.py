file_name='04_001_Op_52.gpx'
uri = file_name+"|layername=track_points"
# Load Layer with points of track gpx 
points = QgsVectorLayer(uri, "Original Points", "ogr")

# For Calculating distance points
d = QgsDistanceArea()
d.setEllipsoid('WGS84')

point_origin=0

# For each point in the track, analize information

for point in points.getFeatures():
	# Get Geometry of feature like a point
	geompt = point.geometry().asPoint()
	
	# Calculate lenght of track
	if not point_origin==0:
		distance=d.measureLine(point_origin, geompt)
		coor_m+=(self.distance/1000) # Distance in km
		point_origin=geompt
	else:
		coor_m=0
		distance=0
		point_origin=geompt
		
	# After that I save information in a new layer, in a Geometry LinestringZM.
    # The complete code you can see in: 
	# https://github.com/rbenet71/Sharing_Little_Things/blob/master/Python/Qgis/GPX%203D/GPX_to_3D.py
	 
	 