from pyfiglet import Figlet
from replit import db
import time
import random

slant = Figlet(font='slant')
figlet = Figlet()

print(slant.renderText('SONG GUESSING GAME'))
print(
    'VERSION 1.0\n\n\nYou\'re given the first letter of a song and the artist. Can you name the artist and the song?.'
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
  global currentUser
  currentUser = newUser
  users.append(newUser)
  db['users'] = users
  print('✅ Successfully signed up. You\'re now logged in!')
  return True


# log in the user - including login CLI flow.
def login():

  while loggedIn is not True:
    print(figlet.renderText('\nLog in'))

    name = input("Enter your name: ")
    password = input("Enter your password: ")

    index = -1
    for user in users:
      index += 1
      if user["name"] == name and user["password"] == password:
        print('\n✅ Login successful')
        global currentUser
        currentUser = user
        global currentUserIndex
        currentUserIndex += 1

        return True
    if input(
        "\n❌ Invalid username or password - enter to try again or type s to sign up instead. "
    ).lower() == 's':
      print('\n\n')
      signup()
      break


# log out the user and redisplay the login CLI flow
def logout():
  global currentUser
  currentUser = None
  print('\nSuccessfully logged out.')

  startLoginFlow(False)


# delete the user's account
def deleteAccount():
  if currentUser is not None:
    users.pop(currentUserIndex)
    return True


# change password
def changePassword():
  if currentUser is not None:
    password = input('Type a new password: ')
    passwordConfirm = input('Confirm your new password: ')
    while passwordConfirm != password:
      print('\n❌ Passwords do not match. Please try again.')
      passwordConfirm = input('Confirm your new password: ')

    global currentUser
    currentUser['password'] = password
    global users
    users[currentUserIndex] = currentUser
    db['users'] = users

    print('\n✅ Password changed successfully.')


# change name
def changeName():
  nameNotChanged = True

  while nameNotChanged:
    newName = input('\nType a new name: ')
    if newName != '' and currentUser is not None:
      nameUsed = False
      for user in users:
        if user['name'] == newName:
          nameUsed = True

      if nameUsed == False:
        global currentUser
        currentUser['name'] = newName
        global users
        users[currentUserIndex] = newName
        db['users'] = users
        nameNotChanged = False
      else:
        print('\n❌ This name is already in use. Please use a different one.\n')


# show the admin menu (for viggo only)
def adminMenu(showTitle):
  if showTitle:
    print(figlet.renderText('ADMIN MENU'))
    
  menuText = "Select an option by typing its letter.\n\nUSER CONTROL\n🗑️ d - Delete a user\n🔐 p - Reset a user's password\n💥 x - Delete all user accounts (excluding viggo1)"

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
          global users
          if user['name'] == name:
            users.pop(index)
            userDeleted = True

          if userDeleted == False and input(
              '\n❌ That user does not exist. Please try again, or type x to abort.'
          ).lower() == 'x':
            incomplete = False
      else:
        if input(
            '\n❌ You cannot delete yourself, viggo1, as your are the administrator. Please try again, or type x to abort.'
        ).lower() == 'x':
          incomplete = False

    print('\nReturning to admin menu\n')
    adminMenu(False)


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
    if input('Are you sure you want to delete your account? y for yes.').lower(
    ) == 'y':
      deleteAccount()
      print('\n🗑️ Account deleted. Sorry to see you go!')
      logout()
    else:
      print('\nReturning to main menu\n')
      mainMenu(False)

  elif option == 'p':
    # change password
    print('\n🔐 Change your password\n')
    changePassword()
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
