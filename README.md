# emtmlibpy
## Python wrapper for EMTMLib for EventMeasure

Is a python wrapper for EMTMLib by SeaGIS

Allthough this python wrapper is free, EMTMLib is not and requires a licence, EMTMLib cannot and must not be distributed with this Python module.

To use you need a copy of `libEMTMLib.so` and valid licence to use it.  Available from https://www.seagis.com.au/


```bash
sudo mv libEMTMLib.so /usr/local/lib
sudo ldconfig
```
## Example: 
```python
import emtmlibpy as emtm
from emtmlibpy import EMTMResult

# Set your licence keys before using the library
r = emtm.emtm_set_licence_keys(
    "XXXXXX-XXXXXX-XXXXX",
    "XXXXXX-XXXXXX-XXXXX"
)
assert bool(EMTMResult.ok)
print(emtm.emtm_version())
```

For a full list of examples look at the [unit tests](https://github.com/AutomatedFishID/emtmlibpy/blob/main/src/test_emtmlibpy.py)

## Example: EventMeasure camera functions

The wrapper exposes the EventMeasure camera functions from EMTMLib 4.10+. These let you
query, save, and load the left/right camera (calibration) of an EMObs. `EMCameraLeftLoad` /
`EMCameraRightLoad` in particular allow you to insert a camera file into an existing EMObs.

First load (or create) an EMObs, then call the camera functions using its ID:

```python
import emtmlibpy as emtm

em_file_id = 0
emtm.em_load_data(em_file_id, "example.EMObs")
```

### Querying camera state

```python
# Checks whether a valid left/right camera is present
left_ok = emtm.em_camera_left_valid(em_file_id)          # bool
right_ok = emtm.em_camera_right_valid(em_file_id)        # bool

# Checks whether the left/right camera is a composite camera
left_composite = emtm.em_camera_left_is_composite(em_file_id)    # bool
right_composite = emtm.em_camera_right_is_composite(em_file_id)  # bool
```

### Saving a camera

```python
# Save the current left/right camera to a camera file
r = emtm.em_camera_left_save(em_file_id, "left.EMCam")   # EMTMResult
r = emtm.em_camera_right_save(em_file_id, "right.EMCam") # EMTMResult
```

### Loading a camera in to an EMObs

```python
# Insert a camera file into the left/right camera of the EMObs
r = emtm.em_camera_left_load(em_file_id, "left.EMCam")   # EMTMResult
r = emtm.em_camera_right_load(em_file_id, "right.EMCam") # EMTMResult
```

The Save/Load functions return an `EMTMResult`. Check for success with
`r == emtm.EMTMResult.ok` (or `EMTMResult(r) == EMTMResult.ok`). `Load` will return
`EMTMResult.failed` if the camera file cannot be read.

## Example: Generate YOLOv5 labels and extract images

The EMObs file and the BRUVS videos need to be in the same directory
```bash
./src/scripts/gen_yolo_training_data.py /home/marrabld/data/test_emobs/emtmlibpy/afid.EMObs -o train
```

Should generate something like 

```bash
.
├── gen_yolo_training_data.py
├── __init__.py
└── train
    ├── classes.txt
    ├── G000048 L_small.m4v_10796.png
    ├── G000048 L_small.m4v_10796.txt
    ├── G000048 L_small.m4v_10913.png
    ├── G000048 L_small.m4v_10913.txt
    ├── G000048 L_small.m4v_10916.png
    ├── G000048 L_small.m4v_10916.txt
    ├── G000048 L_small.m4v_11623.png
    ├── G000048 L_small.m4v_11623.txt
```

```bash
cat test/classes.txt 
__
Lethrinidae_Lethrinus_punctulatus
Lutjanidae_Lutjanus_sebae
```
