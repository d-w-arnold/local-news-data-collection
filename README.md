# Local News Data Collection Tool

This is a Python web crawler for local news sites.

Requires Python3.7 or higher.

There are two versions of this program, both versions initially produce TXT files containing a list of links found on the webpages at each URL listed in `links.txt`.

The 'simple' version then visits each URL listed in `links.txt`, and generates a HTML file for each webpage visited.

The 'all' version then visits each URL listed in `links.txt`, generates a HTML file for each webpage visited, and also visits each URL found on each webpage and generates a HTML file for each of those webpages too.

### How to run via Bash script:

```bash
# For 'simple' version of the Python 3 program
bash run_data_collection.sh simple

# For 'all' version of the Python 3 program
bash run_data_collection.sh all
```

### How to install Python 3 dependencies:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
python3 -m pip install -r ./requirements.txt
```

### How to run in Python 3:

```bash
# For 'simple' version of the Python 3 program
python3 main.py simple

# For 'all' version of the Python 3 program
python3 main.py all
```

### Generated HTMLs and TXTs

Generated HTML files can be found in `./htmls` and generated TXTs can be found in `./list_of_links`, these directories will
be deleted on successive runs of the Python program.
