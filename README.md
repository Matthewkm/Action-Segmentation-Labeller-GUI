# GUI for Segment Level Annotations for Action Recognition.
This is a simplistic and lightweight GUI for producing segment level labels for action recognition in videos.

The GUI provides a quick and easy way to look at a video and add real time labels to a csv file in the form: 
* Single label mode: ```vid_name, t_start, t_finish, action, action_id```
* Noun/Verb mode: ```vid_name, t_start, t_finish, verb, verb_id, noun, noun_id```

The GUI can be applied to any labelling problem via the use of a csv containing the desired classes - see running the GUI.


# Installation 
* Clone directory
  * ```git clone yada```
* Move to directory and (optionally set up a virtual environment)
  * ```cd action_labeller```
* Install required Python packages
  * ```pip install -r requirements.txt```
* Install and add ffmpeg to environment path:
  * video decoding is done with ffmpeg via the command line.
  * Instructions to set up ffmpeg on windows machine can be found here: ```https://video.stackexchange.com/questions/20495/how-do-i-set-up-and-use-ffmpeg-in-windows```
  
# Running the GUI:
* The GUI is openeD via the main.py python script and can either operate in single label mode or verb,noun (two label) model via the two_label boolean:
```python
python main.py --two_label True --video_path VIDEOPATH --label_csv CSV_FILE_OF_LABELS --verb_csv CSV_OF_VERBS --noun_csv CSV_OF_NOUNS 
```

```python
python main.py --two_label Flase --video_path VIDEOPATH --label_csv CSV_FILE_OF_LABELS --classes_csv CSV_OF_CLASSES
```
  * Arguments:
    * two_label - Boolian, if True operate in verb,noun mode (will require a path to a verb and noun csv)
    * video_path - The path to the video to be labelled, currently supports video formats supported by ffmpeg (only tested on .avi)
    * label_csv - Path to the csv file where annotations will be added to. The GUI is set to append to this CSV so wont delete any labels already exiting within the file.
    * classes_csv - Path to csv file containing desired classes for annotations. First column should contain the id of the label (starting at 0) with the second column containing the class as a string
    * verb_csv - Path to csv file containing desired verb classes for annotations.
    * noun_csv - Path to csv file containing desired noun classes for annotations.
  
  
# Using the GUI:
