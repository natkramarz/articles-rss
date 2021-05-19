# Overview 
The Application web scrapes titles and links to articles from Polish news websites' rss pages. It runs every hour and updates the articles database.  

# TimerTrigger 

The function is triggered at minute 0 past every hour from 7 through 21 UTC (9 through 23 in the Polish Time Zone) 

# Storing Secrets in Azure Key Vault 

For security reasons the connection string to mongodb cluster, database name and collection name are stored in an azure keyvault.

# Resources 

To use this project you will need to:
* Create a mongodb cluster 
* Create a database with articles' sources using this script: 

```python
import pymongo
from pymongo import MongoClient

cluster = MongoClient(<connection_string_to_your_cluster>)
db = cluster[<your_database_name>]
collection = db[<your_collection_name>]

source0 = {"_id": 0, "name": "tvn24.pl", "articles": [], "url": "https://tvn24.pl/najwazniejsze.xml" }
source1 = {"_id": 1, "name": "krytykapolityczna.pl", "articles": [], "url": "https://krytykapolityczna.pl/feed/"}
source2 = {"_id": 2, "name": "oko.press", "articles": [], "url": "https://oko.press/feed/"}
source3 = {"_id": 3, "name": "wydarzenia.interia.pl", "articles": [], "url": "https://wydarzenia.interia.pl/feed"}
source4 = {"_id": 4, "name": "dorzeczy.pl", "articles": [], "url": "https://dorzeczy.pl/feed/kraj/"}
source5 = {"_id": 5, "name": "polsatnews.pl", "articles": [], "url": "https://www.polsatnews.pl/rss/wszystkie.xml"}
source6 = {"_id": 6, "name": "wprost.pl", "articles": [], "url": "https://www.wprost.pl/rss"}

collection.insert_many([source0, source1, source2, source3, source4, source5, source6])
```
* Create an azure keyvault to store connection data to the mongodb database (cluster connection string, database name and collection name) 
* Switch on your Azure Function's identity 
* Add access policy for your Azure Function to the keyvault (set secret permissions to Get and List, then select your Azure Function as a principal) 
* add 3 application settings in your Azure Function (CLUSTER_NAME, DATABASE_NAME, COLLECTION_NAME, set their to the secrets' addresses in your keyvault using 
@Microsoft.KeyVault(SecretUri=<path_to_the_secret>))
