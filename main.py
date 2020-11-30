from tkinter import *
from gui_1_label import single_label_GUI
from gui_2_label  import two_label_GUI

import argparse


def arg_parse():
	parser = argparse.ArgumentParser(description='Arguments for the GUI action recognition video labeler')
	parser.add_argument("--two_label", dest="two_label", help = "True if wanting to implement a verb,noun labelling system.")
	parser.add_argument("--video_path", dest="video_path", help="Path to video being labelled")
	parser.add_argument("--label_csv", dest="label_csv", help="Path to csv file where labels will be stored")
	parser.add_argument("--classes_csv", dest="classes_csv", help="Path to csv file containing all labels")
	parser.add_argument("--verb_csv", dest="verb_csv", help="Path to csv file containing all verb labels")
	parser.add_argument("--noun_csv", dest="noun_csv", help="Path to csv file containing all noun labels")

	return parser.parse_args()


if __name__ == '__main__':	
	
	root = Tk()
	args = arg_parse()

	video_path = args.video_path
	label_csv = args.label_csv

	print(args.two_label)
	if args.two_label == True:  #if using verb,noun labeling system.
		verb_csv = args.verb_csv
		noun_csv = args.noun_csv
		two_label_GUI(root,video_path,label_csv,verb_csv,noun_csv)

	else:
		classes_csv = args.classes_csv
		single_label_GUI(root,video_path,label_csv,classes_csv)

