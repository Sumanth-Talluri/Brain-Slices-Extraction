import os
import cv2
import glob
import shutil
from pathlib import Path

def createSlices():

	# deleting the slices folder if it is already present 
	slicesPresent = os.path.isdir(os.path.join(os.getcwd(),"Slices"))
	if slicesPresent:
		shutil.rmtree(os.path.join(os.getcwd(),"Slices"))
		#  waiting until the folder and it's contents are deleted
		while os.path.isdir(os.path.join(os.getcwd(),"Slices")):
			pass

	# deleting the slices and boundaries folder if it is already present 
	boundariesPresent = os.path.isdir(os.path.join(os.getcwd(),"Boundaries"))
	if boundariesPresent:
		shutil.rmtree(os.path.join(os.getcwd(),"Boundaries"))
		#  waiting until the folder and it's contents are deleted
		while os.path.isdir(os.path.join(os.getcwd(),"Boundaries")):
			pass

	# creating slices folder
	slicesPresent = os.path.isdir(os.path.join(os.getcwd(),"Slices"))
	if not slicesPresent:
		os.mkdir(os.path.join(os.getcwd(),"Slices"))

	# creating a boundaries folder
	boundariesPresent = os.path.isdir(os.path.join(os.getcwd(),"Boundaries"))
	if not boundariesPresent:
		os.mkdir(os.path.join(os.getcwd(),"Boundaries"))

	# getting the images one by one from the data
	for img_path in glob.glob("./testPatient/*thresh.png"):

		fileName = Path(img_path).name.split('.')[0]

		# creating a folder with the image name inside slices folder
		folderPresent = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Slices"),fileName))
		if not folderPresent:
			os.mkdir(os.path.join(os.path.join(os.getcwd(),"Slices"),fileName))

		# creating a folder with the image name inside boundaries folder
		folderPresent = os.path.isdir(os.path.join(os.path.join(os.getcwd(),"Boundaries"),fileName))
		if not folderPresent:
			os.mkdir(os.path.join(os.path.join(os.getcwd(),"Boundaries"),fileName))

		# reading the thresh image
		image = cv2.imread(img_path)
		# getting the length of the image
		image_length = image.shape[1]
		# cropping the top and the right side noise in the image
		final_image = image[20:,:image_length-82,:]

		#  calculating the vertical coordinates of R in the image
		v_rs = []
		for i in range(len(final_image)):
			for j in range(len(final_image[i])):
				if final_image[i][j].sum() >= 1:
					if j in [0,1,2,3,4]:
						v_rs.append(i)
		v_rs = set(v_rs)
		v_lst = list(v_rs)
		v_lst.sort()
		# storing the starting R coordinates in v_r_start
		v_r_start = [v_lst[i] for i in range(0,len(v_lst),5)]

		#  calculating the horizontal coordinates of R in the image
		h_rs = []
		for i in range(len(final_image)):
			for j in range(len(final_image[i])):
				if final_image[i][j].sum() >= 1:
					if i==v_r_start[0]:
						h_rs.append(j)
		h_rs = set(h_rs)
		h_lst = list(h_rs)
		h_lst.sort()
		# storing the starting R coordinates in h_r_start
		h_r_start = [h_lst[i] for i in range(0,len(h_lst),4)]

		# dividing the final image into columns based on R and storing in the imagesArr
		imagesArr = []
		# each R is 5 pixels hoizontall
		w = 5
		i = 1
		while i < len(h_r_start):
			col = final_image[:,w:h_r_start[i],:]
			imagesArr.append(col)
			w = h_r_start[i]+5
			i+=1
		# we will miss the last col in the above loop so appending it
		imagesArr.append(final_image[:,w:,:])

		#  from the columns we need to divide them into slices
		slices = []
		for img in imagesArr:
			h = 0
			i = 0
			while i < len(v_r_start):
				slice = img[h:v_r_start[i],:,:]
				slices.append(slice)
				#  each R is 4 pixels vertically
				h = v_r_start[i]+4
				i+=1
		#  after above loop we will get all the slices in the slices list

		# detecting contours in the slices
		i = 1
		for slice in slices:
			# Detecting the Brain boundary
			b, g, r = cv2.split(slice)
			# detecting contours using green channel and without thresholding
			contours, hierarchy = cv2.findContours(image=g, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
			# draw contours on the slice
			image_contour_green = slice.copy()
			cv2.drawContours(image=image_contour_green, contours=contours, contourIdx=-1, color=(51,214,255), thickness=1, lineType=cv2.LINE_AA)
			#  checking if there is a contour in the slice
			if len(contours):
				cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Slices"), fileName) + '/' + str(i) + ".png", slice)
				cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Boundaries"), fileName) + '/' + str(i) + ".png", image_contour_green)
				i+=1

		print(fileName, "successfully saved")