import json

class ConfigDetails:
    mongo_db_name = None
    mongo_collection_name = None
    column_mapping = {}

class ConfigService:

    def get_table_config( table_name) -> ConfigDetails:
        config_details = ConfigDetails()
        file = open('./configs/mysql_to_mongo.json', 'r', encoding="ascii")
        table_config = json.load(file.read())[table_name]
        config_details.mongo_db_name = table_config['mongo_db_name']
        config_details.mongo_collection_name = table_config['mongo_collection_name']
        config_details.column_mapping = table_config['column_mapping']
        return config_details

