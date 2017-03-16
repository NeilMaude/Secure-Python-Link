# Secure-Python-Link

This is a set of tools to allow a calling process to pass credentials 
to a Python script securely.  

Requires Python 3.5.

## Purpose
The motivation for this code is to allow calling of Python scripts 
from within the Arena Group **mstore** EDMS (electronic document 
management system). The EDMS calls the Python script in order to 
perform some action on EDMS data.  To do this, the Python program will
need to log in to the EDMS database (usually Microsoft SQL-Server).
It is not appropriate to pass credentials in plain, nor to store a
username/password in clear within the Python scripts.

Hence the protocol is as follows:

* Create the username/password pairing
* Run the `secure_account()` function to store the user/password
* Record the keys returned
* When calling Python programs pass the keys
* The Python progam recovers the username/password using those keys

This allows the username and password to be held in a persistent file
(a pickle file) and for anyone configuring the calling process to not
have direct database access (just these API-style keys).

_Why not just pass the user/password from the main application at run 
time?_ This would be possible, but the calling application would then 
have credentials all over the place in the configuration (and yes, it
will now have keys all over the place).  However, there's every 
opportunity to (a) centrally store the keys on the **mstore** side and
(b) at some point that process will be cross-machine and so we don't 
want credentials passed in clear over a network.

## Security
It is assumed that a bad actor may have access to the Python scripts 
and even the persistent store of credentials.  These are protected by 
one-time-pad (OTP) encryption (i.e. _perfect_ cryptography).

## Potential attacks
The use of randomly generated OTPs is theoretically _perfect_ security.
However, this does rely on the effectiveness of the random number 
generator. 

The internals of the process do use the last 2 digits of the encrypted
store of the username and password to store the lengthe of the string
which is used. An attacker with source access would know this, but the 
use of an OTP means that every option is equally likely (i.e. no 
useful information can be gained from the the last 2 digits). This did
cause me a few concerns in development and I had to spend a little time
staring at the code to satisfy myself that this (really useful) record
of the length of each string was not making the system crackable.

Note: one way I can think of to break this encryption would be a brute
force attack to find strings of alpha characters which look like a user
name - it's fairly likely that user names will not have non-alpha 
characters. Use of OTP makes every user name equally likely, so there 
is no way to tell which is correct.

A trivial weakness in this process would be if someone used the same
string for the user name and password - in which case the OTPs are
recoverable (this is the same as if the same encryption string was
used to encrypt two plain-text strings - the encryption string is then
directly recoverable). So don't do that...  
