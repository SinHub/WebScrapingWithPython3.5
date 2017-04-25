import requests
import lxml.html
import pprint
from PIL import Image
from io import BytesIO
import base64
import pytesseract

REGISTER_URL = 'http://example.webscraping.com/user/register'


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

def init():
    html = requests.get(REGISTER_URL).text
    form = parse_form(html)
    pprint.pprint(form)
    '''
    {
	'_formkey': '89b65f63-62fc-4b22-b40b-d3abeec6bcb7',
	'_formname': 'register',
	'_next': '/',
	'email': '',
	'first_name': '',
	'last_name': '',
	'password': '',
	'password_two': '',
	'recaptcha_response_field': None
    }

    '''
    return html

def get_captcha(html):
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

def first():
    # 如果提示winerror2 找不到文件，先检查是否安装了 tesseract-orc 引擎
    # 如果还是不行就添加全路径（可以在pytesseract.py中修改）
    # pytesseract.pytesseract.tesseract_cmd = 'E:\Program Files (x86)\Tesseract-OCR'
    html = requests.get(REGISTER_URL).text
    img = get_captcha(html)
    # 阈值化处理
    img.save('captcha_original.png')
    gray = img.convert('L')
    gray.save('captcha_gray.png')
    bw = gray.point(lambda x: 0 if x<1 else 255, '1')
    bw.save('captcha_thresholded.png')
    # 提交 tesseract 识别
    print(pytesseract.image_to_string(bw))
    return


if __name__ == '__main__':
    first()