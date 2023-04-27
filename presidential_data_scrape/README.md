# Scraping Presidential Speeches
This folder contains the code used to scrape, clean, and store presidential speech data stored by UC Santa Barbara's American Presidency Project.

There are two methods to scraping the data one written in python that is single threaded and then a second multi-threaded version written in Rust. The Rust version was not used during this project out of consideration for the UC Santa Barbara's servers and the wonderful service they provide; I would sugggest not using it as well. The python version has some built in rate limiting that can be easily changed by adjusting the global variables found in `download.py`.

## Getting Started
* Run the `download.py` script and it will start the scraping process.
* Run the `parse.py` script and it will clean all of the scraped data.
* You will find the cleaned data in the `data` folder located in the main directory.

## Index
* `parallel_download` - The Rust version of the scraper. This can be run by running `cargo run` in the directory. Rust must be installed for the command to work.
* `copy_separated_to_html.py` - This was a utility script that was used to rename and organize the data. You should not need this script.
* `download.py` - The python version of the scraper. This script is single threaded and uses rate limits that can be adjusted. The script will store the scraped data in the `data` folder located in the main directory; it will be in its raw html format.
* `map_url_to_slug.py` - This script was used to map the url to the slug. It was used to correct a previous error in the download script. You should not need this script.
* `parse.py` - This script is used to clean the scraped data. The cleaned data will be stored in the `data` folder located in the main directory. In order for this script to work the `download.py` script must be run first.
* `utils.py` - This script contains some utility functions that are used by the `download.py` to parse beautfil soup objects.