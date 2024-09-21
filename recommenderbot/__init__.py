
from spider import Spider
app = Spider()
params = {"css_extraction_map":{"/":[{"name":"paragraphs","selectors":["p"]}],"/blog":[{"name":"headings","selectors":["h1","h2","h3","h4"]}]}}
crawl_result = app.scrape('https://roadmap.sh/frontend', params=params)
print(crawl_result)