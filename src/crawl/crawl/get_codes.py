import json 
import requests
from datetime import datetime
import aiohttp
import asyncio
import re

# record current timestamp
start = datetime.now()


# for url in urls:
#     response = requests.get(url)
#     print(response.status_code)
 
# Asynchronous function to fetch data from a given URL using aiohttp
async def fetch_data(session, site_data):
    # Use 'session.get()' to make an asynchronous HTTP GET request
    try:
        async with session.get(site_data["robots_url"]) as response:
            # Return the JSON content of the response using 'response.json()'
            # return await response.status
            content = ((await response.text()).split('\n'))
            sitemap_url = []
            # print(content)
            for item in content:
                '''
                WE ONLY WANT TO SCRAPE THE STATUS CODES THAT ARE 200 AND 
                
                '''
                if 'sitemap' in item:

                    m = re.search(r'https?:\/\/(www\.)?[\w\-]+(\.[\w\-]+)+\/.*sitemap*\.(xml)', item)
                    if m:
                        url = m.group()
                        print(url)
                        sitemap_url.append({'url': url})

            site_data["sitemap_data"] = sitemap_url
            return site_data
    except:
        pass

# Asynchronous main function
async def main():
    # List of URLs to fetch data from
    urls = [
        
    ]

    with open('/Users/santiagosaldivar/Coding/govGlaceCrawler/src/crawl/crawl/urls_copy.json', encoding= 'utf-8') as data_file:
        data = json.load(data_file)
        keys = [item for item in data.keys()]

        '''
        I dont need to just pass the url, I can pass the entire dictionary and then select the url. Example//

        web_data
        '''
    # Create an aiohttp ClientSession for making asynchronous HTTP requests
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks, where each task is a call to 'fetch_data' with a specific URL
        for key in keys:
            tasks = [fetch_data(session, item) for item in data["science_magazines"]]
            # Use 'asyncio.gather()' to run the tasks concurrently and gather their results
            results = await asyncio.gather(*tasks)


    ''' 
    These results contain tuples of the url and their status code
    '''

    # data['science_magazines'] = results
    print(results)
    # print(data['science_magazines'])
    # print(len(data['science_magazines']))
    # data = json.load(data_file)
    '''
    The GOAL:

    - we need to itereate throuhg all of the 
    '''
    # keys = [item for item in data.keys()]
    # values = []
    # for key in keys:
    #     for web_data in data[key]:
    #         for result in results:
    #             web_data['code'] = result
    #         values.append(web_Data)

# Run the main function using 'asyncio.run()' if the script is executed
if __name__ == "__main__":
    asyncio.run(main())

print(datetime.now() - start)