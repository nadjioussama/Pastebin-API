import requests

#### this first part get all pastes metadata from the provided login details ####
print("FIRST PART :")
print("#################")

API_ENDPOINT = "https://pastebin.com/api/api_post.php"


# Unique API key (can be retrieved after signing up and visiting https://pastebin.com/doc_api)
API_KEY = "your unique dev key"

# getting the api user key, ie: getting an id that identifies you when using the api by the login provided
LOGIN_ENDPOINT = "https://pastebin.com/api/api_login.php"

login_data = {'api_dev_key': API_KEY,
              'api_user_name': 'your user name',
              'api_user_password': 'your password'}

user_key_request = requests.post(url=LOGIN_ENDPOINT, data=login_data)

API_USER_KEY = user_key_request.text
# print(API_USER_KEY)

# data to be provided to get all pastes from the given user login details
data = {'api_dev_key': API_KEY,
        'api_user_key': API_USER_KEY,
        'api_results_limit ': '10',
        'api_option': 'list'}

r = requests.post(url=API_ENDPOINT, data=data)

print(r.text)




### this part gets the raw pastes from the previous request result ###
print("SECOND PART :")
print("#################")

from bs4 import BeautifulSoup

# save the request result as a BeautifulSoup object to use in the this part
soup = BeautifulSoup(r.content, "lxml")


# parse the result and get only the links
pasteKeys = soup.findAll("paste_key")
pasteKeys = [elem.get_text() for elem in pasteKeys]

pastes = []
API_RAW_ENDPOINT = "https://pastebin.com/api/api_raw.php"

for elem in pasteKeys:
    print(elem)
    data = {'api_dev_key': API_KEY,
            'api_user_key': API_USER_KEY,
            'api_paste_key': elem,
            'api_option': 'show_paste'}
    r = requests.post(url=API_RAW_ENDPOINT, data=data)

    # the api also provides this https://scrape.pastebin.com/api_scrape_item.php?i=UNIQUE_PASTE_KEY as an alternate way to scrape for pro users
    newPaste ={'id': elem,
               'content':r.text}
    
    pastes.append(newPaste)
      

print(pastes)


### the next part is about storing the pulled pastes into an sql database and doing some calculation and pusing it back to pastebin ###
print("THIRD PART :")
print("#################")

import mysql.connector

# i used XAMPP server to start a MYSQL server and changed the config to the following details
# (open xampp, start mysql, click shell and type 'mysqladmin -u root password root')

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "root"
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS myPastes")

cursor.execute("USE mypastes")


cursor.execute("DROP TABLE IF EXISTS pastes")

cursor.execute("CREATE TABLE IF NOT EXISTS pastes (pasteID VARCHAR(255), content VARCHAR(255))")

sql = "INSERT INTO pastes (pasteID, content) VALUES (%s, %s)"

val = [('Peter', 'Lowstreet 4'),
       ('Amy', 'Apple st 652')

]
val = [ (elem['id'], elem['content']) for elem in pastes]

cursor.executemany(sql, val)

mydb.commit()

cursor.execute("SELECT * from pastes")


result = cursor.fetchall()

print(result)


### the final part is creating a new paste from the retrieved pastes
print("FOURTH PART :")
print("#################")

API_ENDPOINT = "https://pastebin.com/api/api_post.php"


# content of the new pastebin post
source_code = ''
for elem in result:
    source_code += "paste id: " + elem[0] + "\n"
    source_code += "paste content:\n" + elem[1] + "\n\n"

# data to be sent to api
data = {'api_dev_key': API_KEY,
          'api_option': 'paste',
          'api_user_key': API_USER_KEY,
          'api_paste_code': source_code,
          'api_paste_format': 'python'}



# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)


# extracting response text

print("The first pastebin URL is: %s" % r.text)

