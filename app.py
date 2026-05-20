from flask import Flask, request, jsonify
import re
import uuid
import json
from datetime import datetime
from db import get_db_connection

app = Flask(__name__)

@app.route("/generate-label", methods=["POST"])
def generate_label():

    data = request.get_json()
    requestid = str(uuid.uuid4())
    now = datetime.now()

    required_fields = [
        "from_name",
        "from_address",
        "from_phone",
        "to_name",
        "to_address",
        "to_phone",
        "service"
    ]

    for field in required_fields:
        if not data or field not in data or str(data[field]).strip() == "":
            response_json = {
                "status": "invalid",
                "reason": f"{field} is missing"
            }
            return_code = 400
            break
    else:
        response_json = {
            "status": "valid",
            "requestid": requestid,
            "from": "USA",
            "from_address": data["from_address"],
            "sender_name": data["from_name"],
            "sender_phone": "+1 " + data["from_phone"],
            "to": "India",
            "to_address": data["to_address"],
            "receiver_name": data["to_name"],
            "receiver_phone": "+91 " + data["to_phone"],
            "service": data["service"]
        }
        return_code = 200

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO shipment_requests
    (datetime, requestid, from_name, from_address, from_phone,
    to_name, to_address, to_phone, service, return_code, return_json)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        now,
        requestid,
        data.get("from_name") if data else None,
        data.get("from_address") if data else None,
        data.get("from_phone") if data else None,
        data.get("to_name") if data else None,
        data.get("to_address") if data else None,
        data.get("to_phone") if data else None,
        data.get("service") if data else None,
        return_code,
        json.dumps(response_json)
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(response_json), return_code

if __name__ == "__main__":
    app.run(debug=True)
    