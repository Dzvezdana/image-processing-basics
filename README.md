# Description

[**processing_gui**](https://github.com/Dzvezdana/image-processing-basics/tree/master/processing_gui)  
Allows the user to apply a filter, add (and removed the added) noise and plot a historgram of an image.  
The following features are implemented:  
Salt and Pepper noise (together or separately)
* Gauss noise
* Median filter
* Mean filter
* Max filter
* Min filter
* High Pass filter
* Low Pass filter
* Histogram plot
* Adjust kernel size
* Adjust pepper value
* Adjust salt value
* Adjust sigma value
* Adjust dilation kernel
* Adjust erosion kernel
* Adjust LPF/HPF/mean filter size
* Remove noise
  
A sample image [cat.jpg](https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/processing_gui/cat.jpg) is provided, but any other image .png or .jpg image can be used.  
  
Execute using:  
```shell
python processing_gui.py
```

**Output**     
<p align="center">
	<img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/processing_gui/gui_image.png">  
</p>

[**hoffman_encoding**](https://github.com/Dzvezdana/image-processing-basics/tree/master/huffman_coding)  

Execute using:  
```shell
python hoffman_coding.py
```

[**morphology_operations**](https://github.com/Dzvezdana/image-processing-basics/tree/master/morphological_operations)  

1. *Eliminate small squares*. Implemented using erosion followed by dilation of a structuring element of 5x5.
2. *Noise filtering*. Implemented using opening followed by closing using 8x8 structuring element.
3. *Boundary extraction*. Implemented by appling erosion on the image using a 5x5 structuring element and then subtracting the eroded image from the original image. A thicker boundary can be obtained by increasing the size of the structuring element.
4. *Blob region filling*. Region filling algorithm was used.
5. *Count all squares in an image*.

Execute using:  
```shell
python morphology_gui.py
```

[**Singular Value Equalization**](https://github.com/Dzvezdana/image-processing-basics/tree/master/SVE)  

Implementation of image equalization based on singular value decomposition. The singular value matrix represents the intensity information of an image. Thus any change on the singular values results in a change of the intensity of the input image. This procedure is carried out using the following steps:  
* convert the image into the SVD domain,  
* normalize the singular value matrix,  
* reconstructs the image in the spatial domain by using the updated singular value matrix.  

Execute using:  
```shell
python SVE.py
```

[**presentation_perspective_transformation**](https://github.com/Dzvezdana/image-processing-basics/tree/master/presentation_perspective_transformation)  

Detects and centers presentation images.

**Output**     
<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/1.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/1_updated.jpg" width="300" /> 
</p>

<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/2.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/2_updated.jpg" width="300" /> 
</p>

<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/3.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/3_updated.jpg" width="300" /> 
</p>

<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/4.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/4_updated.jpg" width="300" /> 
</p>

<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/5.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/5_updated.jpg" width="300" /> 
</p>

<p float="center">
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/6.jpg" width="250" />
  <img src="https://raw.githubusercontent.com/Dzvezdana/image-processing-basics/master/presentation_perspective_transformation/results/6_updated.jpg" width="300" /> 
</p>

Execute using:  
```shell
python perspective_transform.py --img_dir "path_to_image_directory/*.jpg"
```

# Requirements

* Python 2.6 or higher and the following python modules:
	* Matplotlib
 	* OpenCV
 	* NumPy
 	* PIL
 	* SciPy	
 	
You can install them using pip.

Developed on Ubuntu 16.04.

To run it using Python 3x use:
```python
   from tkinter import *
   from tkinter import filedialog
```

instead of:
```python
from Tkinter import *
import tkFileDialog as filedialog
```