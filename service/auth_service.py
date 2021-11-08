import re
import requests

# RFC 5322 email pattern
EMAIL_RFC5322 = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


def _is_email(email):
    """Returns `true` if email is valid."""
    return re.match(EMAIL_RFC5322, email) != None


def _is_password_valid(pw):
    """Returns `true` if password is strong enough for Firebase Auth."""
    return len(pw) >= 6


class AuthService:
    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def _create_payload(self, email: str, password: str) -> dict:
        """Returns the response body for sign-in and sign-up.

        Args:
            email (str): The email address.
            password (str): The password.

        Returns:
            dict: The payload.
        """
        return {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

    def _validate_email_password(self, email: str, password: str):
        """Raises `ValueError` exception if the email and/or password does not satisfy
        Firebast Auth's requirement.

        Args:
            email (str): The email address.
            password (str): The password.

        Raises:
            ValueError: If the email and/or password does not satisfy Firebase Auth's requirement.
        """
        if not _is_email(email):
            raise ValueError(f"The email {email} is invalid!")

        if not _is_password_valid(password):
            raise ValueError("Password must be at least 6 characters long!")

    def sign_up(self, email: str, password: str) -> str:
        """Creates a new user account and returns the uid.

        Args:
            email (str): The email address.
            password (str): The password.

        Returns:
            str: The user's uid.
        """
        self._validate_email_password(email, password)

        response = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}',
            data=self._create_payload(email, password)
        )

        # Throw exception if fails
        response.raise_for_status()

        # Return the uid
        return response.json()['localId']

    def sign_in(self, email: str, password: str) -> str:
        """Logins with the email and password and returns the user's uid.

        Args:
            email (str): The email address.
            password (str): The password.

        Returns:
            str: The user's uid.
        """
        self._validate_email_password(email, password)

        response = requests.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}',
            data=self._create_payload(email, password)
        )

        # Throw exception if fails
        response.raise_for_status()

        # Return the uid
        return response.json()['localId']
