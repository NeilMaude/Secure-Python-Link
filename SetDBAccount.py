# Set the database account details for this instance
# Neil Maude, Mar 2017

import WorkflowSecurity

# Run once to set the user name and password

print('Enter credentials to save to file')
print()
username = input('Enter user name: ')
password = input('Enter password : ')
filename = input('Enter filename : ')
print()
success, user_key, pass_key = WorkflowSecurity.secure_account(username, password, filename)
if success:
    print('Successfully saved the user/password')
    print('File    : ', filename)
    print('User key: ', user_key)
    print('Pass key: ', pass_key)
    print()
    input('Press Enter to close...')
else:
    print('Failed to create keys')
    input('Press Enter to close...')

