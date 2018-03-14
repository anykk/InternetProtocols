# Python3 SNTP server implementation

It was made agreed with [RFC4330](https://tools.ietf.org/html/rfc4330) 

Decomposition:

- In sntp.py was represented SNTPPacket class in accordance with RFC

Interface: from_bytes(data[bytes]) & to_bytes() [constructor takes all field, by default it's configure the client's request]

- In server.py declared the main function, where described the server's logic
- In client.py simple function for tests

Usage:

```
python3 server.py [lie]
```

By default, lie equals to 0, so, it is mean, that server doesn't lie.

#Examples:

##Test our SNTPPacket structure and parse from bytes

![](.\images\req_w.png)

Here we make request and you can see, that all fields are correct (it is default SNTPPacket parameters).

It is string representation of my SNTPPacket class:

![](.\images\resp_c.png)

You can compare it with wireshark's info:

![](.\images\resp_w.png)

##Server test

- With self-made script:

![](.\images\&self_made.png)

- With achron:

![](.\images\&achron.png)

- With non-sntp client:

![](.\images\&non_sntp.png)

You can see, that it still works, but notify about parse exceptions.