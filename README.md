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
pip install jupyter
pip install tldextract
```

## Step two: Place your linkedin information into `parameters.py`

## Step three: Place companies you are sourcing in companies.txt

## Step four: Run LinkedinScraper.py and keep tabs open

LinkedinScraper will create a file called recruiters.csv

## Step five: Run EmailPermuter.ipynb

EmailPermuter will permute all the names generated from LinkedinScraper with their company to create plausible emails used <br>
The output will be in out/permutedEmailsResult.csv

## Important Notes

Note that with each new run, you should wipe recruiters.csv. Why? Because we append each new row instead of deleting the csv and starting over. So, let's say
you finish sourcing for 5 companies, you should save those results and then add the new companies you want to source.
