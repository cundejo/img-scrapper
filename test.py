# from urllib2 import Request
# from urllib2 import HTTPError
#
# req = Request(url=r"http://rule34c.paheal.net/books/C83_Gerupin_Minazuki_Juuzou_Chousoku_Kankei_Gyro_Fucker/01",
#               headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
# try:
#     handler =
#     print handler
# except HTTPError as e:
#     content = e.read()


import urllib2

req = urllib2.Request(url=r"http://rule34c.paheal.net/books/C83_Gerupin_Minazuki_Juuzou_Chousoku_Kankei_Gyro_Fucker/01/",
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
response = urllib2.urlopen(req)
the_page = response.read()
print the_page