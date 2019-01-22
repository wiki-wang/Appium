import time
import traceback
from appium import webdriver
#aapt.exe dump badging d:\apk\toutiao.apk
desired_caps ={}
desired_caps ['platformName'] = 'Android'
desired_caps ['platformVersion'] = '4'
desired_caps ['deviceName'] = 'test'
#desired_caps [ '应用' ] =  - [R ' E：\一个 PK \吨 outiao.apk'
desired_caps ['appPackage'] = 'io.manong.developerdaily'
desired_caps ['appActivity'] = 'io.toutiao.android.ui.activity.LaunchActivity'
#desired_caps [ ' unicodeKeyboard ' ]   =  真
#desired_caps [ ' resetKeyboard ' ]   =  真
desired_caps ['noReset'] = True
desired_caps ['newCommandTimeout'] = 6000
#启动远程RPC
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
try:
    driver.implicitly_wait(10)

    #根据id找到元素，并点击，id和html元素的id不同
    driver.find_element_by_id("io.manong.developerdaily:id/tab_bar_plus").click()

    time.sleep(1)
    driver.find_element_by_id("io.manong.developerdaily:id/btn_email").click()
    time.sleep(1)

    #输入用户名，密码
    ele = driver.find_element_by_id("io.manong.developerdaily:id/edt_email")
    ele.send_keys('jcyrss@163.com')
    ele = driver.find_element_by_id("io.manong.developerdaily:id/edt_password")
    ele.send_keys('sdfsdf')

    time.sleep(2)
    #点击登录
    driver.find_element_by_id("io.manong.developerdaily:id/btn_login").click()

except:
    print(traceback.format_exc())


input(' ****按退出.. ')
driver.quit()