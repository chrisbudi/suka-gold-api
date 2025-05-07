from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from reporting.api.serializers.gold_chart_serializer import (
    GoldChartDaysContractSerializer,
    GoldChartHoursContractSerializer,
)
from reporting.contracts.gold_chart import (
    GoldChartDailyContract,
    GoldChartWeeklyContract,
)
from ..serializers.gold_transaction_serializer import (
    GoldTransactionContractSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter


class GoldChartDailyView(APIView):
    def get(self, request):
        query = """            
            SELECT DISTINCT ON (DATE_TRUNC('hour', gp.timestamps)) 
                DATE_TRUNC('hour', gp.timestamps) AS hour,
                gp.gold_price_sell, gp.gold_price_buy
            FROM core_gold_price gp
            WHERE timestamps >= NOW() - INTERVAL '24 hours'
            ORDER BY DATE_TRUNC('hour', timestamps), timestamps DESC;
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        contracts = [GoldChartDailyContract(**dict(zip(columns, row))) for row in rows]
        return Response(GoldChartHoursContractSerializer(contracts, many=True).data)


class GoldChartWeeklyView(APIView):
    def get(self, request):
        query = """            
            SELECT DISTINCT ON (DATE(gp.timestamps)) 
                DATE(gp.timestamps) AS day,
                gold_price_sell, gold_price_buy,
                gp.timestamps
            FROM core_gold_price gp 
            WHERE gp.timestamps >= NOW() - INTERVAL '7 days'
            ORDER BY DATE(gp.timestamps), gp.timestamps DESC;
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        contracts = [GoldChartWeeklyContract(**dict(zip(columns, row))) for row in rows]
        return Response(GoldChartDaysContractSerializer(contracts, many=True).data)


class GoldChartMonthlyView(APIView):
    def get(self, request):
        query = """            
            SELECT DISTINCT ON (DATE(gp.timestamps)) 
                DATE(gp.timestamps) AS day,
                gold_price_sell, gold_price_buy,
                gp.timestamps
            FROM core_gold_price gp 
            WHERE gp.timestamps >= NOW() - INTERVAL '30 days'
            ORDER BY DATE(gp.timestamps), gp.timestamps DESC;
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            else:
                columns = []
                rows = []

        contracts = [GoldChartWeeklyContract(**dict(zip(columns, row))) for row in rows]
        return Response(GoldChartDaysContractSerializer(contracts, many=True).data)
