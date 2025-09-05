import socket
import pickle
import argparse
import pandas as pd
from config import *

def compute_metrics(df, worker_id):
    print(f"[{worker_id}] Computing metrics...")
    metrics = {
        'worker_id': worker_id,
        'rows_processed': len(df),
        'total_sales': (df['Units Sold'] * df['Unit Price']).sum(),
        'min_price': df['Unit Price'].min(),
        'max_price': df['Unit Price'].max(),
        'avg_price': df['Unit Price'].mean()
    }
    print(f"[{worker_id}] Metrics computed.")
    return metrics

def main(worker_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[+] {worker_id} connected to server")

    # to solve error of data chunks not being received, I implemented size headers
    # First, receive the 8-byte header
    header = client.recv(8)
    data_len = int.from_bytes(header, byteorder='big')

    # then receive the actual data chunk
    print(f"[{worker_id}] Waiting to receive data chunk...")
    data = b""
    while len(data) < data_len:
        to_read = min(BUFFER_SIZE, data_len - len(data))
        packet = client.recv(to_read)
        if not packet:
            break
        data += packet

    # deserializing data received using pickle
    print(f"[{worker_id}] Data received. Deserializing...")
    df = pickle.loads(data)

    print(f"[{worker_id}] Received data chunk of size: {len(df)}")

    result = compute_metrics(df, worker_id)

    # Sending result back to server using same connection
    print(f"[{worker_id}] Sending result back to server...")
    client.sendall(pickle.dumps(result))
    print(f"[{worker_id}] Result sent. Closing connection.")
    client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="Worker ID (e.g., worker1)")
    args = parser.parse_args()
    main(args.id)
