from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options

SLEEP_TIME = 3


def sign(username, password):
    global SLEEP_TIME

    def click(xpath, find_way=By.XPATH):
        time.sleep(SLEEP_TIME)
        try:
            print(f"current_url:{driver.title}\t{driver.current_url}")
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((find_way, xpath))
            )
            element.click()
        except Exception as e:  # TimeoutException
            print("error")
            raise e
        return element

    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 绕过js检测
    # 在chrome79版本之后，上面的实验选项已经不能屏蔽webdriver特征了
    # 屏蔽webdriver特征
    options.add_argument("--disable-blink-features")
    options.add_argument('--log-level=3')

    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    home_url = "https://xmuxg.xmu.edu.cn/login#"
    driver.get(home_url)

    sign_xpath = '//*[@id="loginLayout"]/div[3]/div[2]/div/button[2]'
    click(sign_xpath)

    input_username = '//*[@id="username"]'
    input_password = '//*[@id="password"]'
    submit = '//*[@id="casLoginForm"]/p[4]/button'

    health = '//*[@id="mainPage-page"]/div[1]/div[3]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]'
    table = '//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]'
    select = '//*[@id="select_1582538939790"]/div/div'
    yes = '/html/body/div[8]/ul/div/div[3]/li/label'
    save = '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/span/span'

    click(input_username).send_keys(username)
    click(input_password).send_keys(password)
    click(submit)
    click(health)
    time.sleep(SLEEP_TIME)
    driver.switch_to.window(driver.window_handles[-1])

    click(table)
    e = click(select)

    if not is_sign(e):
        click(yes)
        click(save)
        driver.switch_to.alert.accept()
        driver.refresh()
        click(table)
        e = click(select)
        assert is_sign(e)

    print('finished')
    driver.quit()
    return driver


def is_sign(e):
    print(f'\n\n{datetime.now()}')
    if '请选择' in e.text:
        print('\n' + '=' * 20 + "未打卡" + '=' * 20 + '\n')
        return False
    else:
        print('\n' + '=' * 20 + "已打卡" + '=' * 20 + '\n')
        return True
