import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_html(url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    timeout = random.choice(range(80, 100))
    while True:
        try:
            response = requests.get(url, headers = header, timeout = timeout)
            response.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
        except socket.error as e:
            print(e)
            time.sleep(random.choice(range(0, 60)))
        except http.client.BadStatusLine as e:
            print(e)
            time.sleep(random.choice(range(30, 60)))
        except http.client.IncompleteRead as e:
            print(e)
            time.sleep(random.choice(range(20, 60)))
    return response.text

def data_output(data, filename):
    with open(filename, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

if __name__ == '__main__':
    
    url = 'https://movie.douban.com/top250?start=0'
    html = get_html(url)
    bs = BeautifulSoup(html, "html.parser")
    content = bs.find_all('div', {'class': 'info'})
    rank = 1
    for movie in content:
        result = []
        temp = []
        temp.append(rank)
        rank += 1
        for spa in movie.find_all('span','title'):
            temp.append(spa.text.replace('/', ''))
            print(spa.text.replace('/', ''))
            if len(movie.find_all('span','title')) == 1:
                temp.append(movie.find('span','other').text.replace('/', ''))
                print(movie.find('span','other').text.replace('/', ''))
        for spa in movie.find_all('span','rating_num'):
            temp.append(spa.text)
            print (spa.text)
        print (movie.find('p').text.strip())
        temp.append(movie.find('p').text.strip())
        a_tag = movie.find('a')
        temp.append(a_tag['href'])
        print(a_tag['href'])
        result.append(temp)
        data_output(result, 'Top25.csv')
        