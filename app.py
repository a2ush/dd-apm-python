from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def index():
    return "welcome demo env!!"

def memory(percentage):
    size_mb = int((percentage / 100) * 1024)
    _ = [bytearray(1024 * 1024) for _ in range(size_mb)]
    time.sleep(4)

def cpu(percentage):
    duration = 4
    end_time = time.time() + duration
    while time.time() < end_time:
        for _ in range(percentage * 10000):
            _ = 123 * 456

@app.route("/memory")
def memory_half():
    memory(50)
    return "Memory usage increased to 50%"

@app.route("/memoryall")
def memory_full():
    memory(100)
    return "Memory usage increased to 100%"

@app.route("/cpu")
def cpu_load():
    cpu(90)
    return "CPU usage increased to 90%"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

