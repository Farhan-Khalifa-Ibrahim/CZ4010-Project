## Repository Classes

Repository classes are the classes that call the database. These classes provides all the CRUD operations for the data classes.

> ⚠️ Do **NOT** instantiate the class `FirestoreRepository`. This class is an abstract class.

### Using the Repository

Before instantiating the repository, call the following code to initialize Firebase SDK.

```python
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('service_account.json')
firebase_admin.initialize_app(cred)
```

Next, instantiate the repository according to the data class that you want to interact with.

```python
from repository.issue_repository import IssueRepository

repository = IssueRepository()
```

### CRUD Operations

#### List

Call the `list` method.

```python
repository.list()
```

#### Get by Id

Call the `get` method and pass the id as argument.

```python
repository.get(id)
```

#### Insert/Update

Call the `save` method. The repository will decide on the operation depending on the `id` of the data class. If the `id` is an empty string, insert will be performed. Otherwise, update is performed.

```python
issue = Issue(
    id='',  # New data
    category=FACILITIES,
    status=PENDING,
    title="Red Bus is Slow!",
    desc="Buses are always close to each other. Not efficient!",
)

repository.save(issue)
```

#### Delete

Call the `delete` method and pass the id as argument.

```python
repository.delete(id)
```
