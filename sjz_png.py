# -*- coding:utf-8 -*-
# author:zyn
"""石家庄污染物专题制图"""
import sys
import os
import arcpy


class SjzPolution:
    """石家庄PM2.5 PM10分布 专题制图

    输入参数argv:
        time: '201709060300'
        raster_path: = u'E:/work/shijiazhuang/TEST/INPUT2/'
        png_path = u'E:/work/shijiazhuang/TEST/OUTPUT/'"""

    def __init__(self, argv):
        # def __init__(self):
        """参数初始化

                    参数表征：
            self.time: '201709060300'
            self.raster_path: = u'E:/work/shijiazhuang/TEST/INPUT2/'
            self.png_path = u'E:/work/shijiazhuang/TEST/OUTPUT/'
            self.year: 年
            self.month: 月
            self.day: 日
            self.hour: 小时
            self.minute: 分钟
            self.product_type: 产品类型
            self.raster_branch_dir: 栅格 dir
            self.png_branch_dir: PNG dir
            self.input_mxd_dir: mxd dir"""

        if len(argv) <= 4:
            sys.exit()
        else:
            # 服务器测试
            # self.time = "2017092820171104"
            # self.raster_path = u"E:/DATA/download_data/H8_processedData/l2/"
            # self.png_path = u"E:/DATA/product_data/"
            # self.cycle = u"COSD"
            self.time = sys.argv[1]
            self.raster_path = sys.argv[2]
            self.png_path = sys.argv[3]
            self.cycle = sys.argv[4]
            self.year = ""
            self.month = ""
            self.day = ""
            self.hour = ""
            self.minute = ""
            self.year02 = ""
            self.month02 = ""
            self.day02 = self.time[12:14]
            self.product_type_list = []
            self.raster_branch_dir = ""
            self.png_branch_path = ""
            self.png_branch_dir = ""
            self.input_mxd_path = ""

    def get_mxd_path(self):
        # 当前文件的路径
        # pwd = os.getcwd()
        pwd = os.path.dirname(sys.argv[0])
        # 当前文件的父路径
        father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + ".")
        # 当前文件的前两级目录
        grader_father = os.path.abspath(os.path.dirname(father_path) + os.path.sep + "..")

        self.input_mxd_path = (grader_father + os.path.sep + "data" +
                               os.path.sep + "mxd" + os.path.sep +
                               "model_mxd" + os.path.sep)
        print self.input_mxd_path

    def get_time(self):
        """获取年月日时分"""

        if len(self.time) == 12:
            self.year = self.time[:4]
            self.month = self.time[4:6]
            self.day = self.time[6:8]
            self.hour = str(int(self.time[8:10]) + 8)
            self.minute = self.time[10:12]
        else:
            self.year = self.time[:4]
            self.month = self.time[4:6]
            self.day = self.time[6:8]
            self.year02 = self.time[8:12]
            self.month02 = self.time[12:14]
            self.day02 = self.time[14:16]

    def generate_mxd_list(self, input_type="PM10"):
        """生成mxd list"""

        if not os.path.exists(self.input_mxd_path):
            sys.exit()
        input_mxd_dir = []
        for mxd_name in os.listdir(self.input_mxd_path):
            if input_type in mxd_name:
                mxd_branch_dir = os.path.join(self.input_mxd_path, mxd_name)
                if os.path.splitext(mxd_branch_dir)[1] == ".mxd":
                    input_mxd_dir.append(mxd_branch_dir)

        if len(input_mxd_dir) < 1:
            print input_type + "has no mxd files"

        return input_mxd_dir

    def get_branch_product_type(self):
        """获取栅格路径下所有的产品类别"""

        if self.cycle == "COTM":
            self.product_type_list = ["PM10_DAILY", "PM25_DAILY"]
        elif self.cycle == "COOD":
            self.product_type_list = ["PM10_Interp", "PM25_Interp"]
        elif self.cycle == "COSD":
            self.product_type_list = ["PM10_WEEK_Avg", "PM25_WEEK_Avg"]

    def get_raster_dir(self, input_type="PM10"):
        """获取raster dir

        raster_branch_path: 'E:/work/shijiazhuang/TEST/INPUT2/' +
            'PM25/tif/20170906"""
        self.raster_branch_dir = ""
        if len(self.time) == 12:
            raster_branch_path = (os.path.join(self.raster_path, input_type) +
                                  "/tif/" + self.year + self.month +
                                  self.day + "/")
        else:
            raster_branch_path = (os.path.join(self.raster_path, input_type) +
                                  "/tif/" + self.time + "/")

        if not os.path.isdir(raster_branch_path):
            self.raster_branch_dir = ""
            return

        for raster_name in os.listdir(raster_branch_path):
            if self.time in raster_name:
                self.raster_branch_dir = os.path.join(
                    raster_branch_path, raster_name)
        if self.raster_branch_dir == "":
            self.raster_branch_dir = ""
            return

    def get_png_path(self, input_type="PM10"):
        """获取png dir

        png_branch_path: 'E:/work/shijiazhuang/TEST/INPUT2/' +
            'PM25/png/20170906"""

        if len(self.time) == 12:
            self.png_branch_path = (os.path.join(self.png_path, input_type) +
                                    "/png/" + self.year + self.month +
                                    self.day + "/")
        else:
            self.png_branch_path = (os.path.join(self.png_path, input_type) +
                                    "/png/" + self.time + "/")

        if not os.path.exists(self.png_branch_path):
            os.mkdir(self.png_branch_path)

    def auto_mapping(self, input_mxd="", input_type="", out_png=""):
        """自动制图

            实现的功能主要包括：修复数据源、修改文本元素、输出PNG图片"""

        if "PM25" in input_type:
            input_type = "PM2.5"
        else:
            input_type = "PM10"

        input_workspace = os.path.dirname(self.raster_branch_dir)
        input_datasetname = os.path.basename(self.raster_branch_dir)

        mxd = arcpy.mapping.MapDocument(input_mxd)

        # 修复数据源
        brokenlist = arcpy.mapping.ListBrokenDataSources(mxd)
        for brokenlyr in brokenlist:
            if brokenlyr.supports("DATASOURCE"):
                brokenlyr.replaceDataSource(input_workspace, "RASTER_WORKSPACE",
                                            input_datasetname)

        # 更改TEXT_ELEMENT
        for text_element in arcpy.mapping.ListLayoutElements(mxd,
                                                             "TEXT_ELEMENT"):
            if "WEEK_Avg" in text_element.name:
                txt = text_element.text
                txt = txt.replace("{type}", input_type)
                txt = txt.replace("{yyyy1}", self.year)
                txt = txt.replace("{mm1}", self.month)
                txt = txt.replace("{dd1}", self.day)
                txt = txt.replace("{yyyy2}", self.year02)
                txt = txt.replace("{mm2}", self.month02)
                txt = txt.replace("{dd2}", self.day02)
                text_element.text = txt
            elif "_title" in text_element.name:
                txt = text_element.text
                txt = txt.replace("{type}", input_type)
                txt = txt.replace("{yyyy}", self.year)
                txt = txt.replace("{mm}", self.month)
                txt = txt.replace("{dd}", self.day)
                txt = txt.replace("{hh}", self.hour)
                txt = txt.replace("{mt}", self.minute)
                text_element.text = txt

        # 输出PNG
        arcpy.mapping.ExportToPNG(mxd, out_png)

        del mxd


def main():
    # 初始化
    sjz_polution = SjzPolution(sys.argv)
    # sjz_polution = SjzPolution()

    # 获取产品时间
    sjz_polution.get_time()
    # 获取产品周期
    sjz_cycle = sjz_polution.cycle
    # 获取产品类别名称列表
    sjz_polution.get_branch_product_type()
    # 获取mxd路径
    sjz_polution.get_mxd_path()
    # 世界时间更改为北京时间
    sjz_time = sjz_polution.time
    if len(sjz_time) == 12:
        sjz_time_hour = int(sjz_time[8:10]) + 8
        if sjz_time_hour < 10:
            sjz_time = (sjz_time[0:8] + "0" +
                        str(int(sjz_time[8:10]) + 8) + sjz_time[10:])
        else:
            sjz_time = sjz_time[0:8] + str(int(sjz_time[8:10]) + 8) + sjz_time[10:]
    # 获取产品类别
    branch_product_type_list = sjz_polution.product_type_list

    for branch_product_type in branch_product_type_list:
        # 获取栅格dir
        sjz_polution.get_raster_dir(input_type=branch_product_type)
        if sjz_polution.raster_branch_dir == "":
            continue
        # png path
        sjz_polution.get_png_path(input_type=branch_product_type)
        #
        sjz_png_path = sjz_polution.png_branch_path

        # 遍历mxd dir
        mxd_dirs = sjz_polution.generate_mxd_list(
            input_type=branch_product_type)
        for mxd_dir in mxd_dirs:
            if "APP" in mxd_dir:
                # 设置PNG文件名
                # HAZ_PM10_RCUR_201710130200_COOH_HIM8AHI_130100.tif

                png_branch_dir = (sjz_png_path + "/" + "HAZ_" +
                                  branch_product_type + "_ZCUR_" + sjz_time +
                                  "_" + sjz_cycle + "_HIM8AHI_130100" + "_APP.png")
                print png_branch_dir
            elif "Report" in mxd_dir:
                # 设置PNG文件名
                png_branch_dir = (sjz_png_path + "/" + "HAZ_" +
                                  branch_product_type + "_ZCUR_" + sjz_time +
                                  "_" + sjz_cycle + "_HIM8AHI_130100" + "_Report.png")
            else:
                png_branch_dir = (sjz_png_path + "/" + "HAZ_" +
                                  branch_product_type + "_ZCUR_" + sjz_time +
                                  "_" + sjz_cycle + "_HIM8AHI_130100" + ".png")

            # 制图
            sjz_polution.auto_mapping(input_mxd=mxd_dir,
                                      input_type=branch_product_type,
                                      out_png=png_branch_dir)


if __name__ == '__main__':
    sys.exit(main())
