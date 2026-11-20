### Part 2: Proof of concept

My solution is a tool that uses invoices in order to associate the invoice with the company details from Company House sample. 

To create the invoices sample, I created a script (generateInvoices.py file) to generate these invoices with name variations for different companies. The invoices contain the VAT registration number. 

The match.py script uses search.py file in order to associate the company name/number from the invoice with the Company house data. match.py is not looking for only a 100% match and for every invoice title calculates a similarity score with the existing UK companies ( score = len(q & tokens) / len(q) - 0.1 * len(tokens - q), where q = words in the title we are searching for, tokens = similar words in the company names from Company House sample ). I am looking for scores that are above 0.7, and the row with highest score is returned as the matching result. Also, this script will return the result 'not found' if there is not a similar company name in the sample. There are 3 output files/folders: sample-invoices, matches.csv, and companies_vat.csv. [sample-invoices](./sample-invoices/) contains the generated invoices, [matches.csv](./matches.csv) contains the invoices matched to the Company house records, and [companies_vat.csv](./companies_vat.csv) contains the VAT number extracted from each invoice, together with the company name from Company House.

In practice, this tool will be used on real invoices, so the VAT registration number will be real and it will return a real result on HMRC checker. 

My solution implemented in match.py, search.py scripts returns the right results if the invoices are in pdf format, they contain the name of the company (or a variation of it), or the company number.

A future update for this solution might be searching for other data from the invoice (e.g. address).