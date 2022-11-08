# emtmlibpy
## Python wrapper for EMTMLib for EventMeasure

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
assert r == EMTMResult.ok
print(emtm.emtm_version())
```

For a full list of examples look at the [unit tests](https://github.com/AutomatedFishID/emtmlibpy/blob/main/src/test_emtmlibpy.py)

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
