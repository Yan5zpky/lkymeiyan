# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for
from PIL import Image, ImageDraw
from werkzeug.utils import secure_filename

import face_recognition
import os

UPLOAD_FOLDER = '/var/www/html/meiyanapi/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
			
		# 将jpg文件加载到numpy数组中
		imgName = app.config['UPLOAD_FOLDER']+ '/'+filename
		im = Image.open(imgName)
		image = face_recognition.load_image_file(imgName)

		# 查找图像中所有面部的所有面部特征

		face_landmarks_list = face_recognition.face_landmarks(image)

		for face_landmarks in face_landmarks_list:

        		pil_image = Image.fromarray(image)

			d = ImageDraw.Draw(im, 'RGBA')

			# 让眉毛变成了一场噩梦

			d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))

			d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))

			d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)

			d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

			# 光泽的嘴唇

			d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))

			d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))

			d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)

			d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

			# 闪耀眼睛

			d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))

			d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

			# 涂一些眼线

			d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)

			d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

			im.save(app.config['UPLOAD_FOLDER']+"/beautiful"+filename)

			return "beautiful"+filename
