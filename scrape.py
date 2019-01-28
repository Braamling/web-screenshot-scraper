from highlighter import Highlighter
from urllib.parse import urlsplit
from time import sleep
import requests
import os
import time
import subprocess
import argparse
import random

"""
Create a set of three snapshots from a url.

highligher: Highligher object containing a selenium driver
url: url to use for snapshots
query: string containing the query to highlight
query_id: query id used for storing snapshots
doc_id: document id to use for storing snapshots
"""
def create_snapshots(highlighter, url, query, query_id, doc_id):
    highlighter.prepare(url, wayback=FLAGS.remove_wayback_banner)
    append_log(highlighter.get_final_url(), query_id, doc_id)
    highlighter.store_snapshot("storage/snapshots/{}.png".format(doc_id))
    highlighter.set_highlights(query)
    highlighter.store_snapshot("storage/highlights/{}-{}.png".format(query_id, doc_id))
    highlighter.remove_content()
    highlighter.store_snapshot("storage/masks/{}-{}.png".format(query_id, doc_id), grayscale=True)
    highlighter.close()

def append_log(final_url, query_id, doc_id):
    with open(FLAGS.log_file, 'a') as f:
        f.write("{} {} {}\n".format(query_id, doc_id, final_url))

"""
Convert a url and date to a wayback url.
The closed available wayback machine snapshot url is returned.
If the full path is not available, the url will be stripped to just the domain root.
If the domain root is not available, the url is returned as is.

url: url check at wayback
date: YYYYMMDD string that should be used for retrieving the snapshot
"""
def get_web_link(url, date):
    # Try to get the actual link
    avail, waybackUrl = check_wayback_avail(url, date)
    if avail:
        print(waybackUrl)
        return waybackUrl

    domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))

    # Attempt to get the root domain instead.
    avail, waybackUrl = check_wayback_avail(domain, date)
    if avail:
        print(waybackUrl)
        return waybackUrl

    print(url)
    return url


"""
Check whether a url/date combination is available in the wayback machine.

url: url check at wayback
date: YYYYMMDD string that should be used for retrieving the snapshot
""" 
def check_wayback_avail(url, date):
    waybackUrl = "http://archive.org/wayback/available?url={}&timestamp={}"

    url = waybackUrl.format(url, date)

    json = requests.get(url).json()

    snapshots = json["archived_snapshots"]

    if "closest" in snapshots:
        print("available:", snapshots["closest"]["available"])
        return True, snapshots["closest"]["url"]

    return False, ""

def get_clueweb12_url(clueweb_id):
    return "http://<username>:<password>!@boston.lti.cs.cmu.edu/Services/clueweb12_render/renderpage.cgi?id={}".format(clueweb_id)

""" 
Create a dict with all query id's and their corresponding queries.
"""
def make_queries_dict():
    queries = {}
    with open("storage/TREC/queries", 'r') as f:
        for line in f:
            query_id, query = line.rstrip().split(":", 1)
            queries[query_id] = query

    return queries

"""
Yield doc_id, url pairs for the configured query.
"""
def document_generator():
    with open("storage/TREC/{}_docs".format(FLAGS.query), 'r') as fd:
        with open("storage/TREC/{}_urls".format(FLAGS.query), 'r') as fu:
            for doc_id, url in zip(fd, fu):
                yield doc_id.strip(), url.strip()

"""
Scrape a file with all entries for a specific query. 
"""
def scrape_query_file(query, highlighter):
    global_start = time.time()
    for i, (doc_id, url) in enumerate(document_generator()):
        if not os.path.isfile("storage/masks/{}-{}.png".format(FLAGS.query, doc_id)):
            try:
                start = time.time()
                if FLAGS.get_wayback_url:
                    url = get_web_link(url, FLAGS.date)
                create_snapshots(highlighter, url, query, FLAGS.query, doc_id)
            except Exception as e:
                highlighter.close(driver=False)
                print(e)
                print("failed to retrieve", doc_id, "from url", url)
            sleep(max(0, random.randint(60, 75) - (time.time() - start)))
            print("Elapsed time", time.time() - global_start, "average time", (time.time() - global_start)/(i+1))
        else:
            print("File has already been scraped.") 

"""
Scrape all documents in a file containing the query_id, document_id and url
"""
def scrape_document_file(file, queries, highlighter):
    global_start = time.time()
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            query_id, doc_id, url = line.rstrip().split(" ")
            query = queries[query_id]
            if not os.path.isfile("storage/masks/{}-{}.png".format(query_id, doc_id)):
                try:
                    start = time.time()
                    if FLAGS.get_wayback_url:
                        url = get_web_link(url, FLAGS.date)
                    elif FLAGS.get_render_service:
                        url = get_clueweb12_url(doc_id)
                    print(url)
                    create_snapshots(highlighter, url, query, query_id, doc_id)
                except Exception as e:
                    highlighter.close(driver=False)
                    print(e)
                    print("failed to retrieve", doc_id, "from url", url)
                sleep(max(0, random.randint(60, 65) - (time.time() - start)))
                print("Elapsed time", time.time() - global_start, "average time", (time.time() - global_start)/(i+1))
            else:
                print("File has already been scraped.") 

def main():
    highlighter = Highlighter() 
    queries = make_queries_dict()

    if FLAGS.input_file is not None:
        scrape_document_file(FLAGS.input_file, queries, highlighter)
    else:
        scrape_query_file(queries[FLAGS.query], highlighter)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--query', type=str, default='207',
                        help='The query id to retrieve.')
    parser.add_argument('--date', type=str, default='20120202',
                        help='The date (YYYYMMDD) to aim for while scraping.')
    parser.add_argument('--get_wayback_url', type=str, default="False",
                        help='Select whether the url should be looked up in the wayback machine.')
    parser.add_argument('--get_render_service', type=str, default="False",
                        help='Select whether the url should be looked up in the ClueWeb12 online rendering service.')
    parser.add_argument('--remove_wayback_banner', type=str, default="True",
                        help='Select whether the wayback banner should be removed before taking a screenshot.')
    parser.add_argument('--input_file', type=str,
                        help='Select whether the url should be looked up in the wayback machine.')
    parser.add_argument('--log_file', type=str, default="scrape_logs",
                        help='This file is used to store logs during scraping.')

    FLAGS, unparsed = parser.parse_known_args()
    FLAGS.get_wayback_url = FLAGS.get_wayback_url == "True"
    FLAGS.get_render_service = FLAGS.get_render_service == "True"
    FLAGS.remove_wayback_banner = FLAGS.remove_wayback_banner == "True"
    print(FLAGS)
    main()
