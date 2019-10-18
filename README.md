# LOST Pipeline Zoo 

Collection of pipelines for the web-based annotation framework LOST.

This repository is currently under construction.

## Docs
Everything you need to know about creating your own pipelines is described here:
https://lost.readthedocs.io/en/latest/designers.html

All information about pipeline projects and how to import them can be found here:
https://lost.readthedocs.io/en/latest/all_about_pipelines.html

A documentation for creating own worker containers with Docker and any own dependencies of the scripts will follow soon.


## Pipelines

### lost-example-pipes
The lost-example-pipes folder contains the pipelines contained out of the box in LOST.

#### all_elements
- all_element_pipe: 
This pipeline is an example for all available pipeline elements.

#### instant_export
- export_annos: 
This will read an AnnoTask element and export all annotations at its output.

#### mia
- anno_all_imgs: 
This pipeline selects all images of an rawFile for an annotation task.
- semiauto_kmeans: 
This pipeline selects all images of an rawFile, clusters them using KMeans and CNN features and requests a mia annotation task.
- semiauto_resnet: 
This pipeline selects all images of an rawFile, clusters them using ResNet50 prediction and requests a mia annotation task.

#### no_ai
- mia_all_imgs: 
This pipeline selects all images of a datasource for an MIA annotation task.
- sia_all_tools: 
 This pipeline selects all images of a datasource and requests annotations. All Tools in SIA are allowed.
- sia_multi_label_support: 
This pipeline selects all images of a datasource and requests annotations. Multiple labels per annotation are allowed.

#### sia
- semiauto_yolov3: 
This pipeline selects all images of an rawFile and request annotations using yolov3 predictions.
- sia_all_tools: 
This pipeline selects all images of a datasource and requests annotations.

#### two_stage
- looped_kmeans: 
This pipe represents a two stage annotation process. In a first stage bbox annotations are created and in the second stage this bboxes will be labeled by MIA
- looped_resnet: 
This pipe represents a two stage annotation process. In a first stage bbox annotations are created and in the second stage this bboxes will be labeled by MIA
- semiauto_yolo: 
This pipe represents a two stage annotation process. In a first stage bbox annotations are created and in the second stage this bboxes will be labeled by MIA. Semi Automatic support is achieved using yolo box proposals in first stage and class label for clustering in second stage.