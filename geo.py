from os.path import dirname, join
import geopandas as gpd

from sqlalchemy import create_engine

from geopandas_postgis import PostGIS

engine = create_engine("postgresql://localhost/crewasis")
my_gdf = gpd.GeoDataFrame.from_file(join(dirname(__file__), 'app/main/data/states', 'gz_2010_us_040_00_20m.shp'))
print (my_gdf.head())
my_gdf.postgis.to_postgis(con=engine, table_name='geodata', geometry='GEOMETRY')
