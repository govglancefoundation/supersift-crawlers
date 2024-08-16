import json

urls = []
results = [('https://www.newscientist.com/robots.txt', 200), ('https://www.scientificamerican.com/robots.txt', 200), ('https://www.nationalgeographic.com/robots.txt', 200), ('https://www.popsci.com/robots.txt', 200), ('https://www.discovermagazine.com/robots.txt', 200), ('https://www.smithsonianmag.com/robots.txt', 200), ('https://www.science.org/robots.txt', 200), ('https://www.nature.com/robots.txt', 200), ('https://www.thelancet.com/robots.txt', 200), ('https://www.cell.com/robots.txt', 200), ('https://www.nature.com/ncomms/robots.txt', 404), ('https://www.science.org/journal/sciadv/robots.txt', 403), ('https://journals.plos.org/plosone/robots.txt', 404), ('https://www.pnas.org/robots.txt', 200), ('https://bqic.berkeley.edu/robots.txt', 404), ('https://jqi.umd.edu/robots.txt', 200), ('https://quantum.ustc.edu.cn/robots.txt', 404), ('https://quantum.uchicago.edu/robots.txt', 200), ('https://www.mobile.ifi.lmu.de/robots.txt', 200), ('https://www.jhu.edu/robots.txt', 200), ('https://www.ucl.ac.uk/robots.txt', 200), ('https://www.mit.edu/robots.txt', 200), ('https://neurosciences.ucsd.edu/robots.txt', 404), ('https://neuro.hms.harvard.edu/robots.txt', 404), ('https://www.u-tokyo.ac.jp/en/robots.txt', 404), ('https://www.mit.edu/robots.txt', 200), ('https://uwaterloo.ca/robots.txt', 404), ('https://ethz.ch/en.html/robots.txt', 404), ('https://www.stanford.edu/robots.txt', 200), ('https://bcmp.hms.harvard.edu/robots.txt', 404), ('https://biology.stanford.edu/robots.txt', 200), None, ('https://www.bioc.cam.ac.uk/robots.txt', 200), ('https://mcdb.yale.edu/robots.txt', 200), ('https://www.mpg.de/en/robots.txt', 404), ('https://www.caltech.edu/robots.txt', 200), ('https://www.cam.ac.uk/research/robots.txt', 404), ('https://www.ox.ac.uk/research/robots.txt', 404), ('https://www.nus.edu.sg/research/robots.txt', 200), ('https://www.britishmuseum.org/robots.txt', 200), ('https://www.theacropolismuseum.gr/en/robots.txt', 403), ('https://americanhistory.si.edu/robots.txt', 200), ('https://www.mna.inah.gob.mx/robots.txt', 404), ('http://en.chnmuseum.cn/robots.txt', 404), None, ('https://www.apartheidmuseum.org/robots.txt', 200), ('https://www.louvre.fr/en/robots.txt', 404), ('https://www.rijksmuseum.nl/en/robots.txt', 404), ('https://www.metmuseum.org/robots.txt', 200), ('https://www.museodelprado.es/en/robots.txt', 500), ('https://www.uffizi.it/en/robots.txt', 200), ('https://www.ngv.vic.gov.au/robots.txt', 200), ('https://zeitzmocaa.museum/robots.txt', 200), ('https://airandspace.si.edu/robots.txt', 200), ('https://www.deutsches-museum.de/en/robots.txt', 404), ('https://www.scienceandindustrymuseum.org.uk/robots.txt', 405), ('https://www.sstm.org.cn/kjg_Web/html/kjg_english/portal/index/index.htm/robots.txt', 200), ('https://www.sea.museum/robots.txt', 200), ('https://www.kopernik.org.pl/en/robots.txt', 404), ('https://www.nemosciencemuseum.nl/en/robots.txt', 404)]

with open('/Users/santiagosaldivar/Coding/govGlaceCrawler/src/crawl/crawl/urls_copy.json', encoding= 'utf-8') as data_file:
        data = json.load(data_file)
        keys = [item for item in data.keys()]
        for key in keys[:10]:
            for web_data in (data[key]):
                urls.append(web_data['robots_url'])


'''
Use this code to append the dictionary with the status_codes so we know which robots txt exists and which do not
'''
keys = [item for item in data.keys()] # We are getting a list of keys that exist in the data



data_with_codes = [] # We are initializing an empty list to collect the data (This may not be the best approach since we need to keep a running list of all the urls that are valid)


for key in keys:    # We iterate through all the keys
    for web_dat in data[key]:   # We look at websites to scrape
        for result in results: 
            if result:
                if web_dat['robots_url'] == result[0]:
                    web_dat['status'] = result[1]
                    data_with_codes.append(web_dat)
for data_codes in data_with_codes:
    if data_with_codes['codes'] == 200:
        print(data_with_codes)


