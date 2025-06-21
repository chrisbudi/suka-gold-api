from django.core.management.base import BaseCommand
from core.domain.delivery import delivery_partner
from core.domain import delivery_partner_district, delivery_shipment_content
from concurrent.futures import ThreadPoolExecutor

from shared.services.external.delivery.sapx.sapx_service import SapxService


class Command(BaseCommand):
    help = "Seed data from a endpoint"

    def add_arguments(self, parser):
        parser.add_argument("--table", type=str, help="Specify the table name")

    def handle(self, *args, **kwargs):
        table = kwargs["table"]

        if table == "district":
            """get sapx district"""

            sapx_service = SapxService()
            data = sapx_service.get_district()
            batch_size = 100

            def seed_batch(batch):
                districts_to_create = [
                    delivery_partner_district(
                        delivery_partner_id=delivery_partner.objects.first(),
                        city_code=district["city_code"],
                        district_code=district["district_code"],
                        district_name=district["district_name"],
                        zone_code=district["zone_code"],
                        provinsi_code=district["provinsi_code"],
                        city_name=district["city_name"],
                        tlc_branch_code=district["tlc_branch_code"],
                        province_name=district["provinsi_name"],
                    )
                    for district in batch
                ]
                delivery_partner_district.objects.bulk_create(districts_to_create)
                print(f"Seeded batch with {len(batch)} districts")

            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(seed_batch, data[i : i + batch_size])
                    for i in range(0, len(data), batch_size)
                ]
                for future in futures:
                    future.result()
            print("Data seeded successfully")

        if table == "shipment_content":
            """get sapx shipment content"""

            sapx_service = SapxService()
            data = sapx_service.get_shipping_content()
            shipment_content_to_create = [
                delivery_shipment_content(
                    delivery_partner_id=delivery_partner.objects.first(),
                    shipment_type_code=shipment_content["shipment_type_code"],
                    shipment_content_code=shipment_content["shipment_content_code"],
                    shipment_content_name=shipment_content["shipment_content_name"],
                )
                for shipment_content in data
            ]
            delivery_shipment_content.objects.bulk_create(shipment_content_to_create)
            print("Data seeded successfully")
