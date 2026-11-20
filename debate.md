## Debate topics

### 1. Pointing the checksum at HMRC's checker

The first 7 digits can be anything from 0000000 to 9999999, and for each of them the last 2 digits are decided by the formula. So there are only about 10 million valid numbers for the old series, and a similar amount for the 9755 series. Companies House says there are around 4.2 million live companies and the task says ~2.18 million VAT registrations, so maybe 1 in 10 of the valid numbers actually exists. In theory, I could send all of them to HMRC and it would return the name and address for every real one. This would solve the discovery problem.

I don't think it is a good idea. First, the HMRC checker was made to verify a number you already have, not to download the whole database. I think they have rate limits and terms of use that don't allow this, and even if I didn't get blocked, I would risk losing my access. I didn't check the exact limits, so this is something I would read before saying anything to a customer. Second, even if it was allowed, it takes millions of requests. 


### 2. Keeping the dataset current

Companies register and deregister all the time, so a number that was right last month can be wrong now. I would recheck the numbers on HMRC again and again, and not wait for something to go wrong. Companies that are new or that changed (a new name, a new address, a new status in the Companies House monthly file) would be checked first, and the old ones less often, for example every few months. If HMRC doesn't find a number anymore, I would not delete the record, I would mark it with the date and "no longer registered", because this is also useful information for the customer. I would also keep for every record the date of the last check, so the customer knows how fresh it is.



### 3. Knowing the dataset is wrong at scale

This is hard, because there is nothing complete to compare with. What I would do:
- Check a random sample of the delivered pairs by hand every week and measure how many are wrong. It is slow, but it is the only real measure.
- Check each source separately. If one source has a lot more mistakes than the others, I would stop using it.
- Look at warning signs: the same VAT number attached to many companies (this is suspicious, unless they are in the same group), or the name from HMRC being very different from the name in Companies House.
- Keep a small set where I know the answer from another source (for example from an invoice or a public contract) and see how many of them I find.

The mistake I'm most afraid of is a valid number attached to another company, because HMRC will say "valid" and nothing in the process will warn me. This is why I compare the name and the address, not only the number.



### 4. Sources I wouldn't use in a product

- **vat-lookup.co.uk**: it was the only site I found that gives a VAT number by company name, but it is not secure (http), it has no API and I couldn't find clear terms of use. I don't know where its data comes from, so I wouldn't use it in a product. I used it only to understand the problem.
- **Real invoices**: this data belongs to the customer and to their suppliers. I would use the tool only on the customer's own data, with their agreement, and I would not keep or reuse the invoices for other customers.
- **Anything with a number but no clear source**: if I can't say where a VAT number came from, I can't defend it when a customer asks, so I wouldn't sell it.

Companies House data I would be comfortable with, because it is published by the government for public use.