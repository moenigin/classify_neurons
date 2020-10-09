# Neuroglancer tool to classify neurons

## Prerequisites

1. requires [chrome](https://www.google.com/chrome/) and ChromeDriver to be 
installed. For ChromeDriver download and unzip 
the [ChromeDriver](https://chromedriver.chromium.org/downloads) for your 
chrome version and include the chrome driver location in your PATH environment 
variable. 

2. [anaconda](https://www.anaconda.com/distribution/) and git

3. membership in the Google Cloud Project in which the segmentation is stored

## Installation

Create a folder for the proofreading tool and clone the git repository
```
cd <dir_path_to_tool>
git clone https://github.com/moenigin/classify_neurons.git
```
navigate to the proofreading folder and install the downloaded environment.yml,
```
cd .\classify_neurons
conda env create -f cls_neurons.yml
```
