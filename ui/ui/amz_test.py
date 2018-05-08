from amazonapi import AmazonScraper


aso = AmazonScraper(locale="UK")

current_url = "https://www.amazon.com/dp/0545919738"
res = aso.scrape(current_url)

print("res:",res)