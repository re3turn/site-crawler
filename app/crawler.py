#!/usr/bin/python3

import logging
import re
import time
from typing import List, Any

import requests
from slack_sdk.webhook import WebhookClient

from app.env import Env
from app.log import Log


class Crawler:
    def __init__(self):
        slack_webhook_url = Env.get_environment('SLACK_WEBHOOK_URL', required=True)
        self.slack_webhook = WebhookClient(slack_webhook_url)

        target_urls: str = Env.get_environment('TARGET_URLS', required=True)
        self.target_url_list: List[str] = [url for url in target_urls.split(',')]

        scraping_words: str = Env.get_environment('SCRAPING_WORDS', required=True)
        self.regex_list: List[Any] = [re.compile(f'.*${word}.*') for word in scraping_words.split(',')]

    def crawling_site(self, target_url: str, regex: Any) -> None:
        html = requests.get(target_url)
        if regex.match(html.text):
            self._send_slack(target_url)

    def _send_slack(self, target_url: str):
        self.slack_webhook.send(
            text="探しものが見つかったよ🔎",
            blocks=[{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "探しものが見つかったよ🔎"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "サイトを開く",
                        "emoji": True
                    },
                    "url": target_url
                }
            }],
        )

    def main(self) -> None:
        interval_minutes: int = int(Env.get_environment('INTERVAL', default='5'))

        while True:
            try:
                for i, url in enumerate(self.target_url_list):
                    self.crawling_site(url, self.regex_list[i])
            except Exception as e:
                logger.exception(f'Crawling error exception={e.args}')

            logger.info(f'Interval. sleep {interval_minutes} minutes.')
            time.sleep(interval_minutes * 60)


logger: logging.Logger = logging.getLogger(__name__)

if __name__ == '__main__':
    Log.init_logger(log_name='crawler')
    logger = logging.getLogger(__name__)
    crawler = Crawler()
    crawler.main()
