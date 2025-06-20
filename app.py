import logging
import time
import json
from flask import Flask, request
from ddtrace import tracer, patch

# ✅ Inject trace context into logs
patch(logging=True)

# ✅ JSON log formatter for Datadog
class DatadogJSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "dd.trace_id"):
            log_record["dd.trace_id"] = getattr(record, "dd.trace_id", None)
        if hasattr(record, "dd.span_id"):
            log_record["dd.span_id"] = getattr(record, "dd.span_id", None)
        return json.dumps(log_record)

# ✅ Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(DatadogJSONFormatter())
logger.addHandler(handler)

# ✅ Disable default Werkzeug access logs
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# ✅ Flask app
app = Flask(__name__)

# ✅ Custom access logging (Datadog-trace-aware)
@app.before_request
def log_access():
    logger.info(f"Access log: {request.method} {request.path} from {request.remote_addr}")

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
