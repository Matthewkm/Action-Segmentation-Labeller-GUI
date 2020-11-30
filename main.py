from tkinter import *
from label_gui import label_GUI

import argparse


def arg_parse():
	parser = argparse.ArgumentParser(description='Arguments for the GUI action recognition video labeler')
	parser.add_argument("--mode", dest="mode", help = 'Can be either "single" label mode or noun-verb "duo" mode')
	parser.add_argument("--video_path", dest="video_path", help="Path to video being labelled")
	parser.add_argument("--label_csv", dest="label_csv", help="Path to csv file where labels will be stored")
	parser.add_argument("--classes_csv", dest="classes_csv", help="Path to csv file containing all labels")
	parser.add_argument("--verb_csv", dest="verb_csv", help="Path to csv file containing all verb labels")
	parser.add_argument("--noun_csv", dest="noun_csv", help="Path to csv file containing all noun labels")

	return parser.parse_args()


if __name__ == '__main__':	
	
	root = Tk()
	args = arg_parse()

	mode = args.mode
	video_path = args.video_path
	label_csv = args.label_csv

	modes = ['single','duo']
	if mode not in modes:
		print('Error, mode {} not recognised, please enter either single or duo mode'.format(mode))
		quit()

	if args.mode == 'duo':  #if using verb,noun labeling system.
		verb_csv = args.verb_csv
		noun_csv = args.noun_csv
		classes_csv  = verb_csv,noun_csv


	if args.mode == 'single':
		classes_csv = args.classes_csv


	label_GUI(root,video_path,label_csv,classes_csv,mode)
