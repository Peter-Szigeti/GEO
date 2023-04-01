# Co-Author: Chat GPT and Copilot
import requests
import re
import pandas as pd
# Set the base URL for the GEO API
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Define your search query
platform = 'gpl16791'
query = f'{platform} AND "lung cancer"* AND treatment NOT ("single-cell") AND 20:10000[Number of Samples]' 

# Set the search parameters
params = {
    "db": "gds",
    "term": query,
    "retmax": 1000, 
    "retmode": "json",
    'sort':'SAMPLE_SIZE',
    'order':'descending'
}

# Send the search request
print("Sending search request...")
response = requests.get(base_url + "esearch.fcgi", params=params)
data = response.json()

# Get the list of data set IDs from the search results
id_list = data["esearchresult"]["idlist"]
print(f"Found {len(id_list)} results.")

# Get the data set metadata for each data set ID
print("Getting data set metadata...")
mylist = [requests.get(base_url + "efetch.fcgi", params={"db": "gds", "id": id, "rettype": "xml"}) for id in id_list]
mylist = [el.content.decode('utf-8') for el in mylist]
print('Done.')

# Get the accession numbers from mylist
accession_numbers = [el.split('\n')[-2].split(' ')[1].split('\t')[0] for el in mylist if len(el.split('\n')[-2].split(' ')) == 3]
# Define a function to retrieve metadata from GEO Accession viewer
get_content = lambda accession_number: requests.get(f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession_number}&targ=self&form=text&view=brief").content.decode('utf-8')
# Some lists for saving my choices
super_series = []
no_good = []
good = []
maybe = []
# Loop through the accession numbers and manually decide whether to use the specific number or not
# Based on some metadata
for accession_number in accession_numbers:
    series_content = get_content(accession_number)
    overall_design = re.findall(r'!Series_overall_design = .*', series_content)[0]
    if overall_design.split('=')[-1] == ' Refer to individual Series\r':
        super_series.append([accession_number, overall_design])
    else:
        print(overall_design)
        inpt = input('g/n: ')
        if inpt == 'g':
            good.append([accession_number, overall_design])
        elif inpt == 'n':
            no_good.append([accession_number, overall_design])
        else:
            maybe.append([accession_number, overall_design])

# Save results
pd.DataFrame(super_series, columns=['Accession Number', 'Content']).to_csv(f'super_series_{platform}.csv', index=False)
pd.DataFrame(no_good, columns=['Accession Number', 'Content']).to_csv(f'no_good_{platform}.csv', index=False)
pd.DataFrame(good, columns=['Accession Number', 'Content']).to_csv(f'good_{platform}.csv', index=False)
pd.DataFrame(maybe, columns=['Accession Number', 'Content']).to_csv(f'maybe_{platform}.csv', index=False)
