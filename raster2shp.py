#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
parameters:
    in_file: input raster file path --输入栅格影像
    out_file: output shapefile path --输出的shp图层

"""

import os
import arcpy
# 解决中文路径
import sys


def get_basename(filename):
    basename, ext = os.path.splitext(filename)
    return (basename,ext)

def main(in_file, out_file):

    temp_file = get_basename(in_file)[0] + '_2shp.shp'

    if arcpy.Exists(temp_file):
        arcpy.Delete_management(temp_file)

    field = "VALUE"
    # Execute RasterToPolygon
    arcpy.RasterToPolygon_conversion(in_file, temp_file, "NO_SIMPLIFY", field)

    if arcpy.Exists(out_file):
        arcpy.Delete_management(out_file)
    # 解决空格
    arcpy.Copy_management(temp_file, out_file)

if __name__=="__main__":

    main(sys.argv[1], sys.argv[2])
