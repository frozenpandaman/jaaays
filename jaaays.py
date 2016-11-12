import urllib2
from PIL import Image
from PIL import ImageStat
import os
import sys
import time
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2


# (484) ALG-JAYS

response = "I don't know what you mean, sorry."
debug = False
if len(sys.argv) > 1:
	if sys.argv[1] == "debug":
		debug = True
f = "img/capture.jpg"

# modified from http://stackoverflow.com/a/21844162
#  and http://www.chioka.in/python-live-video-streaming-example/
def grabimg():
	stream = urllib2.urlopen('http://jays-place.cam.hmc.edu:80/mjpg/video.mjpg') # 134.173.32.137
	bytes = ''
	for i in range (0,20):
		bytes+=stream.read(1024)
		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')
		if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes = bytes[b+2:]
			#with open('img/capture.jpg','wb') as f:
			with open(f, 'wb') as fi:
				fi.write(jpg)

def brightness():
	im = Image.open(f).convert('L')
	stat = ImageStat.Stat(im)
	brightness = stat.mean[0]
	if (brightness < 70):
		r1 = "Jay's Place is closed."
	else:
		r1 = "The lights are on, so Jay's Place is most likely open!"
	if debug:
		r1 += "\n   brightness = " + str(brightness)
	print r1
	return r1

# def line():
# 	im = Image.open(f).convert('RGB')
# 	w_st, h_st, w_end, h_end = 15, 130, 42, 206
# 	r, g, b = 0, 0, 0
# 	for i in xrange(w_st, w_end):
# 		for j in xrange(h_st, h_end):
# 			r += im.getpixel((i, j))[0]
# 			g += im.getpixel((i, j))[1]
# 			b += im.getpixel((i, j))[2]
# 	r /= 2052
# 	g /= 2052
# 	b /= 2052 # change this so it looks at the past 10 secs or something
# 	if r > 200 and g > 200 and b > 200:
# 		r2 = "The line at Jay's Place is short."
# 	else:
# 		r2 = "The line at Jay's Place is relatively long."
# 	if debug:
# 		r2 += "\n   rgb = " + str((r, g, b))
# 	print r2
# 	return r2

def line():
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	# load the image and resize it to (1) reduce detection time
	# and (2) improve detection accuracy
	image = cv2.imread(f)
	image = imutils.resize(image, width=min(400, image.shape[1]))
	orig = image.copy()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(2, 2),
		padding=(8, 8), scale=1.05)

	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	## draw the final bounding boxes
	# for (xA, yA, xB, yB) in pick:
	# 	cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

	## show some information on the number of bounding boxes
	# filename = imagePath[imagePath.rfind("/") + 1:]
	# print("[INFO] {}: {} original boxes, {} after suppression".format(
	# 	filename, len(rects), len(pick)))

	# # show the output images
	# cv2.imshow("Before NMS", orig)
	# cv2.imshow("After NMS", image)
	# cv2.waitKey(0)

	HeadCount = len(pick)
	if HeadCount == 0:
		r2 = "There's nobody in line."
	elif HeadCount == 1:
		r2 = "There's 1 person in line."
	else:
		r2 = "There's about " + str(len(pick)) + " people in line."
	print r2
	return r2


starttime = time.time()
while True:
	grabimg()
	r1 = brightness()
	r2 = line()
	# os.remove(f)
	with open('out_open.txt', 'wb') as fi:
		fi.write(r1)
	with open('out_line.txt', 'wb') as fi:
		fi.write(r2)
	time.sleep(1.0 - ((time.time() - starttime) % 1.0))


