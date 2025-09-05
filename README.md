# Distributed Sales Data Analysis System

## 📌 Overview

This project demonstrates a distributed system that processes a large CSV dataset (5 million sales transactions) using multiple Python worker nodes communicating with a central server via TCP sockets.

## ⚙️ Technologies Used

- Python 3.8+
- Pandas
- SQLite
- TCP Sockets
- Pickle (Serialization)

## 📁 Project Structure
sales_distributed_analysis/
│
├── config.py
├── db_handler.py
├── server.py
├── worker.py
├── sample_data.csv
└── results.db