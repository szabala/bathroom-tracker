# Name to be determined
*if you are from my work, please don't read this, it's not for you*

Welcome! This project is a half-joke, half-serious endeavor to track the... disposals... of a group of friends over the course of a year. We use a WhatsApp group chat as our data source.

## How It Works

We have a Python script, [`processing.py`](processing.py), that reads an export of our WhatsApp group chat and counts the occurrences of specific emojis per person. The emojis we track are defined in the `EMOJIS_TO_TRACK` variable. The script only counts emojis sent by users listed in the `VALID_USERS` set.

The script then saves the counts to a CSV file in the `data/` directory.

We also have a Jupyter notebook, [`plotting.ipynb`](plotting.ipynb), that reads the CSV file and generates various plots to visualize the data. The notebook uses libraries like pandas, matplotlib, seaborn, and calmap to create these visualizations.

## Running the Project

To run the project, you'll first need to run `processing.py` to generate the CSV file. Then, you can open `plotting.ipynb` in Jupyter Notebook to generate the plots.

Please note that this project is intended for fun and is not meant to be taken too seriously. Enjoy!