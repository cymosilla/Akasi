# Akasi for Artemis II
NASA HRP Data Challenge for displaying Artemis II crew's health data

## About
The purpose is to showcase a variety of methods, both data modeling and analyses, for the upcoming Artemis II crew health data. This is a showcase on quantity and the corresponding components included in the submission delineate how these methods can be interchangeable between the selected proxy datasets.

## Dependencies
Python 3.14
Pandas
Pathlib
Plotly
Numpy
Matplotlib
Streamlit 
statsmodels

For installing them, I utilized Anaconda, created a new conda environment "Akasi", and ran the commands in the next section from there. 

## Instructions for App

TODO: Add a script for user to run all analyses
TODO: Add a script for downloading files
TODO: Update .gitignore to include only data/sample folder

1. Clone this repo.
2. Extract Akasi/data/compressed. # XXX: See if this needs to be added or erased before submission.
3. In the command-line terminal, type or paste in the following two lines:
    cd Akasi/ui \
    python app.py
4. If the app produces an error, proceed to the next heading.

## Instructions for Data Analysis
In the case the Streamlit app does not work, this can showcase how to generate the necessary graphs.

## Common Errors
- If the .csv is open when rerunning the Python analyses files, a large error pops up. It is most likely that the user will need to close the .csv window & rerun the command.

## Datasets included
NHANES CDS
PhysioNet
UTM 1, 3, 11 Campaigns

## How this is structured
data                Holds all databases
    compressed      Compressed folders of the data [In case GitHub does not allow large file size uploads]
    processed 
    raw             Extracted unedited data

docs                Components 1, 3-5 from the submission

img                Images utilized for the README & examples

src - Source code
    analysis        Analysis after preprocessing
    config          yaml files 
    models          Machine Learning, in case I have the time
    preprocessing   Raw data converted into formats readable for all
    ui              Streamlit UI for easier user viewing

XXX: Users are expected to download the databases from the original sources. Multiple databases with similar parameters have been utilized. If certain databases cannot be found, this will not obstruct the program from running. However, at least one database per subcategory under the previous heading "Databases included" should be downloaded.

## Methods
This is explained more in Component 1 of my submission, but for a brief summary, this project aims to combine preexisting models and analyses methods with unknown variances of data. This is done through time series and Baynesian modeling. 

## Akasi Origin
Akasi is the name of the god of health and sickness in Sambal tradition. Heavily revered alongside the central Malyari, he was both feared and revered for his magnificent powers. Sambal refers to the linguistic group from the Zambales province of the Philippines.

Not much is known about him; only a few websites and a book from 1969 were written with him being mentioned alongside the more prominent Malyari. I chose this name because there are a lot of unknowns even with the advances of modern-day medicine; it's like exploring the dark side of the Moon. In typical NASA fashion, I also tried creating an acronym out of it, but settled on keeping the namesake for representation.