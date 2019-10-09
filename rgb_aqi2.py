#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
    针对自动制图
    实现的功能主要包括：修复数据源、修改文本元素、输出PNG图片

"""

import sys
import os
import arcpy

def get_file_date(in_file):

    base_name = os.path.splitext(os.path.basename(in_file))[0]

    name_list = base_name.split('_')

    if len(name_list) > 1:
        date = name_list[1]
    else:
        date = name_list[0]
    # date = name_list[1]
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = str(int(date[8:10]) + 8)
    minute = date[10:12]


    # print year, month, day, hour, minute

    return year, month, day, hour, minute


def main(in_mxd, in_shp, in_raster, out_png):

    date_list = get_file_date(in_raster)

    # 解决中文路径
    # in_mxd = unicode(in_mxd,'utf-8')
    # in_file_dir = unicode(os.path.dirname(in_file),'utf-8')
    # in_file_name = unicode(os.path.basename(in_file),'utf-8')

    if in_shp != 0:

        in_shp_dir = os.path.dirname(in_shp)
        in_shp_name = os.path.splitext(os.path.basename(in_shp))[0]
    else:
        in_shp_dir = 0
        in_shp_name = 0

    in_raster_dir = os.path.dirname(in_raster)
    in_raster_name = os.path.basename(in_raster)

    mxd = arcpy.mapping.MapDocument(in_mxd)
    # 修复数据源
    for lyr in arcpy.mapping.ListLayers(mxd):

        if lyr.supports("DATASOURCE"):

            if in_shp != 0:

                # print lyr.name
                if 'HAZ' in lyr.name:
                # print lyr.name
                    lyr.replaceDataSource(in_shp_dir, "SHAPEFILE_WORKSPACE",
                                         in_shp_name)
            if 'vis' in lyr.name:
                # print lyr.name
                lyr.replaceDataSource(in_raster_dir, "RASTER_WORKSPACE",
                                      in_raster_name)
    # mxd.save()
    # out_mxd = os.path.join(os.path.dirname(in_mxd), '%s_.mxd' %
    #                        (os.path.splitext(os.path.basename(in_mxd))[0]))
    # mxd.saveACopy(out_mxd)
    # 输出PNG

    for text_element in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):

        text_element.text = text_element.text.replace("{yyyy}", date_list[0])
        text_element.text = text_element.text.replace("{mm}", date_list[1])
        text_element.text = text_element.text.replace("{dd}", date_list[2])
        text_element.text = text_element.text.replace("{hh}", date_list[3])
        text_element.text = text_element.text.replace("{mt}", date_list[4])
    # arcpy.mapping.ExportToPNG(mxd, unicode(out_png,'utf-8'))
    arcpy.mapping.ExportToPNG(mxd, out_png)
    del mxd


if __name__ == '__main__':


    if len(sys.argv[1:]) < 3:
        sys.exit('Problem reading input')

    if len(sys.argv[1:]) == 4:

        in_mxd = sys.argv[1]
        in_shp = sys.argv[2]
        in_raster = sys.argv[3]
        out_png = sys.argv[4]
    else:
        in_mxd = sys.argv[1]
        in_shp = 0
        in_raster = sys.argv[2]
        out_png = sys.argv[3]


    # in_mxd = r"D:\实施项目\石家庄大气环境监测\材料\sjz_polution\PM10_DAILY_Report.mxd"
    # in_file = r"D:\实施项目\石家庄大气环境监测\数据\PM10_tif\HAZ_PM10_RJ1D_201710040000_COOD_HIM8AHI_130100.tif"
    # out_png = r"D:\实施项目\石家庄大气环境监测\材料\sjz_polution\PM10_DAILY_Report_png.png"

    main(in_mxd, in_shp, in_raster, out_png)