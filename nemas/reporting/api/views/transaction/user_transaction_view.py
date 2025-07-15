from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from reporting.contracts.transaction import user_transaction
from reporting.api.serializers.transaction.user_transaction_serializer import (
    user_transaction_serializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="user_id",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="offset",
            required=False,
            type=int,
            description="Pagination offset",
        ),
        OpenApiParameter(
            name="limit",
            required=False,
            type=int,
            description="Pagination limit",
        ),
    ],
    responses={
        200: user_transaction_serializer(many=True),
    },
)
class user_transaction_view(APIView):
    def get(self, request):
        query = """            
            SELECT reftrans,
                transaction_id,
                transaction_number,
                transaction_date,
                transaction_method,
                transaction_desc,
                transaction_nettvalue,
                nettvalue_unit,
                transaction_value,
                value_unit,
                transaction_admin,
                adminvalue_unit,
                transaction_payment_number,
                transaction_ref,
                transaction_ref_code,
                transaction_channel_code,
                transaction_expires_at,
                transaction_note,
                transaction_status,
                transaction_timestamp,
                update_user,
                update_date,
                update_user_id,
                user_id,
                user_from_id,
                user_to_id
            FROM ( SELECT 'TOP UP'::text AS reftrans,
                        wallet_topup_transaction.topup_transaction_id AS transaction_id,
                        wallet_topup_transaction.topup_number AS transaction_number,
                        (wallet_topup_transaction.create_date AT TIME ZONE 'Asia/Jakarta'::text) AS transaction_date,
                        wallet_topup_transaction.topup_payment_method AS transaction_method,
                        wallet_topup_transaction.topup_payment_bank_name AS transaction_desc,
                        wallet_topup_transaction.topup_total_amount AS transaction_nettvalue,
                        'IDR'::text AS nettvalue_unit,
                        wallet_topup_transaction.topup_amount AS transaction_value,
                        'IDR'::text AS value_unit,
                        wallet_topup_transaction.topup_admin AS transaction_admin,
                        'IDR'::text AS adminvalue_unit,
                        wallet_topup_transaction.topup_payment_number AS transaction_payment_number,
                        wallet_topup_transaction.topup_payment_ref AS transaction_ref,
                        wallet_topup_transaction.topup_payment_ref_code AS transaction_ref_code,
                        wallet_topup_transaction.topup_payment_channel_code AS transaction_channel_code,
                        wallet_topup_transaction.topup_payment_expires_at AS transaction_expires_at,
                        wallet_topup_transaction.topup_notes AS transaction_note,
                        wallet_topup_transaction.topup_status AS transaction_status,
                        wallet_topup_transaction.topup_timestamp AS transaction_timestamp,
                        wallet_topup_transaction.update_user,
                        wallet_topup_transaction.update_date,
                        wallet_topup_transaction.update_user_id,
                        wallet_topup_transaction.user_id,
                        wallet_topup_transaction.user_id AS user_from_id,
                        wallet_topup_transaction.user_id AS user_to_id
                    FROM wallet_topup_transaction
                    UNION ALL
                    SELECT 'TRANSFER MEMBER - SEND'::text AS reftrans,
                        gold_transaction_gold_transfer.gold_transfer_id,
                        gold_transaction_gold_transfer.transfer_ref_number,
                        (gold_transaction_gold_transfer.transfer_member_datetime AT TIME ZONE 'Asia/Jakarta'::text) AS transaction_date,
                        'RECEIVER'::character varying AS refmethode,
                        gold_transaction_gold_transfer.user_to_name AS topup_payment_bank_name,
                        gold_transaction_gold_transfer.transfer_member_transfered_weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_transfer.transfer_member_gold_weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_transfer.transfer_member_admin_weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_transfer.phone_number,
                        gold_transaction_gold_transfer.user_to_name,
                        gold_transaction_gold_transfer.gold_transfer_number,
                        gold_transaction_gold_transfer.transfer_member_service_option,
                        gold_transaction_gold_transfer.transfer_member_datetime AS expires_at,
                        gold_transaction_gold_transfer.transfer_member_notes,
                        'SEND'::character varying AS status,
                        gold_transaction_gold_transfer.transfer_member_datetime AS topup_timestamp,
                        gold_transaction_gold_transfer.user_from_name AS update_user,
                        gold_transaction_gold_transfer.transfer_member_datetime AS update_date,
                        gold_transaction_gold_transfer.user_from_name AS update_user_id,
                        gold_transaction_gold_transfer.user_from_id,
                        gold_transaction_gold_transfer.user_from_id,
                        gold_transaction_gold_transfer.user_to_id
                    FROM gold_transaction_gold_transfer
                    UNION ALL
                    SELECT 'TRANSFER MEMBER - RECEIVED'::text AS reftrans,
                        gold_transaction_gold_transfer.gold_transfer_id,
                        gold_transaction_gold_transfer.transfer_ref_number,
                        (gold_transaction_gold_transfer.transfer_member_datetime AT TIME ZONE 'Asia/Jakarta'::text) AS transaction_date,
                        'SENDER'::character varying AS refmethode,
                        gold_transaction_gold_transfer.user_from_name AS topup_payment_bank_name,
                        gold_transaction_gold_transfer.transfer_member_transfered_weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_transfer.transfer_member_gold_weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_transfer.transfer_member_admin_weight,
                        'gr'::text AS nettvalue_unit,
                        ''::character varying AS phone_number,
                        gold_transaction_gold_transfer.user_from_name,
                        gold_transaction_gold_transfer.gold_transfer_number,
                        gold_transaction_gold_transfer.transfer_member_service_option,
                        gold_transaction_gold_transfer.transfer_member_datetime AS expires_at,
                        gold_transaction_gold_transfer.transfer_member_notes,
                        'RECEIVED'::character varying AS status,
                        gold_transaction_gold_transfer.transfer_member_datetime AS topup_timestamp,
                        gold_transaction_gold_transfer.user_from_name AS update_user,
                        gold_transaction_gold_transfer.transfer_member_datetime AS update_date,
                        gold_transaction_gold_transfer.user_from_name AS update_user_id,
                        gold_transaction_gold_transfer.user_to_id,
                        gold_transaction_gold_transfer.user_from_id,
                        gold_transaction_gold_transfer.user_to_id
                    FROM gold_transaction_gold_transfer
                    UNION ALL
                    SELECT 'GOLD - BUY'::text AS reftrans,
                        gold_transaction_gold_saving_buy.gold_transaction_id,
                        gold_transaction_gold_saving_buy.gold_buy_number,
                        gold_transaction_gold_saving_buy.transaction_date,
                        'BUY'::character varying AS refmethode,
                        ''::character varying AS topup_payment_bank_name,
                        gold_transaction_gold_saving_buy.weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_saving_buy.price,
                        'IDR'::text AS nettvalue_unit,
                        gold_transaction_gold_saving_buy.total_price,
                        'IDR'::text AS nettvalue_unit,
                        ''::character varying AS phone_number,
                        ''::character varying AS user_from_name,
                        ''::character varying AS gold_transfer_number,
                        ''::character varying AS transfer_member_service_option,
                        gold_transaction_gold_saving_buy.transaction_date AS expires_at,
                        ''::text AS transfer_member_notes,
                        gold_transaction_gold_saving_buy.status,
                        gold_transaction_gold_saving_buy.transaction_date AS topup_timestamp,
                        ''::character varying AS update_user,
                        gold_transaction_gold_saving_buy.transaction_date AS update_date,
                        ''::character varying AS update_user_id,
                        gold_transaction_gold_saving_buy.user_id,
                        gold_transaction_gold_saving_buy.user_id,
                        gold_transaction_gold_saving_buy.user_id
                    FROM gold_transaction_gold_saving_buy
                    UNION ALL
                    SELECT 'GOLD - SELL'::text AS reftrans,
                        gold_transaction_gold_saving_sell.gold_transaction_id,
                        gold_transaction_gold_saving_sell.gold_sell_number,
                        gold_transaction_gold_saving_sell.transaction_date,
                        'SELL'::character varying AS refmethode,
                        ''::character varying AS topup_payment_bank_name,
                        gold_transaction_gold_saving_sell.weight,
                        'gr'::text AS nettvalue_unit,
                        gold_transaction_gold_saving_sell.price,
                        'IDR'::text AS nettvalue_unit,
                        gold_transaction_gold_saving_sell.total_price,
                        'IDR'::text AS nettvalue_unit,
                        ''::character varying AS phone_number,
                        ''::character varying AS user_from_name,
                        ''::character varying AS gold_transfer_number,
                        ''::character varying AS transfer_member_service_option,
                        gold_transaction_gold_saving_sell.transaction_date AS expires_at,
                        ''::text AS transfer_member_notes,
                        gold_transaction_gold_saving_sell.status,
                        gold_transaction_gold_saving_sell.transaction_date AS topup_timestamp,
                        ''::character varying AS update_user,
                        gold_transaction_gold_saving_sell.transaction_date AS update_date,
                        ''::character varying AS update_user_id,
                        gold_transaction_gold_saving_sell.user_id,
                        gold_transaction_gold_saving_sell.user_id,
                        gold_transaction_gold_saving_sell.user_id
                    FROM gold_transaction_gold_saving_sell) unnamed_subquery
            ORDER BY transaction_date DESC, update_date DESC
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        contracts = [
            user_transaction.user_transaction_contract(**dict(zip(columns, row)))
            for row in rows
        ]
        # Implement pagination using Django default offset and limit
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 10))
        paged_contracts = contracts[offset : offset + limit]

        response_data = {
            "count": len(contracts),
            "offset": offset,
            "limit": limit,
            "results": user_transaction_serializer(paged_contracts, many=True).data,
        }
        return Response(response_data)
