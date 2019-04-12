import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import sys
sys.path.append("./model")
import MysqlConn

date = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def run(code,path_url):
    try:
        argvs = sys.argv
        print(argvs)
        # email = argvs[1]
        email = "gtdad_flow_" + str(time.strftime("%Y%m%d")) + "_" + str(time.time())[-5:] + "@gtdunique.youzu.com"
        # password = argvs[1]
        password = 'password'
        url = 'http://v3m.gtarcade.com/?q='+code
        filename = './log/'+date+'loginTest.txt'
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option)
        driver = webdriver.Chrome(desired_capabilities=caps)
        # driver.maximize_window()
        # url = 'http://v3m.gtarcade.com/?q=5c98a8143666c6236284'
        driver.get(url)
        q_arr = url.split('=')
        q = q_arr[1]
        register_dom_type = 'id'
        register_dom_value = 'registerEmail'
        register_email = '//input[@'+register_dom_type+'="'+register_dom_value+'"]'
        driver.find_element_by_xpath(register_email).send_keys(email)
        time.sleep(2)

        register_dom_type = 'id'
        register_dom_value = 'password'
        register_password = '//input[@'+register_dom_type+'="'+register_dom_value+'"]'
        driver.find_element_by_xpath(register_password).send_keys(password)
        time.sleep(2)

        driver.find_element_by_xpath("//a[@id='registerPlayNow']").click()
        time.sleep(20)

        print(url)

        try:
            cururl = driver.current_url
        except Exception as e:
            # if url == cururl
            data = {
                'q': q,
                'is_success': 'success',
                'email': email,
                'msg': 'account already exists'
            }
            result = json.dumps(data)
            fp = open(filename, 'a+')
            fp.write(result + '\n')
            driver.close()
            exit('account already exists')

        logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]
        is_success = 'fail'
        callable_url = None
        for item in logs:
            if item['method'] == 'Network.responseReceived':
                params = item['params']
                response = params['response']
                if 'url' in response.keys():
                    url = response['url']
                    status = response['status']
                    if re.match(path_url+'/.*', url) and status >= 200:
                        print(url)
                        print(status)
                        callable_url = url
                        is_success = 'success'
        if callable_url is not None:
            data = {
                'q': q,
                'is_success': is_success,
                'email': email,
                'callable_url': callable_url,
                'status':status
            }

            result = json.dumps(data)
            fp = open(filename, 'a+')
            fp.write(result + '\n')
            driver.close()

    except Exception as e:
        data = {
            'email': email,
            'date':date,
            'code':code,
            'callable_url': path_url,
            'error_info':repr(e)
        }
        filename = './log/'+date+'error_log.txt'
        result = json.dumps(data)
        fp = open(filename, 'a+')
        fp.write(result + '\n')
        driver.close()
        # exit('参数错误' + repr(e))

a = MysqlConn.Connection()
code_sql = "select code,url from code_url"
a.execute(code_sql)
data = a.fetchall()
for value in data:
    code = value[0]
    url = value[1]
    run(code,url)
a.close()
