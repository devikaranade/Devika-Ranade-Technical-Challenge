## Block Crawler

### Ethereum Block Data Retrieval and Storage

This Python script connects to an Ethereum JSON-RPC endpoint, retrieves blockchain data within a specified block range, and stores it in an SQLite database. It uses the Web3 library to interact with the Ethereum blockchain.

### Technologies
 - Python 3.12.2
 - Web3 library(installation: ```pip install web3```)
 - SQLite3
 - JSON RPC Endpoint: Infura API

### Usage
1. Clone the repository or download the script script.py.
2. Install the required libraries.
3. Run the script with the following command:
   ```
   python3 script.py <JSON-RPC endpoint> <SQLite file path> <block range>
   ```
4. Replace <JSON-RPC endpoint>, <SQLite file path>, and <block range> with your specific values. For example:
   ```
   python3 script.py https://mainnet.infura.io/v3/key db.sqlite3 18911300-18911320
   ```
5. The script will connect to the JSON-RPC endpoint, retrieve block data within the specified range, and store it in the SQLite database.

### Functionality

- connect_to_rpc(endpoint): Connects to the Ethereum JSON-RPC endpoint.
- create_tables(cursor): Creates the necessary tables in the SQLite database for storing block and transaction data.
- retrieve_and_store_transactions(web3, start_block, end_block, cursor): Retrieves block data and associated transactions within the specified block range and stores them in the SQLite database.

### Additional Notes
- The script converts transaction values from Wei to **Gwei** (GigaWei) for storage.
- Error handling is included for connection failures and invalid input.
- Ensure that the required dependencies are installed before running the script.

Output Part2: 

<img width="700" alt="output" src="https://github.com/devikaranade/Devika-Ranade-Technical-Challenge/assets/41178447/99587c26-35c9-4bc0-92d4-e81da799dd99">


<img width="700" alt="sql-query" src="https://github.com/devikaranade/Devika-Ranade-Technical-Challenge/assets/41178447/989466d5-8720-469e-bae7-72f62aa6ec73">



