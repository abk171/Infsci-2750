from cassandra.cluster import Cluster
import hashlib
import json
class Server:
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.merkle_tree = None
        self.keyspace = "project3"  # keyspace(database) name for storing data
        self.table = "data" # table name for storing data

        # Create keyspace and corresponding table
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS " + self.keyspace + " WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};")
        self.session.set_keyspace(self.keyspace)
        self.session.execute(f"CREATE TABLE IF NOT EXISTS {self.table} (key text PRIMARY KEY, value text);")


    # Use insert syntax to add new key value pair to the target table
    def add_data(self, key, value):
        """
        Add a new key-value pair to the data table in Cassandra.
        """
        # Hash the value
        value_hash = hashlib.sha256(value.encode()).hexdigest()

        # Insert the key-value pair into the table
        query = f"INSERT INTO {self.table} (key, value) VALUES (%s, %s);"
        self.session.execute(query, (key, value_hash))

    def get_data(self, key):
        """
        Retrieve a value from the data table in Cassandra, given a key.
        """
        # Query the table for the value
        query = f"SELECT value FROM {self.table} WHERE key=%s;"
        result = self.session.execute(query, (key,))

        # If a result was found, return the corresponding value
        if result:
            value_hash = result[0].value
            return value_hash
        else:
            return None