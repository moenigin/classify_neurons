# Usage Instructions

heads-up: the very initial loading of whole cells to the viewer can take its time!

##### The goal is to group neurons into classes based on morphological features.

At the beginning 2 neurons are displayed. The user now has to make the decision 
whether these neurons belong to the same class. If this is the case, this can be 
acknowledged pressing the key "T". A third neuron will load and the user needs 
to decide whether is to be grouped with the first two neurons. 

If a newly loaded cell does not belong to the same class as the other 
cells currently displayed, it can be assigned to a new group by pressing the key 
"N".<br/> 
If it resembles a group of neurons that has been created previously, the 
list of cell classes created can be navigated using the keys "D" to decrement the group 
id and "F" to increment the group id. The current group number and the id of the 
newly loaded neuron are displayed in the message board of neuroglancer in the 
bottom left. 

Neurons that are not yet assigned to a neuron are stored in a list. Newly loaded 
neurons are chosen from this list. This list can also be navigated: 
Pressing key "V" will move downward in the list and key "Q" will move upward in the list.

If a newly loaded neuron needs to be investigated in a bit more detail the 
display of the other neuron can be toggled off and on using key "X".

If it becomes apparent that a class/group of neurons is composed of 2 
subclasses, the group can be divided. To do so, the cells belonging to one of two 
subclasses have to be removed from the viewer. This can be achieved in two ways: <br/>
1. by doubleclicking on the mesh or the segment in the viewer 
[xy or 3D viewport]. <br/> 
2. by control+click on the tab in upper left that is named "segmentation" 
(see below). 
This opens a panel on the right. Under the tab seg. one can find a list of 
segment ids displayed. Checking or unchecking of the box to the left of each id 
can be used to hide or the display the neuron. <br/>

![gui](./data/NG_layerinfo.png)

If only the set of neurons that should be assigned to a new class is displayed,
press "control"+ "P". The next neuron to assign to a group will be automatically 
loaded afterwards.

If a neuron has been wrongly assigned to a group it can be removed from that 
group by isolating it in the viewer (manually deselect all other
cells, see above). Then press control + "]" (SWISS KEYBOARD: control + ".."). 
The neuron will be removed from that group and is placed in the list of neurons 
that are yet unassigned.

Press ctrl+s to save the data.  Data is automatically saved at a time interval 
specified on start, default = 600 sec.

Press ctrl+delete to exit the program. This will automatically save the 
class assignments. The classification can be stopped at any time and with the 
latest assignments being loaded upon restart (not the exact viewer state!). 


## Useful shortcuts 

+ "H" opens the help window which lists full list of neuroglancer functions and 
their key and mouse bindings. Press ESC to close the window.
+ ctrl+click onto the tap holding a particular layer (upper left) will open up 
detail layer information, e.g. the list of segments in the layer 
+ scrolling wheel for zooming in and out in the 3D viewport
+ "L" - recolors the segments
+ right mouse button jumps the viewer location to the position of the cursor
+ space and shift+space to display and hide the raw image and segmentation view

+ "Q": display next neuron to be assigned to a class
+ "V": display previous neuron to be assigned to a class
+ "T": assign neuron to current class displayed 
+ "N": assign neuron to a new group
+ "F": increment the current class number
+ "D": decrement the current class number
+ "Ctrl+]": remove the neuron in the viewer from the class it was assigned to
+ "Ctrl+P": assign all neurons displayed in the viewer to a new group
+ "Ctrl+Delete": exit program

DIFFERENCE IN SWISS KEYBOARD SHORTCUTS
+ "Ctrl+..": remove the neuron in the viewer from the class it was assigned to
