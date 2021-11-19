## Motivation

Grieve is a part of everyday life as a human. However, it does not mean that grieve should not be reported, especially if it is harmful to the society. Because everyone has a right to voice out to the one of authority responsibly. Unfortunately, their voices are not always heard or there are not enough attentions received. The main reason is that many voices lacks the power to remain relevant or seen as crucial.

This application is designed to address this problem. We want to make it possible for any user with or without power to voice out their grieves safely and responsibly. Grieves are posted anonymously, and the system will deliver grieves to the corresponding authority. The public can attest to the reported issue by voting. The system also protects the one in authority. They can post issue redressal progress anonymously. If the system perceives that an issue is not genuine, they have the power to reject the reported issue.

## Getting Started

### Requirements

These are the requirements for the project to run.

- [Python](https://www.python.org/) 3.7
- A Firebase project with the following services enabled
  - Firebase Authentication email/password provider
  - Firestore

### Running the App

First, install the required dependencies for this project by running the following command.

```
pip install -r requirements.txt
```

Add the Firebase credential files required in the root folder of this project.

1. [Generate the private key](https://firebase.google.com/docs/admin/setup#initialize-sdk) for your Firebase project and name it `service_account.json`.
2. [Register a web app](https://cloud.google.com/appengine/docs/standard/python3/building-app/adding-firebase#adding_firebase_to_your_web_service) to Firebase. Copy the value of `firebaseConfig` into a json file named `firebase_key.json`.

Finally, run `main.py` to start the application.

```
python main.py
```

## Research

TODO

## Design Considerations

### Anonymous with Responsibility

Issues, redressal, and votes do not display the user.

Responsibility measures:

- Posts, redressal, and votes can only be created if you have account
- Only 1 account allowed per email address

### Transparency

The public user can see the progress of redressal.

Display image of redressal timeline here

### Integrity of Grieve and Redressal

Issues and the corresponding redressal are ensured that they are genuine by public voting.
Post issue -> the public supports your case
Post redressal -> accountability of voting protects your case.

## Development Stack

- Python cryptography library
- Firebase Auth
- Firebase Firestore
