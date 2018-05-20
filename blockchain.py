import time
import datetime
import uuid
import hashlib

#
# Simple class representing a financial transition
#
class Transaction:

    def __init__ (self, sender_id, receiver_id, amount):

        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount

        self.transaction_id = uuid.uuid4()

    def __str__(self):

        return str(self.transaction_id)



#
# Reprsents a single block in the blockchain
#
class Block:

    def __init__(self, index, datetime, transaction, previous_hash):

        self.index = index
        self.datetime = datetime
        self.transaction = transaction
        self.previous_hash = previous_hash

        self.create_hash()


    #
    # Creates a hash for the Block
    #
    def create_hash(self):

        string_to_hash = str(self.index) + str(self.datetime) + str (self.transaction) + str(self.previous_hash)

        self.hash = hashlib.sha224(string_to_hash).hexdigest()
    #
    #
    #
    def __str__(self):

        return "Index: " + str(self.index) + " Date: " + str(self.datetime) + " Transaction:" + str(self.transaction) + " Hash: " + self.hash + " Previous Hash: " + self.previous_hash


#
# Represnts a chain of transactoin blocks
#
class Blockchain:

    def __init__(self):

        # Add a dummy first transition
        dummy_transaction = Transaction("1", "1", 0)
        self.chain = []
        self.chain.append(Block(0,datetime.datetime.now(), dummy_transaction, hashlib.sha224("First").hexdigest()))

    #
    # Adds a transaction to the Blockchain
    #
    def add_transaction(self, sender_id, receiver_id, amount):

        # Create a transaction and add it to the chain
        next_index = len(self.chain)
        new_transaction = Transaction(sender_id, receiver_id, amount)
        previous_hash = self.chain[next_index - 1].hash

        self.chain.append(Block(next_index, datetime.datetime.now(),new_transaction,previous_hash))


    def validate_chain(self):
        return true

    #
    # Prints a list of all transactions in the chain
    #
    def __str__(self):

        blockchain_string = ""

        i = 0
        while(i < len(self.chain)):
            blockchain_string += str(self.chain[i]) + "\n"
            i+=1

        return blockchain_string

#
# RUN
#

block_chain = Blockchain()

block_chain.add_transaction("5555", "4444", 10)
block_chain.add_transaction("4444", "2222", 8)

print block_chain
