# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import psycopg2
from psycopg2 import errors

class CrawlPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name =='page_description':
                value = adapter[field_name]
                if isinstance(value, list):
                    value = [item.rstrip().lstrip() for item in value if item]
                    adapter[field_name] = ' '.join(value)
        return item


class WriteElectionArticles:

    def __init__(self):
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()
            self.table = 'supersift_engine'

    def check_item(self, item, spider):
        try:
            table = self.table
            self.cur.execute(f"""SELECT url FROM {table} WHERE url = '{item['url']}'""")
            results = [i[0] for i in self.cur.fetchall()]
            print(results)
            if results:
                pass
            else:
                return item
        except errors.UndefinedTable as e:
            # Handle the UndefinedTable exception here
            print(f"The table {table} does not exist.")
            pass

    def process_item(self, item, spider): # Here we are going to get a dictionary or dataframe and publish new data
        table_name = self.table
        try:
            columns = []

            """
            - Here we can add description if we do not have it in the key of items
            - We added a condition to look for created_at to add it as a timestamp with timezone for consistency 
            - 

            """
            columns.append("id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )")
            
            for key in item.keys():
                if key in ['created_at', 'signing_date']:
                    columns.append(f'{key} timestamp with time zone')
                elif key in ['phone_numbers', 'polling_info_urls', 'election_info', 'cycles', 'election_districts', 'election_years']:
                    columns.append(f"{key} JSONB")
                else:
                    if key != 'collection_name':
                        columns.append(f"{key} VARCHAR")

            # columns = [f"{key} VARCHAR" for key in item.keys()] # removed this code and made it so it looks for craeted at 
            
            '''
            These appends are gor the columns that every table will need like id, topic, and collected_at
            '''
            collection_name = table_name.title().replace('_', ' ')
            columns.append(f"""collection_name character varying COLLATE pg_catalog."default" DEFAULT '{collection_name}'::character varying""")

            columns.append(f"""CONSTRAINT {table_name}_pkey PRIMARY KEY (id)""")
            columns.append("collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP")
            columns.append("ts tsvector GENERATED ALWAYS AS (to_tsvector('english'::regconfig, title || ' ' || content)) STORED")

            # Constructing the full query
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            self.cur.execute(query)

            
            columns = ', '.join(item.keys())
            values = ', '.join('%({})s'.format(key) for key in item.keys())
            # values = ', '.join('%({})s'.format(key) if not 'references' else 'ARRAY[%({})s]::TEXT[]'.format(key) for key in item.keys())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            # print(query)
            self.cur.execute(query, item)
            print(f"page {item["title"]}: {item['url']} inserted to {table_name}")
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: ", e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()