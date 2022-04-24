#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 06 18:24:25 2021
@author: jlee
"""


import numpy as np
import glob, os
import pandas as pd
from astropy.io import fits
from pathlib import Path


# ----- Basic setting ----- #
current_dir = os.getcwd()

dir_Img = current_dir+"/Phot/Images/"
if (glob.glob(dir_Img) == []):
    os.system("mkdir "+dir_Img)
else:
    os.system("rm -rfv "+dir_Img+"*.fits")

dir_Obj = str(Path("./Object").absolute())
imglist = sorted(glob.glob(dir_Obj+"/*/*/comb2.fits"))
n_img = len(imglist)
band = [s.split("/")[-3] for s in imglist]
os.chdir(dir_Img)


# ----- Writing .param file ----- #
par_file = "output.param"
with open(par_file, "w") as f:
    # SExtractor output parameters
    f.write("X_IMAGE\nY_IMAGE\nNUMBER\n")
    f.write("MAG_AUTO\nMAGERR_AUTO\nMAG_APER(2)\nMAGERR_APER(2)\n")
    f.write("KRON_RADIUS\nPETRO_RADIUS\nBACKGROUND\n")
    f.write("ALPHA_J2000\nDELTA_J2000\nCXX_IMAGE\nCYY_IMAGE\nCXY_IMAGE\n")
    f.write("A_IMAGE\nB_IMAGE\nTHETA_IMAGE\nMU_MAX\nMU_THRESHOLD\n")
    f.write("FLAGS\nFWHM_IMAGE\nFLUX_RADIUS\nCLASS_STAR")


# ----- Initial SExtractor photometry ----- #
os.system("rm -rfv *.sex *.cat")
cfg_file = "config.sex"
os.system("sex -dd > "+cfg_file)

sh_file = "sephot.sh"
with open(sh_file, "w") as f:
    # SExtractor scripts
    for i in np.arange(n_img):
        str_run = "sex "+imglist[i]+" -c config.sex "
        str_param = "-DETECT_MINAREA 5 -DETECT_THRESH 3.0 -ANALYSIS_THRESH 3.0 "
        str_param += "-DEBLEND_NTHRESH 32 -DEBLEND_MINCONT 0.005 "
        str_param += "-FILTER_NAME /usr/share/sextractor/default.conv "
        str_param += "-PHOT_APERTURES 5,10 "
        str_param += "-SATUR_LEVEL 10000.0 -MAG_ZEROPOINT 25.0 "
        str_param += "-PIXEL_SCALE 0.202 -SEEING_FWHM 1.0 "
        str_param += "-STARNNW_NAME /usr/share/sextractor/default.nnw "
        str_param += "-BACK_SIZE 64 -BACK_FILTERSIZE 3 -BACKPHOTO_TYPE LOCAL"

        if (i == 0):
            set_num = 1
        else:
            if (band[i] == band[i-1]):
                set_num += 1
            else:
                set_num = 1

        f.write(str_run)
        f.write("-CATALOG_NAME "+band[i]+f"_set{set_num:02d}.cat ")
        f.write("-CATALOG_TYPE ASCII_HEAD ")
        f.write("-PARAMETERS_NAME output.param ")
        f.write(str_param)
        f.write("\n\n")

os.system("sh "+sh_file)



os.chdir(current_dir)

