# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, jsonify
from PIL import Image, ImageDraw, ImageFilter
from werkzeug.utils import secure_filename

import face_recognition
import os
import dlib
import cv2
import math
import random, string

UPLOAD_FOLDER = '/var/www/html/meiyanapi/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
def random_str(randomlength=8):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:randomlength])

def image_filter(img, filterType):
	if (filterType is 0):
		filteredImg = img
	elif (filterType is 1):
		# 模糊滤波
		filteredImg = img.filter(ImageFilter.BLUR)
	elif (filterType is 2):
		# 轮廓滤波
		filteredImg = img.filter(ImageFilter.CONTOUR)
	elif (filterType is 3):
		# 细节增强滤波
		filteredImg = img.filter(ImageFilter.DETAIL)
	elif (filterType is 4):
		# 边缘增强滤波
		filteredImg = img.filter(ImageFilter.EDGE_ENHANCE)
	elif (filterType is 5):
		# 深度边缘增强滤波
		filteredImg = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	elif (filterType is 6):
		# 浮雕滤波
		filteredImg = img.filter(ImageFilter.EMBOSS)
	elif (filterType is 7):
		# 浮雕滤波
		filteredImg = img.filter(ImageFilter.SMOOTH)
	return filteredImg		
	
def face5(img):
    landmark_predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    detector = dlib.get_frontal_face_detector()
    faces = detector(img,1)
    if (len(faces) > 0):
        for k,d in enumerate(faces):
            #draw_rec(img,d)
            shape = landmark_predictor(img,d)
            #特征点全部保存在了shape里面，d是dlib.rectangle()，人脸检测矩形的左上和右下坐标，shape.part(i)是第i个特征点
            #for i in range(5):
               # cv2.circle(img,(shape.part(i).x,shape.part(i).y),2,(255,0,0),-1)
               # cv2.putText(img, '{}'.format(i),(shape.part(i).x,shape.part#(i).y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2,cv2.LINE_8, 0)

            #cv2.line(img,(shape.part(0).x,shape.part(0).y),(shape.part(1).x,shape.part(1).y),(0,255,0),1)
            #cv2.line(img,(shape.part(1).x,shape.part(1).y),(shape.part(4).x,shape.part(4).y),(0,255,0),1)
            #cv2.line(img,(shape.part(4).x,shape.part(4).y),(shape.part(3).x,shape.part(3).y),(0,255,0),1)
            #cv2.line(img,(shape.part(3).x,shape.part(3).y),(shape.part(2).x,shape.part(2).y),(0,255,0),1)

            angle=math.atan((shape.part(2).y-shape.part(0).y)/(shape.part(0).x-shape.part(2).x))*180/3.14

            wr=int((shape.part(0).x-shape.part(2).x))
            hr=wr
            w=int(wr*1.8)
            h=w
            logo = cv2.imread('sunglass.jpg')
            glass=cv2.resize(logo,(w,h), interpolation = cv2.INTER_CUBIC)
            glass=cv2.GaussianBlur(glass,(5,5),0)

            rotate = cv2.getRotationMatrix2D((w//2,h//2),angle,1)
            glass = cv2.warpAffine(glass,rotate,(w,h))

            roi=img[(shape.part(2).y-h//2):(shape.part(2).y-h//2+h),(shape.part(2).x-w//5):(shape.part(2).x-w//5+w)]

            gray = cv2.cvtColor(glass,cv2.COLOR_BGR2GRAY)               #logo转化为灰度图
            ret, mask = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY)  #设定一个阈值扣除背景变为黑白蒙版
            mask_inv = cv2.bitwise_not(mask)                            #把蒙版区域互换的效果
            img_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)   #把背景图中rio区域内不覆盖logo的地方找出来
            #cv2.imshow('mask1',mask)
            #cv2.imwrite('a1.jpg',mask)
            logo_fg = cv2.bitwise_and(glass,glass,mask = mask)          #把背景透明的logo图找出来
            #cv2.imshow('mask2',mask_inv)
            #cv2.imwrite('a2.jpg',mask_inv)
            dst = cv2.add(img_bg,logo_fg)   #两者相加
            img[(shape.part(2).y-h//2):(shape.part(2).y-h//2+h),(shape.part(2).x-w//5):(shape.part(2).x-w//5+w)]=dst    

@app.route('/makeup', methods=['GET', 'POST'])
def digital_makeup():
	if request.method == 'POST':
        # check if the post request has the file part
       		if 'file' not in request.files:           
            		return 'No file part'
       		file = request.files['file']
       		# if user does not select file, browser also
        	# submit a empty part without filename
        	if file.filename == '':
	        	return 'invalid file name'
        	if file and allowed_file(file.filename):
            		filename = secure_filename(file.filename)
            		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))	
		
		useSunglass = request.args.get("sunglass")
		filterType = request.args.get("filterType")
		# 将jpg文件加载到numpy数组中
		imgName = app.config['UPLOAD_FOLDER']+ '/'+filename
		im = Image.open(imgName)
		greyImg = Image.open(imgName).convert("L")
		greyImg.save(app.config['UPLOAD_FOLDER']+ '/grey'+filename)
		image = face_recognition.load_image_file(app.config['UPLOAD_FOLDER']+ '/grey'+filename)

		

		face_landmarks_list = face_recognition.face_landmarks(image)

		for face_landmarks in face_landmarks_list:

        		pil_image = Image.fromarray(image)

			d = ImageDraw.Draw(im, 'RGBA')

			
			
			if useSunglass == "0":

				d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))

				d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))

				d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)

				d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

			

			d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))

			d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))

			d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=3)

			d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=3)

			
			
			if useSunglass == "0":

				d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))

				d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

				

				d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)

				d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
			
			fileprefix = random_str(16)
			im.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			if useSunglass == "1":
				sunImg = cv2.imread(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
				face5(sunImg)
				cv2.imwrite(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename, sunImg)

			filterImg = Image.open(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			if (filterType == "0"):
				resultImg = filterImg
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "1"):
				# 模糊滤波
				resultImg = filterImg.filter(ImageFilter.BLUR)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "2"):
				# 轮廓滤波
				resultImg = filterImg.filter(ImageFilter.CONTOUR)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "3"):
				# 细节增强滤波
				resultImg = filterImg.filter(ImageFilter.DETAIL)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "4"):
				# 边缘增强滤波
				resultImg = filterImg.filter(ImageFilter.EDGE_ENHANCE)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "5"):
				# 深度边缘增强滤波
				resultImg = filterImg.filter(ImageFilter.EDGE_ENHANCE_MORE)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "6"):
				# 浮雕滤波
				resultImg = filterImg.filter(ImageFilter.EMBOSS)
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
			elif (filterType == "7"):
				# 浮雕滤波
				resultImg = filterImg.filter(ImageFilter.SMOOTH)	
				resultImg.save(app.config['UPLOAD_FOLDER']+"/beautiful"+fileprefix+filename)
				
			returnData = {
				'beautifulpath': "beautiful"+fileprefix+filename,
				'originpath': filename
			}

			return jsonify(returnData)
