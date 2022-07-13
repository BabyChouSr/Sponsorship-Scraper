# search query
with open('../data/companies.txt', 'r') as f:
    # for each line in the file append to list
    companies = f.readlines()
    companies = [x.strip() for x in companies]


# login credentials
linkedin_username = 'INSERT YOUR USERNAME HERE'
linkedin_password = 'INSERT YOUR PASSWORD HERE'
clearbit_key = 'sk_8677c344dfbc76e3b31b68b64fa8f65d'