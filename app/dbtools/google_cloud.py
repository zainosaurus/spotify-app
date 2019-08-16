import google.cloud.firestore
import google.cloud.exceptions
import time

# Class which takes care of transactions to and from the database (Google Cloud Firestore)
# Represents a Document
class FirestoreRecord():
    # Static field for Google CLoud Firestore client
    CLIENT = google.cloud.firestore.Client()

    # Create a new document with this object's parameters
    # Updates ID if creation is successful
    # returns boolean indicating whether the transaction was successful
    def create(self):
        try:
            params = self.params
            params.update({'created_at': time.time()})
            doc_snapshot = self.collection.add(params, self.id)[1].get()
            # If the previous line does not raise an error, the transaction was successful
            self.id = doc_snapshot.id
            self.params = params
            return True
        except google.cloud.exceptions.Conflict:    # Already Exists
            return False

    # Update an existing document with current object params
    # Returns boolean indicating whether document was updated successfully
    # Raises error if ID is not set (so it is a new record)
    def update(self):
        try:
            params = self.params
            params.update({'updated_at': time.time()})
            self.collection.document(self.id).update(params)
            # If the previous line does not raise an error, the transaction was successful
            self.params = params
            return True
        except google.cloud.exceptions.NotFound:
            return False

    # Save (Create if document is new, update if it exists)
    # Returns instance of this object
    def save(self):
        # TODO fix this code a bit maybe? seems kind of hacky
        if self.update():
            return True
        elif self.create():
            return True
        else:
            return False

    # Find document with the current instance params
    def find(self):
        try:
            if self.id:
                doc = self.collection.document(self.id).get()
            else:
                query = self.collection
                for key, val in self.params.items():
                    query = query.where(str(key), '==', str(val))
                doc = next(query.stream())
            return self.__init__(doc.to_dict(), doc.id)
        except StopIteration:
            return None
        except google.cloud.exceptions.NotFound:
            return None

    # Runs a 'where' query => Same as #find method but returns an iterator
        # Currently not implemented

    # Delete the current document
    def delete(self):
        self.collection.document(self.id).delete()

    # Constructor
    def __init__(self, collection_name, params = {}, id = None):
        self.collection = FirestoreRecord.CLIENT.collection(collection_name)
        self.id = id
        self.params = params