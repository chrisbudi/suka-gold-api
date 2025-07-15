from rest_framework import serializers


class user_transaction_serializer(serializers.Serializer):
    """Serializer for user transactions"""

    reftrans = serializers.CharField(read_only=True)
    transaction_id = serializers.CharField(read_only=True)
    transaction_number = serializers.CharField(read_only=True)
    transaction_date = serializers.DateTimeField(read_only=True)
    transaction_method = serializers.CharField(read_only=True)
    transaction_desc = serializers.CharField(read_only=True)
    transaction_nettvalue = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    nettvalue_unit = serializers.CharField(read_only=True)
    transaction_value = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    value_unit = serializers.CharField(read_only=True)
    transaction_admin = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    adminvalue_unit = serializers.CharField(read_only=True)
    transaction_payment_number = serializers.CharField(read_only=True)
    transaction_ref = serializers.CharField(read_only=True)
    transaction_ref_code = serializers.CharField(read_only=True)
    transaction_channel_code = serializers.CharField(read_only=True)
    transaction_expires_at = serializers.DateTimeField(read_only=True)
    transaction_note = serializers.CharField(read_only=True)
    transaction_status = serializers.CharField(read_only=True)
    transaction_timestamp = serializers.DateTimeField(read_only=True)
    update_user = serializers.CharField(read_only=True)
    update_date = serializers.DateTimeField(read_only=True)
    update_user_id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    user_from_id = serializers.CharField(read_only=True)
    user_to_id = serializers.CharField(read_only=True)
