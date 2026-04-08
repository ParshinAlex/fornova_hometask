# Fornova HomeTask

The aim of this project is to scrape traveloka's page via link: https://www.traveloka.com/en-th/hotel/detail?spec=20-02-2025.21-02-2025.1.1.HOTEL.9000001153383.novotel%20hua%20hin%20cha-am%20beach%20resort%20&%20spa.2 - according to specifications.

## Quickstart

To get the result - please, run:

```bash
python main.py
```

After execution, you will see 2 files in the results folder:

1. **api_response.json** - this file stores data from API request via link https://www.traveloka.com/api/v2/hotel/search/rooms - analysis showed, that all required data is located here
2. **rates.json** - this file is final result of the task, presented in requested format

File **api_response.json** is stored, as it is more stable and convenient to have a file with all required data locally for parsing.

## Structure comments

All code is split into 3 files:

1. **scrape_api_response.py** - here functions for all scraping processes are stored
2. **parse_api_response.py** - here functions for parsing and normalizing data are stored
3. **main.py** - executes the workflow

## Task comments

There were several ambiguities in both scraping and parsing sections. 

Scraping:
1. Requested link for scraping was holding specifications for dates **20-02-2025.21-02-2025** - it seems pretty obsolete, but I have scraped this exact link nevertheless. Possibly, it was required to generate current date, but this was not mentioned in the task.
2. It was required to generate deep_link during the program - I am not quite sure, what was meant here. Possibly, link must have been updated as speculated in p.1.
3. It was requested to use only python library Requests - I couldn't see how it was possible, as the source site actively uses JS to load content. Requests library does not work with JS, so I have used Playwright for scraping. It is not BeautifulSoup, so I hope it still counts.

Parsing:
1. I saw discrepancy between **p. III.B**, where fields were mentioned and **p. IV** - the lists of fields does not match.
2. Regarding field rate_name - I could not see the difference in prices between **Price/room/night** or **Total price** (with matching taxes / without taxes). So this field does not make much sense - I have hardcoded it to **"Price/room/night"**.
3. Regarding field shown_price.rate_name - API gives all possible variants, but we can choose by ourselves, how prices are shown - with or without taxes. So I also hardcoded this value to **"Exclude taxes & fees"**.
4. As all prices are per stay - I parsed 6 fields for prices: **total_price_per_stay**, **shown_price_per_stay**, **taxes_amount** - and same fields, but original ones. This does not really match the requirements, but this is the best logical parse that I could come up with.

## Final comments

Thanks, this was quite an interesting task to work on.