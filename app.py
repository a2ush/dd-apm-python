import logging
from flask import Flask
import time

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    logger.info("Accessing index page")
    return "welcome demo env!!"

def memory(percentage):
    size_mb = int((percentage / 100) * 1024)
    logger.info(f"Allocating {size_mb} MB of memory")
    _ = [bytearray(1024 * 1024) for _ in range(size_mb)]
    time.sleep(4)
    logger.info("Memory allocation complete")

def cpu(percentage):
    duration = 4
    end_time = time.time() + duration
    logger.info(f"Starting CPU load at {percentage}% for {duration} seconds")
    while time.time() < end_time:
        for _ in range(percentage * 10000):
            _ = 123 * 456
    logger.info("CPU load complete")

@app.route("/memory")
def memory_half():
    memory(50)
    logger.info("Memory usage increased to 50%")
    return "Memory usage increased to 50%"

@app.route("/memoryall")
def memory_full():
    memory(100)
    logger.info("Memory usage increased to 100%")
    return "Memory usage increased to 100%"

@app.route("/cpu")
def cpu_load():
    cpu(90)
    logger.info("CPU usage increased to 90%")
    return "CPU usage increased to 90%"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

