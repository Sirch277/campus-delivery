import uuid

def simulate_charge(db, delivery_id, amount):
    return f"HOLD-{uuid.uuid4().hex}"

def simulate_release(db, payment_reference):
    return True
def simulate_refund(db, payment_reference):
    return True