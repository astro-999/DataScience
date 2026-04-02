import requests
# r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
# print(r.json()) 
r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(r.json())