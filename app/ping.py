"""
API to return a "pong" with inbound request latency
after receiving a "ping" request.
"""
import argparse
from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route("/ping/", methods=["GET"])
def ping():
  return "pong"


@app.route("/ping_latency/", methods=["POST"])
def ping_latency():
  ping_data = request.json
  ping_sent = ping_data["ping"]
  # This must be in UTC
  request_datetime_format = "%H:%M:%S.%f"
  ping_request_datetime = datetime.strptime(
    ping_sent,
    request_datetime_format
  )
  current_datetime = datetime.utcnow()
  time_diff = current_datetime - ping_request_datetime
  time_diff_formatted = time_diff.total_seconds() * 1000
  return_data = {
    "pong_ms": time_diff_formatted
  }
  return jsonify(return_data)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Flask API to return ping/pong requests"
    )
  parser.add_argument(
    "--port",
    type=int,
    default=8080,
    help="Port to serve API on. Default=8080"
  )
  args = parser.parse_args()
  port = args["port"]
  app.run(host="0.0.0.0", port=port)
