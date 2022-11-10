import csv
import json

CSV_ADS = "ad.csv"
JSON_ADS = "ads.json"
CSV_CATEGORIES = "category.csv"
JSON_CATEGORIES = "categories.json"
CSV_LOCATION = "location.csv"
JSON_LOCATIONS = "locations.json"
CSV_USER = "user.csv"
JSON_USERS = "user.json"


def convert_to_json(csv_file, json_file, model_name):
    result_data = []

    with open(csv_file, encoding="utf-8") as csv_files:
        for row in csv.DictReader(csv_files):
            data_add = {"model": model_name, "pk": int(row["Id"] if "Id" in row else row["id"])}

            if "Id" in row:
                del row["Id"]
            else:
                del row["id"]

            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            if "price" in row:
                row["price"] = int(row["price"])

            if "author_id" and "category_id" in row:
                row["author_id"] = int(row["author_id"])
                row["category_id"] = int(row["category_id"])

            if "age" and "location_id" in row:
                row["age"] = int(row["age"])
                row["location_id"] = int(row["location_id"])

            data_add["fields"] = row
            result_data.append(data_add)

    with open(json_file, "w", encoding="utf-8") as json_files:
        json_files.write(json.dumps(result_data, ensure_ascii=False))


convert_to_json(CSV_ADS, JSON_ADS, "ads.ad")
convert_to_json(CSV_CATEGORIES, JSON_CATEGORIES, "ads.category")
convert_to_json(CSV_LOCATION, JSON_LOCATIONS, "users.location")
convert_to_json(CSV_USER, JSON_USERS, "users.user")
