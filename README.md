# A new strategy to map landslides with a generalized convolutional neural network
Code repository for https://www.nature.com/articles/s41598-021-89015-8

[![DOI](https://zenodo.org/badge/320126384.svg)](https://zenodo.org/badge/latestdoi/320126384)

The file "M_ALL_006.hdf5" is the trained TensorFlow model.

![](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-021-89015-8/MediaObjects/41598_2021_89015_Fig7_HTML.png?as=webp)
Pre-processing workflow adopted for training of CNN. (A) Systematic tiling of input images with 50% overlap. In this study , a tile size of 224×224 was used as an input to the CNN. The tile size in display is for representation purposes and does not scale to the actual base resolution used in training the CNN. (B) Steps involved in the data-augmentation of input images with their corresponding landslide mask.

![](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-021-89015-8/MediaObjects/41598_2021_89015_Fig8_HTML.png?as=webp)
An overview of proposed U-Net architecture with residual blocks and deep-supervision. The complete description of all the layers in the network is available in Supplementary Figure Folder.
