# search query
with open('../data/companies.txt', 'r') as f:
    # for each line in the file append to list
    companies = f.readlines()
    companies = [x.strip() for x in companies]


# login credentials
linkedin_credentials = '../data/linkedin_account.txt'
with open(linkedin_credentials, 'r') as f:
    linkedin_username = f.readline().strip()
    linkedin_password = f.readline().strip()

clearbit_key = 'sk_8677c344dfbc76e3b31b68b64fa8f65d'