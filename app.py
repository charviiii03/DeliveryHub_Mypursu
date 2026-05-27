
# run flask server only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
    # generates unique ids
import uuid

# generates secure random tokens
import secrets

# used for date and time operations
from datetime import datetime, timedelta

# used to hash passwords/tokens securely
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, request, jsonify
from db import get_db_connection

app = Flask(__name__)


def log_auth_attempt(application_id, endpoint, status, reason=None, ip_address=None, request_details=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO authentication_logs
    (application_id, endpoint, status, reason, ip_address, request_details)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        application_id,
        endpoint,
        status,
        reason,
        ip_address,
        request_details
    ))

    connection.commit()
    cursor.close()
    connection.close()


# common function to check application authentication
def check_application_auth(application_id, application_token, endpoint):
    ip_address = request.remote_addr
    request_details = f"method={request.method}, path={request.path}"

    if not application_id or not application_token:
        log_auth_attempt(
            application_id or "unknown",
            endpoint,
            "failure",
            "application id or token missing",
            ip_address,
            request_details
        )
        return None

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    sql = """
    SELECT * FROM applications
    WHERE application_id = %s
    AND expiry_date >= CURDATE()
    AND is_active = TRUE
    """

    cursor.execute(sql, (application_id,))
    application = cursor.fetchone()

    cursor.close()
    connection.close()

    if not application:
        log_auth_attempt(
            application_id,
            endpoint,
            "failure",
            "application not found, expired, or inactive",
            ip_address,
            request_details
        )
        return None

    if not check_password_hash(application["application_token"], application_token):
        log_auth_attempt(
            application_id,
            endpoint,
            "failure",
            "invalid token",
            ip_address,
            request_details
        )
        return None

    log_auth_attempt(
        application_id,
        endpoint,
        "success",
        None,
        ip_address,
        request_details
    )

    return application


# Checks: application ID, application token, expiry date
@app.route("/generate-label", methods=["POST"])
def generate_label():
    data = request.get_json()

    application_id = data.get("application_id") if data else None
    application_token = data.get("application_token") if data else None

    application = check_application_auth(application_id, application_token, "/generate-label")

    if not application:
        return jsonify({
            "status": "invalid",
            "reason": "authentication failed"
        }), 401

    return jsonify({
        "status": "valid",
        "message": "label generated successfully"
    }), 200


# Returns valid/invalid application
@app.route("/validate-auth", methods=["POST"])
def validate_auth():
    data = request.get_json()

    application_id = data.get("application_id") if data else None
    application_token = data.get("application_token") if data else None

    application = check_application_auth(application_id, application_token, "/validate-auth")

    if application:
        return jsonify({
            "status": "valid",
            "message": "valid application"
        }), 200

    return jsonify({
        "status": "invalid",
        "reason": "invalid or expired application"
    }), 401


@app.route("/admin/create-application", methods=["POST"])
def signup():
    data = request.get_json()

    application_name = data.get("application_name")
    user_email = data.get("user_email")

    application_id = str(uuid.uuid4())
    application_token = secrets.token_urlsafe(32)

    hashed_token = generate_password_hash(application_token)
    # this converts token into encrypted/hashed form,
    # original token is protected even if database leaks

    expiry_date = datetime.now() + timedelta(days=90)

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO applications
    (application_id, application_token, application_name, user_email, expiry_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        application_id,
        hashed_token,
        application_name,
        user_email,
        expiry_date
    )

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "status": "success",
        "message": "application created successfully",
        "application_id": application_id,
        "application_token": application_token,
        "expiry_date": expiry_date.strftime("%Y-%m-%d")
    }), 201


@app.route("/admin/applications", methods=["GET"])
def view_applications():
    # connect to database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # get all application details
    cursor.execute("""
        SELECT application_id, application_name, user_email, expiry_date, is_active
        FROM applications
    """)

    # fetch all applications
    applications = cursor.fetchall()

    # close database connection
    cursor.close()
    connection.close()

    # return applications response
    return jsonify({
        "status": "success",
        "applications": applications
    }), 200


@app.route("/admin/update-status", methods=["PUT"])
def update_status():
    # get request data
    data = request.get_json()

    # get application id and active status
    application_id = data.get("application_id")
    is_active = data.get("is_active")

    # connect to database
    connection = get_db_connection()
    cursor = connection.cursor()

    # update application status
    cursor.execute("""
        UPDATE applications
        SET is_active = %s
        WHERE application_id = %s
    """, (is_active, application_id))

    # save changes
    connection.commit()

    # close database connection
    cursor.close()
    connection.close()

    # success response
    return jsonify({
        "status": "success",
        "message": "application status updated"
    }), 200


@app.route("/admin/auth-logs", methods=["GET"])
def view_auth_logs():
    # connect to database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # get authentication logs
    cursor.execute("""
        SELECT application_id, endpoint, request_time, status, reason, ip_address, request_details
        FROM authentication_logs
        ORDER BY request_time DESC
    """)

    # fetch all log records
    logs = cursor.fetchall()

    # close database connection
    cursor.close()
    connection.close()

    # return logs response
    return jsonify({
        "status": "success",
        "logs": logs
    }), 200


@app.route("/admin/update-expiry", methods=["PUT"])
def update_expiry():
    # get request data
    data = request.get_json()

    # get application id and new expiry date
    application_id = data.get("application_id")
    new_expiry_date = data.get("expiry_date")

    # connect to database
    connection = get_db_connection()
    cursor = connection.cursor()

    # update expiry date
    cursor.execute("""
        UPDATE applications
        SET expiry_date = %s
        WHERE application_id = %s
    """, (new_expiry_date, application_id))

    # save changes
    connection.commit()

    # close database connection
    cursor.close()
    connection.close()

    # success response
    return jsonify({
        "status": "success",
        "message": "expiry date updated"
    }), 200


@app.route("/signin", methods=["POST"])
def signin():
    # get request data
    data = request.get_json()

    # get application credentials
    application_id = data.get("application_id")
    application_token = data.get("application_token")

    # use shared authentication helper
    application = check_application_auth(application_id, application_token, "/signin")

    # check if application exists and token is valid
    if not application:
        return jsonify({
            "status": "invalid",
            "reason": "application not found, expired, inactive, or token invalid"
        }), 401

    # successful signin
    return jsonify({
        "status": "valid",
        "message": "signin successful"
    }), 200


# run flask server only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)