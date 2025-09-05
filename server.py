import socket
import threading
import pickle
import pandas as pd
from config import *
from db_handler import initialize_db, insert_result, aggregate_results

# Global to hold chunks
data_chunks = []

def load_and_split_data():
    print("[*] Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    print(f"[✓] Loaded {len(df)} rows.")
    chunks = [df[i:i+CHUNK_SIZE] for i in range(0, len(df), CHUNK_SIZE)]
    print(f"[✓] Split data into {len(chunks)} chunks of {CHUNK_SIZE} rows each.")
    return chunks

def handle_worker(conn, addr, chunk, worker_id):
    print(f"[+] Worker {worker_id} connected from {addr}")

    # Send the data chunk
    print(f"[→] Sending chunk to {worker_id}...")

    chunk_bytes = pickle.dumps(chunk)
    chunk_size = len(chunk_bytes)
    conn.sendall(chunk_size.to_bytes(8, byteorder='big'))  # Send length first
    conn.sendall(chunk_bytes)  # Then send actual data

    print(f"[✓] Chunk sent to {worker_id}.")

    # Receiving results
    print(f"[←] Waiting for result from {worker_id}...")
    data = b""
    while True:
        packet = conn.recv(BUFFER_SIZE)
        if not packet:
            break
        data += packet

    result = pickle.loads(data)
    insert_result(result)
    print(f"[✓] Received and stored result from {worker_id}")
    conn.close()

def main():
    print("[*] Initializing database...")
    initialize_db()
    chunks = load_and_split_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(NUM_WORKERS)
    print(f"[*] Server listening on {HOST}:{PORT}")

    threads = []

    for i in range(NUM_WORKERS):
        conn, addr = server.accept()
        t = threading.Thread(target=handle_worker, args=(conn, addr, chunks[i], f'worker{i+1}'))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[*] All workers finished. Aggregating final results...\n")
    result = aggregate_results()

    print(f"Final Aggregated Results:")
    print(f"Total Rows Processed: {result[0]}")
    print(f"Total Sales Amount: {result[1]:.2f}")
    print(f"Min Price: {result[2]:.2f}")
    print(f"Max Price: {result[3]:.2f}")
    print(f"Average Price: {result[4]:.2f}")

if __name__ == "__main__":
    main()
