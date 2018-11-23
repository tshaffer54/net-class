<<<<<<< HEAD
# The Story about Ping

Implement a *ping* application using ICMP request and reply messages. You have to use Python's *RAW* sockets to properly send ICMP messages. You should complete the provided ping application so that it sends 5 Echo requests to each RIR (ARIN, RIPE, LACNIC, AFRINIC, APNIC), 1 request every second. Each message contains a payload of data that includes a timestamp. After sending each packet, the application waits up to one second to receive a reply. If the one-second timer expires, assume the packet is lost or the server is down. Report the following statistics for each host:

* packet loss
* maximum round-trip time
* minimum RTT
* average RTT
* RTT standard deviation

## Code notes

You need to receive the structure ICMP_ECHO_REPLY and fetch the information you need, such as checksum, sequence number, time to live (TTL), etc.

This application requires the use of raw sockets. You may need administrator/root privileges to run your program.

When running this application as a root, make sure to use `python3`.

### Functions

* `print_raw_bytes`: auxiliary function, useful for debugging. Takes (received) *packet bytes* as an argument. **Can be used without modifications**

* `checksum`: calculates packet checksum. Takes *packet bytes* as an argument. **Can be used without modifications**

* `parse_reply`: receives and parses an echo reply. Takes the following arguments: *socket*, *request id*, *timeout*, and the *destination address*. Returns a tuple of the *destination address*, *packet size*, *roundtrip time*, *time to live*, and *sequence number*. You need to modify lines between labels **TODO** and **DONE**. This function should raise an error if the response message type, code, or checksum are incorrect.

* `format_request`: formats echo request. Takes *request id* and *sequence number* as arguments. **Can be used without modifications**

0 || 15 ||
---|---|---|---
type | code | checksum
id || sequence


* `send_request`: creates a socket and uses sends a message prepared by `format_request`. **Can be used without modifications**

* `ping`: main loop. Takes a *destination host*, *number of packets to send*, and *timeout* as arguments. Displays host statistics. You need to modify lines between labels **TODO** and **DONE**.

## References

* [socket — Low-level networking interface — Python 3.7.1 documentation](https://docs.python.org/3/library/socket.html)

* [https://sock-raw.org/papers/sock_raw](https://sock-raw.org/papers/sock_raw)

* [TCP/IP Raw Sockets | Microsoft Docs](https://docs.microsoft.com/en-us/windows/desktop/WinSock/tcp-ip-raw-sockets-2)

* [Converting between Structs and Byte Arrays – GameDev<T>](http://genericgamedev.com/general/converting-between-structs-and-byte-arrays/)

* [select — Waiting for I/O completion — Python 3.7.1 documentation](https://docs.python.org/3/library/select.html)

* [How to Work with TCP Sockets in Python (with Select Example)](https://steelkiwi.com/blog/working-tcp-sockets/)

* [select — Wait for I/O Efficiently — PyMOTW 3](https://pymotw.com/3/select/)
>>>>>>> bfded5ec51ed257b76c528efbb65b1383b131eb2
=======
# Tracing the Route

Implement `traceroute` utility.

Language of implementation: any.

Use UDP (preferred) or ICMP (acceptable) socket to send probing messages to the specified host.

Display relevant statistics of the probe.

For you convenience, lines of Python implementation are provided.

## C++

```
g++ --std=gnu++14 traceroute.cpp -o traceroute.out
./traceroute.out example.com
```

## Java

```
javac Traceroute.java
java Traceroute example.com
```

## Python

```
python3 traceroute.py example.com
```

### Functions

* `print_raw_bytes`: takes *packet* as an argument and prints prints all the bytes as hexadecimal values.

* `checksum`: takes *packet* as an argument and returns its Internet **checksum**.

* `format_request`: takes *ICMP type*, *ICMP code*, *request ID*, and *sequence number* as arguments and returns a properly formatted **ICMP request packet** with current time as *data*. This function has to compute the packet's *checksum* and add it to the header of the outgoing message.

* `send_request`: takes *packet* bytes, *destination address*, and *Time-to-Live* value as arguments and returns a new **raw socket**. This function sets the socket's time-to-live option to the supplied value. 

* `receive_reply`: takes a *socket* and *timeout* as arguments and returns a tuple of the **received packet** and the **IP address** of the responding host. This function uses `select` and may raise a `TimeoutError` is the response does not come soon enough.

* `parse_reply`: takes a *packet* as an argument and returns `True` if it is a valid (expected) response. This function parses the response header and verifies that the *ICMP type* is 0, 3, or 11. It also validates the response checksum and raises a `ValueError` if it's incorrect.

* `traceroute`: takes *host* (domain) name as an argument and traces a path to that host. The general approach is to have a big loop that sends *ICMP Echo Request* messages to the host, incrementally increasing TTL value. Each iteration of this loop generates ATTEMPTS (3) messages. There are two possible sources of errors: `Timeout` (response was not received within **timeout**) and `Value` (something is wrong with the response). For each attempts you should do the following:
    1. Format an ICMP Request
    2. Send the request to the destination host
    3. Receive a response (may or may not be a proper ICMP Reply)
    4. Parse the response and check for errors
    5. Print the relevant statistics, if possible
    6. Print the error message, if any
    7. Stop the probe after MAX_HOPS attempts or once a response from the destination host is received

* `main`: takes command line arguments and starts the probe.


## References

* [Traceroute - Wikipedia](https://en.wikipedia.org/wiki/Traceroute)

* [traceroute(8) - Linux man page](https://linux.die.net/man/8/traceroute)

* [Linux Howtos: C/C++ -> Sockets Tutorial](http://www.linuxhowtos.org/C_C++/socket.htm)

* [Socket (Java SE 10 & JDK 10 )](https://docs.oracle.com/javase/10/docs/api/java/net/Socket.html)

* [socket — Low-level networking interface — Python 3.7.1 documentation](https://docs.python.org/3/library/socket.html)
>>>>>>> b4dcf2ac5d4ebfd8148a42b6f8f2c35b6478000b
