from tkinter import *
from tkintertable import TableCanvas, TableModel
from PIL import ImageTk,Image 

import os
import csv
import cv2

from functools import partial

from utils import decode_video, get_image


class get_labels_single():

	def __init__(self,labels_csv,):	

		def read_csv(the_csv):
			with open(the_csv, mode='r') as infile:
				reader = csv.reader(infile)
				mydict = {rows[0]:rows[1] for rows in reader}
			return mydict

		self._labels =  read_csv(labels_csv)


	def labels(self):
		#turns the dic into a list of nouns used to populate the options menu.
		dictlist = []
		for _, value in self._labels.items():
			dictlist.append(value)
		return dictlist


	def label_dict(self):
		return self._labels

class get_labels_duo():

	def __init__(self,verb_csv,noun_csv):	
		#this function will ultimetly parse an input csv containing all the verbs and nounds, for the moment ill just use example lists

		def read_csv(the_csv):
			with open(the_csv, mode='r') as infile:
				reader = csv.reader(infile)
				mydict = {rows[0]:rows[1] for rows in reader}
			return mydict

		self._verbs =  read_csv(verb_csv)
		self._nouns =  read_csv(noun_csv)


	def verbs(self):
		#turns the dic into a list of nouns used to populate the options menu.
		dictlist = []
		for _, value in self._verbs.items():
			dictlist.append(value)
		return dictlist

	def nouns(self):
		dictlist = []
		for _, value in self._nouns.items():
			dictlist.append(value)
		return dictlist


	def verb_dict(self):
		return self._verbs

	def noun_dict(self):
		return self._nouns


class label_GUI:

	def __init__(self, root, video_path, csv_path, labels_csv, mode):

		self.video_path = video_path
		self.fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)
		self.csv_path = csv_path

		self.mode = mode

		if self.mode == 'single':
			self.labels = get_labels_single(labels_csv)
			self.CLASSES = self.labels.labels()
			self.CLASSES_DICT = self.labels.label_dict()
		if self.mode == 'duo':
			verb_csv,noun_csv = labels_csv
			self.labels = get_labels_duo(verb_csv,noun_csv)
			self.NOUNS = self.labels.nouns()
			self.NOUNS_DICT = self.labels.noun_dict()
			self.VERBS = self.labels.verbs()
			self.VERBS_DICT = self.labels.verb_dict()


		self.window = root
		self.canvas = Canvas(self.window,width = 1850,height=1000)
		self.canvas.pack()

		self.current_state = 0 #this is either 0 (not labeling), 1 (mid label (i.e defined start)), 2 labeled waiting for confirmation
		self.console_output = []
		self.current_index = 0
		self.start_frame = None
		self.end_frame = None

		#pay attention to all keypresses
		self.window.bind("<Key>",self.key_pressed)

		#decode the video here (and check if its already been decoded)
		self.image_folder = decode_video(self.video_path)
		
		#==================== create all the widgets =========================:
		
		#label selection
		if self.mode == 'single':
			self.label = Label(self.window,text='Select Label:',font=("Courier", 15))
			self.label.place(x=1150,y=150)

			self.class_drop = StringVar(self.window)
			self.class_drop.set(self.CLASSES[0])
			self.w_classes = OptionMenu(*(self.window, self.class_drop) + tuple(self.CLASSES))
			self.w_classes.place(x=1400,y=150)

		if self.mode == 'duo':
			self.label = Label(self.window,text='Select Label:',font=("Courier", 15))
			self.label.place(x=1150,y=150)

			self.noun_drop = StringVar(self.window)
			self.noun_drop.set(self.NOUNS[0])
			self.w_noun = OptionMenu(*(self.window, self.noun_drop) + tuple(self.NOUNS))
			self.w_noun.place(x=1550,y=150)

			self.verb_drop = StringVar(self.window)
			self.verb_drop.set(self.VERBS[0])
			self.w_verb = OptionMenu(*(self.window, self.verb_drop) + tuple(self.VERBS))
			self.w_verb.place(x=1400,y=150)

		#play buttons:
		self.prev_button = Button(self.window, text="Prev", height=100,width=100,command=self.prev)
		self.next_button = Button(self.window, text="Next", height=100,width=100,command=self.nxt)
		self.pause_button = Button(self.window, text="Stop", height = 50, width=100, command=self.pause_video)
		self.play_button = Button(self.window, text="Play", height=50, width=100, command=partial(self.play_video,speed=1))
		self.play_button2 = Button(self.window, text="x2", height=50, width=100, command=partial(self.play_video,speed=2))
		self.play_button4 = Button(self.window, text="x4", height=50, width=100, command=partial(self.play_video,speed=4))
		self.play_button8 = Button(self.window, text="x8", height=50, width=100, command=partial(self.play_video,speed=8))
		self.speed = 1

		self.prev_button.place(bordermode=OUTSIDE, height=100, width=100, x=45,y=300)
		self.next_button.place(bordermode=OUTSIDE, height=100, width=100, x=1050,y=300)
		self.pause_button.place(bordermode=OUTSIDE, height= 50, width=100, x=400, y=600)
		self.play_button.place(bordermode=OUTSIDE, height=50, width=100, x=550, y=600)
		self.play_button2.place(bordermode=OUTSIDE, height=50, width=100, x=650, y=600)
		self.play_button4.place(bordermode=OUTSIDE, height=50, width=100, x=750, y=600)
		self.play_button8.place(bordermode=OUTSIDE, height=50, width=100, x=850, y=600)

		self.pause = False #boolean, if true, video is in paused (still image state) if faluse, it is playing.
		self.currently_playing = False

		#frame input textbox and button for submitting it.
		self.textBox = Text(self.window, height=1, width=10)
		self.textBox.place(x=150,y=600)
		self.buttonCommit=Button(self.window, height=1, width=10, text="Jump to frame", command=lambda: self.retrieve_input())
		self.buttonCommit.place(x=250,y=600)


		#display frame numbers
		self.frame_no = Label(self.window,text='Current Frame: {}'.format(self.current_index),font=("Courier", 15))
		self.start_no = Label(self.window,text='Start Frame: {}'.format(self.start_frame),font=("Courier", 15))
		self.end_no = Label(self.window,text='End Frame: {}'.format(self.end_frame),font=("Courier", 15))
		self.frame_no.place(x=150,y=45)
		self.start_no.place(x=1150,y=70)
		self.end_no.place(x=1500,y=70)


		#display image with current index.

		self.image = get_image(self.image_folder,self.current_index) #retun the current image from 
		self.max_index =  len(os.listdir(self.image_folder))-1 
		self.img =  ImageTk.PhotoImage(self.image.resize((896,504)))
		self.img_panel = Label(self.window,image=self.img)
		self.img_panel.image = self.img
		self.img_panel.place(x=150,y=75)


		#add a slider to navigate frames
		self.slider = Scale(self.window,from_=0,to=self.max_index,orient=HORIZONTAL)
		self.slider.set(0)
		self.slider.place(width=900,x=150, y=700)

		self.slider_button = Button(self.window, text='Jump',command=self.goto_slider)
		self.slider_button.place(x=1075,y=715)


		#console output.
		self.console_listbox = Listbox(self.window)
		for item in self.console_output:
			self.console_listbox.insert(END,item)
		self.console_listbox.place(height=200,width=600,x=1200,y=700)

		#table output
		self.label_data = self.read_csv()

		self.write('Welcome to my simple video label GUI. Please read the Github for user instructions')

		self.window.mainloop()


	def read_csv(self):
		#reads csv and displays table using tkintertable
		self.tframe = Frame(self.window)
		self.tframe.place(x=1200,y=350,width=600) 
		self.table = TableCanvas(self.tframe)
		self.table.importCSV(self.csv_path)
		self.table.show()

	def write(self, message):
		#function that is used instead of regular print statement to display messages within the GUI output box

		if len(self.console_output) < 10:  #only collect last 10 lines of output.
			self.console_output.append(message)
		else:
			self.console_output = self.console_output[1:]
			self.console_output.append(message)

		self.update_all()
		return self.console_output  

	def prev(self):
		#move to next image
		if self.current_index == 0:
			self.update_all()
		else:
			self.current_index -=1
			self.update_all()

	def nxt(self):
		#move to previous image
		if self.current_index == self.max_index:
			self.update_all()
		else:
			self.current_index +=1
			self.update_all()

	def play_video(self,speed):
		#function that runs when play buttons are pressed.
		self.speed = speed

		def play():
			delay = int((1/(self.speed*self.fps))*1000)
			if self.pause: #if currently paused and button is pressed, we want to play
					self.window.after_cancel(self.after_id)
					self.pause = False
					self.currently_playing = False

			else:	
				self.currently_playing = True
				self.current_index+=1
				self.update_image()
				delay = int(max(1,(delay-(1000*finish))))
				self.after_id = self.window.after(delay,play)

		play()

	def pause_video(self):
		if self.currently_playing:
			self.pause = True
		else:
			self.pause = False


	def retrieve_input(self):
		input_val = self.textBox.get("1.0",END)
		try:
			input_val = int(input_val)
		except:
			self.write('please input an intiger')
			self.window.mainloop()
			input_val = 0
		if input_val < 0 or input_val > int(self.max_index):
			self.write('please enter a value between 0 and {}'.format(self.max_index))
			self.window.mainloop()
		else:
			self.current_index = input_val
			self.write('jumped to frame {}'.format(self.current_index))
			self.window.mainloop()

	def goto_slider(self):
		self.current_index = self.slider.get() #set current index to slider value.
		self.update_all()


	#code for using keyboard shortcuts.
	def key_pressed(self,event):
		if event.keysym == 'Right':
			self.nxt()
		if event.keysym == 'Left':
			self.prev()
		if event.keysym == 'space':
			if self.current_state == 0:
				self.start_frame = self.current_index
				self.write('selected a start frame, press space to select end frame or esc to cancel selection')
				self.end_frame = None
				self.current_state = 1 #change state to 1.
			elif self.current_state == 1:
				self.end_frame = self.current_index
				self.write('Selected an end frame, press space to change end frame, return to submit the label or esc to cancel selection')
				self.current_state = 2
			elif self.current_state == 2:
				self.end_frame = self.current_index
			self.update_all()
		if event.keysym == 'Return':
			if self.current_state == 2: #only care is someone is in state 2.
				self.make_label() 
				self.current_state=0
				self.start_frame = None
				self.end_frame = None
			else:
				self.write('You must make a start and end frame selection before submitting the label')
			self.update_all()
		if event.keysym == 'Escape':
			#if escape is hit, delete all frame selections and return to state 0, ready for a new input sequence.
			self.start_frame = None #delete frame selection
			self.end_frame = None
			self.current_state = 0 #set current state back to 0.
			self.write('cancled frame selection')
			self.update_all()

	def make_label(self):
		video_name = os.path.basename(self.video_path)[:-4] 

		if self.mode == 'single':
			_class = self.class_drop.get()

			with open(self.csv_path,'a',newline='') as csvfile:
				linewriter = csv.writer(csvfile,delimiter=',')
				linewriter.writerow([video_name,self.start_frame,self.end_frame,_class,self.CLASSES.index(_class)])

			self.write('added action {} between frames {} and {} to csv file'.format(_class,self.start_frame,self.end_frame))

		if self.mode == 'duo':
			verb = self.verb_drop.get()
			noun = self.noun_drop.get()

					#still need to implement checks here, e.g make sure end frame is after begining, that they are not the same frame etc...
			with open(self.csv_path,'a',newline='') as csvfile:
				linewriter = csv.writer(csvfile,delimiter=',')
				linewriter.writerow([video_name,self.start_frame,self.end_frame,verb,self.VERBS.index(verb),noun,self.NOUNS.index(noun)])

			self.write('added label to csv file, action {} {} between frames {} and {}'.format(verb,noun,self.start_frame,self.end_frame))

		self.read_csv()


	def update_image(self):
		"""
		Same as update_all except only updates the image and the current frame - quicker to execute as doenst update csv table
		"""
		pil_img = get_image(self.image_folder,self.current_index)
		img =  ImageTk.PhotoImage(pil_img.resize((896,504)))  #size is 896x504
		self.img_panel.configure(image=img)
		self.img_panel.image = img

		self.frame_no['text'] = "Current Fame: {}".format(self.current_index)
		self.slider.set(self.current_index)

	def update_all(self):
		'''
		the main function that updates everything, run efter nearly every function
		'''

		pil_img = get_image(self.image_folder,self.current_index)
		img =  ImageTk.PhotoImage(pil_img.resize((896,504)))
		self.img_panel.configure(image=img)
		self.img_panel.image = img

		self.slider.set(self.current_index)
		self.table.show()

		self.frame_no['text'] = "Current Fame: {}".format(self.current_index)
		self.start_no['text'] = "Start Frame: {}".format(self.start_frame)
		self.end_no['text'] = "End Frame: {}".format(self.end_frame)

		self.console_listbox.delete(0,'end')
		for item in self.console_output:
			self.console_listbox.insert(END,item)

