import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Create the genesis block
        self.new_block(previous_hash=1, proof=100)


    def new_block(self,proof, previous_hash=none):
        '''
        Create a new Block and adds it to the chain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (optional) <str> Hash of previous Block
        :return: <dict> New Block
        '''
        block = {
            'index': len(self.chain) +1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_harsh':previous_hash or self.hash(self.chain[-1]),
        }



    def new_transaction(self,sender, recipient, amount):
        '''
        Add a New transaction to the list of transactions
        :param sender: <str> Address of the Sender
        :param receipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block taht will hold this transaction
        '''
        self.current_transactions.append({
            'sender': sender,
            'recipient':recipient,
            'amount': amount,
        })

        return self.last_block['index'] +1





    @property
    def last_block(self):
        #Returns the last Blok in the chain
        return self.chain[-1]



    @staticmethod
    def hash(block):
        '''
        hashes a block SHA-256
        :param block: <dict> Block
        :return: <str>
        '''
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dump(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


#理解工作量证明












