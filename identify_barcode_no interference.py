# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 21:01:01 2016

@author: Administrator
"""

import cv2
import numpy as np
import itertools

decoding_table = {
    '110101001011': 'a', '101101001011': 'b', '110110100101': 'c',
    '101011001011': 'd', '110101100101': 'e', '101101100101': 'f',
    '101010011011': 'g', '110101001101': 'h', '101101001101': 'i',
    '101011001101': 'j', '110101010011': 'k', '101101010011': 'l',
    '110110101001': 'm', '101011010011': 'n', '110101101001': 'o',
    '101101101001': 'p', '101010110011': 'q', '110101011001': 'r',
    '101101011001': 's', '101011011001': 't', '110010101011': 'u',
    '100110101011': 'v', '110011010101': 'w', '100101101011': 'x',
    '110010110101': 'y', '100110110101': 'z', '101001101101': '0',
    '110100101011': '1', '101100101011': '2', '110110010101': '3',
    '101001101011': '4', '110100110101': '5', '101100110101': '6',
    '101001011011': '7', '110100101101': '8', '101100101101': '9',
    '100101001001': '+', '100101011011': '-', '100101101101': '*',
    '100100101001': '/', '101001001001': '%', '100100100101': '$',
    '110010101101': '.', '100110101101': ' ',
    }

def get_bar_space_width(img):
    row = img.shape[0] *1/2#取中间这行的像素值
    currentPix = -1#初始化
    lastPix = -1
    pos = 0
    width = []
    for i in range(img.shape[1]):#遍历一整行
        currentPix = img[row][i]
        if currentPix != lastPix:
            if lastPix == -1:
                lastPix = currentPix
                pos = i
            else:
                width.append( i - pos )
                pos = i
                lastPix = currentPix
    return width

def bar_or_space(barspacewidth):
    bar=[]
    space=[]
    bar_value=[]
    space_value=[]
    for i in range (len(barspacewidth)):
        if i%2==0:
            bar.append(barspacewidth[i])
        else:
            space.append(barspacewidth[i])

    bar_seq=np.sort(bar)
    space_seq=np.sort(space)
    bar_value.append(bar_seq[0])
    space_value.append(space_seq[0])
    for i in range(1,len(bar_seq)):
        if bar_seq[i] not in bar_value:
            if bar_seq[i] !=  bar_seq[0]:
                bar_value.append(bar_seq[i])
    for i in range(1,len(space_seq)):
        if space_seq[i] not in space_value:
            if space_seq[i] !=  space_seq[0]:
                space_value.append(space_seq[i])
    
    bar_mean=np.mean(bar_value)
    space_mean=np.mean(space_value)

    return bar_mean, space_mean
    
def decoding(barspacewidth, bar_mean, space_mean):   
    length = len(barspacewidth)/10
    state =[0]
    state = state * len(barspacewidth)
    identify_code = [0]
    identify_code = identify_code * length
    for i in range(length):
        for k in range(10 * i, 10 * i + 9):
            if k % 2 == 0:
                if barspacewidth[k] >bar_mean:
                    state[k] = '11'
                else:
                    state[k] = '1'
            else:
                if barspacewidth[k] >space_mean:
                    state[k] = '00'
                else:
                    state[k] = '0'
        state_chain=''.join(itertools.chain(*state[10*i:10*i+9]))
        identify_code[i]=decoding_table.get(state_chain)
    
    return identify_code

if __name__ == '__main__':
    file_num = 259
    file_str = []
    for i in range(200,file_num+1):
        if(i/100 != 0):
            file_str.append('BC0'+str(i)+'.jpg')
        else:
            if(i/10 != 0):
                file_str.append('BC00'+str(i)+'.jpg')
            else:
                file_str.append('BC000'+str(i)+'.jpg')
    
    for k, v in enumerate(file_str):
        img_original = cv2.imread(v)#读取图片
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)#转换成单通道图像
        ret, img_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)#二值化
        #提取条空宽度
        barSpaceWidth = get_bar_space_width(img_binary)
        barSpaceWidth_1=barSpaceWidth[11:-19]#去掉空白，起始码，检查吗，终止码
        #求出bar和space的均值
        bar_mean, space_mean = bar_or_space(barSpaceWidth_1)
        #译码
        code = decoding(barSpaceWidth_1, bar_mean, space_mean)
        identify_code = ''.join(itertools.chain(*code)) 
        print v,identify_code 