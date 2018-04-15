from sseclient import SSEClient

messages = SSEClient('http://localhost')
for msg in messages:
    print('hit')
    print(msg)