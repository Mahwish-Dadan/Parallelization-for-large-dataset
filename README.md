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
├── config.py

├── db_handler.py

├── server.py

├── worker.py

├── sample_data.csv

└── results.db

🚀 How It Works
1. Data Loading & Chunking: The server loads the full sales CSV and splits it into chunks.
2. Parallel Processing: Each worker connects to the server, receives a chunk, processes sales data (computing aggregates like total sales, min/max/avg prices), and sends back results.
3. Result Aggregation: The server collects results from all workers and stores them in the SQLite database with timestamps.
4. Exploratory Data Analysis: The eda.py script uses the aggregated results and original sales data to generate insightful visualizations — including worker performance, sales trends over time, and price distributions.

📊 Visualizations Include
1. Rows processed by each worker (bar chart)
2. Sales contribution by worker (pie chart)
3. Price metrics (average with min/max error bars per worker)
4. Monthly and yearly sales trends with smoothing and peak highlights

💡 Notes
- The system supports easy scaling by adding more worker nodes.
- Database timestamps allow tracking when each chunk was processed.
- The EDA script can be run independently to generate up-to-date visualizations.
