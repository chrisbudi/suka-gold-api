# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
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
                enum=["gold_buy", "gold_sell", "gold_transfer", "order"],
                many=True,  # Allow multiple values
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
                       gb.gold_history_price_base,
                       gb.gold_buy_number AS ref_number,
                       'gold_buy' AS transaction_type
                FROM gold_transaction_gold_saving_buy gb

                UNION ALL

                SELECT gs.transaction_date,
                       gs.gold_transaction_id AS transaction_id,
                       gs.user_id,
                       gs.weight,
                       gs.price,
                       gs.gold_history_price_base,
                       gs.gold_sell_number AS ref_number,
                       'gold_sell' AS transaction_type
                FROM gold_transaction_gold_saving_sell gs

                UNION ALL

                SELECT gt.transfer_member_datetime AS transaction_date,
                       gt.gold_transfer_id AS transaction_id,
                       gt.user_from_id AS user_id,
                       NULL AS weight,
                       NULL AS price,
                       NULL AS gold_history_price_base,
                       gt.gold_transfer_number AS ref_number,
                       'gold_transfer' AS transaction_type
                FROM gold_transaction_gold_transfer gt

                UNION ALL

                SELECT og.order_timestamp AS transaction_date,
                       og.order_gold_id AS transaction_id,
                       og.user_id,
                       NULL AS weight,
                       NULL AS price,
                       NULL AS gold_history_price_base,
                       og.order_number AS ref_number,
                       'order' AS transaction_type
                FROM order_order_gold og
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
