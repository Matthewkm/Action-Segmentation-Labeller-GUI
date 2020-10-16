# GUI for Segment Level Annotations for Action Recognition.

This is a simplistic and lightweight GUI implemented in python for producing segment level labels for action recognition in videos. Please note this was created as a little helper GUI for labelling some video data i had - it is provided as is and is a little buggy/rough around the edges, but gets the job done.

The GUI provides a quick and easy way to look at a video and add real time labels to a csv file in the form: 
* Single label mode: ```vid_name, t_start, t_finish, action, action_id```
* Noun/Verb mode: ```vid_name, t_start, t_finish, verb, verb_id, noun, noun_id```

The GUI can be applied to any labelling problem via the use of a csv containing the desired classes - see running the GUI.


# Installation 
* Clone directory
  * ```git clone https://github.com/Matthewkm/Segmentation-Labeler-for-action-recognition.git```
* Move to directory and (optionally set up a virtual environment)
  * ```cd action_labeller```
* Install required Python packages
  * ```pip install -r requirements.txt```
* Install and add ffmpeg to environment path:
  * video decoding is done with ffmpeg via the command line and can be downloaded from https://www.gyan.dev/ffmpeg/builds/. Once downloaded add to the environment path (following https://video.stackexchange.com/questions/20495/how-do-i-set-up-and-use-ffmpeg-in-windows)
  
# Running the GUI:
* The GUI is opened via running main.py and can either operate in single label mode or verb,noun (two label) model via the two_label boolean:
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
    * classes_csv - Path to csv file containing desired classes for annotations.
    * verb_csv - Path to csv file containing desired verb classes for annotations.
    * noun_csv - Path to csv file containing desired noun classes for annotations.
    
  * The classes, verb and noun csv files should all be set up in the following manner: First column containing the id of the label (starting at 0) and the second column containing the class as a string. An example is shown:
  
|             |            | 
|-------------|------------|
| 0      | Laughing       |
| 1   |   Smiling     |
| 2   |   Crying |
| 3   |  Frowning \|

  
# Using the GUI:
When passing a video to the GUI for the first time, it must first be decoded - this is a fairly lengthy process, and depends on video length, resolution, fps etc.
During this process the frames of the video are saved into the data folder. If a video with the same name is passed to the GUI, the already decoded images will be used.

Once the video has been decoded (or a folder with images exists already) the GUI will load a look like the following:



