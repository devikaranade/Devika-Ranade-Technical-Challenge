import datetime
import sys
import sqlite3
from web3 import Web3

# connect to RPC endpoint
def connect_to_rpc(endpoint):
    try:
        web3 = Web3(Web3.HTTPProvider(endpoint))
        if web3.is_connected():
            return web3
        else:
            print("Failed to connect to JSON-RPC endpoint.")
            sys.exit(1)
    except Exception as e:
        print(f"Error connecting to JSON-RPC endpoint: {e}")
        sys.exit(1)

# creating tables for storing database
def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS blocks
                    (hash TEXT PRIMARY KEY,
                    number INTEGER,
                    timestamp INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (hash TEXT PRIMARY KEY,
                    block_hash TEXT,
                    block_number INTEGER,
                    sender TEXT,
                    receiver TEXT,
                    value REAL,
                    FOREIGN KEY (block_hash) REFERENCES blocks(hash))''')


def retrieve_and_store_transactions(web3, start_block, end_block, cursor):
    if start_block>end_block:
        print("Enter a valid block")
    for block_number in range(start_block, end_block + 1):
        block = web3.eth.get_block(block_number)
        if block is not None and 'transactions' in block:
            unix_timestamp = block['timestamp']
            datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
            cursor.execute('''INSERT OR IGNORE INTO blocks
                            (hash, number, timestamp)
                            VALUES (?, ?, ?)''',
                            (block['hash'], block['number'], datetime_obj)) # insert into blocks
            
            for tx_hash in block['transactions']:
                tx = web3.eth.get_transaction(tx_hash)
                block_hash = tx['blockHash']
                sender = tx['from']
                receiver = tx['to'] if tx['to'] else None
                value = (tx['value']) // 10**9 #in GWei 
                cursor.execute('''INSERT OR IGNORE INTO transactions
                                (hash, block_hash, block_number, sender, receiver, value)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                                (tx_hash, block_hash, block_number, sender, receiver, value)) #insert into transactions
                
    cursor.connection.commit()

# main program exec
def main():
    if len(sys.argv) != 4:
        print("Run: python3 script.py <JSON-RPC endpoint> <SQLite file path> <block range>")
        sys.exit(1)

    endpoint = sys.argv[1]
    db_path = sys.argv[2]
    block_range = sys.argv[3].split('-')
    start_block = int(block_range[0])
    end_block = int(block_range[1])

    web3 = connect_to_rpc(endpoint)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_tables(cursor)

    retrieve_and_store_transactions(web3, start_block, end_block, cursor)

    conn.close()

if __name__ == "__main__":
    main()


