条形码识别
=====
识别无干扰、带不同水平的高斯噪声、带背景色、旋转、畸变这5类code39型条形码，进行安全解密。
------
code39码的介绍：http://www.systron.com.cn/tiaoxingma/book2-4.htm
> 
identify_barcode_no interference.py：对无干扰条形码的识别
identify_barcode_with interference.py：对带不同水平的高斯噪声的条形码的识别
identify_barcode_with backgroudcolor.py：对带背景色的条形码的识别
identify_barcode_with rotate.py：对旋转的条形码的识别
identify_barcode_with distortion.py：对畸变的条形码的识别
BC0200.jpg～BC0259.jpg为无干扰图像
BC0260.jpg～BC0409.jpg为带不同水平的高斯噪声的图像
BC0410.jpg～BC0439.jpg为带背景色的图像
BC0440.jpg～BC0469.jpg为旋转图像
BC0470.jpg～BC0499.jpg为畸变图像
compare.py：识别结果跟正确结果相比，得到正确率
true_result.txt：正确的识别结果
my_result.txt：自己测试的结果
识别正确率为99.7%。
