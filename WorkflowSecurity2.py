# Library module for adding Python modules to mstore EDMS with a level of security
# Requirement is to use Python code on the server, without exposing user names/passwords
# Principle is for the calling process (in mstore workflow) to pass application keys
# These application keys are one-time-pad (OTP) strings used to decode the user and password for database connection
# The encrypted user and password are stored in a standard pickle file with the Python modules
# This is safe because the user/password are encrypted and cannot be retrieved, even with access to the Python code
# Note: *MUST* use a separate OTP for each value to be encrypted, or perfect security is broken!
# Neil Maude, March 2017

# WorkflowSecurity2 is the Python2 version - going back a version so that I can use zBar for a demo project

import pickle
from random import randint

VALID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$%&*+=?#@'
OTP_LENGTH = 25

# Function to create a random string of OTP characters of a set length
def random_chars(length=50):
    r_chars = ''
    for i in range(0,length):
        random = randint(0, len(VALID_CHARS)-1)       # Note: does not include len(VALID_CHARS) in range - would error
        r_chars += VALID_CHARS[random]
    return r_chars

# Function to XOR two strings
# Returns a boolean for success/failure, plus the XOR string
def string_XOR(string1, string2):
    fSuccess = False
    output_string = ''
    if len(string1) == len(string2):
        a1 = bytearray(string1, 'utf-8')
        a2 = bytearray(string2, 'utf-8')
        for i in range(len(a1)):
            a1[i] ^= a2[i]
        output_string = a1.decode('utf-8')
        fSuccess = True
    return fSuccess, output_string

# Function to pickle a list
# Assumes that the path is valid
def save_values(pfile, val_list):
    data_pickle = {}
    data_pickle['list'] = val_list
    pickle.dump(data_pickle, open(pfile, 'wb'))
    return True

# Function to retrieve a pickled list
def load_values(pfile):
    val_pickle = pickle.load(open(pfile, 'rb'))
    val_list = val_pickle['list']
    return val_list

# Function to pad a string with random characters
def pad_string(input_string, required_length):
    if len(input_string) < required_length:
        # string not already long enough
        r_char = random_chars(required_length - len(input_string))
        return input_string + r_char
    else:
        return input_string

# Function to take a string, pad it out, add the string length markers and encrypt it using a supplied key
# Assumes that the plain string is 99 characters or less (i.e. 2 digits)
def encrypt_string(plain_string, required_length, key_string):
    len_plain = len(plain_string)
    len_marker = str(len_plain).rjust(2,'0')
    extended = pad_string(plain_string, required_length-2) + len_marker
    #print(extended)
    success, encrypted = string_XOR(extended, key_string)
    return success, encrypted

# Function to retrieve a string using a supplied key - with management of the original string length
def retrieve_string(cipher_string, key_string):
    success, decrypted = string_XOR(cipher_string, key_string)
    if success:
        # get the length from the end of the string
        len_marker = decrypted[len(decrypted)-2:]
        len_plain = int(len_marker)
        decrypted = decrypted[0:len_plain]
        return True, decrypted
    else:
        return False, 'Failed to decrypt'

# Function to secure a user and password string to an acceptable level of security
def secure_account(user, password, file):
    # encrypt both values, ship out to a file
    user_key = random_chars(OTP_LENGTH)
    pass_key = random_chars(OTP_LENGTH)
    u_success, e_user = encrypt_string(user, OTP_LENGTH, user_key)
    p_success, e_pass = encrypt_string(password, OTP_LENGTH, pass_key)
    if u_success and p_success:
        values_list = [e_user, e_pass]
        if save_values(file, values_list):
            return True, user_key, pass_key
        else:
            return False, '', ''
    else:
        return False, '', ''

def get_account_details(user_key, pass_key, file):
    values_list = load_values(file)
    if len(values_list) == 2:
        u_success, user = retrieve_string(values_list[0], user_key)
        p_success, password = retrieve_string(values_list[1], pass_key)
        if u_success and p_success:
            return True, user, password
        else:
            return False, '', ''
    else:
        return False, '', ''

# Unit testing
# user = 'Neil'
# password = 'SomethingElse'
# file = 'Account1.p'
# success, user_key, pass_key = secure_account(user, password, file)
# print('Keys: ', user_key, pass_key)
# success, name, password2 = get_account_details(user_key, pass_key, file)
# print('Retrieved: ', name, password2)

