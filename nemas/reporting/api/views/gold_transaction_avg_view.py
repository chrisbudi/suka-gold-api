# views.py
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
            WITH
            avg_buy AS (
                SELECT
                    SUM(gb.weight * gb.gold_history_price_buy)::decimal / NULLIF(SUM(gb.weight), 0) AS avg_buy_price
                FROM gold_transaction_gold_saving_buy gb
                WHERE (%(user_id)s IS NULL OR gb.user_id = %(user_id)s)
            ),
            avg_sell AS (
                SELECT
                    SUM(weight * gs.gold_history_price_sell)::decimal / NULLIF(SUM(gs.weight), 0) AS avg_sell_price
                FROM gold_transaction_gold_saving_sell gs
                WHERE (%(user_id)s IS NULL OR gs.user_id = %(user_id)s)
            ),
            latest_price AS (
                SELECT gold_price_buy AS current_gold_price_buy,
                    gold_price_sell AS current_gold_price_sell
                FROM core_gold_price cgp 
                ORDER BY cgp.timestamps DESC
                LIMIT 1
            )
            SELECT
                %(user_id)s AS user_id,
                lp.current_gold_price_buy, 
                lp.current_gold_price_sell,
                ab.avg_buy_price,
                asell.avg_sell_price,
                lp.current_gold_price_sell / asell.avg_sell_price * 100 AS percentage_from_sell,
                lp.current_gold_price_buy / ab.avg_buy_price * 100 AS percentage_from_buy
            FROM latest_price lp
            CROSS JOIN avg_buy ab
            CROSS JOIN avg_sell asell
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
                user_id=user_id or "",
                current_gold_price_buy=0,
                current_gold_price_sell=0,
                avg_buy_price=0,
                avg_sell_price=0,
                percentage_from_sell=0,
                percentage_from_buy=0,
            )
        contracts = contract

        print(contracts)

        serializer = GoldTransactionAvgContractSerializer(contracts, many=False)
        return Response(serializer.data, status=200)
