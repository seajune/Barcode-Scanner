# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:27:24 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 17:28:42 2016

@author: Administrator
"""

import cv2
import numpy as np
import itertools
from PIL import Image

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

def get_angle(img_binary):
    for j in range(img_binary.shape[1]):
            for i in range(img_binary.shape[0]):
                if img_binary[i][j] <145:
                    i_0 = i
                    j_0 = j
                    break
    
    for i in range(img_binary.shape[0]):
            for j in range(img_binary.shape[1]):
                if img_binary[i][j] < 145:
                    i_1 = i
                    j_1 = j
                    break
    
    k = (i_0-i_1)*1.0/(j_1-j_0)
    angle = np.arctan(k)*180/np.pi
    
    return angle
 
def get_pixel(img):
    get_img = []
    a = 137.2
    for j in range(49,(img.shape[1]-50)):
        if img[0][j] > a:
            get_img.append(255)
        else:
            get_img.append(0)  
          
    return get_img
 
def get_middle_row(img):
    row= img.shape[0]/2
    img_mean=np.zeros((1,img.shape[1]))
    a=[]
    for j in range(img.shape[1]):
        for i in range((row-4),(row+4)):
            a.append(img[i][j])
        img_mean[0][j]=np.mean(a)
        a=[]

    return img_mean
    
def get_bar_space_width(img):
    currentPix = -1#初始化
    lastPix = -1
    pos = 0
    width = []
    for i in range(len(img)):#遍历一整行
        currentPix = img[i]
        if currentPix != lastPix:
            if lastPix == -1:
                lastPix = currentPix
                pos = i
            else:
                width.append( i - pos )
                pos = i
                lastPix = currentPix
    return width

def image_corrected_generate(img_original, img):    
    img_show = np.zeros((img_original.shape[0],len(img)))
    for j in range(len(img)):
        for i in range(img_show.shape[0]):
            img_show[i][j] = img[j]
            
    return img_show

def decoding(barspacewidth):   
    length = len(barspacewidth)/10
    state =[0]
    state = state * len(barspacewidth)
    identify_code = [0]
    identify_code = identify_code * length
    for i in range(length):
        for k in range(10 * i, 10 * i + 9):
            if k % 2 == 0:
                if barspacewidth[k] >3:
                    state[k] = '11'
                else:
                    state[k] = '1'
            else:
                if barspacewidth[k] >3:
                    state[k] = '00'
                else:
                    state[k] = '0'
        state_chain=''.join(itertools.chain(*state[10*i:10*i+9]))
        identify_code[i]=decoding_table.get(state_chain)
    
    return identify_code

if __name__ == '__main__':
    file_num = 469
    file_str = []
    for i in range(440,file_num+1):
        if(i/100 != 0):
            file_str.append('BC0'+str(i)+'.jpg')
        else:
            if(i/10 != 0):
                file_str.append('BC00'+str(i)+'.jpg')
            else:
                file_str.append('BC000'+str(i)+'.jpg')
    
    for k, v in enumerate(file_str):
        img_original = cv2.imread(v)
        img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)#转换成单通道图像

        cv2.imwrite('img_gray.jpg', img_gray)
  
        #校正旋转
        im = Image.open('img_gray.jpg')
        angle = get_angle(img_gray)#获取旋转的角度
        im_rotate = im.rotate(-angle)#旋转
        im_rotate.save('im_rotate.jpg')

        #统一像素
        img_rotate = cv2.imread('im_rotate.jpg')
        img_mean=get_middle_row(img_rotate)#取中间几行的平均像素
        #二值化
        img_binary = get_pixel(img_mean)
        
        img_show = image_corrected_generate(img_original, img_binary)#还原成无干扰图像
        cv2.imwrite('img_correct_rotation.jpg', img_show)
        
        #提取条空宽度
        barSpaceWidth = get_bar_space_width(img_binary)
        barSpaceWidth_1=barSpaceWidth[11:-19]#去掉空白，起始码，检查码，终止码
    
        #译码
        code = decoding(barSpaceWidth_1)
        #print code
        identify_code = ''.join(itertools.chain(*code)) 
        print v,identify_code 