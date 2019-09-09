import requests
import pandas as pd
from pandas.io.json import json_normalize


class YandexWebmaster(object):
    """
    Класс для работы с Yandex Webmaster
    """
    _WEBMASTER_URL = "https://api.webmaster.yandex.net/v4/user/"  # ссылка API Яндекс.Вебмастер
    token = None

    def __init__(self, token):
        """
        Инициализация объекта класса. Требуется токен.
        """
        self.token = token

    def get_header(self):
        """
        Генерирует заголовок с данными авторизации.
        """
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }

    @property
    def get_id(self):
        """
        Получить ID
        """
        url = self._WEBMASTER_URL
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        return response.json()['user_id']

    def get_host(self):
        """
        Получить ID хостов
        """
        url = self._WEBMASTER_URL + str(self.get_id) + '/hosts/'
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        return pd.DataFrame(response.json()['hosts'])

    def get_site_stat(self, site):
        """
        Получить статистику по сайту
        :params:
        site: строка с адресом сайта
        """
        host = self.get_host()
        host = host[host['unicode_host_url'] == site]['host_id'].values
        host = str(host)[2:-2]
        url = self._WEBMASTER_URL + str(self.get_id) + '/hosts/' + host + '/summary/'
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        result = response.json()
        return result

    def get_queries(self, site):
        host = self.get_host()
        host = host[host['unicode_host_url'] == site]['host_id'].values
        host = str(host)[2:-2]
        url = self._WEBMASTER_URL + str(
            self.get_id) + "/hosts/" + host + "/search-queries/popular/" \
                                              "?order_by=TOTAL_SHOWS" \
                                              "&query_indicator=AVG_SHOW_POSITION" \
                                              "&query_indicator=TOTAL_SHOWS" \
                                              "&query_indicator=TOTAL_CLICKS"
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        response = response.json()
        result = json_normalize(response['queries'])
        result['date_from'] = pd.to_datetime(response['date_from'])
        result['date_to'] = pd.to_datetime(response['date_to'])
        result.columns = ['avg_page_position', 'clicks', 'impressions', 'id', 'query', 'date_from', 'date_to']
        result = result[['query', 'avg_page_position', 'impressions', 'clicks', 'date_from', 'date_to']]
        return result
