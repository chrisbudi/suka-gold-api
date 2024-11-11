import csv
from django.core.management.base import BaseCommand
from concurrent.futures import ThreadPoolExecutor
from core.domain.address import (
    province,
    city,
    district,
    subdistrict,
    postal_code,
)


class Command(BaseCommand):
    help = "Seed data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("table", type=str, help="table that will be seeded")
        parser.add_argument("csv_file", type=str, help="The CSV file to load data from")
        parser.add_argument(
            "--separator",
            type=str,
            default=",",
            help='The CSV separator (default is ",")',
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        table = kwargs["table"]
        separator = kwargs["separator"]

        print(csv_file, table, separator, "csv_file, table separator")
        print(f"Seeding data... {table}")
        if table == "province":
            with open(csv_file, "r", newline="") as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    print(row, row.get("province_id", None), "row")
                    province.objects.create(
                        province_id=row.get("province_id"),
                        province_name=row.get("province_name"),
                    )
            print("Data seeded successfully")
        if table == "city":
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file, delimiter=separator)
                for row in reader:
                    city.objects.create(
                        city_id=row["city_id"],
                        city_name=row["city_name"],
                        province_id=row["province_id"],
                    )
            print("Data seeded successfully")
        if table == "district":
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file, delimiter=separator)
                for row in reader:
                    district.objects.create(
                        district_id=row["district_id"],
                        district_name=row["district_name"],
                        city_id=row["city_id"],
                    )
            print("Data seeded successfully")
        if table == "subdistrict":
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file, delimiter=separator)
                for row in reader:
                    subdistricts = []
                    count = 0
                    for row in reader:
                        subdistricts.append(
                            subdistrict(
                                subdistrict_id=row["subdistrict_id"],
                                subdistrict_name=row["subdistrict_name"],
                                district_id=row["district_id"],
                            )
                        )

                        if len(subdistricts) == 50:
                            count += 1
                            print(count)
                            subdistrict.objects.bulk_create(subdistricts)
                            subdistricts = []
                    if subdistricts:
                        subdistrict.objects.bulk_create(subdistricts)
            print("Data seeded successfully")
        if table == "postal_code":
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file, delimiter=separator)
                count = 0
                postal_codes = []

                def bulk_insert(postal_codes):
                    postal_code.objects.bulk_create(postal_codes)

                with ThreadPoolExecutor(max_workers=5) as executor:
                    for row in reader:
                        postal_codes.append(
                            postal_code(
                                postal_code_id=row["postal_code_id"],
                                subdistrict_id=row["subdistrict_id"],
                                district_id=row["district_id"],
                                city_id=row["city_id"],
                                province_id=row["province_id"],
                                post_code=row["post_code"],
                            )
                        )
                        if len(postal_codes) >= 0:
                            count += 1
                            print(count)
                            executor.submit(bulk_insert, postal_codes)
                            postal_codes = []
                    if postal_codes:
                        executor.submit(bulk_insert, postal_codes)
            print("Data seeded successfully")
