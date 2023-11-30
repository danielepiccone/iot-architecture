import json
from flask import Flask, jsonify, request, g
from common.telemetry_service import TelemetryService
from common.device_service import DeviceService

app = Flask(__name__)


@app.before_request
def init_services():
    g.telemetry_service = TelemetryService()
    g.device_service = DeviceService()


@app.route("/device/<device_id>", methods=["GET"])
def get_device(device_id):
    if request.method == "GET":
        device_service = g.device_service
        device = device_service.get_device(device_id)

        if device:
            return jsonify(device), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    else:
        return jsonify({"error": "Method not allowed"}), 405


@app.route("/device/<device_id>/telemetry", methods=["GET"])
def get_device_telemetry(device_id):
    if request.method == "GET":
        telemetry_service = g.telemetry_service
        payloads = telemetry_service.list("/" + device_id + "/")
        return jsonify(payloads), 200
    else:
        return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
