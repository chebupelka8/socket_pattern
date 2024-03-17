```shell
# how to launch server
>>> server

# if you want to launch server with client
>>> server [count clients]
>>> server 3  # server will launch and 3 clients will connect
```

```shell
# if server has already launched and you need to connect some clients use this:
<<<<<<< HEAD
>>> client [coun clients (default=1)]
>>> client 3  # 3 clients will connect to server
=======
>>> clnt [coun clients (default=1)]
>>> clnt 3  # 3 clients will connect to server
>>>>>>> dd0f5f2480773ec3cec8281d20c4e93774213941
```
