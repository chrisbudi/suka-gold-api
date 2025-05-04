# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .contracts import GoldTransactionContract
from .serializer import GoldTransactionContractSerializer


class GoldTransactionLogView(APIView):
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
                       gb.gold_buy_number AS ref_number
                FROM gold_transaction_gold_saving_buy gb

                UNION ALL

                SELECT gs.transaction_date,
                       gs.gold_transaction_id AS transaction_id,
                       gs.user_id,
                       gs.weight,
                       gs.price,
                       gs.gold_history_price_base,
                       gs.gold_sell_number AS ref_number
                FROM gold_transaction_gold_saving_sell gs

                UNION ALL

                SELECT gt.transfer_member_datetime AS transaction_date,
                       gt.gold_transfer_id AS transaction_id,
                       gt.user_from_id AS user_id,
                       NULL AS weight,
                       NULL AS price,
                       NULL AS gold_history_price_base,
                       gt.gold_transfer_number AS ref_number
                FROM gold_transaction_gold_transfer gt

                UNION ALL

                SELECT og.order_timestamp AS transaction_date,
                       og.order_gold_id AS transaction_id,
                       og.user_id,
                       NULL AS weight,
                       NULL AS price,
                       NULL AS gold_history_price_base,
                       og.order_number AS ref_number
                FROM order_order_gold og
            ) gt
            INNER JOIN user_user uu ON uu.id = gt.user_id
            ORDER BY gt.transaction_date DESC;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        contracts = [GoldTransactionContract(**dict(zip(columns, row))) for row in rows]

        serializer = GoldTransactionContractSerializer(contracts, many=True)
        return Response(serializer.data)
