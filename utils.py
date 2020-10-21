#some utility classes and functions for the GUI, mainly video processing.
import os
from PIL import Image 

def create_list(folder):
	'''
	converts a folder of images into a list of PIL images.
	'''
	video = []
	for img in os.listdir(folder):
		img_path = os.path.join(folder,img)
		video.append(Image.open(img_path))
	return video

def vid2imgs(video_path):

	#if running first time must create data folder.
	if os.path.exists('data') == False:
		os.mkdir('data')

	#check if decoding has been done before, if so use that file
	video_name = os.path.basename(video_path)[:-4] 

	new_folder = os.path.join('data',video_name)


	if os.path.isdir(new_folder): #if folder already exists
		if os.listdir(new_folder) == 0: #if folder is empty, decode the video into it.
			print('decoding the video, this may take a while... Once finished GUI will load')
			bashCommand = 'ffmpeg -i "{}" -vf scale=-1:720 -q:v 0  "{}/%06d.jpg'.format(video_path,new_folder,video_name) #create clips.
			os.system(bashCommand)

			return create_list(new_folder)

		else: #assume the video has been successfully decoded already.
			print('A folder with this video name already exists, loading that instead (much quicker)')
			return create_list(new_folder) 

	else: #need to decode the video into a folder of images - makes life easier...
		print('decoding the video, this may take a while... Once finished GUI will load')
		os.mkdir(new_folder)
		bashCommand = 'ffmpeg -i "{}" -vf scale=-1:720 -q:v 0  "{}/%06d.jpg'.format(video_path,new_folder,video_name) #create clips.
		os.system(bashCommand)

		return create_list(new_folder)
