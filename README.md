Console-based anonymous and secure grievance redressal application.

## Table of Contents

- [Motivation](#motivation)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Running the App](#running-the-app)
  - [Creating Admin Users (Optional)](#creating-admin-users-optional)
- [Features](#features)
  - [Public User](#public-user)
  - [Admin User](#admin-user)
- [Design Considerations](#design-considerations)
  - [Anonymous with Responsibility](#anonymous-with-responsibility)
  - [Transparency](#transparency)
  - [Integrity of Grieve and Redressal](#integrity-of-grieve-and-redressal)
- [Development Stack](#development-stack)
- [For the More Advanced](#for-the-more-advanced)
  - [App Architecture](#app-architecture)
  - [Data Structure](#data-structure)

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

### Creating Admin Users (Optional)

Accounts signed up using the application will always be a public user. Admin users are assumed to be created using a different system with higher privilege.

To simulate this creation, manually create the admin accounts from [Firebase console](https://console.firebase.google.com/).

1. Go to your Firebase Auth in your Firebase console
2. Under "Users" section, click "Add user" and enter the credentials
3. Copy the account's UID and go to Firestore Database
4. Inside the "user" collection, add document
5. Add the field `uid` and set it to the account's UID
6. Add the field `is_admin` and set it to `true`
7. Add the field `category` and set it to one of these values: `ADMIN`, `FACILITIES`, `ENVIRONMENT`, `EDUCATION`

## Features

### Public User

#### Post issue anonymously

Public user can specify the details of the issue, set a category to the issue, without worrying that their identity will be disclosed.
![Post issue demo](/docs/post-issue.png)

When posted, the admin user that is assigned to that category will be notified.

#### View, upvote, or downvote issue

Public users can see the list of issues, sorted by the number of votes.
![List issue demo](/docs/list-issue.png)

They can also support the issue by upvoting or downvoting the issue.
![Vote issue demo](/docs/vote-issue.png)

#### View, upvote or downvote redressal

Public user can see the redressal progress of the issue in detail. They can upvote or downvote to express their satisfaction/dissatisfaction.

![Redressal demo](/docs/view-redressal.png)

### Admin User

#### Received targeted issue

Receive only issues that are specific to admin's assigned category. The admin can see the statistics of the issues: how many new pending issues, how many issues are in progress, and any redressal complaints if any.
![Admin notified demo](/docs/admin-notify.png)

#### Handle issue

Make updates to the issue by adding action items or changing the issue status. If issues are deemed as fake, admin can reject the issue.
![Add redressal item demo](/docs/update-issue.png)

If the issue has been redressed before, admin can link it to the relevant past redressal.
![Link redressal demo](/docs/solve-issue-link.png)

### View Redressal Satisfaction

Admin user can list issues that have been redressed and see the public user's votes for the redressal. If the votes shows dissatisfaction, admin user can reopen the issue.
![List redressed issues](/docs/admin-issue-redressed.png)

## Design Considerations

### Anonymous with Responsibility

The system encrypts the user id whenever it needs to be persisted to the database. Also, the system will not display the user id at any point.

Unfortunately, anonymity and accountability is a trade-off. In this case, posting anonymously means that the posted issue can be invalid. To reduce this probability, the following measures are implemented:

- Posts, redressal, and votes can only be created with an account, without disclosing the identity of the account
- Only 1 account is allowed per email address

### Transparency

The public user can see the progress of redressal so that they know the issue is being addressed. This timeline displays the date and time as well as the message from admin.

This also handles the case in which a user posts an issue that has been redressed but nobody knows about it. Admin user will link it to the past redressal, so the user can see that it really has been redressed.

### Integrity of Grieve and Redressal

The system should ensure that both issues and redressal are genuine. This is done by public voting mechanism.

If an issue is invalid, public users can downvote the issue. When there are at least 10 votes and at least 70% of them are downvotes, the system assumes that the issue is invalid. Admin user can then decide if they want to reject the issue.

If an issue is valid but not redressed, public users can upvote the issue. List of issues that the user and the admin see is sorted by the number of votes. Therefore, issues with a lot of upvotes will get the limelight to be noticed by admin. On the other hand, issues with a lot of downvotes will attract more public users to vote, thus, the validity of the issue is more accurate.

If the redressal is invalid or unsatisfactory, public users can downvote the redressal. When there are at least 10 votes and at least 70% of them are downvotes, this will be reported to the admin. The admin can then reopen the issue.

If the redressal is valid, public users can upvote the redressal. This will help other public users to confirm that the issue has been redressed properly.

## Development Stack

The following tech stacks are used.

- [Python cryptography](https://cryptography.io/en/latest/) for cryptographic operations
- [Firebase Auth](https://firebase.google.com/docs/auth) for user authentication
- [Firebase Firestore](https://firebase.google.com/docs/firestore) as the database

## For the More Advanced

### App Architecture

The application uses 3 different layers to separate responsibilities. The following diagram shows the relation between layers.

![App Architecture](/docs/general-diagram.png)

#### Application Layer

This layer is the layer that the user interacts with. It receives interaction from user and receives data from the repository layer.

The entry point of the app is `main.py`. This file will then call `user.py` if the authenticated user is a public user or `admin.py` if the authenticated user is an admin.

#### Repository Layer

This layer receives and sends data from and to Cloud Firestore. It is also the layer for making authentication requests to Firebase Authentication.

For more information on data persisting, see the [the repository subdirectory](/repository).

For more information on authentication, see the [the service subdirectory](/service).

#### Firestore Layer

This layer contains services provided by Firebase.

### Data Structure

The following diagram is the entity relation diagram for this application.

![ER Diagram](/docs/er-diagram.png)

For more information on the entities and their attributes, see the [the data subdirectory](/data).
