# Brain-Slices-Extraction

## Purpose

In this project I am extracting the brain boundaries from the resting state functional magnetic resonance imaging (rs-fMRI) scans

## Objectives

* To extract brain slices from the data set.
* To extract the brain boundary (periphery) from those slices.

## Description

In this project I am working on rs-fmri data. rs-fMRI is a functional magnetic resonance imaging which is done to evaluate the functional connectivity in the brain networks when the patient is in resting state. Patient’s brain evaluation is done based on the blood consumption activations (shown as red clusters) in different regions of the brain. These clusters reflect the changes in brain’s activity which are driven by the active areas of human body. The fMRI data is usually a 4D data and it is further decomposed into spatial independent components (ICs) using MELODIC software. The brain scan images will show the brain changes over a period of time. A patient usually has 100 such images and the red cluster’s locations will differ in all these images based on the current active part of the body.

### Files

* brainExtraction.py - The brainExtraction.py reads all the images (images those end with word “thresh”) from the given data and perform the brain slice extraction and brain boundary extraction.

* test.py -  This file is executed and it will call the functions in brainExtraction.

* testPatient - The test.py reads a folder named ‘testPatient’ and outputs two folders. One folder named “Slices” and another folder named "Boundaries". ‘Slices’ folder will further have ‘N’ number of folders where N is number of images that ends with “thresh”.
