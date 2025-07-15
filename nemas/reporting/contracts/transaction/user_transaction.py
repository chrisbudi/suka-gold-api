from attr import dataclass


@dataclass
class user_transaction_contract:
    reftrans: str
    transaction_id: str
    transaction_number: str
    transaction_date: str
    transaction_method: str
    transaction_desc: str
    transaction_nettvalue: float
    nettvalue_unit: str
    transaction_value: float
    value_unit: str
    transaction_admin: float
    adminvalue_unit: str
    transaction_payment_number: str
    transaction_ref: str
    transaction_ref_code: str
    transaction_channel_code: str
    transaction_expires_at: str
    transaction_note: str
    transaction_status: str
    transaction_timestamp: str
    update_user: str
    update_date: str
    update_user_id: str
    user_id: str
    user_from_id: str
    user_to_id: str
