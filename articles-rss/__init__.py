import datetime
import logging
import os 
import azure.functions as func

import requests
import bs4
import pymongo


class Scraper: 

    def __init__(self, cluster_name, database_name, collection_name):
        # setting connection to database 
        cluster = pymongo.MongoClient(cluster_name)
        db = cluster[database_name]
        self.collection = db[collection_name]

        # headers for requests
        self.req_headers = {'User-Agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def get_articles(self):
        for source in self.collection.find({}, {"name": 0, "defaultAssignment": 0, "articles": 0}):
            try:
                res = requests.get(source['url'], headers=self.req_headers)
                res.raise_for_status()
                source_object = bs4.BeautifulSoup(res.text, features="html.parser")
                articles_object = source_object.select('item')
                articles_data = []

                for j in range(7):
                    title = articles_object[j].select('title')[0].getText()
                    link = articles_object[j].select('guid')[0].getText()
                    articles_data.append({"title": title, "link": link})
                self.collection.update_one({"_id": source['_id']}, {"$set": {"articles": articles_data}})
            except Exception as exc:
                logging.info(f"error: {exc}")


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    cluster_name = os.environ["CLUSTER_NAME"]
    database_name = os.environ["DATABASE_NAME"]
    collection_name = os.environ["COLLECTION_NAME"] 
    
    scraper = Scraper(cluster_name, database_name, collection_name)
    scraper.get_articles()

