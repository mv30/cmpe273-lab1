import json

class ConfigDetails:
    mongo_db_name = None
    mongo_collection_name = None
    column_mapping = {}

class ConfigService:

    @staticmethod
    def get_table_config( table_name) -> ConfigDetails:
        config_details = ConfigDetails()
        file = open('./configs/mysql_to_mongo.json', 'r', encoding="ascii")
        file_content = file.read()
        file.close()
        table_config = json.loads(file_content)[table_name]
        config_details.mongo_db_name = table_config['mongo_db_name']
        config_details.mongo_collection_name = table_config['mongo_collection_name']
        config_details.column_mapping = table_config['column_mapping']
        return config_details

    @staticmethod
    def get_json_object( table_config: ConfigDetails, col_names, col_values):
        json_object = {}
        for i in range(len(col_names)):
            col_name = col_names[i]
            col_value = col_values[i]
            json_tag = table_config.column_mapping[col_name]
            json_object[json_tag] = col_value
        return json_object

if __name__ == '__main__':
    table_config = ConfigService.get_table_config('student_temp')
    print(ConfigService.get_table_config('student_temp'))
    col_names = ['s_id', 'marks', 'name']
    col_values = [ 1, 100, 'Mayank']
    json_object = ConfigService.get_json_object( table_config, col_names, col_values)
    print(json_object)    

