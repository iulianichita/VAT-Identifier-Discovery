### Part 2: Proof of concept

My solution is a tool that uses invoices in order to associate the invoice with the company details from Company House sample. 

In order to obtain an invoice sample, I created a script to generate these invoices with name variations for different companies. The invoice contains the VAT registration number. The script is match.py and it uses search.py script in order to associate the company details. As I said, this script is not looking for a 100% match and for every title calculates a similarity score (score = len(q & tokens) / len(q) - 0.1 * len(tokens - q), where q = words in the title we are searching for, tokens = similar words in the company names from Company House sample). I am looking for scores that are above 0.7, and the row with highest score is return as the matching results. Also, this script will return the result 'not found' if there is not a similar company name in the sample. There are 3 output files/folders: sample-invoices, matches.csv, and companies_vat.csv. [sample-invoices](./sample-invoices/) contains the generated invoices, [matches.csv](./matches.csv) contains the Companies House record matched to each invoice, and [companies_vat.csv](./companies_vat.csv) contains the VAT number extracted from each invoice, together with its company.

In practice, this tool will be used on real invoices, so the VAT registration number will be real and it will return a real result on HMRC checker. 

My solution implemented in match.py, search.py scripts returns the right results if the invoices are in pdf format, they contain the name of the company (or a variation of it), or the company number.

A future update for this solution might be searching for other data from the invoice (e.g. address).