# GEO search, Accession viewer data and metadata with python
## TLDR;
I made this script becouse I wanted to
1. Query stuff from GEO
2. For individual results, manually review some metadata to decide whether it is eligible to use in our study or not.
3. And than write down their Accession numbers in some spreadsheet so that we can find them later.
4. This is faster and more flexible than trying to do it with a browser

This method uses the requests module in python and these two urls:
1. For searching in GEO: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
    + with parameters:
        + params = {
    "db": "gds",
    "term": query,
    "retmax": 1000, 
    "retmode": "json",
    'sort':'SAMPLE_SIZE',
    'order':'descending'
}
2. Geting the metadata from the Accession viewer by the accession number:  
 https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession_number}&targ=self&form=text&view=brief    (note that this is an f string)

## Sample code: *choose_accessions.py* 
You can provide a platform(the id of the device that was used for sequencing) and some search terms at the start of the code. Than gets all the matching Series and their Accession numbers. It than loops around the Accession numbers, prints some metadata(in my case *study design*) and than you can decide whether it is good for you bad for you or you have no idea. Finally it saves these into csv files(good.csv, no_good.csv, maybe.csv )

For now the script doesn't handle SuperSeries so it puts their Accession numbers into another csv file(super_series.csv)