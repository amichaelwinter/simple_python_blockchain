import time
import datetime
import uuid
import hashlib
import random

#
# Simple class representing a financial transition
#
class Transaction:

    def __init__ (self, sender_id, receiver_id, amount):

        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount

        self.transaction_id = uuid.uuid4()

    #
    # Returns a string primarily meant for being hashed
    #
    def long_string(self):
        return self.sender_id + self.receiver_id + str(self.amount) + str(self.transaction_id)

    def __str__(self):

        return str(self.transaction_id)



#
# Represents a single block in the blockchain
#
class Block:

    def __init__(self, index, datetime, transaction, previous_hash):

        self.index = index
        self.datetime = datetime
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nounce = str(random.randint(1,1000))

        self.hash = self.generate_hash()


    #
    # Creates a hash for the Block
    #
    def generate_hash(self):

        string_to_hash = str(self.index) + str(self.datetime) + self.transaction.long_string() + str(self.previous_hash) + self.nounce

        return hashlib.sha224(string_to_hash).hexdigest()

    def __str__(self):

        return "Index: " + str(self.index) + " Date: " + str(self.datetime) + " Transaction:" + str(self.transaction) + " Hash: " + self.hash + " Previous Hash: " + self.previous_hash


#
# Represents a chain of transaction blocks
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

    #
    # Valdiate the chain
    #
    def validate_chain(self):

        i = 1
        while (i < len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Confirm the current block has not been manipulated
            if(current_block.hash != current_block.generate_hash()):
                print current_block.hash
                print current_block.generate_hash()
                print "Block manipuated"
                return False

            # Confirm the previous blocks hash is equal to the blocks hash
            if(current_block.previous_hash != previous_block.hash):
                print current_block.previous_hash
                print previous_block.hash
                print "Previous block manipuated"
                return False

            i += 1


        return True

    #
    # Prints a list of all transactions in the chain
    #
    def __str__(self):

        blockchain_string = ""

        # Write all the blocks in the chain
        i = 0
        while(i < len(self.chain)):
            blockchain_string += str(self.chain[i]) + "\n"
            i+=1

        # Append a valid string
        if(self.validate_chain()):
            blockchain_string += "Blockchain is valid"
        else:
            blockchain_string += "Blockchain is not valid"

        return blockchain_string

#
# Helped function to get a test chain
#
def get_test_chain():

    test_chain = Blockchain()
    test_chain.add_transaction("5555", "4444", 10)
    test_chain.add_transaction("4444", "2222", 8)

    return test_chain

#
# RUN
#
print "\n----------PRINT A TEST CHAIN----------"
bc_1 = get_test_chain()
print bc_1

print "\n----------TEST A NON MANIPULATED CHAIN----------"
print str(bc_1.validate_chain())

print "\n----------TEST MANIPULATING AN IDEX----------"
bc_1.chain[0].index = 5
print(bc_1.chain[0])
print str(bc_1.validate_chain())

print "\n----------TEST MANIPULATING AN AMOUNT----------"
bc_2 = get_test_chain()
bc_2.chain[1].transaction.amount = 100
print str(bc_2.validate_chain())

print "\n----------TEST MANIPULATING AN HASH----------"
bc_3 = get_test_chain()
bc_3.chain[1].hash = "234234"
print str(bc_3.validate_chain())
