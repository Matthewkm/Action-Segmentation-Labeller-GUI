# GUI for Temporally Labelling Action Segments within Video data for use within Action Recognition.

This is a simplistic and lightweight GUI implemented in python for producing segment level labels for action recognition in untrimmed videos.

The GUI provides a quick and easy way to look at a video and add real time labels to a csv file in the form: 
* Single label mode: ```vid_name, t_start, t_finish, action, action_id```
* Noun/Verb mode: ```vid_name, t_start, t_finish, verb, verb_id, noun, noun_id```

The GUI can be applied to any custom labelling problem via the use of custom csv files containing the desired classes - please see running the GUI section.


# Installation 
* Clone directory
   ```git clone https://github.com/Matthewkm/Action-Recognition-Labeller-GUI.git```
* Move to directory and (optionally set up a virtual environment)
   ```cd action_labeller```
* Install required Python packages
   ```pip install -r requirements.txt```
* Install and add ffmpeg to environment path:
  * video decoding is done with ffmpeg via the command line and can be downloaded from https://www.gyan.dev/ffmpeg/builds/. Once downloaded add to the environment path (following https://video.stackexchange.com/questions/20495/how-do-i-set-up-and-use-ffmpeg-in-windows)
  
# Running the GUI:
* The GUI is opened via running main.py and can either operate in single label mode or verb,noun (two label) model via the two_label boolean:

```python
python main.py --mode single --video_path VIDEOPATH --label_csv CSV_FILE_OF_LABELS --classes_csv CSV_OF_CLASSES
```

```python
python main.py --mode duo --video_path VIDEOPATH --label_csv CSV_FILE_OF_LABELS --verb_csv CSV_OF_VERBS --noun_csv CSV_OF_NOUNS 
```
  * Arguments:
    * two_label - Boolian, if True operate in verb,noun mode (will require a path to a verb and noun csv)
    * video_path - The path to the video to be labelled, currently supports video formats supported by ffmpeg (only tested on .avi)
    * label_csv - Path to the csv file where annotations will be added to. The GUI is set to append to this CSV so wont delete any labels already exiting within the file.
    * classes_csv - Path to csv file containing desired classes for annotations.
    * verb_csv - Path to csv file containing desired verb classes for annotations.
    * noun_csv - Path to csv file containing desired noun classes for annotations.
    
 ## Prepping Custom classes and label CSV files:

  * The classes, verb and noun csv files should all be set up in the following manner: First column containing the id of the label (starting at 0) and the second column containing the class as a string. An example is shown:
  
|             |            | 
|-------------|------------|
| 0           | Laughing   |
| 1           | Smiling    |
| 2           | Crying     |
| 3           |  Frowning  |

The directory has 3 example csv files: ```classes.csv```, ```verb.csv``` and ```noun.csv```.
  
 * The labeling csv file used to save the labes should either be in the single or duo format
   * Single Format:

|   Vid_id    |    Start_frame    |  End_frame  |  class  |  class_id  |
|-------------|-------------------|-------------|---------|------------|
| vid_0       | 1228              | 1930        |  Dancing|  32        |

   * Noun-verb (double) format:
   
|   Vid_id    |    Start_frame    |  End_frame  |  verb    |  verb_id  |  noun    |  noun_id  |
|-------------|-------------------|-------------|----------|-----------|----------|-----------|
| vid_0       | 1228              | 1930        |  slowly  |  05       |  Dancing |  32       |

Examples have been put in the directory with the name ```train_labels_single.csv``` and ```train_labels_double.csv```.


  
# User Instructions:
When passing a video to the GUI for the first time, it must first be decoded - this is a fairly lengthy process, and depends on video length, resolution, fps etc.
During this process the frames of the video are saved into a folder within the data folder. If the same video is passed to the GUI (or any video with the same name), the already decoded images will be used.

Once the video has been decoded (or a folder with images exists already) the GUI will load a look like the following:
![demo](https://user-images.githubusercontent.com/43727012/96495406-b68f0d00-123f-11eb-952b-2f32ba2c3113.PNG)

* **Navigating though the video:**
   * The main image shows the current frame of video, with the frame index shown above.
   * Prev/Next button (or the left/right arrow keys) can be used to move to the previous and next frame one at a time.
   * The Play button (and x2, x4 and x8) will automatically play the video (at real time and corresponding sped up speeds) and are stopped using the stop button (The stop button must be used to stop the playing, not repressing the play button)
   * The input box (bottom left) allows you to jump to a desired frame. Simply enter an integer value and click the jump to frame button.
   * Similarly you can drag the progress bar below the image to a desired frame and click the Jump button to skip to that frame.
 
* **Creating a label:**
   * To create a label, first navigate to the start frame of the action.
   * Press the space bar to log the start frame of the action - the Start frame should now display the current frame
   * Navigate to the end of the action using methods outlined above.
   * Press space bar again to log the end frame - the End Frame value should now show the current frame
   * Select the label for the current action using the drop down boxes.
   * Press Enter to add the label to the csv file. A new entry should appear in the table and the csv file will automatically save.
   * At any point in the frame selection process the Esc key can be pressed to delete the current start and end frame selection.
 
 
# Other:
Please note this was created as a little helper GUI for labelling some video as part of my PhD - it is provided as is and is a little buggy/rough around the edges, but gets the job done.
If you've got any suggestions please let me know, and I can potentially add them when i have time, however, please feel free to add features and make a pull request 😊
 
