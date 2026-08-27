# tls-basics

# Scenario A: Intercepting WITHOUT HTTPS (Plain HTTP)
*  First, let's look at what happens when a website doesn't use encryption.
* Start the Interceptor: Run python interceptor.py in your terminal. Leave it open.
* Simulate the Client Request: Open a second terminal window and simulate an unencrypted HTTP text transmission using Python's raw socket capabilities (or simple curl). Let's use Python to send a plain-text payload directly to our interceptor on port 4444:

# The Result in the Interceptor Terminal:
* Because there is no TLS wrapping the data, the interceptor prints the stream out as plain text:
* Anyone on the network infrastructure can read your password effortlessly.

# Scenario B: Intercepting WITH HTTPS (TLS Enforced)
* Now, let's see what happens if the client wraps the communication inside a TLS layer using an SSL context before sending it over the network.
* Keep your interceptor.py running in the first terminal.
* In your second terminal, let's run a client that enforces a secure TLS context using Python's built-in ssl module, but try to point it at our interceptor port 4444.

# The Result in the Interceptor Terminal:
* Look at your interceptor terminal window now. Instead of seeing password=SuperSecret123, the terminal outputs binary noise:

# Steps to Run
1. Terminal 1: The Backend Server
PowerShell
cd C:\Users\User\Downloads\repos\python-basics\tls-basics\
python backend_server.py
(It should print: [*] Target Backend Server running on port 8080. Ready for data!)

2. Terminal 2: The Interceptor
PowerShell
cd C:\Users\User\Downloads\repos\python-basics\tls-basics\
python interceptor.py
(It will sit silently waiting on port 4444)

3. Terminal 3: The Plain HTTP Client
PowerShell
cd C:\Users\User\Downloads\repos\python-basics\tls-basics\
python client_plain.py
What You Will Observe Instantly
The moment you run Terminal 3, look back at Terminal 2 (Interceptor). You will see the magic happen right in front of you:

Plaintext
================ [ INTERCEPTED TRAFFIC ] ================
b'POST /login HTTP/1.1\r\nHost: mybank.com\r\n\r\npassword=SuperSecret123\r\n'
=========================================================
And your Client Terminal (Terminal 3) will cleanly output:
[Client] Received back: Hello Client

3. Terminal 3: The Plain HTTPS Client
PowerShell
cd C:\Users\User\Downloads\repos\python-basics\tls-basics\
python client_plain.py
What You Will Observe Instantly
The moment you run Terminal 3, look back at Terminal 2 (Interceptor). You will see the magic happen right in front of you:

Plaintext
================ [ INTERCEPTED TRAFFIC ] ================
b'\x16\x03\x01\x02\x00\x01\x00\x01\xfc\x03\x03\xad\x8a\xcf\x91...\x00\x13\x02\x13\x03\x13\x01'
=========================================================


