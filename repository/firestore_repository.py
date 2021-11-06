from firebase_admin import firestore
import threading


class FirestoreRepository:
    """
    This class is a base class for repository that interacts with Firestore Database.
    This class is an abstract class, so instantiate one of the subclasses of this class instead.
    """

    def __init__(self, collection_name) -> None:
        db = firestore.client()

        self._items = {}
        """Keys are item ids, values are the items."""

        # Listen to realtime changes of the data
        self.callback_done = threading.Event()
        self.collection = db.collection(collection_name)
        """Reference to the firestore collection."""
        self.collection.on_snapshot(self._on_collection_change())

        # Wait until the first data comes
        self.callback_done.wait()

    def _object_type(self):
        """Returns the object type that the repository is dealing with.

        Raises:
            NotImplementedError: If the subclass does not override this method.
        """
        raise NotImplementedError(
            "Not implemented! Use one of the subclasses of FirestoreRepository and make sure that this method has been overridden.")

    def _on_collection_change(self):
        """
        Creates a callback that handles realtime changes to the data.
        """
        def on_snapshot(doc_snapshot, *_):
            updated = {}

            # Convert firestore docs to objects
            for doc in doc_snapshot:
                item = self._create_from_doc(doc.id, doc.to_dict())
                updated[item.id] = item

            # Update the objects
            self._items = updated

            self.callback_done.set()

        return on_snapshot

    def _create_from_doc(self, id: str, data: dict):
        """Creates the relevant object from the given id and data. This function *MUST* be 
        overridden by the subclass, and should return the corresponding data object.

        Args:
            id (str): The id of the object.
            data (dict): The data of the object.

        Raises:
            RuntimeError: If this function is not overridden.
        """
        raise NotImplementedError(
            "Not implemented! Use one of the subclasses of FirestoreRepository and make sure that this method has been overridden.")

    def list(self) -> list:
        """Returns all the item in the database.

        Returns:
            list: All items in the database.
        """
        return self._items.values()

    def save(self, data):
        """Persists the given data to the database. This operation can be insert or update.
        If the id of the data is empty, insert will be performed. Otherwise, update will be 
        performed.

        Args:
            data : The data to be saved.
        """

        # Make sure that the object is of the correct type.
        if not isinstance(data, self._object_type()):
            raise TypeError(f"Expected instance of type {self._object_type()}")

        firestore_data = data.to_firestore()

        if (data.id == ''):
            # Insert
            self.collection.add(firestore_data)
        else:
            # Update
            self.collection.document(data.id).set(firestore_data)

    def get(self, id: str):
        """Returns the object from the given id.

        Args:
            id (str): The id of the object.
        """
        return self._items[id]

    def delete(self, id: str) -> bool:
        """Removes the object with the given id from the database.

        Args:
            id (str): The object id to be removed.

        Returns:
            bool: `True` if removed. Otherwise, false.
        """

        # Delete if the given id exists.
        if id in self._items.keys():
            self.collection.document(id).delete()
            return True

        return False
