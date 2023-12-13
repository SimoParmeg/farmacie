import sys
import os
from osgeo import ogr
import pandas as pd
# from simpledbf import Dbf5
import geopandas as gpd

def get_cities(fn):
    # EXCEL TO PANDAS
    # excel_file = "/home/simone/GIS3W/input/Com01012023_WGS84.dbf" -> converti in xls
    # df = pd.ExcelFile(excel_file)

    # WITH DBF5 TO DATAFRAME
    # dbf = Dbf5('/home/simone/GIS3W/input/Com01012023_WGS84.dbf')
    # df = dbf.to_dataframe()

    # WITH GEOPANDAS
    df = gpd.read_file(fn, encoding='utf-8')
    return df["COMUNE"].unique()


def extract_feature(fn, filter_field, value_to_filter, out_shp):
    ds = ogr.Open(fn, 1)

    if ds is None:
        sys.exit("File non trovato")

    in_lyr = ds.GetLayer(0)

    driver = ogr.GetDriverByName("ESRI shapefile")
    out_ds = driver.CreateDataSource(out_shp)

    if ds.GetLayer(out_shp):
        ds.DeleteLayer(out_shp)

    out_lyr = out_ds.CreateLayer(outfile, 
                            in_lyr.GetSpatialRef(), 
                            ogr.wkbPolygon)

    out_lyr.CreateFields(in_lyr.schema)

    out_defn = out_lyr.GetLayerDefn()
    out_feat = ogr.Feature(out_defn)

    for feat in in_lyr:
        if feat.GetField(filter_field) == value_to_filter:
            poly = feat.geometry()
            out_feat.SetGeometry(poly)
            for i in range(feat.GetFieldCount()):
                value = feat.GetField(i)
                out_feat.SetField(i, value)

            out_lyr.CreateFeature(out_feat)
        
    del ds

def reproject_vector(in_shp, crs_to_project):
    gdf = gpd.read_file(in_shp)
    gdf_reproj = gdf.to_crs({'init': crs_to_project})
    return gdf_reproj


def clip_by_extent(in_fn, out_fn):
    pass

if __name__ == "__main__":


    infile = "/home/simone/GIS3W/farmacie/istat/confini_amministrativi_2023/Limiti01012023/Com01012023/Com01012023_WGS84.shp"
    
    cities = get_cities("/home/simone/GIS3W/farmacie/input/Com01012023_WGS84.dbf")

    output_dir = "/home/simone/GIS3W/farmacie/output"
    # print(cities)

    for c in cities:
        outfile = f"output/{c}"
        extract_feature(infile, "COMUNE" , c, outfile)

        farmacie_dir = os.path.join(outfile, "farmacie")
        if not os. path. isdir(os.path.join(farmacie_dir)):
            os.mkdir(os.path.join(farmacie_dir))

        voronoi_dir = os.path.join(outfile, "voronoi")
        if not os. path. isdir(os.path.join(voronoi_dir)):
            os.mkdir(os.path.join(voronoi_dir))

        buffer_dir = os.path.join(outfile, "buffer")
        if not os. path. isdir(os.path.join(buffer_dir)):
            os.mkdir(os.path.join(buffer_dir))

        isochrones_dir = os.path.join(outfile, "isocrone")
        if not os. path. isdir(os.path.join(isochrones_dir)):
            os.mkdir(os.path.join(isochrones_dir))

        osm_dir = os.path.join(outfile, "osm")
        if not os. path. isdir(os.path.join(osm_dir)):
            os.mkdir(os.path.join(osm_dir))



    # create_filtered_shapefile(infile,"COMUNE" ,"Milano", outfile)

    # UNCOMMENT FOR TEST PURPOSES
    # outfile = "output/Milano"
    # c = "Milano"
    # extract_feature(infile, "COMUNE" , c, outfile)
        

    # reproject_vector()

