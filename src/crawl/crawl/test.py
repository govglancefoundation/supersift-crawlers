import os
import json
import uuid


file_name = '/Users/santiagosaldivar/Coding/govGlaceCrawler/src/crawl/crawl/urls_copy.json'

with open(file_name, encoding='utf-8') as data_file:
    data = json.load(data_file)
    keys = [key for key in data.keys()]
    for key in keys:
        for web_data in data[key]:
            robots_url=  web_data['website'] + '/robots.txt'
            web_data['robots_url'] = robots_url.replace('//robots.txt', '/robots.txt')

# create randomly named temporary file to avoid 
# interference with other thread/asynchronous request
tempfile = os.path.join(os.path.dirname(file_name), str(uuid.uuid4()))
print(tempfile)
with open(tempfile, 'w') as f:
    json.dump(data, f, indent=4)

# rename temporary file replacing old file
os.rename(tempfile, file_name)


# import time

# # documents = [f"document {i}" for i in range(1, 1000000001)]  # Simulating 1 billion documents


# start_time = time.time()
# # for i in range(1, 1000000):
# #     print(i)

# # items = [i*2 for i in range(1, 200000000)]
# # samplelist = [x**2 for x in range(int(20000000000000**0.5))]

# for x in range(int(20000000000000**0.5)):
#     print(x**2)
# # items = []
# # for i in range(1, 1000000):
# #     items.append(i)
# # print(items)
# # query = "document 999999999"
# # found = query in documents
# end_time = time.time()

# print(f"Search time: {end_time - start_time} seconds")