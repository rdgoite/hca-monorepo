[![Docker Repository on Quay](https://quay.io/repository/humancellatlas/ingest-exporter/status "Docker Repository on Quay")](https://quay.io/repository/humancellatlas/ingest-demo)

# ingest-exporter

Component that handles the generation and transmission of DSS bundles from submissions
 
This component listens for submissions on the ingest API messaging queue. When a submission is valid and complete (i.e. all data files have been uploaded to the staging area) a will run to generate the 
bundles and submit them to the HCA datastore. The export service needs the URL of the messaging queue along with the queue name. You can also override the URLs to the staging API and the DSS API.  To see all the argument use the --help argument. 

```
pip install -r requirements.txt
```

```
python export-to-dss.py
```
