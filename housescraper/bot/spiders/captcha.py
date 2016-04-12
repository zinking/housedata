__author__ = 'awang'

import matplotlib.pyplot as plt
from skimage.data import data_dir
import matplotlib.pyplot as plt

from skimage.util import img_as_ubyte
from skimage import io
from skimage.filters import threshold_otsu
from skimage.viewer import ImageViewer
import os
import ctypes
import commands

import pdb


filename = "download.png"
workdir = "/tmp/captcha/"
processed_dir = "/tmp/captcha/cleaned/"
libname="/usr/local/Cellar/tesseract/3.02.02_3/lib/libtesseract.dylib"

def ocr_recognition_shell(filename):
    commands.getstatusoutput('tesseract %s out -l chi_sim -psm 7'%(filename))
    with  open("out.txt") as f:
        content = f.readlines()
        if len(content) == 0 :
            print 'recognize as',"[]"
            return ""
        else:
            content1 = content[0][:-1].replace(" ","")
            print 'recognize as[%s]'%(content1)
            return content1


def ocr_recognition(cleaned_captcha):
    lang = "chi_sim"
    #Please make sure the TESSDATA_PREFIX environment variable
    #is set to the parent directory of your "tessdata" directory.

    TESSDATA_PREFIX = "/usr/local/Cellar/tesseract/3.02.02_3/share/tessdata/"
    tesseract = ctypes.cdll.LoadLibrary(libname)
    tesseract.TessVersion.restype = ctypes.c_char_p
    api = tesseract.TessBaseAPICreate()
    rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
    if (rc):
        tesseract.TessBaseAPIDelete(api)
        print("Could not initialize tesseract.\n")
        exit(3)

    text_out = tesseract.TessBaseAPIProcessPages(api, cleaned_captcha, None, 0)
    result_text = ctypes.string_at(text_out)
    print 'recognized as:',result_text


def run_decaptcha(captcha_filename):
    captcha_file = img_as_ubyte(io.imread(workdir+captcha_filename))
    p1 = transform_captcha(captcha_file,200)
    cleaned_filename = processed_dir+captcha_filename+".bmp"
    io.imsave(cleaned_filename,p1)
    text = ocr_recognition_shell(cleaned_filename)
    v3 = ImageViewer(p1)
    v3.show()
    return text

def transform_captcha(captcha,thresh):
    p1 = captcha.copy()
    def is_scale(px):
        scale_thresh = 5
        return abs(px[0]-px[1])<scale_thresh \
               and abs(px[0]-px[2])<scale_thresh \
               and abs(px[1]-px[2])<scale_thresh
    def is_grey(px,thresh):
        return is_scale(px) and px[0]>255-thresh and px[1]>255-thresh and px[2]>255-thresh
    def is_black(px,thresh):
        return is_scale(px) and px[0]<thresh and px[1]<thresh and px[2]<thresh
    for i in range(0,p1.shape[0]):
         for j in range(0,p1.shape[1]):
              px = p1[i][j]
              if is_grey(px,thresh) or is_black(px,thresh):
                   p1[i][j] = px
              else:
                   p1[i][j] = [255,255,255]

    return p1



if __name__ == '__main__':
    run_decaptcha(filename)


