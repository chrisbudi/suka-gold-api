import decimal
from common.responses import NemasReponses
from order.models import order_payment, order_gold
from user.models import user_virtual_account as UserVa
from core.domain import bank as core_bank
from datetime import datetime, timedelta
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from uuid import uuid4
from decimal import Decimal
from rest_framework import serializers

import json


class TrackingProcess:
    def __init__(self, order):
        self.order = order
