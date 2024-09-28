from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime
import re
import time
import configparser
import platform

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
username = config['selenium']['username']
password = config['selenium']['password']
coef = int(config['selenium']['counts_coef'])

debug = not (platform.system() == "Linux")

driver = None
if debug:
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.edge.options import Options
    # # 设置无头edge浏览器
    edge_options = Options()
    edge_options.add_argument("--headless")  # 无头模式
    edge_options.add_argument("--no-sandbox")  # 解决DevToolsActivePort文件不存在的报错
    edge_options.add_argument("--disable-dev-shm-usage")  # 共享内存
    edge_options.add_argument('--disable-gpu')  # 禁用GPU加速
    edge_options.add_argument('--window-size=2560,1080') 
    edge_options.binary_location = "/Applications/Microsoft Edge Canary.app/Contents/MacOS/Microsoft Edge Canary"

    # 启动浏览器
    service = Service('/Users/kzz6991/msedgedriver')  # 替换为edgedriver的实际路径
    driver = webdriver.Edge(service=service, options=edge_options)
else:
    # # 设置无头chrome浏览器
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("user-agent=" + user_agent)
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument("--disable-dev-shm-usage")  # 共享内存
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--window-size=2560,1080') 

    # 启动浏览器
    service = Service('/usr/local/bin/chromedriver')  # 替换为chromedriver的实际路径
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(driver.execute_script("return navigator.userAgent;"))

# 打开你想要测试的页面
driver.get("https://api.wlai.vip/home")

def set_key_string(string = 'sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d'):
    # 等待 <input> 元素加载完成
    input_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.semi-input.semi-input-default'))
    )

    # 输入字符串到 <input> 元素
    input_element.send_keys(string)


def get_balance(driver,api_key = 'sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d'):
    result = -1
    # 获取当前网址
    current_url = driver.current_url
    # 检查网址是否以特定字符串开头
    if current_url.startswith("https://chaxun.wlai.vip/"):
        new_print("当前网址以 https://chaxun.wlai.vip/ 开头。")
    else:
        new_print("当前网址不以 https://chaxun.wlai.vip/ 开头。")
        driver.get('https://chaxun.wlai.vip/')
        time.sleep(0.2)
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "semi-table-tbody"))
        )
    set_key_string(api_key)
    # 等待按钮元素加载完成并点击
    button_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'semi-button'))
    )
    button_element.click()

    try:
        # 等待通知出现
        toast_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Toastify__toast--success'))
        )
        
        # 检查通知内容
        toast_text = toast_element.find_element(By.CSS_SELECTOR, 'div.Toastify__toast-body').text
        new_print(f'通知内容: {toast_text}')

        # 等待总额元素出现并获取其文本
        total_amount_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.semi-tag-content'))
        )
        total_amount_text = total_amount_element.text
        # new_print(f'总额信息: {total_amount_text}')


        # 解析总额文本内容中的数字
        match = re.search(r'\$([0-9.]+)', total_amount_text)
        if match:
            amount_str = match.group(1)
            amount = float(amount_str)
            result = amount * 100
            new_print(f'总额乘以100后的结果: {result}')
        else:
            new_print('未找到总额信息中的金额')
    except:
        new_print("未找到通知元素")
    return result

def new_print(text):
    print(text)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间戳
    log_entry = f"{timestamp} - {text}"  # 格式化日志条目

    with open("log.txt", 'a', encoding='utf-8') as file:
        file.write(log_entry + '\n')  # 在字符串后加换行符
        
def login(driver):
    driver.get("https://api.wlai.vip/home")
    time.sleep(1)
    try:
        # 查找按钮元素
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-textPrimary') and text()='关闭']"))
        )
        # 点击按钮
        button.click()
        new_print("按钮已点击。")
    except Exception as e:
        new_print(f"出现异常：{e}")
    try:
        # 等待按钮元素出现，最多等待10秒
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'MuiButton-containedPrimary') and text()='登入']"))
        )
        # 点击链接
        login_link.click()
        new_print("已点击登入链接。")
    except Exception as e:
        new_print(f"出现异常：{e}")
    try:
        # 等待输入框出现，最多等待10秒
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "outlined-adornment-username-login"))
        )
        # 输入账号
        username_input.send_keys(username)
        new_print("已输入账号。")
        
        # 等待密码输入框出现，最多等待10秒
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "outlined-adornment-password-login"))
        )
        # 输入密码
        password_input.send_keys(password)
        new_print("已输入密码。")
        
        # 等待登录按钮出现并点击，最多等待10秒
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='登录']"))
        )
        # 点击登录按钮
        login_button.click()
        new_print("已点击登录按钮。")
        

    except Exception as e:
        new_print(f"出现异常：{e}")

def search_api(key):
    time.sleep(0.5)
    url = "https://api.wlai.vip/token"
    driver.get(url)
    driver.refresh()
    time.sleep(0.5)
    # 等待输入框出现，最多等待10秒
    token_key_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='搜索令牌的 key...']"))
    )
    token_key_input.clear()
    time.sleep(0.1)
    # 输入令牌的 key
    token_key_input.send_keys(key)
    new_print("已输入令牌的 key。")
    
    # 搜索key
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='搜索']"))
    )
    search_button.click()
    new_print("已点击搜索按钮。")
    
    time.sleep(1)
    wait = WebDriverWait(driver, 5)
    # 等待表格元素出现
    table_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTableContainer-root")))

    new_print("table load finished")
    # 获取所有表格行 <tr>，只从 <tbody> 中获取
    rows = table_container.find_elements(By.XPATH, ".//tbody/tr")
    if len(rows) == 0 or len(rows) > 1:
        # 未找到
        return False
    else:
        return True
def check_data_after_now(date = ["2024","十二月","31","00","00"]):
    months = {
    "一月": 1, "二月": 2, "三月": 3, "四月": 4, "五月": 5,
    "六月": 6, "七月": 7, "八月": 8, "九月": 9, "十月": 10,
    "十一月": 11, "十二月": 12}
    while len(date) < 5:
        date.append("0")
    # 提取年、月、日、时、分
    year = int(date[0])
    month = months[date[1]]
    day = int(date[2])
    hour = int(date[3])
    minute = int(date[4])
    # 创建 datetime 对象
    given_date = datetime.datetime(year, month, day, hour, minute)

    # 获取当前日期
    current_date = datetime.datetime.now()
    if given_date > current_date:
        new_print("给定日期大于当前日期")
        return True
    else:
        new_print("给定日期不大于当前日期")
        return False
    
def change_key_life_time(life = ["2024","十二月","31","00","00"]):
    if not check_data_after_now(life):
        return False
    # life 调整
    wait = WebDriverWait(driver, 10)
    # 等待输入框可见并选择它
    input_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiInputBase-root input[placeholder='YYYY/MM/DD hh:mm']")))
    month_mapping = {
        "一月": "01",
        "二月": "02",
        "三月": "03",
        "四月": "04",
        "五月": "05",
        "六月": "06",
        "七月": "07",
        "八月": "08",
        "九月": "09",
        "十月": "10",
        "十一月": "11",
        "十二月": "12"
    }

    # 规整化为字符串
    year = life[0]
    month = month_mapping[life[1]]  # 将中文月份转换为数字
    day = life[2]
    hour = life[3]
    minute = life[4]
    formatted_date = f"{year}/{month}/{day} {hour}:{minute}"
    if debug:
        input_box.send_keys(formatted_date)  # 输入日期
        new_print("input")
        # 保存截图
        driver.get_screenshot_as_file("screenshot.png")
        time.sleep(0.5)
        input_box.send_keys(formatted_date)  # 输入日期
        new_print("input")
        time.sleep(0.5)
        input_box.send_keys(formatted_date)  # 输入日期
        new_print("input")
        time.sleep(0.5)
        input_box.send_keys(formatted_date)  # 输入日期
        new_print("input")
    else:
        time.sleep(0.5)
        input_box.send_keys(formatted_date) # 其实是打开日期选择器
        new_print("find CalendarHeader")
        time.sleep(0.1)
        wait = WebDriverWait(driver, 10)
        month_label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiPickersCalendarHeader-label")))
        # 根据空格进行分割
        month, year = month_label.text.split()
        new_print("month : " + str(month) + " year :" + str(year))
        if not (year == life[0]):
            new_print("set year")
            # 设置年份
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='calendar view is open, switch to year view']"))
            ).click()
            
            print("修改年份")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '" + life[0] + "')]"))
                ).click()
        # if not (month == life[1]):
            # 循环直到当前月份与目标月份匹配
        while not month == life[1]:
            # 如果月份不匹配，点击“上一月”按钮
            if int(month_mapping[month]) < int(month_mapping[life[1]]):
                new_print(f"当前月份是 {month}，需要调整到 {life[1]}，点击下一月按钮。")
                next_month_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Next month']")))
                next_month_button.click()
            if int(month_mapping[month]) > int(month_mapping[life[1]]):
                new_print(f"当前月份是 {month}，需要调整到 {life[1]}，点击上一月按钮。")
                next_month_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Previous month']")))
                next_month_button.click()
            month_label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiPickersCalendarHeader-label")))
            # 根据空格进行分割
            month, year = month_label.text.split()
        new_print("month checked")
        
        # 定位日期所在的父容器
        calendar_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiDayCalendar-monthContainer")))

        # 定位所有天数按钮
        all_day_buttons = calendar_container.find_elements(By.CSS_SELECTOR, "button[role='gridcell']")

        # 遍历所有日期，找到匹配的日期并点击
        for button in all_day_buttons:
            if button.text == life[2]:
                print(f"找到日期：{life[2]}，即将点击。")
                button.click()
                break
        else:
            print(f"未找到匹配的日期：{life[2]}。")
            
    # 检查当前文本
    current_value = input_box.get_attribute('value')
    if current_value == formatted_date:
        print("输入成功，当前文本为:", current_value)
    else:
        print("输入失败，当前文本为:", current_value)
        # return False
        # 等待并点击“OK”按钮
    ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']")))
    ok_button.click()
    return current_value == formatted_date

def set_dollor(dollor):
    if dollor < 0.5:
        return False
    # 等待金额输入框出现，最多等待10秒
    amount_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "channel-remain_quota-label"))
    )
    
    # 获取当前金额并加上 10
    # current_value = int(amount_input.get_attribute("value"))
    new_value = dollor
    amount_input.click()
    # 清空输入框并输入新的金额
    # amount_input.clear()
    time.sleep(0.1)
    for i in range(len(amount_input.text) + 1):
        amount_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
        new_print("current value: "+amount_input.text)
    amount_input.send_keys(str(new_value))

    # driver.execute_script("arguments[0].value = arguments[1];", amount_input, str(new_value))
    
    new_print(f"已输入新的金额：{new_value}")
    return True

def change_token_dollar_and_life(driver,dollor = 0,life = ["2024","十二月","31","00","00"],key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"):
    """
    1: success
    2: no dollar
    3: no date
    4: no key
    """
    # 检查输入
    try:
        if ( 0 < dollor < 0.5):
            new_print("no dollar")
            return 2
    except:
        dollor = float(dollor)
        if ( 0 < dollor < 0.5):
            new_print("no dollar")
            return 2
    # 检查日期
    if(len(life) > 0)
        if(not check_data_after_now(life)):
            new_print("no date")
            return 3
    if not search_api(key):
        # 未找到
        return 4
    
    new_print("查找三点button")
    # 等待按钮可点击
    wait = WebDriverWait(driver, 10)  # 最长等待10秒
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-hbyu9u')]")))
    # 点击按钮
    ActionChains(driver).move_to_element(button).click().perform()

    time.sleep(0.5)
    
    new_print("查找编辑菜单")
    # 等待并点击编辑菜单项，最多等待10秒
    edit_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and text()='编辑']"))
    )
    edit_menu_item.click()
    new_print("已点击编辑菜单项。")
    
    time.sleep(0.1)
    if dollor >= 0:
        # 设置金额
        set_dollor(dollor)
    if len(life) > 0:
        if change_key_life_time(life):
            new_print("life changed")
        else:
            new_print("error")
        
    time.sleep(1)
    new_print("查找提交button")
    # 等待并点击提交按钮，最多等待10秒
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='提交']"))
    )
    submit_button.click()
    new_print("已点击提交按钮。")
    return 1
def get_token_info(driver,key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"):
    result = ["","","",""]
    search_api(key)
    new_print("search finished")
    # 等待 <tr> 元素加载
    wait = WebDriverWait(driver, 5)
    # 等待表格元素出现
    table_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTableContainer-root")))

    new_print("table load finished")
    # 获取所有表格行 <tr>，只从 <tbody> 中获取
    rows = table_container.find_elements(By.XPATH, ".//tbody/tr")
    if len(rows) == 0 or len(rows) > 1:
        # 未找到
        return result
    # 确保有数据行
    if len(rows) > 0:
        # 选择第二行，索引为1
        for row in rows:
            if "\n复制" in row.text:
                second_row = row
        new_print("row finded")
        # 从第二行中找到所有 <td> 元素
        td_elements = second_row.find_elements(By.TAG_NAME, "td")

        # 提取信息
        if len(td_elements) >= 8:
            used_quota = td_elements[4].text  # 已用额度
            remaining_quota = td_elements[5].text  # 剩余额度
            created_time = td_elements[6].text  # 创建时间
            expiry_time = td_elements[7].text  # 过期时间

            # 输出提取的信息
            new_print("已用额度:"+ used_quota)
            new_print("剩余额度:"+ remaining_quota)
            new_print("创建时间:"+ created_time)
            new_print("过期时间:"+ expiry_time)
            # 剩余次数
            counts_remain = str(float(remaining_quota[1:])*coef)
            # 已用次数
            counts_used = str(float(used_quota[1:])*coef)
            result = [counts_used,counts_remain,created_time,expiry_time]
        else:
            new_print("未找到足够的 <td> 元素")
    else:
        new_print("没有找到足够的行元素")
    return result

def create_new_key(dollor,date):
    if not check_data_after_now(date):
        return False
    if float(dollor) < 0.5:
        return False
    url = "https://api.wlai.vip/token"
    driver.get(url)
    time.sleep(0.5)
    driver.refresh()
    # 等待按钮可点击
    wait = WebDriverWait(driver, 10)  # 最多等待10秒
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-contained') and contains(., '新建令牌')]")))
    # 点击按钮
    button.click()
    time.sleep(0.5)
    # 等待输入框出现
    wait = WebDriverWait(driver, 10)
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='channel-name-label']")))  # 根据实际的 ID 替换

    # 获取当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 格式化时间
    
    # 填写当前时间
    input_box.send_keys(current_time)
    
    # 等待下拉框出现并可点击
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "models-multiple-select")))

    # 点击下拉框
    dropdown.click()
    
    # 等待复选框出现并可点击
    # 等待 div 元素出现
    wait = WebDriverWait(driver, 20)
    combobox = wait.until(EC.visibility_of_element_located((By.ID, "group-select")))

    # 使用 JavaScript 点击
    driver.execute_script("arguments[0].click();", combobox)
        
    # 等待下拉框出现并可点击
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "models-multiple-select")))

    # 点击下拉框
    dropdown.click()
    
    
    
    
    # 等待下拉框出现并可点击
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "group-select-label")))

    # 点击下拉框
    dropdown.click()
    
    # 等待复选框出现并可点击
    wait = WebDriverWait(driver, 10)
    checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.PrivateSwitchBase-input")))

    # 点击复选框
    checkbox.click()
    
    # 等待下拉框出现并可点击
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable((By.ID, "group-select-label")))

    # 点击下拉框
    dropdown.click()
    
    set_dollor(dollor)
    change_key_life_time(date)
    time.sleep(1)
    # 等待并点击提交按钮，最多等待10秒
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='提交']"))
    )
    submit_button.click()
    new_print("已点击提交按钮。")
    return True

def pay_for_enlong():
    pass
            
login(driver)
time.sleep(1)

if __name__ == "__main__":
    pass
    # login(driver) # 登陆
    # get_balance(driver)
    # # change_token_dollar_and_life(driver,dollor=1) # 进行修改
    key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"
    # key = "123"
    # new_print(get_token_info(driver,key=key))
    print(change_token_dollar_and_life(driver,dollor=10,life=["2026","六月","15","0","0"],key = key))
    # create_new_key("123",["2024","十二月","31","00","00"])
    # change_token_dollar_and_life(driver,dollor=1,life=0,key = key)
# finally:
#     # 关闭浏览器
#     # driver.quit()
#     pass    
