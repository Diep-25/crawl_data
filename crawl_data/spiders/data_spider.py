import scrapy
import logging
import requests
from unidecode import unidecode
import re
from translate import Translator


class DataSpider(scrapy.Spider):
    name = "data_spider"

    telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
    telegram_chat_id = "YOUR_TELEGRAM_BOT_TOKEN"

    def __init__(self, url=None, keyword=None, limit=5, *args, **kwargs):
        super(DataSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            logging.warning("No URL provided. Parsing terminated.")
            self.start_urls = []
        self.keyword = unidecode(keyword.replace("-", " ")) if keyword else None
        self.limit = int(limit)
        self.article_count = 0
        self.tag_card = kwargs.get('tag_card', 'article')

    def send_to_telegram(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send message to Telegram: {e}")

    def translate_text(self, text):
        translator = Translator(from_lang='en', to_lang='vi')
        translation = translator.translate(text)
        return translation       

    def parse(self, response):
        articles = response.css(self.tag_card)

        for article in articles:
            title = article.css('h3 a::text').get()
            link = article.css('h3 a::attr(href)').get()

            if title:
                title_no_unidecode = title.strip().replace('\r', '').replace('\n', '')
                title = unidecode(title.strip().lower())
                title = re.sub(r'[^a-z0-9]+', ' ', title) 

                title_no_unidecode = self.translate_text(title_no_unidecode) 

            if title and (self.keyword is None or self.keyword.lower() in title.lower()):
                
                if title and link:
                    message = f"<a href='{response.urljoin(link)}'><b>{title_no_unidecode}</b></a>"
                    self.send_to_telegram(message)
                    yield {
                        'title': title_no_unidecode,
                        'link': response.urljoin(link),
                    }

                self.article_count += 1
                if self.article_count >= self.limit:
                    return

        if self.article_count < self.limit:
            next_page = response.css('a.pagination__next::attr(href)').get()
            logging.info(f"Next page: {next_page}")
            if next_page is not None:
                yield response.follow(next_page, self.parse)
