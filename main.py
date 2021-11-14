import json
import firebase_admin
from firebase_admin import credentials

from data.user import User
from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository, RedressalItemRepository
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from getpass import getpass
from user import user_class


def init_firebase_sdk():
    # Initialize firebase admin SDK
    cred = credentials.Certificate('service_account.json')
    firebase_admin.initialize_app(cred)


def create_auth_service() -> AuthService:
    # Initialize firebase REST api for authentication
    with open('firebase_key.json') as f:
        content = json.load(f)
        api_key = content['apiKey']

    return AuthService(api_key)


def sign_in(auth: AuthService, repo: UserRepository):
    print('Please enter your credentials to sign in.')
    email = input('Email: ')
    password = getpass()

    try:
        uid = auth.sign_in(email, password)
    except Exception:
        print('Failed to login! Make you sure your credentials are correct.')

    # Get the user data
    user = repo.get(uid)

    # Run the main app flow
    if user.is_admin:
        # TODO: Run admin flow
        pass
    else:
        # TODO: Run user flow
        user = user_class(user)
        user.main()
        pass


def sign_up(auth: AuthService, repo: UserRepository):
    print('Please enter your credentials for the new account.')
    email = input('Email: ')
    password = getpass()

    try:
        uid = auth.sign_up(email, password)
    except ValueError as e:
        print(e)
        print()
        return
    except Exception:
        print('Failed to create a new account! Please try again.')
        print()
        return

    # Save the new user data to the database.
    user = User(id=uid, uid=uid, is_admin=False)
    repo.save(user)

    print('Your account has been created. You may now sign in.')


def main():
    init_firebase_sdk()

    auth = create_auth_service()

    # Create the repositories
    issue_repo = IssueRepository()
    redressal_repo = RedressalRepository()
    redressal_item_repo = RedressalItemRepository()
    user_repo = UserRepository()

    while True:
        print('Welcome to the app! Please select your action.')
        print('1. Sign In')
        print('2. Sign Up')
        print('0. Exit')
        action = input('Action: ')

        print()

        if action == '1':
            # Sign in
            sign_in(auth, user_repo)
        elif action == '2':
            # Sign up
            sign_up(auth, user_repo)
        elif action == '0':
            # Quit
            print("Thank you for using our app.")
            break


if __name__ == "__main__":
    main()
