import requests
import lxml.html
import pprint

LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'

def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

def init():
    html = requests.get(LOGIN_URL).text
    form = parse_form(html)
    pprint.pprint(form)
    '''
    {
        '_formkey': 'a466c92a-cb6e-4438-9041-4fd2a4697878',
        '_formname': 'login',
        '_next': '/',
        'email': '',
        'password': '',
        'remember_me': 'on'
    }
    '''
    # formkey 属性是这里的关键部分，服务器端使用这个唯一的ID来避免表单多次提交。
    # 每次加载网页时，都会产生不同的ID。
    # 然后服务器端就可以通过这个给定的ID来判断表单是否己经提交过。        

def first():
    LOGIN_URL = 'http://example.webscraping.com/user/login'
    LOGIN_EMAIL = 'example@webscraping.com'
    LOGIN_PASSWORD = 'example'
    data = {'email':LOGIN_EMAIL, 'password':LOGIN_PASSWORD}
    response = requests.post(LOGIN_URL, data=data)    
    print(response.url)

def second():
    html = requests.get(LOGIN_URL).text
    data = parse_form(html)
    data["email"] = LOGIN_EMAIL
    data["password"] = LOGIN_PASSWORD
    response = requests.post(LOGIN_URL, data=data)
    print(response.url)
    # http://example.webscraping.com/user/login
    # Still can not login
    
def third():
    r = requests.get(LOGIN_URL)
    cookie = r.cookies       # Get Cookie
    html = r.text            # Get Response Text
    data = parse_form(html)
    data["email"] = LOGIN_EMAIL
    data["password"] = LOGIN_PASSWORD
    response = requests.post(LOGIN_URL, data=data, cookies=cookie)
    print(response.url)
    # http://example.webscraping.com/
    # Login Successfully

def fourth():
    '''Use robot'''
    import robobrowser
    br = robobrowser.RoboBrowser()
    br.open(LOGIN_URL)
    form = br.get_form()
    form['email'] = LOGIN_EMAIL
    form['password'] = LOGIN_PASSWORD
    response = br.submit_form(form)
    br.open(COUNTRY_URL)
    form = br.get_form()
    form['population'] = str(int(form['population'].value) + 1)
    br.submit_form(form)

    
    
if __name__ == '__main__':
    fourth()