from pyfiglet import Figlet
from replit import db
import time
import random

figlet = Figlet()

print(figlet.renderText('SONG GUESSING GAME'))
print(
    'VERSION 1.0\n\n\nYou\'re given the first letter of a song and the artist. Can you name the artist and the song?. And yea.'
)

users = db["users"]

loggedIn = False

currentUser = None
currentUserIndex = 0


def startLoginFlow(isSessionStart):
  if isSessionStart:
    msg = '\nWelcome. Please log in or sign up to start.'
  else:
    msg = '\nWelcome back. Please log in again or sign up to continue.'

  print(msg)

  userInput = input('Type s to sign up or anything else to log in: ').lower()

  if userInput == 's':
    if signup():
      return True
  else:
    if login():
      return True


# sign up the new user - including CLI signup flow.
def signup():
  global currentUser
  print(figlet.renderText('\nSign up'))

  def checkIfUserExists(uname):
    for i in users:
      if i['name'] == uname:
        return True

  name = input("Enter a name: ")

  while checkIfUserExists(name):
    print(
        '\n❌ A user already exists with this name. Please choose another name.'
    )
    name = input('Enter a name: ')

  password = input("Enter a password: ")
  passwordConfirm = input('Confirm your password: ')
  while passwordConfirm != password:
    print('\n❌ Passwords do not match. Please try again.')
    passwordConfirm = input('Confirm your password: ')

  newUser = {'name': name, 'password': password}
  currentUser = newUser
  users.append(newUser)
  db['users'] = users
  print('✅ Successfully signed up. You\'re now logged in!')
  return True


# log in the user - including login CLI flow.
def login():
  global currentUser, currentUserIndex, users
  while loggedIn is not True:

    print(figlet.renderText('\nLog in'))

    name = input("Enter your name: ")
    password = input("Enter your password: ")

    index = -1
    for user in users:
      index += 1
      if user["name"] == name and user["password"] == password:
        currentUser = user
        currentUserIndex = index

        if 'passwordChange' in user and user['passwordChange']:
          print(
              '\n🔐 Your password was reset by admin and must now be changed.\n'
          )
          if changePassword(True):
            users[index]['passwordChange'] = False
            currentUser = users[index]
            db['users'] = users

        currentUser = user
        currentUserIndex = index

        print('\n✅ Login successful')

        return True
    if input(
        "\n❌ Invalid username or password - enter to try again or type s to sign up instead. "
    ).lower() == 's':
      print('\n\n')
      return signup()


# log out the user and redisplay the login CLI flow
def logout():
  global currentUser, currentUserIndex
  currentUser = None
  currentUserIndex = 0
  print('\nSuccessfully logged out.')

  if startLoginFlow(False):
    if currentUser is not None:
      print('Welcome to the game, ' + currentUser['name'] + '!')
    mainMenu(True)


# delete the user's account
def deleteAccount():
  global users
  if currentUser is not None:
    if currentUser['name'] != 'viggo1':
      users.pop(currentUserIndex)
      db['users'] = users

      return True
    else:
      print(
          '\n❌ You cannot delete your account, viggo1, as you are the administrator.\n'
      )
      return True


# change password
def changePassword(noAbort):
  global currentUser, users
  while True:
    if currentUser is not None:
      password = input('Type a new password: ')
      passwordConfirm = input('Confirm your new password: ')
      while passwordConfirm != password:
        if noAbort:
          print('\n❌ Passwords do not match. Please try again.\n')
          passwordConfirm = input('Confirm your new password: ')
        else:
          if input(
              '\n❌ Passwords do not match. Press enter to try again or type x to abort. '
          ).lower() != 'x':
            passwordConfirm = input('Confirm your new password: ')
          else:
            break

      currentUser['password'] = password
      users[currentUserIndex] = currentUser
      db['users'] = users
      print('\n✅ Password changed successfully.')
      return True


# change name
def changeName():
  global currentUser, users
  nameNotChanged = True

  while nameNotChanged:
    newName = input('\nType a new name: ')
    if newName != '' and currentUser is not None:
      nameUsed = False
      for user in users:
        if user['name'] == newName:
          nameUsed = True

      if nameUsed == False:
        currentUser['name'] = newName

        users[currentUserIndex] = newName
        db['users'] = users
        nameNotChanged = False
      else:
        print('\n❌ This name is already in use. Please use a different one.\n')


# show the admin menu (for viggo only)
def adminMenu(showTitle):
  global users

  if showTitle:
    print(figlet.renderText('ADMIN MENU'))

  menuText = "Select an option by typing its letter.\n\nUSER CONTROL\n📋 l - List all usernames\n🗑️ d - Delete a user\n+ c - Create a new user\n🔐 p - Reset a user's password\n💥 x - Delete all user accounts (excluding viggo1)\n\n⬅ b - RETURN TO MAIN MENU"

  print(menuText + '\n\n')

  option = input('Please type a letter: ').lower()

  if option == 'd':
    # delete a user
    print('\n🗑️ Delete a user\n')

    incomplete = True

    while incomplete:
      name = input('Please enter the user\'s name: ')
      if name != 'viggo1':
        index = -1
        userDeleted = False
        for user in users:
          index += 1

          if user['name'] == name:
            users.pop(index)
            userDeleted = True
            print('\n✅ The user ' + name + ' has been deleted.\n')
            incomplete = False

        if userDeleted == False and input(
            '\n❌ That user does not exist. Please try again, or type x to abort. '
        ).lower() == 'x':
          incomplete = False
      else:
        if input(
            '\n❌ You cannot delete yourself, viggo1, as your are the administrator. Please try again, or type x to abort. '
        ).lower() == 'x':
          incomplete = False

    print('\nReturning to admin menu\n')
    adminMenu(False)

  elif option == 'l':
    print('\n📋 List of all usernames\n')
    toPrint = ''
    for user in users:
      if user['name'] == 'viggo1':
        toPrint = toPrint + '\n- You, viggo1'
      else:
        toPrint = toPrint + '\n- ' + user['name']

    print(toPrint + '\n')

    print('\nReturning to admin menu\n')
    adminMenu(False)

  elif option == 'p':
    print(
        '\n🔐 Reset a user\'s password\nThe user\'s password will be reset to "password1". When the user next logs in, they will be asked to change it something else.\n'
    )
    notDone = True
    while notDone:
      username = input('Enter the name of the user: ')
      index = -1
      for user in users:
        index += 1
        if user['name'] == username:
          users[index]['password'] = 'password1'
          users[index]['passwordChange'] = True
          db['users'] = users
          print('\n✅ The password of ' + username +
                ' has been reset to "password1".')
          notDone = False

      if notDone and input(
          '\n❌ No user exists with that name. Please try again, or type x to abort. '
      ).lower() == 'x':
        notDone = False

    print('\nReturning to admin menu\n')
    adminMenu(False)

  elif option == 'x' and currentUser is not None:
    print(
        '\n💥 Delete all user accounts (excluding viggo1)\n❗️ DANGER! This action has significant effects on the entire system.\n'
    )

    if input('Are you sure you want to continue? y for yes. ').lower() == 'y':
      users = [{'name': 'viggo1', 'password': currentUser['password']}]
      db['users'] = users

      print('\n✅ All users have been deleted, apart from you, viggo1.\n')

    print('\nReturning to admin menu\n')
    adminMenu(False)

  
  elif option == 'c':
    print('\n+ Create a new user\n')

    def checkIfUserExists(uname):
      for i in users:
        if i['name'] == uname:
          return True

    name = input('Enter their name: ')
    while checkIfUserExists(name):
      if input('\n❌ A user already exists with that name. Please try again, or type x to abort.').lower() == 'x':
        print('\nReturning to admin menu\n')
        adminMenu(False)
        break
      else:
        name = input('Enter another name: ')

    password = input("Enter their password: ")
    passwordConfirm = input('Confirm their password: ')
    while passwordConfirm != password:
      print('\n❌ Passwords do not match. Please try again.')
      passwordConfirm = input('Confirm their password: ')


    users.append({
      'name': name,
      'password': password
    })

    print('\n✅ User successfully created.\n')
    print('\nReturning to admin menu\n')
    adminMenu(False)

  
    

  
  elif option == 'b':
    print('\nReturning to main menu\n')
    mainMenu(True)

  else:
    print('❌ Sorry, that letter is not an option. Please try again.')
    adminMenu(False)


# show the main menu
def mainMenu(showTitle):
  if showTitle:
    print(figlet.renderText('MAIN MENU'))

  menuText = "Select an option by typing its letter.\n\nGAMES\n▶ n - Start a new game\n\nACCOUNT\n🚪 l - Log out\n🔐 p - Change your password\n🗑️ d - Delete your account"
  if currentUser is not None and currentUser['name'] == 'viggo1':
    menuText = menuText + '\n\nADMIN\n♦ a - Open the admin menu'

  menuText = menuText + '\n\n'
  print(menuText)

  option = input('Please type a letter: ').lower()

  if option == 'a' and currentUser is not None and currentUser[
      'name'] == 'viggo1':
    # show the secret admin menu - only if viggo is logged in
    adminMenu(True)
  elif option == 'd':
    # deleted account, logout
    print('\n🗑️ Delete your account\n')
    if input('Are you sure you want to delete your account? y for yes. '
             ).lower() == 'y' and deleteAccount():
      print('\n🗑️ Account deleted. Sorry to see you go!')
      logout()
    else:
      print('\nReturning to main menu\n')
      mainMenu(False)

  elif option == 'p':
    # change password
    print('\n🔐 Change your password\n')
    changePassword(False)
    print('\nReturning to main menu\n')
    mainMenu(False)
  elif option == 'l':
    print('🚪 Logging out...')
    logout()
  else:
    print('❌ Sorry, that letter is not an option. Please try again.')
    mainMenu(False)


if startLoginFlow(True):
  if currentUser is not None:
    print('Welcome to the game, ' + currentUser['name'] + '!')
  mainMenu(True)
