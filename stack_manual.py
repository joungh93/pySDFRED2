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
from astropy.stats import sigma_clipped_stats


# ----- Basic setting ----- #
os.system("rm -rfv AspgfTo*weight*.fits")
imglist = sorted(glob.glob("AspgfTo*.fits"))
n_img = len(imglist)


# ----- Writing .param file ----- #
par_file = "default.param"
with open(par_file, "w") as f:
    # SExtractor for SCAMP
    f.write("XWIN_IMAGE\nYWIN_IMAGE\n")
    f.write("ERRAWIN_IMAGE\nERRBWIN_IMAGE\nERRTHETAWIN_IMAGE\n")
    f.write("FLUX_AUTO\nFLUXERR_AUTO\n")
    f.write("FLAGS\nFLAGS_WEIGHT\n")
    f.write("FLUX_RADIUS\nELONGATION\n")


# ----- Writing the SExtractor configuration file ----- #
os.system("rm -rfv config.sex AspgfTo*.cat")
cfg_file = "config.sex"
os.system("sex -dd > "+cfg_file)

sh_file = "sephot.sh"
with open(sh_file, "w") as f:
    
    # SExtractor scripts
    for i in np.arange(n_img):
        str_run = "sex "+imglist[i]+" -c config.sex "
        str_param = "-DETECT_MINAREA 5 -DETECT_THRESH 4.0 -ANALYSIS_THRESH 4.0 "
        str_param += "-DEBLEND_NTHRESH 32 -DEBLEND_MINCONT 0.005 "
        str_param += "-FILTER_NAME /usr/share/sextractor/default.conv "
        str_param += "-SATUR_LEVEL 10000.0 -MAG_ZEROPOINT 25.0 "
        str_param += "-PIXEL_SCALE 0.202 -SEEING_FWHM 1.0 "
        str_param += "-STARNNW_NAME /usr/share/sextractor/default.nnw "
        str_param += "-BACK_SIZE 64 -BACK_FILTERSIZE 3 -BACKPHOTO_TYPE LOCAL"

        # FITS_LDAC
        f.write(str_run)
        f.write("-CATALOG_NAME "+imglist[i].split(".fits")[0]+".cat ")
        f.write("-CATALOG_TYPE FITS_LDAC ")
        f.write(str_param)
        f.write("\n")

        # # ASCII_HEAD
        # f.write(str_run)
        # f.write("-CATALOG_NAME "+band[i]+f"_set{set_num:02d}_ascii.cat ")
        # f.write("-CATALOG_TYPE ASCII_HEAD ")
        # f.write(str_param)
        # f.write("\n\n")

os.system("sh "+sh_file)


# ----- Writing the SCAMP configuration file ----- #
catlist = sorted(glob.glob("AspgfTo*.cat"))
n_cat = len(catlist)

os.system("rm -rfv config.scamp AspgfTo*.head")
cfg_file = "config.scamp"
os.system("scamp -dd > "+cfg_file)

sh_file = "scamp.sh"
with open(sh_file, "w") as f:

    # SCAMP scripts
    for i in np.arange(n_cat):
        f.write("scamp -c config.scamp ")
        f.write(catlist[i]+" ")
        f.write("-REF_SERVER vizier.unistra.fr ")
        f.write("-ASTREF_CATALOG GAIA-EDR3 -MAGZERO_OUT 25.0 ")
        f.write("-SOLVE_ASTROM Y -SOLVE_PHOTOM N ")
        f.write("-FWHM_THRESHOLDS 2.0,7.0 ")
        f.write("\n")

os.system("sh "+sh_file)


# ----- Making weight images ----- #
for i in np.arange(n_img):
    dat, hdr = fits.getdata(imglist[i], header=True)
    exptime = hdr['EXPTIME']
    wei = np.ones_like(dat) * exptime

    avg, med, std = sigma_clipped_stats(dat[dat > -3.2e+4], sigma=2.5, maxiters=5)
    msk = (dat < -3.2e+4)# | (dat > 1.0e+4))
    wei[msk] = 0.0

    print("Writing "+imglist[i].split(".fits")[0]+".weight.fits...")
    fits.writeto(imglist[i].split(".fits")[0]+".weight.fits", wei, hdr, overwrite=True)


# ----- Writing the SWARP configuration file ----- #
os.system("rm -rfv config.swarp comb.fits comb.weight.fits img_swarp.list")
cfg_file = "config.swarp"
os.system("swarp -dd > "+cfg_file)
os.system("ls -1 "+" ".join(imglist)+" > img_swarp.list")

sh_file = "swarp.sh"
with open(sh_file, "w") as f:
    # SWARP scripts
    f.write("swarp @img_swarp.list -c config.swarp ")
    f.write("-IMAGEOUT_NAME comb.fits ")
    f.write("-WEIGHTOUT_NAME comb.weight.fits ")
    f.write("-WEIGHT_TYPE MAP_WEIGHT -BLANK_BADPIXELS Y ")#MAP_WEIGHT ")
    f.write("-PIXELSCALE_TYPE MANUAL -PIXEL_SCALE 0.202 ")
    f.write("-CENTER_TYPE MANUAL -CENTER 20:34:52.32,+60:09:14.1 -IMAGE_SIZE 9000,9000 ")
    f.write("-SATLEV_DEFAULT 10000. ")
    f.write("-SUBTRACT_BACK N -BACK_SIZE 256 ")
    f.write("\n")

os.system("sh "+sh_file)


