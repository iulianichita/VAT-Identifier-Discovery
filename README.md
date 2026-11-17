# VAT-Identifier-Discovery

A procurement team at a mid-sized manufacturer has 40,000 UK suppliers and pays invoices against them every month. Matching an invoice to a supplier record reliably needs one thing: the supplier’s VAT registration number, the only identifier that appears on both the invoice and the tax record. They have it for about a third of their suppliers. For the rest they match on company name, so “J Smith Building Services Ltd” and “J. Smith Building Svcs Limited” are two suppliers, or one, and nobody knows which.

We would like to sell them the missing two thirds. Nobody sells it, and there is no dataset to buy.

The objective is to determine whether a UK company VAT dataset can be built from the open web, and to prove it on a sample.

What makes this difficult:

- The verifier only runs backwards. HMRC will confirm any VAT number you give it. It will not tell you a company’s VAT number.
- Most UK companies don’t have one. Roughly 4.2 million live companies against ~2.18 million VAT registrations nationally, and that second number includes sole traders. So “not found” means either not registered or I failed, and those are very different results.
- A wrong number costs more than a missing one. A gap is visible. A plausible number attached to the wrong company is invisible, and it corrupts every join the customer makes downstream.
- There is no reference dataset to check yourself against.

***

## Deliverable

**Part 1: Research.** What did you learn that wasn’t obvious at the start? Which sources exist, which are usable, what did you rule out and why? Show the trail, not only the conclusion. For the paths that mattered we want the evidence: what you ran, what came back, the number you got. A claim we can trace to something you actually did counts for more than one we cannot. Write up the dead ends too, and be specific: for each one that mattered, name the source, what you expected, and the exact reason it failed. “Scraping is unreliable” is not a dead end; “this source returns VAT numbers but only for a small share of my sample, and here is the evidence” is. The search matters as much as what you found.

**Part 2: Proof of concept.** Build something that works, on a sample you choose. Tell us how you drew the sample and why it’s representative; a sample of companies you already knew published their VAT number will produce an impressive number and teach neither of us anything. Every number you report as found must be confirmed against HMRC’s checker: state the false-positive rate you measured, how you measured it, and on what sample. Numbers you did not verify do not count. Report what your process achieved and what your numbers don’t capture.

**Part 3: What you’d do with real resources.** You’re on a personal laptop with no budget. We aren’t. Given a cluster, a crawling budget, commercial data sources, proxy infrastructure, an annotation team — whatever the problem actually needs — how would coverage and accuracy change, and how would you get there? Be specific enough that we can argue with you: rough cost per company, what breaks first, what you’d monitor in production. “I’d use a distributed crawler” tells us nothing.