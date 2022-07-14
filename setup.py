import os 


# install python packages necessary
os.system('pip install webdriver-manager')
os.system('pip install bs4')
os.system('pip install parsel')
os.system('pip install tldextract')
os.system('pip install pandas')
os.system('pip install selenium')

# open a text file and ask user for their username and password
filename = 'data/linkedin_account.txt'
with open(filename, "w") as f:
  f.write(input("What is your linkedin username? "))
  f.write("\n")
  f.write(input("What is your linkedin password? "))

# What companies do you want to source?
print("MAKE SURE TO INPUT YOUR COMPANIES TO companies.txt!!")