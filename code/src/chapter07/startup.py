import requests
import lxml.html
import pprint
from PIL import Image
from io import BytesIO
import base64
import pytesseract
import string

REGISTER_URL = 'http://example.webscraping.com/user/register'


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

def extract_image(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    # 移除数据类型前缀
    img_data = img_data.partition(',')[-1]
    # 使用Base64解码图像数据，回到最初的二进制格式
    binary_img_data = base64.b64decode(img_data.encode('ascii'))
    # 使用 BytesIO 对这个二进制数据进行了封装
    file_like = BytesIO(binary_img_data)
    # Image类需要一个类似文件的接口
    img = Image.open(file_like)
    return img

def ocr(img):
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x<1 else 255, '1')
    word = pytesseract.image_to_string(bw)
    ascii_word = ''.join(c for c in word if c in string.ascii_letters).lower()
    return ascii_word



def register(first_name, last_name, email, password):
    response = requests.get(REGISTER_URL)
    html = response.text
    cookie = response.cookies
    form = parse_form(html)
    form['first_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = password
    img = extract_image(html)
    captcha = ocr(img)
    form['recaptcha_response_field'] = captcha
    response = requests.post(REGISTER_URL, data=form)
    success = '/user/register' not in response.url
    print(success)
    return success



if __name__ == '__main__':
    register('Micheal','Jordan','M11@126112.com','123123131')