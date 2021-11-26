## Data Classes

This classes are [Python data classes](https://docs.python.org/3/library/dataclasses.html). They store the data used by the application.

> ⚠️ Python 3.7 and above is required because this is the starting version that supports data classes.

## Issue

Contains data for an issue.

| Attribute      | Description                                    |
| -------------- | ---------------------------------------------- |
| `id`           | Issue id.                                      |
| `user_id`      | (Encrypted) the user id that posts the issue.  |
| `category`     | Issue category.                                |
| `status`       | Issue status.                                  |
| `title`        | Issue title.                                   |
| `desc`         | Issue description.                             |
| `upvotes`      | (Encrypted) user ids that upvotes the issue.   |
| `downvotes`    | (Encrypted) user ids that downvotes the issue. |
| `redressal_id` | The redressal for this issue.                  |
| `created_at`   | When the issue was created in POSIX timestamp. |

## Redressal

Contains data for a redressal.

| Attribute    | Description                                        |
| ------------ | -------------------------------------------------- |
| `id`         | Redressal id.                                      |
| `item_ids`   | `RedressalItem` ids for this redressal.            |
| `upvotes`    | (Encrypted) user ids that upvotes the redressal.   |
| `downvotes`  | (Encrypted) user ids that downvotes the redressal. |
| `created_at` | When the redressal was created in POSIX timestamp. |

## RedressalItem

Contains data for a redressal progress.

| Attribute    | Description                                        |
| ------------ | -------------------------------------------------- |
| `id`         | Redressal item id.                                 |
| `message`    | The progress message.                              |
| `signed_by`  | (Encrypted) admin user id that posts the progress. |
| `created_at` | When the progress was posted in POSIX timestamp.   |

## User

Contains data for an account.

> Email and password storage is handled by Firebase Authentication

| Attribute     | Description                                                                          |
| ------------- | ------------------------------------------------------------------------------------ |
| `id`          | Firestore document id. Use `uid` instead.                                            |
| `uid`         | The user's id. This is the same as the one shown in Firebase Authentication console. |
| `is_admin`    | `true` if this is an admin user.                                                     |
| `category`    | Issue category that this account is responsible for. This is `null` for public user. |
| `voted_items` | Issue and redressal ids that this account has voted for.                             |
