from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
import re
import time
import configparser


# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

username = config['selenium']['username']
password = config['selenium']['password']
coef = int(config['selenium']['counts_coef'])

# # 设置无头edge浏览器
edge_options = Options()
# edge_options.add_argument("--headless")  # 无头模式
edge_options.add_argument("--no-sandbox")  # 解决DevToolsActivePort文件不存在的报错
edge_options.add_argument("--disable-dev-shm-usage")  # 共享内存
edge_options.add_argument('--disable-gpu')  # 禁用GPU加速
edge_options.add_argument('--window-size=2560,1080') 
edge_options.binary_location = "/Applications/Microsoft Edge Canary.app/Contents/MacOS/Microsoft Edge Canary"

# 启动浏览器
service = Service('/Users/kzz6991/msedgedriver')  # 替换为edgedriver的实际路径
driver = webdriver.Edge(service=service, options=edge_options)

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
        print("当前网址以 https://chaxun.wlai.vip/ 开头。")
    else:
        print("当前网址不以 https://chaxun.wlai.vip/ 开头。")
        driver.get('https://chaxun.wlai.vip/')
        time.sleep(0.2)
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
        print(f'通知内容: {toast_text}')

        # 等待总额元素出现并获取其文本
        total_amount_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.semi-tag-content'))
        )
        total_amount_text = total_amount_element.text
        # print(f'总额信息: {total_amount_text}')


        # 解析总额文本内容中的数字
        match = re.search(r'\$([0-9.]+)', total_amount_text)
        if match:
            amount_str = match.group(1)
            amount = float(amount_str)
            result = amount * 100
            print(f'总额乘以100后的结果: {result}')
        else:
            print('未找到总额信息中的金额')
    except:
        print("未找到通知元素")
    return result

def new_print(string):
    print(string)
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
        print("按钮已点击。")
    except Exception as e:
        print(f"出现异常：{e}")
    try:
        # 等待按钮元素出现，最多等待10秒
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'MuiButton-containedPrimary') and text()='登入']"))
        )
        # 点击链接
        login_link.click()
        print("已点击登入链接。")
    except Exception as e:
        print(f"出现异常：{e}")
    try:
        # 等待输入框出现，最多等待10秒
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "outlined-adornment-username-login"))
        )
        # 输入账号
        username_input.send_keys(username)
        print("已输入账号。")
        
        # 等待密码输入框出现，最多等待10秒
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "outlined-adornment-password-login"))
        )
        # 输入密码
        password_input.send_keys(password)
        print("已输入密码。")
        
        # 等待登录按钮出现并点击，最多等待10秒
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='登录']"))
        )
        # 点击登录按钮
        login_button.click()
        print("已点击登录按钮。")
        

    except Exception as e:
        print(f"出现异常：{e}")

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
    print("已输入令牌的 key。")
    
    # 搜索key
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='搜索']"))
    )
    search_button.click()
    print("已点击搜索按钮。")
    
    time.sleep(1)

def change_token_dollar_and_life(driver,dollor = 0,life = ["2024","十二月","31"],key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"):
    if (dollor == 0 and life == 0):
        return
    search_api(key)
    # 等待按钮可点击
    wait = WebDriverWait(driver, 10)  # 最长等待10秒
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-hbyu9u')]")))
    # 点击按钮
    ActionChains(driver).move_to_element(button).click().perform()

    time.sleep(0.5)
    
    # 等待并点击编辑菜单项，最多等待10秒
    edit_menu_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'MuiMenuItem-root') and text()='编辑']"))
    )
    edit_menu_item.click()
    print("已点击编辑菜单项。")
    
    time.sleep(0.1)
    if not (dollor == 0):
        # 等待金额输入框出现，最多等待10秒
        amount_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "channel-remain_quota-label"))
        )
        
        # 获取当前金额并加上 10
        # current_value = int(amount_input.get_attribute("value"))
        new_value = dollor
        amount_input.click()
        # 清空输入框并输入新的金额
        amount_input.clear()
        time.sleep(0.2)
        # amount_input.send_keys(str(new_value))

        driver.execute_script("arguments[0].value = arguments[1];", amount_input, str(new_value))
        
        print(f"已输入新的金额：{new_value}")
    if  (life == 0):
        # life 调整
        # 等待日期选择器图标出现并点击
        # 等待日期选择器按钮出现并点击
        date_picker_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label[contains(., 'Choose date')]]"))
        )
        date_picker_button.click()

        # 等待日期选择器弹出，选择特定日期
        # 这里假设我们要选择“2024年9月30日”
        # 你需要根据实际的日期选择器结构进行调整
        # 使用 WebDriverWait 等待显示月份的元素加载（最多等待10秒）
        wait = WebDriverWait(driver, 10)
        month_label = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.MuiPickersCalendarHeader-label")))
        # 根据空格进行分割
        month, year = month_label.text.split()
        # 循环直到当前月份与目标月份匹配
        while not month == life[1]:
            # 如果月份不匹配，点击“上一月”按钮
            new_print(f"当前月份是 {month}，需要调整到 {life[1]}，点击上一月按钮。")
            next_month_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Next month']")))
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
        # 等待并点击“OK”按钮
        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']")))
        ok_button.click()
        
        # 创建一个等待对象
        # wait = WebDriverWait(driver, 10)

        # 选择小时为 "00"
        hour_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@aria-label='0 hours']")))
        hour_element.click()
        print("选择小时 00 成功")

        # 选择分钟为 "00"
        minute_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@aria-label='0 minutes']")))
        minute_element.click()
        print("选择分钟 00 成功")

        # 点击 "OK" 按钮
        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']")))
        ok_button.click()
        print("点击 OK 按钮成功")
        
    time.sleep(1)
    # 等待并点击提交按钮，最多等待10秒
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-containedPrimary') and text()='提交']"))
    )
    submit_button.click()
    print("已点击提交按钮。")

def get_token_info(driver,key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"):
    result = ["","","",""]
    search_api(key)
    

    # 等待 <tr> 元素加载
    wait = WebDriverWait(driver, 5)
    # 等待表格元素出现
    table_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "MuiTableContainer-root")))

    # 获取所有表格行 <tr>，只从 <tbody> 中获取
    rows = table_container.find_elements(By.XPATH, ".//tbody/tr")

    if len(rows) == 0 or len(rows) > 1:
        # 未找到
        return result
    # 确保有数据行
    if len(rows) > 0:
        print(len(rows))
        # 选择第二行，索引为1
        for row in rows:
            if "\n复制" in row.text:
                second_row = row

        # 从第二行中找到所有 <td> 元素
        td_elements = second_row.find_elements(By.TAG_NAME, "td")

        # 提取信息
        if len(td_elements) >= 8:
            used_quota = td_elements[4].text  # 已用额度
            remaining_quota = td_elements[5].text  # 剩余额度
            created_time = td_elements[6].text  # 创建时间
            expiry_time = td_elements[7].text  # 过期时间

            # 输出提取的信息
            print("已用额度:", used_quota)
            print("剩余额度:", remaining_quota)
            print("创建时间:", created_time)
            print("过期时间:", expiry_time)
            # 剩余次数
            counts_remain = str(float(remaining_quota[1:])*coef)
            # 已用次数
            counts_used = str(float(used_quota[1:])*coef)
            result = [counts_used,counts_remain,created_time,expiry_time]
        else:
            print("未找到足够的 <td> 元素")
    else:
        print("没有找到足够的行元素")
    return result
            

if __name__ == "__main__":
    login(driver) # 登陆
    # get_balance(driver)
    # # change_token_dollar_and_life(driver,dollor=1) # 进行修改
    key = "sk-Q4WYHTcuUZYR5qJ7Bc53EeB743A3494d916a4493CdEc380d"
    # key = "1"
    # print(get_token_info(driver,key=key))
    
    change_token_dollar_and_life(driver,dollor=1,life=0,key = key)
# finally:
#     # 关闭浏览器
#     # driver.quit()
#     pass    