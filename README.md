# Moral Foundation's Perspective on American Presidents
This repository contains code for collecting presidential speech data, using word embeddings to create dictionaries sensitive to semantic shift, and evaluating presidential moral tendencies using frequency distributions.

## Getting Started
* Collect the data: You can use the presidential_data_scrape folder to scrape and clean presidential speech data.
* Generate Moral Foundation Dictionaries: You can use the moral_foundation_dictionary folder to generate moral foundation dictionaries. These dictionaries improve upon traditional methods historians use by accounting for semantic shift in words over time.
* Evaluate the Presidents: You can use the evaluation folder to evaluate the presidents using the dictionaries generated in the previous step.

## Index
* `evaluation` - This folder contains code to create and store frequency counts and distributions from moral foundation dictionaries and the scraped presidential speeches.
* `moral_foundation_dictionaries` - This folder contains code to generate and test the validity of moral foundation dictionaries. There are some great utility scripts for make vizualizations in this folder.
* `presidential_data_scrape` - This folder contains the code used to scrape, clean, and store presidential speech data stored by UC Santa Barbara's American Presidency Project.
* `experiment_tsne_embedding_plot.ipynb` - This notebook contains an experiment I ran to analyze the difference between politcal parties using document embeddings. The presidential data scraped and cleaned from the `presidential_data_scrape` folder is embedded using a pre-trained RoBERTA model. The embeddings are then reduced to two dimensions using t-SNE and PCA and plotted. The results seem to just display the time disparity in the data, even after calculating the compnent that represents time and transposing the data into the vector plane that is orthogonal to the time component.