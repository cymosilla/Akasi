# Akasi for Artemis II
NASA HRP Data Challenge Solo Submission

## About
The purpose is to showcase a variety of methods, both data modeling and analyses, for the upcoming Artemis II crew health data. This is a showcase on quantity and the corresponding components included in the submission delineate how these methods can be interchangeable between the selected proxy datasets.

## Instructions for App
Huge update: Due to the free Streamlit app deployment service, the app is online.

# https://akasihrp.streamlit.app/

Navigate to the link to see the Dashboard! 

### Offline Instructions

Note: Raw data contains the set downloaded from the internet already. The raw data was not manipulated outside of deleting the photos folders from every subject in CGMacros, which are not utilized in this project.

1. Clone this repo.
2. In the command-line terminal, type or paste in the following two lines:
    cd Akasi
    python streamlit_app.py

## Common Errors
- If the .csv is open when rerunning the Python analyses files, a large error pops up. It is most likely that the user will need to close the .csv window & rerun the command.
- The age range slider works until reaching age 33. 

## Dependencies
Python 3.14
Pandas
Pathlib
Plotly
Numpy
Matplotlib
Streamlit 
statsmodels
scikit

The point of all these dependencies was to learn more about their features & how they differ. 

For installing them, I utilized Anaconda, created a new conda environment "Akasi", and ran the commands in the next section from there. 

## Datasets included
NHANES CDS
PhysioNet
UTM 1, 3, 11 Campaigns

## How this is structured
data                Holds all databases
    compressed      Compressed folders of the data [In case GitHub does not allow large file size uploads]
    preprocessed    Contains .py files for preprocessing data as necessary to .csv or HDF5
    raw             Extracted unedited data
    sample          Chosen sample data closely aligning with astronaut demographics

pages               Streamlit page UI & Ployly graphs

img                 Images utilized for the README & examples

src - Source code
    analysis        Analysis after preprocessing
    config          yaml files 
    models          Machine Learning, in case I have the time
    preprocessing   Raw data converted into formats readable for all
    ui              Streamlit UI for easier user viewing

## Methods
This is explained more in Component 1 of my submission, but for a brief summary, this project aims to combine preexisting models and analyses methods with unknown variances of data. This is done through time series and Baynesian modeling. 

## Personal Notes
While I have dealt with preprocessing & simulations before, I was only programming preprocessing files & not the models or the statistics themselves within ice sheets and heat. This was a new venture for me & I wanted to learn as much as I can. One day, I'd like to expand on this project & make it more comprehensive, starting with obtaining other datasets and modeling those to expanding to a human model where variables from models affect each other into a whole human model, like the Earth System Model (ESM). If there are any opportunities that arise in that regard, I would love to take them on, especially now after May when I am most available. Otherwise, I'd like to request permission to try expanding this project outside of the competition (afterwards, of course).

## Akasi Origin
Akasi is the name of the god of health and sickness in Sambal tradition. Heavily revered alongside the central Malyari, he was both feared and revered for his magnificent powers. Sambal refers to the linguistic group from the Zambales province of the Philippines.

Not much is known about him; only a few websites and a book from 1969 were written with him being mentioned alongside the more prominent Malyari. I chose this name because there are a lot of unknowns even with the advances of modern-day medicine; it's like exploring the dark side of the Moon. In typical NASA fashion, I also tried creating an acronym out of it, but settled on keeping the namesake for representation.