# local_news-data_collection

This is a Python web crawler for local news sites.

For each URL listed in `links.txt`, this program generates a PDF of the webpage visited, and produces a TXT file
containing a list of links found on each the webpage.

Requires Python3.7 or higher.

### How to install Python 3 dependencies:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
python3 -m pip install -r ./requirements.txt
```

### Generated PDFs and TXTs

Generated PDFs can be found in `./pdfs` and generated TXTs can be found in `./directory_of_links`, these directories
will be deleted on successive runs of the Python program.
