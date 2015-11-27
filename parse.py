# -*-coding:UTF-8-*-

from bs4 import BeautifulSoup, SoupStrainer
import re


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


def parse_out_gold_num(text):
    """ 解析出获得的金币数量
    :param text: 包含获得金币数量的xml文档字符串
    :return: 字符数量 int
    """
    soup = BeautifulSoup(text, 'html5lib')
    only_div_with_class_c = SoupStrainer(name='div', attrs={'class':'c'})
    says = soup.find(only_div_with_class_c).get_text()

    re_pattern = re.compile('金币\s*(\d{1,2})')
    r = re.search(pattern=re_pattern, string=says)
    gold_num = r.group(1)

    return gold_num

if __name__ == '__main__':
    html = open('G:\Python\RSAssistant\sign.html', encoding='utf-8').read()
    r = parse_out_form_hash(html)
    print(r)

    xml = '''<?xml version="1.0" encoding="utf-8"?>
            <root><![CDATA[<script type="text/javascript" reload="1">
            setTimeout("window.location.href='plugin.php?id=dsu_paulsign:sign'", 3000);
            </script>
            <div class="f_c">
            <h3 class="flb">
            <em id="return_win">签到提示</em>
            <span>
            <a href="javascript:;" class="flbc" onclick="hideWindow('qwindow')" title="关闭">关闭</a></span>
            </h3>
            <div class="c">
            恭喜你签到成功!获得随机奖励 金币 5 . </div>
            </div>
            ]]></root>'''
    n = parse_out_gold_num(xml)
    print('金币数为:', n)
