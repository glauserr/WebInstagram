#!/usr/bin/env python

import os
import datetime


def border(input_file, output_file, color, size):
    cmd = "convert {} -bordercolor {} -border {} {}"\
        .format(input_file, color, size, output_file)
    os.system(cmd)


def lomo(input_file, output_file):
    cmd = "convert {} -channel R -level 33\% -channel G -level 33\% {}"\
        .format(input_file, output_file)
    os.system(cmd)


def lens_flare(input_file, output_file, width, hight):
    lens_flare_file = "util/lens_flare.png"
    tmp_file = "tmp/tmp_fil" + datetime.datetime.now().strftime("%S_%f")
    cmd = "convert {} -resize {}x{}\! {}".format(lens_flare_file, width, hight, tmp_file)

    os.system(cmd)

    cmd = "composite -compose screen -gravity northwest {} {} {}"\
        .format(tmp_file, input_file, output_file)

    os.system(cmd)

    os.system("rm " + tmp_file)


def black_white(input_file, output_file, width, hight):
    bwgrad_file = "util/bwgrad.png"
    tmp_file1 = "tmp/tmp_fil" + datetime.datetime.now().strftime("%S_%f") 
    tmp_file2 = "tmp/tmp_fil_" + datetime.datetime.now().strftime("%S_%f")

    cmd = "convert {} -type grayscale {}".format(input_file, tmp_file1)

    os.system(cmd)

    cmd = "convert {} -resize {}x{}\! {}".format(
        bwgrad_file, width, hight, tmp_file2)

    os.system(cmd)

    cmd = "composite -compose softlight -gravity center {} {} {}"\
        .format(tmp_file2, tmp_file1, output_file)

    os.system(cmd)

    os.system("rm " + tmp_file1)
    os.system("rm " + tmp_file2)


def blur(input_file, output_file):
    cmd = "convert {} -blur 0.5x2 {}".format(input_file, output_file)

    os.system(cmd)
