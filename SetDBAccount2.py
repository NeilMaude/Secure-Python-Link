# Set the database account details for this instance
# Neil Maude, Mar 2017

import WorkflowSecurity2

# Run once to set the user name and password

print('Enter credentials to save to file')
print
username = raw_input('Enter user name: ')
password = raw_input('Enter password : ')
filename = raw_input('Enter filename : ')
print
success, user_key, pass_key = WorkflowSecurity2.secure_account(username, password, filename)
if success:
    print('Successfully saved the user/password')
    print('File    : ', filename)
    print('User key: ', user_key)
    print('Pass key: ', pass_key)
    print
    raw_input('Press Enter to close...')
else:
    print('Failed to create keys')
    raw_input('Press Enter to close...')

