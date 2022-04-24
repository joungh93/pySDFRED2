#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 05 15:16:23 2021
@author: jlee
"""


import numpy as np
import glob, os
from astropy.io import fits
from pathlib import Path
import re


# ----- Basic setting ----- #
current_dir = os.getcwd()
phot0_dir = current_dir+"/Phot/Initial/"
dir_Obj = str(Path("./Object").absolute())
if (glob.glob(phot0_dir) == []):
    os.system("mkdir "+phot0_dir)
os.chdir(phot0_dir)

imglist = sorted(glob.glob(dir_Obj+"/*/*/comb.fits"))
n_img = len(imglist)
band = [s.split("/")[-3] for s in imglist]


# ----- Writing .param file ----- #
par_file = "default.param"
with open(par_file, "w") as f:
    # SExtractor for SCAMP
    f.write("XWIN_IMAGE\nYWIN_IMAGE\n")
    f.write("ERRAWIN_IMAGE\nERRBWIN_IMAGE\nERRTHETAWIN_IMAGE\n")
    f.write("FLUX_AUTO\nFLUXERR_AUTO\n")
    f.write("FLAGS\nFLAGS_WEIGHT\n")
    f.write("FLUX_RADIUS\nELONGATION\n")


# # ----- Writing the SExtractor configuration file ----- #
# os.system("rm -rfv *.sex *.cat")
# cfg_file = "config.sex"
# os.system("sex -dd > "+cfg_file)

# sh_file = "sephot.sh"
# with open(sh_file, "w") as f:
#     # SExtractor scripts
#     for i in np.arange(n_img):
#         str_run = "sex "+imglist[i]+" -c config.sex "
#         str_param = "-DETECT_MINAREA 5 -DETECT_THRESH 3.0 -ANALYSIS_THRESH 3.0 "
#         str_param += "-DEBLEND_NTHRESH 32 -DEBLEND_MINCONT 0.005 "
#         str_param += "-FILTER_NAME /usr/share/sextractor/default.conv "
#         str_param += "-SATUR_LEVEL 10000.0 -MAG_ZEROPOINT 25.0 "
#         str_param += "-PIXEL_SCALE 0.202 -SEEING_FWHM 1.0 "
#         str_param += "-STARNNW_NAME /usr/share/sextractor/default.nnw "
#         str_param += "-BACK_SIZE 64 -BACK_FILTERSIZE 3 -BACKPHOTO_TYPE LOCAL"

#         if (i == 0):
#             set_num = 1
#         else:
#             if (band[i] == band[i-1]):
#                 set_num += 1
#             else:
#                 set_num = 1

#         # FITS_LDAC
#         f.write(str_run)
#         f.write("-CATALOG_NAME "+band[i]+f"_set{set_num:02d}.cat ")
#         f.write("-CATALOG_TYPE FITS_LDAC ")
#         f.write(str_param)
#         f.write("\n")

#         # ASCII_HEAD
#         f.write(str_run)
#         f.write("-CATALOG_NAME "+band[i]+f"_set{set_num:02d}_ascii.cat ")
#         f.write("-CATALOG_TYPE ASCII_HEAD ")
#         f.write(str_param)
#         f.write("\n\n")

# os.system("sh "+sh_file)


# ----- Writing the SCAMP configuration file ----- #
catlist = sorted(glob.glob("*.cat"))
catlist_scamp = list(filter(re.compile(".+[_set0][0-9][.].+$").match, catlist))
n_cat = len(catlist_scamp)

# os.system("rm -rfv *.scamp *.head")
# cfg_file = "config.scamp"
# os.system("scamp -dd > "+cfg_file)

# sh_file = "scamp.sh"
# with open(sh_file, "w") as f:
#     # SCAMP scripts
#     for i in np.arange(n_cat):
#         f.write("scamp -c config.scamp ")
#         f.write(catlist_scamp[i]+" ")
#         f.write("-REF_SERVER vizier.unistra.fr ")
#         f.write("-ASTREF_CATALOG GAIA-EDR3 -MAGZERO_OUT 25.0 ")
#         f.write("-FWHM_THRESHOLDS 2.0,7.0 ")
#         f.write("\n")

# os.system("sh "+sh_file)


# # ----- Writing the SWARP configuration file ----- #
# name_scamp0 = []
# for i in np.arange(n_img):
#     imgname = catlist_scamp[i].split(".")[0]+".fits"
#     os.system("cp -rpv "+imglist[i]+" "+imgname)
#     name_scamp0.append(catlist_scamp[i].split(".")[0])

# os.system("rm -rfv *.swarp")
# cfg_file = "config.swarp"
# os.system("swarp -dd > "+cfg_file)

# sh_file = "swarp.sh"
# with open(sh_file, "w") as f:
#     # SWARP scripts
#     for i in np.arange(n_cat):
#         f.write("swarp "+imglist[i]+" -c config.swarp ")
#         f.write("-IMAGEOUT_NAME "+name_scamp0[i]+".fits ")
#         f.write("-WEIGHTOUT_NAME "+name_scamp0[i]+".weight.fits ")
#         f.write("-PIXELSCALE_TYPE MANUAL -PIXEL_SCALE 0.202 ")
#         f.write("-SATLEV_DEFAULT 10000. -SUBTRACT_BACK N")
#         f.write("\n")

# os.system("sh "+sh_file)


os.chdir(current_dir)
