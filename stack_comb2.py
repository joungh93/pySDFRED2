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


for i in np.arange(len(np.unique(band))):
    idx_band = (np.array(band) == np.unique(band)[i])
    for j in np.sum(idx_band):
        



os.chdir(current_dir)
