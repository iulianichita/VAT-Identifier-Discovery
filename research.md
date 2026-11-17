The first thing that caugth my attention was the second reason of why this task is difficult: "not found" means either not registered or I failed. 
When checking a VAT number, the result would be not registered (considered True Negative case) if the VAT number would not exist. When the company has a VAT registration number, but my methods would not find it, that means that I failed (considered False Negative case).

After every sentence was clear for me, I was looking for a dataset of UK companies to test. I used first sample from [companieshouse.gov.uk](https://download.companieshouse.gov.uk/en_output.html). 


First thought: searching the VAT registration number on different websites (bulk web corpora) having the company name is not the solution for sure. In search for a solution, I was thinking that some columns from the downloaded sample might give me some information (maybe a value/part of the value from a column would be part of the VAT registration number or a value from a column is used as a function argument to create the VAT registration number). 

I think the solution is one of these 2:
- having a document with the name of the company/company number and the VAT registration number for that company
- having the algorithm of VAT registration number creation and then check it on HMRC

### First approach: VAT registration number algorithm

Understand how the VAT registration number is created for a company and search for patterns in the process.

For this, I chose a company whose VAT registration number was already known.

---- Row 84 ----
CompanyName : "K" LINE HOLDING (EUROPE) LIMITED
CompanyNumber : 05005018
RegAddress.AddressLine1 : 6TH FLOOR
RegAddress.AddressLine2 : 5 ALDERMANBURY SQUARE
RegAddress.PostTown : LONDON
RegAddress.Country : ENGLAND
RegAddress.PostCode : EC2V 7BP
CompanyCategory : Private Limited Company
CompanyStatus : Active
CountryOfOrigin : United Kingdom
IncorporationDate : 31/12/2003
Accounts.AccountRefDay : 31
Accounts.AccountRefMonth : 3
Accounts.NextDueDate : 31/12/2027
Accounts.LastMadeUpDate : 31/03/2026
Accounts.AccountCategory : FULL
Returns.NextDueDate : 28/01/2017
Returns.LastMadeUpDate : 31/12/2015
Mortgages.NumMortCharges : 0
Mortgages.NumMortOutstanding : 0
Mortgages.NumMortPartSatisfied : 0
Mortgages.NumMortSatisfied : 0
SICCode.SicText_1 : 50200 - Sea and coastal freight water transport
SICCode.SicText_2 : 52220 - Service activities incidental to water transportation
SICCode.SicText_3 : 52241 - Cargo handling for water transport activities
LimitedPartnerships.NumGenPartners : 0
LimitedPartnerships.NumLimPartners : 0
URI : http://business.data.gov.uk/id/company/05005018
ConfStmtNextDueDate : 14/01/2027
ConfStmtLastMadeUpDate : 31/12/2025

(extracted in the processCSV.py)

*** VAT number: *** GB662741528 (on http://www.vat-lookup.co.uk/verify/vat_check.php/VATNumber/GB662741528/CompanyName/K+LINE+HOLDING+%28EUROPE%29+LTD)


There is a validation algorithm for UK VAT registration number:

First there could be 4 formats, GB followed by either:
- standard: 9 digits (block of 3, block of 4, block of 2 – e.g. GB999 9999 73)
- branch traders: 12 digits (as for 9 digits, followed by a block of 3 digits)
- government departments: the letters GD then 3 digits from 000 to 499 (e.g. GBGD001)
- health authorities: the letters HA then 3 digits from 500 to 999 (e.g. GBHA599)

For standard number:
- the first 7 digits are random numbers (according to Wikipedia) and the last 2 digits (named check number) are based on a formula using the first 7 numbers
- the last 2 digits are in the range 00-96 and are derived from a weighted modulus-97 number
- in 2010, the numbers would've ran out, so from November 2009 it is used the '9755' algorithm to determine the check number that added one more step to the existing algorithm
- the formula to check if a VAT number is valid (not if it exists): multiply each of the first 7 digits by its weighting factor (8, 7, 6, 5, 4, 3, 2), sum the results, and then add the check number to the sum. If the result is a multiple of 97 then the VAT number is valid. For the '9755' series, also add 55
- the formula to determine the last 2 digits (the check number): multiply each of the first 7 digits by its weighting factor (8, 7, 6, 5, 4, 3, 2), sum the results, and take the remainder of the sum divided by 97. The check number is 97 minus the remainder (if the remainder is 0, the check number is 00). The '9755' series (since November 2009) adds one more step: subtract 55 from the check number, and if the result is negative, add 97 (equivalent to adding 42 to the original check number)

Sources: https://en.wikipedia.org/wiki/VAT_identification_number, https://www.kmstewart.com/resources/check-vat-number


Test on GB66 27415 28:

- formula to check if this if valid

6*8 + 6*7 + 2*6 + 7*5 + 4*4 + 1*3 + 5*2 = 166
166 + 28 = 194 (2 * 97) => the number is valid

- formula to calculate the last 2 digits (the company was founded before Nov 2009)

48 + 42 + 12 + 35 + 16 + 3 + 10 = 166
166 % 97 = 69
nn (the last 2 digits) = 97 - 69 = 28

I also created a image to easily understand this algorithm with Claude (check [img link]).

This is a way to verify if an existing number is valid, or generating the VAT number is you have the first 7 digits. Sources said that the algorithm of generating the first 7 digits is known by the HRMC and is not public (earlier I said that the forst 7 digits are random numbers, but this is not possible for a computer, there has to be an algorithm, maybe with a seed that creates the illusion of randomness). So, this might be a dead end.


### Second Approach: Lookup Document & Matching Script

Create a new document that associates the company name and company number with the known VAT registration number and create a script to search for a company in that document (matching results despite variations in the company name; the “J Smith Building Services Ltd” and “J. Smith Building Svcs Limited” case)


- another approach - finding existing invoices