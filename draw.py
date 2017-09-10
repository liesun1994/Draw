# -*- coding: utf-8 -*-
import numpy as np
import argparse
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import logging
import numpy
import sys
import pdb

reload(sys)
sys.setdefaultencoding('utf-8')
from matplotlib.font_manager import *

myfont = FontProperties(fname='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')

logger = logging.getLogger(__name__)


class Draw(object):
    def __init__(self, src, trg, align, imgpath):
        self.src = src
        self.trg = trg
        self.align = align
        self.imgpath = imgpath

    def split_align_data(self, data):
        #pdb.set_trace()
        splited_data = []
        for now_data in data:
            splited_now_data = now_data.strip().split(' ')
            splited_now = []
            for n_data in splited_now_data:
                splited_now.append(float(n_data))
            splited_data.append(splited_now)
        return splited_data

    # flag = true means src, else trg
    def split_src_trg_data(self, data, flag=False):
        splited_data = []
        for now_data in data:
            splited_now_data = now_data.strip().split(' ')
            # pdb.set_trace()
            if flag:
                splited_now_data.append('<s>')
            splited_data.append(splited_now_data)
        return splited_data

    def parse_data(self):
        #pdb.set_trace()
        src_obj = open(self.src)
        trg_obj = open(self.trg)
        align_obj = open(self.align)
        src_txt = src_obj.readlines()
        trg_txt = trg_obj.readlines()
        align_txt = align_obj.readlines()
        src_splited = self.split_src_trg_data(src_txt, False)
        trg_splited = self.split_src_trg_data(trg_txt, True)
        align_splited = self.split_align_data(align_txt)
        src_obj.close()
        trg_obj.close()
        align_obj.close()
        return src_splited, trg_splited, align_splited

    def draw(self):
        # added for chinese symbols
        src_parsed, trg_parsed, align_parsed = self.parse_data()
        # plt.rcParams['font.sans-serif']=['simhei']
        # clear figure
        step = 0
        #pdb.set_trace()
        for src_parsed_step, trg_parsed_step, align_parsed_step in zip(src_parsed, trg_parsed, align_parsed):
            #pdb.set_trace()
            step = step+1
            if len(src_parsed_step)>15 or len(trg_parsed_step)>15:
                continue
            plt.clf()
            f = plt.figure()
            ax = f.add_subplot(1, 1, 1)
            activation_map = np.asarray(align_parsed_step).reshape(len(trg_parsed_step), len(src_parsed_step))
            # add image

            i = ax.imshow(activation_map, interpolation='nearest', cmap='gray', aspect='equal')

            ax.set_xticks(range(len(src_parsed_step)))
            src_parsed_step_new = []
            for src in src_parsed_step:
                src = unicode(src, "utf-8")
                src_parsed_step_new.append(src)
            ax.set_xticklabels(src_parsed_step_new, fontproperties=myfont, rotation=90)

            ax.set_yticks(range(len(trg_parsed_step)))
            trg_parsed_step_new = []
            for trg in trg_parsed_step:
                trg = unicode(trg, "utf-8")
                trg_parsed_step_new.append(trg)
            ax.set_yticklabels(trg_parsed_step_new, fontproperties=myfont)
            # set x&y axis props
            for tick in ax.yaxis.get_major_ticks():
                tick.label1On = True
                tick.label2On = False
                tick.tick1On = False
                tick.tick2On = False
            for tick in ax.xaxis.get_major_ticks():
                tick.tick2On = False
                tick.tick1On = False
                tick.label1On = True
                tick.label2On = False

            ax.grid(False)
            #f.savefig(self.imgpath + str(step) + '.pdf', bbox_inches='tight')
            f.savefig(self.imgpath + str(step) + '.pdf')
            # print('Successfully draw a picture.') # python 3.*
            print 'Successfully draw a picture.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str)
    parser.add_argument('trg', type=str)
    parser.add_argument('align', type=str)
    parser.add_argument('imgpath', type=str)
    args = parser.parse_args()
    #pdb.set_trace()
    draw_obj = Draw(src=args.src, trg=args.trg, align=args.align, imgpath=args.imgpath)
    draw_obj.draw()
