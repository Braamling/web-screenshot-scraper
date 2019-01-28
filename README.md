## Webpage Snapshot Creator/Scraper 
Implementation by *Bram van den Akker*.

**Note: Before starting, python3, pi3 and firefox are installed.**
#### About
The code in this directory scrapes archive.org's Wayback Machine for a list of specified urls under a certain search query. The scrape will renderer available webpages using the firefox headless browser mode and removes the WebArchive menu using selenium and jQuery. Three snapshots of 1366x1366 will be created in total: i) a snapshot of the website as is. ii) a snapshot of the website with all query words highlighed in red. iii) a grayscale snapshot where only the highlights are visible in black (experimental). The images are stored in `storage/highlights`, `storage/masks` and `storage/snapshots` under their query id and document id.

##### Setup
In most case the setup can be performed by running:

```
sh setup.sh
```

In case for any reason this setup fails, please follow perform the following steps manually and adapt changes based on your system setup.

```
# Install all requirements.
pip3 install -r requirements

# Install geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -zxvf geckodriver-v0.19.1-linux64.tar.gz
rm geckodriver-v0.19.1-linux64.tar.gz
sudo mv geckodriver /usr/bin/geckodriver
```

#### Scaping
The scraper scrapes per query from the `/TREC/` directory. Each query_id and query content should be added to `queries` seperated by a colon (ie. `201:raspberry pi`). Each query should have two files: i) a file containing all document id's named `<query_id>_docs` (`201_docs`) and ii) a file containing all urls named `<query_id>_urls` (`201_urls`). Both file should have aligned document id's and urls. (TODO: these two files should be merged into one.)

Scraping can now be achieved by running the `scrape.py` file with the query id as an argument. 
```
python3 scrape.py --query 201 
```

