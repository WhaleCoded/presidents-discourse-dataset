# Evaluation
This folder contains code to create and store frequency counts and distributions from moral foundation dictionaries and the scraped presidential speeches.

## Getting Started
* You need to have the data from the `presidential_data_scrape` folder in order to run the scripts in this folder, and at least one of the moral foundation dictionaries created from the `moral_foundation_dictionary` folder.
* Run the `evaluate_dynamic_dictionaries.ipynb` to create frequency counts and distributions for the dynamic dictionaries based on the president and date of the speech.
* Run the `evaluate_static_dictionaries.ipynb` to create frequency counts and distributions for all presidents using teh same dictionary. There are a few comman line options for this script; I suggest just using the default options.

## Index
* `clean_dictionary.py` - This script is used to clean the the static dictionaries curated by experts and located in the `raw_all_liwc_dictionaries.csv` file. The cleaned dictionaries will be stored in the `cleaned_all_liwc_dictionaries.csv` file.
* `dataset.py` - This is a utility class used to load and store the presidential data. This class also provides utilities for mapping over the data, filtering, truncating, and getting the length of the data.
* `evaluate_dynamic_dictionaries.ipynb` - This notebook is used to create frequency counts and distributions for the dynamic dictionaries based on the president and date of the speech. This entails filtering the data by year and using the corresponding dictionary to evaluate that data.
* `evaluate_static_dictionaries.ipynb` - This notebook is used to create frequency counts and distributions for all presidents using the same dictionary. There are a few command line options for this script; I suggest just using the default options. 
* `lists.py` - This is a utility script where I keep a few constant variables that are used throughout the project. For example, in this file you will find a list of the names of all the presidents and their corresponding political party.