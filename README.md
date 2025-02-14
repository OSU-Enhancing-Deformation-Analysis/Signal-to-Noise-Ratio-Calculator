# Signal-to-Noise-Ratio-Calculator

# Description
This tool allows you to input 2 folders of SEM images and compare the signal to noise ratio of both folders.

# Requirements
Python 3.7+
Tkinter
NumPy
OpenCV
Pillow

You can install the dependencies using pip
```
pip install numpy opencv-python pillow
```


# Running the Code
Run the code using this command
```
python SNR_Calculator.py
```

# Preparing SNR Calculation
1. Click Select Folder 1 and navigate to the first folder containing .tif images.
2. Click Select Folder 2 and navigate to the second folder containing .tif images.
   The first .tif from each folder is displayed in the preview panels.
3. Click Start SNR Calculation to open the ROI selection window.
4. Use your mouse to select the region of interest in the displayed image (Folder 1’s first image).
5. Once you select the ROI, the script automatically computes the SNR for each .tif in both folders.
6. A pop-up window shows the average SNR for both folders and indicates which one is higher.

