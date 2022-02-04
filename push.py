import requests

API_ENDPOINT = "https://pastebin.com/api/api_post.php"

# Unique API key
API_KEY = "your unique api key after you signup"

# content of the first pastebin post
source_code_1 = '''
list_1 = (1, 1, 2, 3, 5, 8, 13, 21, 34) 
'''

# content of the second pastebin post
source_code_2 = '''
list_2 = (2, 2, 4, 6, 10, 16, 26, 42, 68)
'''

# data to be sent to api
data_1 = {'api_dev_key': API_KEY,
        'api_option': 'paste',
        'api_paste_code': source_code_1,
        'api_paste_format': 'python'}

data_2 = {'api_dev_key': API_KEY,
          'api_option': 'paste',
          'api_paste_code': source_code_2,
          'api_paste_format': 'python'}

# sending post request and saving response as response object
r1 = requests.post(url=API_ENDPOINT, data=data_1)
r2 = requests.post(url=API_ENDPOINT, data=data_2)

# extracting response text

print("The first pastebin URL is:%s" % r1.text)
print("The first pastebin URL is:%s" % r2.text)
