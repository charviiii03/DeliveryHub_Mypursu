INSERT INTO customers (full_name, phone_number)
VALUES
('john', '9999999999'),
('rahul', '8888888888');


INSERT INTO addresses (
    address_line,
    city,
    state_name,
    country,
    country_code,
    postal_code
)
VALUES
('new york, usa', 'New York', 'NY', 'United States of America', 'US', '10001'),
('delhi, india', 'Delhi', 'Delhi', 'India', 'IN', '110001');

INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-001',
    1,
    2,
    1,
    2,
    'express',
    'valid',
    NULL,
    'initiated',
    200,
    '{"status":"valid"}'
);

INSERT IGNORE INTO shipments ( -- this ignore skips it, if duplicate exists
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-invalid-001',
    1,
    2,
    1,
    2,
    'express',
    'invalid',
    'invalid from country code',
    'initiated',
    400,
    '{"status":"invalid","reason":"invalid from country code"}'
);

INSERT INTO shipment_tracking (
    shipment_id,
    current_status
)
VALUES
(1, 'initiated'),
(2, 'validation_failed');

INSERT INTO applications
(application_id, application_token, application_name, expiry_date)
VALUES
('app123', 'token123', 'test_client', '2026-12-31');

INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-valid-002',
    1,
    2,
    1,
    2,
    'priority',
    'valid',
    NULL,
    'assigned',
    200,
    '{"status":"valid","message":"Shipment request accepted successfully"}'
);

INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-invalid-phone',
    1,
    2,
    1,
    2,
    'express',
    'invalid',
    'sender phone number missing',
    'validation_failed',
    400,
    '{"status":"invalid","reason":"Sender phone number is required"}'
);
INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-invalid-email',
    1,
    2,
    1,
    2,
    'express',
    'invalid',
    'invalid email address',
    'validation_failed',
    400,
    '{"status":"invalid","reason":"Please provide a valid email address"}'
);

INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-return-001',
    2,
    1,
    2,
    1,
    'express',
    'review',
    'return shipment detected',
    'pending_review',
    202,
    '{"status":"review","message":"Return shipment detected and pending confirmation"}'
);

INSERT IGNORE INTO shipments (
    requestid,
    sender_customer_id,
    receiver_customer_id,
    from_address_id,
    to_address_id,
    service,
    validation_status,
    validation_reason,
    state,
    return_code,
    return_json
)
VALUES
(
    'sample-image-001',
    1,
    2,
    1,
    2,
    'express',
    'review',
    'shipment image uploaded',
    'pending_review',
    202,
    '{"status":"review","message":"Shipment image received and pending review"}'
);