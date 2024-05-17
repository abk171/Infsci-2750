from db_provider import Server
from merkletools import MerkleTools
class DataOwner:
    #init data owner with the key value data
    #specify the server object
    def __init__(self,key_value_data,server,blockchain):
        self.data= key_value_data
        self.server= server
        self.merkle_tree = None
        self.blockchain = blockchain

    #insert data to self.server
    def insert_data_to_server(self):
        for key, value in self.data.items():
            self.server.add_data(key, value)

    def build_merkle_tree(self):
        # Convert values to list of strings
        values = [str(value) for value in self.data.values()]
        # Create MerkleTree object
        self.merkle_tree = MerkleTools()
        # Add leaves to Merkle tree
        self.merkle_tree.add_leaf(values,True)

        # Build Merkle tree
        self.merkle_tree.make_tree()

    def upload_merkle_tree_to_server(self):
        root = self.merkle_tree.get_merkle_root()
        self.server.add_data("merkle_root", root)

        # for i, leaf in enumerate(self.merkle_tree.leaves):
        #     self.server.add_data(f"leaf_{i}", leaf)
        # self.server.add_data("merkle_tree", self.merkle_tree.to_json())
        self.server.merkle_tree = self.merkle_tree

    def get_merkle_root(self):
        return self.merkle_tree.get_merkle_root()

    def upload_merkle_root_to_blockchain(self):
        merkle_root = self.get_merkle_root()
        self.blockchain.set_merkle_root(merkle_root)