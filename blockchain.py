import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Create the genesis block
        self.new_block(previous_hash=1, proof=100)


    def new_block(self,proof, previous_hash=None):
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

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        return block



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


    def proof_of_work(self,last_proof):
        '''
        simple proof of work:
         - find p', to make sure hash(pp') start with four 0
         - p is last proof of work, p' is current proof of work
        :param last_proof: <int>
        :return: <int>
        '''

        proof =0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        valid proof: if hash(last_proof, proof) starts with four 0?
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> Ture if correct, False if not
        '''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


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


#Instantiate our Node
app = Flask(__name__)

#Generate a global unique address for this node
node_identifier = str(uuid4()).replace('_','')

#Instantiate the Blockchain

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = blockchain['proof']
    proof = blockchain.proof_of_work(last_proof)

    #give bonus to proof of work node
    #sender is "0", means new mined

    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount=1,
    )

    #Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions':block['transactions'],
        'proof': block['proof'],
        'previous_hash':block['previous_hash'],
    }
    return jsonify(response),200




@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    values = request.get_json()

    #Check taht the requried fields are in teh POST'ed data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    #Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['receipient'], values['amount'])
    response = {'message': f'Trnsaction will ba added to Block {index}'}
    return jsonify(response), 201



@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response),200

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)













