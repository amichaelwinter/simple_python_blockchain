#
# author: amichaelwinter
# Description: Simple single transaction block chain test. This is a
# learning excercise and not meant to be used in any type of production
# environment
#
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

    def __init__(self, datetime, transaction, previous_hash):

        self.datetime = datetime
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nounce = str(random.randint(1,1000))

        self.hash = self.generate_hash()


    #
    # Creates a hash for the Block
    #
    def generate_hash(self):

        string_to_hash = str(self.nounce) + str(self.datetime) + self.transaction.long_string() + str(self.previous_hash)
        return hashlib.sha256(string_to_hash).hexdigest()

    def __str__(self):

        return  "Date: " + str(self.datetime) + " Transaction:" + str(self.transaction) + " Hash: " + self.hash + " Previous Hash: " + self.previous_hash


#
# Represents a chain of transaction blocks
#
class Blockchain:

    def __init__(self):

        # Add a dummy first transition
        dummy_transaction = Transaction("1", "1", 0)
        self.chain = []
        self.chain.append(Block(datetime.datetime.now(), dummy_transaction, hashlib.sha224("First").hexdigest()))

    #
    # Adds a transaction to the Blockchain
    #
    def add_transaction(self, sender_id, receiver_id, amount):

        # Create a transaction and add it to the chain
        next_index = len(self.chain)
        new_transaction = Transaction(sender_id, receiver_id, amount)
        previous_hash = self.chain[next_index - 1].hash

        self.chain.append(Block(datetime.datetime.now(),new_transaction,previous_hash))

    #
    # Valdiate the chain
    #
    def validate_chain(self):

        #C heck that the first block has not been tampered with
        first_block = self.chain[0]
        if(first_block.hash != first_block.generate_hash()):
            return False

        # Check the remaning blocks
        i = 1
        while (i < len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # print i
            # print current_block.hash
            # print current_block.generate_hash()

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

def print_test_result(test_name, result):
    success_string = "Success" if result == True else "Failure"
    print "Test: " + test_name + "\t................." + success_string


#
#
#  RUN
#
#


# Test - Unedited Chain
print "\n\nTesting the Chain"
bc_1 = get_test_chain()
print_test_result("Unedited Chain", bc_1.validate_chain() == True)

# Test - Manipulating an attribute
bc_1.chain[0].datetime = datetime.datetime.now()
print_test_result("Attribute Edit", bc_1.validate_chain() == False)

# Test - Manipulating a transaction
bc_2 = get_test_chain()
bc_2.chain[1].transaction.amount = 100
print_test_result("Transaction Edit", bc_1.validate_chain() == False)
