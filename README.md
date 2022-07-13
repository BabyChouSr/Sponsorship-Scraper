# Sponsorship-Scraper

## Step zero: clone this repo

```
git clone https://github.com/BabyChouSr/Sponsorship-Scraper.git
```

## Step one: install necessary python packages

```
pip install selenium
pip install parsel
pip install webdriver-manager
pip install pandas
pip install tldextract
pip install bs4
```

## Step two: Place your linkedin information into `parameters.py`

Specifically, change the `linkedin_username` and `linkedin_password` to yours.

## Step three: Place companies you are sourcing in companies.txt

Place each company on a new line.

## Step four: Run LinkedinScraper.py and keep tabs open

LinkedinScraper will create a file called recruiters.csv and permutedEmailsResult.csv. Recruiters.csv is result of webscraping and then permutedEmailsResult is the one that has all the emails generated and gone through different permutations of possible emails.

## Important Notes

Note that with each new run, you should wipe recruiters.csv. Why? Because we append each new row instead of deleting the csv and starting over. So, let's say
you finish sourcing for 5 companies, you should save those results and then add the new companies you want to source.
