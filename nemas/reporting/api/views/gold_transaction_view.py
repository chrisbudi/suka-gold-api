# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from reporting.contracts.gold_transaction_avg import GoldTransactionAVGContract
from reporting.contracts.gold_transaction import GoldTransactionContract
from ..serializers.gold_transaction_serializer import (
    GoldTransactionContractSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


class GoldTransactionLogView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="start_date",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="end_date",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="order_by",
                required=False,
                type=str,
                enum=["transaction_date", "user_id", "weight", "price"],
            ),
            OpenApiParameter(
                name="transaction_type",
                required=False,
                type=str,
                enum=[
                    "gold_buy",
                    "gold_sell",
                    "gold_transfer_send",
                    "gold_transfer_receive",
                    "order_buy",
                    "order_redeem",
                    "disburst",
                    "topup",
                ],
                many=True,
                style="form",
                explode=True,
            ),
            OpenApiParameter(
                name="order_direction",
                required=False,
                type=str,
                enum=["ASC", "DESC"],
            ),
            OpenApiParameter(
                name="fetch",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="offset",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: GoldTransactionContractSerializer(many=True),
        },
    )
    def get(self, request):
        query = """
            SELECT uu.email, uu.id AS user_id, uu.user_name, gt.*
            FROM (
                SELECT gb.transaction_date,
                       gb.gold_transaction_id AS transaction_id,
                       gb.user_id,
                       gb.weight,
                       gb.price,
                       0 AS admin_price,
                       0 AS admin_weight,
                       gb.gold_history_price_base,
                       gb.gold_buy_number AS ref_number,
                       'gold_buy' AS transaction_type,
                       '' AS user_from,
                	   '' AS user_to,
					   0.0 AS transfered_weight,
					   0.0 AS transfered_admin_weight
                FROM gold_transaction_gold_saving_buy gb
                UNION ALL
                SELECT gs.transaction_date,
                       gs.gold_transaction_id AS transaction_id,
                       gs.user_id,
                       gs.weight,
                       gs.price,
                       0 AS admin_price,
                       0 AS admin_weight,
                       gs.gold_history_price_base,
                       gs.gold_sell_number AS ref_number,
                       'gold_sell' AS transaction_type,
                       '' AS user_from,
                	   '' AS user_to,
					   0.0 AS transfered_weight,
					   0.0 AS transfered_admin_weight
                FROM gold_transaction_gold_saving_sell gs
                UNION ALL
                SELECT gt.transfer_member_datetime AS transaction_date,
                       gt.gold_transfer_id AS transaction_id,
                       gt.user_from_id AS user_id,
					   gt.transfer_member_gold_weight AS weight,
                       gt.transfer_member_amount_received AS price,
                       0 AS admin_price,
                       gt.transfer_member_admin_weight AS admin_weight,
                       NULL AS gold_history_price_base,
                       gt.gold_transfer_number AS ref_number,
                       'gold_transfer_send' AS transaction_type,
                	   user_from_name AS user_from,
                	   user_to_name AS user_to,
                	   gt.transfer_member_gold_weight AS transfered_weight,
                	   gt.transfer_member_admin_weight AS transfered_admin_weight
                FROM gold_transaction_gold_transfer gt
                UNION ALL
                SELECT gt.transfer_member_datetime AS transaction_date,
                       gt.gold_transfer_id AS transaction_id,
                       gt.user_to_id AS user_id,
                       gt.transfer_member_gold_weight AS weight,
                       gt.transfer_member_amount_received AS price,
                       0 AS admin_price,
                       gt.transfer_member_admin_weight AS admin_weight,
                       NULL AS gold_history_price_base,
                       gt.gold_transfer_number AS ref_number,
                       'gold_transfer_receive' AS transaction_type,
                	   user_from_name AS user_from,
                	   user_to_name AS user_to,
                	   gt.transfer_member_gold_weight AS transfered_weight,
                	   gt.transfer_member_admin_weight AS transfered_admin_weight
                FROM gold_transaction_gold_transfer gt
                UNION ALL
                SELECT og.order_timestamp AS transaction_date,
                       og.order_gold_id AS transaction_id,
                       og.user_id,
                       og.order_item_weight AS weight,
                       og.order_grand_total_price AS price,
                       og.order_admin_amount AS admin_price,
                       0 AS admin_weight,
                       NULL AS gold_history_price_base,
                       og.order_number AS ref_number,
                       'order_buy' AS transaction_type,
					   '' AS user_from,
                	   '' AS user_to,
					   0.0 AS transfered_weight,
					   0.0 AS transfered_admin_weight
                FROM order_order_gold og
                WHERE og.order_type = 'buy'
                UNION ALL
                SELECT ogr.order_timestamp AS transaction_date,
                       ogr.order_gold_id AS transaction_id,
                       ogr.user_id,
                       ogr.order_item_weight AS weight,
                       ogr.order_grand_total_price AS price,
                       ogr.order_admin_amount AS admin_amount,
                       0 AS admin_weight,
                       NULL AS gold_history_price_base,
                       ogr.order_number AS ref_number,
                       'order_redeem' AS transaction_type,
                        '' AS user_from,
                	   '' AS user_to,
					   0.0 AS transfered_weight,
					   0.0 AS transfered_admin_weight
                FROM order_order_gold ogr 
                WHERE ogr.order_type = 'redeem'
                UNION ALL
                SELECT 
                	wdt.disburst_timestamp AS transaction_date,
                	wdt.disburst_transaction_id AS transaction_id,
                	wdt.user_id, 
                	NULL AS weight,
                	wdt.disburst_amount AS price,
                	wdt.disburst_admin  AS admin_price,
                	0 AS admin_weight,
                	NULL AS gold_history_price_base,
                	wdt.disburst_number AS ref_number,
                	'disburst' AS transaction_type,
                	'' AS user_from,
            	    '' AS user_to,
				    0.0 AS transfered_weight,
				    0.0 AS transfered_admin_weight
                FROM wallet_disburst_transaction wdt  
                WHERE 1=1
               UNION ALL
               SELECT 
	            	wtt.topup_timestamp  AS transaction_date,
	            	wtt.topup_transaction_id  AS transaction_id ,
	            	wtt.user_id ,
	            	NULL AS weight,
	            	wtt.topup_amount AS price,
	            	wtt.topup_admin AS admin_price,
	            	0 AS admin_weight,
	            	NULL AS gold_history_price_base,
	            	wtt.topup_number AS ref_number,
	            	'topup' AS transaction_type,
	            	'' AS user_from,
                	'' AS user_to,
					0.0 AS transfered_weight,
					0.0 AS transfered_admin_weight
	            FROM wallet_topup_transaction wtt   
            ) gt
            INNER JOIN user_user uu ON uu.id = gt.user_id
        """

        # Apply filters
        user_id = request.query_params.get("user_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        order_by = request.query_params.get("order_by", "transaction_date")
        order_direction = request.query_params.get("order_direction", "DESC")
        # Accept multiple transaction_type values
        transaction_types = request.query_params.getlist("transaction_type")

        filters = []
        if user_id:
            filters.append(f"uu.id = '{user_id}' ")
        if start_date:
            filters.append(f"gt.transaction_date >= '{start_date}'")
        if end_date:
            filters.append(f"gt.transaction_date <= '{end_date}'")

        if transaction_types:
            types_str = ", ".join(f"'{t}'" for t in transaction_types)
            filters.append(f"gt.transaction_type IN ({types_str})")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Apply ordering
        query += f" ORDER BY {order_by} {order_direction}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        # Apply pagination
        fetch = int(request.query_params.get("fetch", 10))
        offset = int(request.query_params.get("offset", 0))
        paginated_rows = rows[offset : offset + fetch]

        contracts = [
            GoldTransactionContract(**dict(zip(columns, row))) for row in paginated_rows
        ]

        serializer = GoldTransactionContractSerializer(contracts, many=True)
        return Response(
            {
                "count": len(rows),
                "results": serializer.data,
            }
        )
