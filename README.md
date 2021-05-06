# Overview 
The Application implements web scraping articles' titles and links from rss pages of Polish news websites. It runs every hour and updates a database with the articles.  

# TimerTrigger 

The function is triggered at minute 0 past every hour from 7 through 21 UTC (9 through 23 in the Polish Time Zone) 

# Storing Secrets in Azure Key Vault 

For security reasons connection string to mongodb cluster, database name and collection name are stored in an azure keyvault.

# Resources 

To use this project you will need to:
* Create a mongodb cluster 
* Set up a database with articles using this script: 

```python
import pymongo
from pymongo import MongoClient

cluster = MongoClient(<connection_string_to_the_cluster>)
db = cluster[<cluster_name>]
collection = db[<collection_name>]

sources = ['https://tvn24.pl/najwazniejsze.xml', 'https://krytykapolityczna.pl/feed/', 'https://oko.press/feed/',
           'https://wydarzenia.interia.pl/feed', 'https://dorzeczy.pl/feed/kraj/',
           'https://www.polsatnews.pl/rss/wszystkie.xml', 'https://www.wprost.pl/rss']

source0 = {"_id": 0, "name": "tvn24.pl", "articles": []}
source1 = {"_id": 1, "name": "krytykapolityczna.pl", "articles": []}
source2 = {"_id": 2, "name": "oko.press", "articles": []}
source3 = {"_id": 3, "name": "wydarzenia.interia.pl", "articles": []}
source4 = {"_id": 4, "name": "dorzeczy.pl", "articles": []}
source5 = {"_id": 5, "name": "polsatnews.pl", "articles": []}
source6 = {"_id": 6, "name": "wprost.pl", "articles": []}

collection.insert_many([source0, source1, source2, source3, source4, source5, source6])
```
* Create an azure keyvault to store connection data to the mongodb database (cluster connection string, database name and collection name) 
* Switch on your Azure Function's identity 
* Add access policy for your Azure Function to the keyvault (Secret permissions -> Get, List, then select your Azure Function as a principal) 
add 3 Application Settings in your Azure Function  (CLUSTER_NAME, DATABASE_NAME, COLLECTION_NAME, their values should point to the secrets' addresses in your keyvault 
@Microsoft.KeyVault(SecretUri=<path_to_the_secret>))
