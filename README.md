# HCA ingest accession service

Scripts for metadata accessioning 
 
To run scripts locally you'll need python 2.7 and all the dependencies in [requirements.txt](requirements.txt).


```
pip install -r requirements.txt
```

# CLI application 
## Accession service

This script listens for messages from ingest API messaging queue and assigns accession number for each metadata created in the ingest service

```
python accession-app.py
```

