from web3 import Web3
from solcx import compile_source, install_solc, get_installed_solc_versions

class Blockchain:
    def __init__(self, host):
        self.host = host
        self.contract_id = None
        self.contract_interface = None
        self.abi = None
        self.bytecode = None
        self.contract_instance = None
        self.service_provider = None

    def set_merkle_root(self, merkle_root):
        # Data owner sets merkle root
        print("Setting Merkle Root:", merkle_root)
        try:
            set_tx_hash = self.contract_instance.functions.setMerkleRoot(merkle_root).transact({
                'from': self.service_provider.eth.default_account,
                'gas': 2000000
            })
            set_tx_receipt = self.service_provider.eth.wait_for_transaction_receipt(set_tx_hash)
            print("Transaction receipt:", set_tx_receipt)
            print("Transaction hash for setting Merkle root:", set_tx_hash.hex())
            print("Transaction receipt status:", set_tx_receipt.status)
            print("Gas used for setting Merkle Root:", set_tx_receipt.gasUsed)
        except Exception as e:
            print("Failed to set Merkle Root:", e)

    def get_merkle_root(self):
        print("Attempting to retrieve Merkle Root...")
        try:
            root = self.contract_instance.functions.getMerkleRoot().call()
            print("Merkle Root retrieved:", root)
            return root
        except Exception as e:
            print("Failed to retrieve Merkle Root:", e)
            return None

    def compile_contract(self):
        solc_version = '0.5.17'
        # Check if the specified version of solc is installed, and install it if not
        if not get_installed_solc_versions() or solc_version not in get_installed_solc_versions():
            install_solc(solc_version)

        compiled_sol = compile_source(
            '''
            pragma solidity ^0.5.17;
            contract Verify {
                string merkleRoot = "default";
                event MerkleRootSet(string newRoot);

                function setMerkleRoot(string memory _merkleRoot) public {
                    merkleRoot = _merkleRoot;
                    emit MerkleRootSet(merkleRoot);
                }

                function getMerkleRoot() view public returns (string memory) {
                    return merkleRoot;
                }
            }
            ''',
            solc_version=solc_version,
            output_values=['abi', 'bin']
        )

        contract_id, contract_interface = compiled_sol.popitem()
        self.bytecode = contract_interface['bin']
        self.abi = contract_interface['abi']

    def deploy_contract(self):
        w3 = Web3(Web3.HTTPProvider(self.host))
        print("Is Connected?", w3.isConnected())
        self.service_provider = w3
        w3.eth.default_account = w3.eth.accounts[0]

        Verify = w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        deploy_tx_hash = Verify.constructor().transact()
        deploy_tx_receipt = w3.eth.wait_for_transaction_receipt(deploy_tx_hash)
        print("Contract deployed at address:", deploy_tx_receipt.contractAddress)

        self.contract_instance = w3.eth.contract(
            address=deploy_tx_receipt.contractAddress,
            abi=self.abi
        )

        

