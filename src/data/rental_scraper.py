from collections import defaultdict
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from src.data.utils import get_project_root, load_config
from src.data.preprocessing import check_urls, get_contents, get_next_page


def main(base_url, country_code, areas, min_rent, max_rent, output_file):
    """Pipeline to scrape Malaysia rental lists from website
    roomz.asia. Append contents of valid rental lists to a dictionary,
    then write the data to a csv file.

    Parameters
    ----------
    areas : iterable
        Areas to scrape in Malaysia.
    """

    rental_dict = defaultdict(list)

    class Rental_Spider(scrapy.Spider):
        """Spider that crawls over multiple websites to scrape Malaysia
        rental data."""

        name = "rental_spider"
        start_urls = {base_url.format(country_code, area) for area in areas}

        def parse(self, response):
            """Check the contents of each url. If it is a valid url,
            append the contents to a dictionary. Repeat the same for
            the following pages until encounter an invalid url."""

            content = response.json()
            if check_urls(content) == "valid_urls":
                get_contents(content, rental_dict, country_code, min_rent, max_rent)
                next_page = get_next_page(response.url)
                yield scrapy.Request(url=next_page)

    process = CrawlerProcess()
    process.crawl(Rental_Spider)
    process.start()
    rental_df = pd.DataFrame(rental_dict)
    rental_df.to_csv(get_project_root().joinpath("data", output_file), index=False)


if __name__ == "__main__":
    conf = load_config("conf", "parameters", "data.yaml")
    main(
        base_url=conf["base_url"],
        country_code=conf["country_code"],
        areas=conf["areas"],
        min_rent=conf["min_rent"],
        max_rent=conf["max_rent"],
        output_file=conf["output_file"],
    )
