## Part 3: What I would do with real resources

On my laptop, my solution only works if I already have the invoice. It matches a VAT number to a company. With a budget, I would try to do the discovery part.

I think searching company by company on the internet is too slow and it doesn't scale (I saw this when I tried to find the VAT number for a few companies from my sample and I almost never found it). So I would do it the other way around: collect all the pairs (VAT number, company) that already exist on the web, and then match them with Companies House.

**What I would do**

1. Use a big web archive like Common Crawl and look for the word "VAT" followed by 9 digits. This needs a cluster, because the archive is huge.
2. For the companies that are still missing, get their website from a commercial data source and crawl only a few pages (contact, terms, footer). For this I would need proxies, because many sites block crawlers.
3. Match the number to the company, using the company number if the page has it, otherwise name and address (here I would use something like my search.py script).
4. Check everything on the HMRC checker and keep a pair only if the name and address from HMRC are similar to the ones from Companies House. The doubtful ones go to people who check them by hand.

**Cost per company**

I don't have real numbers for this, so these are only guesses. I think it would be somewhere between a few cents and 10 cents per company, mostly for the crawl and the proxies. The HMRC checker is free, but I don't know the limits in production, so that could be the slowest part. I would run a small pilot with a few thousand companies and measure the real cost before saying anything to a customer.

**What I think would break first**

I think the matching, not the crawler. I read that a website can show the VAT number of the parent company, or of another company in the same group. The number is valid on HMRC, but it is not the number of the company we want. The HMRC checker can't see this mistake, because the number exists. This is the "plausible number attached to the wrong company" case from the task. Comparing the name and address from HMRC with Companies House would catch some of them, but not all.

The second problem is coverage. Only the companies that are VAT registered and also write the number online can be found. I can't know how many they are, so I would not promise a percentage to the customer. If a company is "not found", I would mark it as unknown, not as "not registered".

**What I would monitor**

- Every week, take a random sample of the pairs we deliver, check them again and have a person review them. This gives the real precision, and I would do it for each source separately.
- The share of numbers that HMRC doesn't find anymore. If it grows, the data is getting old (companies deregister) or the extraction brings noise.
- How old each record is.
- A small set of companies where I know the answer from another source, to estimate how many I miss.