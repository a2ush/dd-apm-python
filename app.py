import logging
import time
from flask import Flask
from ddtrace import tracer

# ロガー設定（フォーマットのみ）
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] '
          '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
@tracer.wrap()
def index():
    logger.info("Accessing index page")
    return "welcome demo env!!"

@tracer.wrap()
def memory(percentage):
    size_mb = int((percentage / 100) * 1024)
    logger.info(f"Allocating {size_mb} MB of memory")
    _ = [bytearray(1024 * 1024) for _ in range(size_mb)]
    time.sleep(4)
    logger.info("Memory allocation complete")

@tracer.wrap()
def cpu(percentage):
    duration = 4
    end_time = time.time() + duration
    logger.info(f"Starting CPU load at {percentage}% for {duration} seconds")
    while time.time() < end_time:
        for _ in range(percentage * 10000):
            _ = 123 * 456
    logger.info("CPU load complete")

@app.route("/memory")
@tracer.wrap()
def memory_half():
    memory(50)
    logger.info("Memory usage increased to 50%")
    return "Memory usage increased to 50%"

@app.route("/memoryall")
@tracer.wrap()
def memory_full():
    memory(100)
    logger.info("Memory usage increased to 100%")
    return "Memory usage increased to 100%"

@app.route("/cpu")
@tracer.wrap()
def cpu_load():
    cpu(90)
    logger.info("CPU usage increased to 90%")
    return "CPU usage increased to 90%"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
