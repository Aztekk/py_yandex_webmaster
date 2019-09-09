from py_yandex_webmaster import YandexWebmaster

TOKEN = 'AgAAAAARKO0UAAXDHMMrRUn-JkAtlv8f9goH42o'

yandex_webmaster = YandexWebmaster(token=TOKEN)

print('My Webmaster ID: ', yandex_webmaster.get_id)
