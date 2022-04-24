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
phot0_dir = current_dir+"/Phot/Initial/"
dir_Obj = str(Path("./Object").absolute())

imglist = sorted(glob.glob(dir_Obj+"/*/*/comb.fits"))
n_img = len(imglist)
band = [s.split("/")[-3] for s in imglist]
headlist = sorted(glob.glob(phot0_dir+"*.head"))


# ----- Reading the headers ----- #
for i in np.arange(n_img):
    dat, hdr = fits.getdata(imglist[i], header=True)
    dh = pd.read_csv(headlist[i], skiprows=3, skipfooter=1,
                     header=None, delimiter=r'[=/]', engine='python',
                     usecols=(0,1), names=('key','value'))
    n_key = len(dh)
    dh_key = dh['key'].str.strip()

    for j in np.arange(n_key):
        try:
            val = float(dh['value'][j])
        except ValueError:
            if (dh['value'][j].strip() == 'T'):
                val = True
            elif (dh['value'][j].strip() == 'F'):
                val = False
            else:
                val = dh['value'][j].replace("'", "").strip()
        hdr[dh_key[j]] = val

    dir_img = imglist[i].split("comb.fits")[0]
    fits.writeto(dir_img+"comb2.fits", dat, hdr, overwrite=True)
