# views.py
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from reporting.contracts.gold_transaction_avg import GoldTransactionAVGContract
from ..serializers.gold_transaction_avg_serializer import (
    GoldTransactionAvgContractSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


class GoldTransactionAvgView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: GoldTransactionAvgContractSerializer(many=False),
        },
    )
    def get(self, request):
        # Apply filters
        user_id = request.query_params.get("user_id")

        # Use SQL parameters to prevent SQL injection
        query = """
            WITH ordered_tx AS (
            SELECT
                    gold_transaction_id,
                    TYPE AS tr_type,
                    weight,
                    price,
                    transaction_date,
                    user_id,
                    CASE WHEN type = 'buy' THEN weight ELSE weight * -1 END AS qty,
                    CASE WHEN TYPE = 'buy' THEN weight * price ELSE (weight * price * -1) END AS cost
                FROM gold_transactions
                WHERE user_id = %(user_id)s
                ORDER BY transaction_date
            ),
            cumulative AS (
                SELECT
                    transaction_date,
                    SUM(qty) OVER (ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_qty,
                    SUM(cost) OVER (ORDER BY transaction_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_cost
                FROM ordered_tx
            ),
            stock_avg AS (
                SELECT
                    *,
                    CASE
                        WHEN cum_qty > 0 THEN cum_cost / cum_qty
                        ELSE NULL
                    END AS avg_price
                FROM cumulative
            )
            SELECT
                current_gold_price.price AS current_gold_price,
                stock_avg.avg_price AS avg_saving_price,
                current_gold_price.price - stock_avg.avg_price AS diff,
                ((current_gold_price.price - stock_avg.avg_price) / stock_avg.avg_price) * 100 AS avg_pct
            FROM stock_avg
            JOIN (
                SELECT gold_price_buy AS price
                FROM core_gold_price 
                ORDER BY timestamps DESC
                LIMIT 1
                ) current_gold_price ON true
            ORDER BY stock_avg.transaction_date DESC
            LIMIT 1;

        """
        query_params = {"user_id": user_id}

        # Apply ordering

        with connection.cursor() as cursor:
            cursor.execute(query, query_params)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        if rows:
            contract = GoldTransactionAVGContract(**dict(zip(columns, rows[0])))
        else:
            # If no rows are returned, create an empty contract
            contract = GoldTransactionAVGContract(
                avg_pct=Decimal(0),
            )
        contracts = contract

        serializer = GoldTransactionAvgContractSerializer(contracts, many=False)
        return Response(serializer.data, status=200)
