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
    date = name_list[3]
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = (date[8:10])
    minute = '00'


    # print year, month, day, hour, minute

    return year, month, day, hour, minute


def main(in_mxd, in_file, out_png):

    date_list = get_file_date(in_file)

    pm_type = os.path.splitext(os.path.basename(in_mxd))[0].split('_')[0]

    if pm_type == 'PM25':
        input_type = 'PM2.5'
    else:
        input_type = pm_type

    # 解决中文路径
    # in_mxd = unicode(in_mxd,'utf-8')
    # in_file_dir = unicode(os.path.dirname(in_file),'utf-8')
    # in_file_name = unicode(os.path.basename(in_file),'utf-8')

    in_file_dir = os.path.dirname(in_file)
    in_file_name = os.path.basename(in_file)

    mxd = arcpy.mapping.MapDocument(in_mxd)
    # 修复数据源
    for lyr in arcpy.mapping.ListLayers(mxd):
        # print lyr.name
        if 'HAZ' in lyr.name:
            # print lyr.name
            lyr.replaceDataSource(in_file_dir, "RASTER_WORKSPACE",
                                  in_file_name)

    # # 更改TEXT_ELEMENT
    # input_type = 'PM10'
    for text_element in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):

        text_element.text = text_element.text.replace("{type}", input_type)
        text_element.text = text_element.text.replace("{yyyy}", date_list[0])
        text_element.text = text_element.text.replace("{mm}", date_list[1])
        text_element.text = text_element.text.replace("{dd}", date_list[2])
        text_element.text = text_element.text.replace("{hh}", date_list[3])
        text_element.text = text_element.text.replace("{mt}", date_list[4])


    # mxd.save()
    # out_mxd = os.path.join(os.path.dirname(in_mxd), '%s_.mxd' %
    #                        (os.path.splitext(os.path.basename(in_mxd))[0]))
    # mxd.saveACopy(out_mxd)
    # 输出PNG
    arcpy.mapping.ExportToPNG(mxd, out_png)
    # arcpy.mapping.ExportToPNG(mxd, unicode(out_png,'utf-8'))
    del mxd


if __name__ == '__main__':


    if len(sys.argv[1:]) < 3:
        sys.exit('Problem reading input')

    in_mxd = sys.argv[1]
    in_file = sys.argv[2]
    out_png = sys.argv[3]


    # in_mxd = r"D:\实施项目\石家庄大气环境监测\材料\sjz_polution\PM10_DAILY_Report.mxd"
    # in_file = r"D:\实施项目\石家庄大气环境监测\数据\PM10_tif\HAZ_PM10_RJ1D_201710040000_COOD_HIM8AHI_130100.tif"
    # out_png = r"D:\实施项目\石家庄大气环境监测\材料\sjz_polution\PM10_DAILY_Report_png.png"

    main(in_mxd, in_file, out_png)