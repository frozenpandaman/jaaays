import urllib2
from PIL import Image
from PIL import ImageStat
import os
import sys

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
		r1 += " (" + str(brightness) + ")"
	print r1
	return r1


grabimg()
r1 = brightness()
os.remove(f)
with open('out.txt', 'wb') as fi:
	fi.write('"' + r1 + '", ')