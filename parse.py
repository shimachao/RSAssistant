# -*-coding:UTF-8-*-

from bs4 import BeautifulSoup


def parse_out_form_hash(text):
    soup = BeautifulSoup(text, 'html5lib')
    a = soup.body.find('div', id='hd').\
        find('div', class_='wp').\
        find('div', class_='hdc cl').\
        find('div', id='um').\
        findAll('p')[0].findAll('a')[-1]

    href = a['href']
    index = href.rfind('=')
    form_hash = href[index+1:]

    return form_hash


if __name__ == '__main__':
    html = open('G:\Python\RSAssistant\sign.html', encoding='utf-8').read()
    r = parse_out_form_hash(html)
    print(r)
