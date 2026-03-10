import hashlib
import datetime


# ---------------- BLOCK ----------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()


# ---------------- BLOCKCHAIN ----------------
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), datetime.datetime.now(), data, prev_block.hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("\n----------------------")
            print("Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True


# ---------------- ENTITIES ----------------
class Voter:
    def __init__(self, voter_id, name):
        self.voter_id = voter_id
        self.name = name
        self.has_voted = False


class Candidate:
    def __init__(self, candidate_id, name):
        self.candidate_id = candidate_id
        self.name = name


# ---------------- DATA STORAGE ----------------
voters = {}
candidates = {}

blockchain = Blockchain()


# ---------------- FUNCTIONS ----------------
def add_voter():
    voter_id = input("Enter Voter ID: ")

    if voter_id in voters:
        print("Voter ID already exists!")
        return

    name = input("Enter Voter Name: ")
    voters[voter_id] = Voter(voter_id, name)

    print("Voter added successfully.")


def add_candidate():
    candidate_id = input("Enter Candidate ID: ")

    if candidate_id in candidates:
        print("Candidate ID already exists!")
        return

    name = input("Enter Candidate Name: ")
    candidates[candidate_id] = Candidate(candidate_id, name)

    print("Candidate added successfully.")


def cast_vote():
    voter_id = input("Enter Voter ID: ")

    if voter_id not in voters:
        print("Voter not found!")
        return

    voter = voters[voter_id]

    if voter.has_voted:
        print("This voter has already voted!")
        return

    print("\nCandidates:")
    for cid, c in candidates.items():
        print(cid, "-", c.name)

    candidate_id = input("Enter Candidate ID to vote: ")

    if candidate_id not in candidates:
        print("Invalid candidate!")
        return

    vote_data = {
        "voter_id": voter_id,
        "candidate_id": candidate_id
    }

    blockchain.add_block(vote_data)

    voter.has_voted = True

    print("Vote cast successfully!")


# ---------------- MENU ----------------
def menu():
    while True:
        print("\n===== Voting System Menu =====")
        print("1. Add Candidate")
        print("2. Add Voter")
        print("3. Cast Vote")
        print("4. Print Blockchain")
        print("5. Validate Chain")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_candidate()

        elif choice == "2":
            add_voter()

        elif choice == "3":
            cast_vote()

        elif choice == "4":
            blockchain.print_chain()

        elif choice == "5":
            if blockchain.validate_chain():
                print("Blockchain is VALID")
            else:
                print("Blockchain is INVALID")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


# ---------------- RUN ----------------
menu()