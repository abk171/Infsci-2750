import hashlib
from blockchain import  Blockchain
from db_provider import Server
from data_owner import DataOwner
import merkletools
from adv_client import  MaliciousClient
#This class serves as a query client and also perform verification
class QueryClient:

    def __init__(self, server,blockchain):
        self.server = server
        self.blockchain = blockchain

    #perform query to server
    def query_by_key(self, key):
        value = self.server.get_data(key)
        return value

    # get proof from server's merkle tree
    def retrieve_verification_path_by_tree(self, key_index):
        self.server.merkle_tree.make_tree()
        return self.server.merkle_tree.get_proof(key_index)

    # get index from server's merkle tree
    def retrieve_key_index_in_tree(self, key):
        return self.server.merkle_tree.get_index(key)

    # get merkle root from blockchain
    def retrieve_root_from_blockchain(self):
        return self.blockchain.get_merkle_root()

    # Query clients issue query verifications
    def query_verification(self, retrieved_value, proofs, root_from_contract):
        merkle = merkletools.MerkleTools()
        # print(f"retrieved value is {retrieved_value}")
        # print(f"proofs is {proofs}")
        return merkle.validate_proof(proofs, retrieved_value,root_from_contract)
