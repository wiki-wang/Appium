from appium import webdriver
import time, traceback

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4'
desired_caps['deviceName'] = 'wiki'
# desired_caps['app'] = r'e:\apk\toutiao.apk'
desired_caps['appPackage'] = 'com.ibox.calculators'
desired_caps['appActivity'] = 'com.ibox.calculators.SplashActivity'
desired_caps['appWaitActivity'] = 'com.ibox.calculators.CalculatorActivity'


# desired_caps['unicodeKeyboard']  = True
# desired_caps['resetKeyboard']  = True
desired_caps['noReset'] = True
desired_caps['newCommandTimeout'] = 6000
#启动Remote RPC
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

try:
    driver.implicitly_wait(10)

    # 根据id找到元素，并点击，数字和符号都有唯一的resource-id

    driver.find_element_by_id('com.ibox.calculators:id/digit3').click()
    driver.find_element_by_id('com.ibox.calculators:id/plus').click()
    driver.find_element_by_id('com.ibox.calculators:id/digit9').click()
    ele = driver.find_element_by_id('com.ibox.calculators:id/equal')
    ele.click()

    #停顿一下
    time.sleep(1)

    driver.find_element_by_id('com.ibox.calculators:id/mul').click()
    driver.find_element_by_id('com.ibox.calculators:id/digit5').click()
    ele.click()

    # 停顿一下
    time.sleep(1)

    # 判断结果是否等于60
    if driver.find_element_by_xpath('//*[@resource-id="com.ibox.calculators:id/cv"]/*[2]').text == '60':
        print('测试通过')
    else:
        print('测试不通过')

except:
    print(traceback.format_exc())

finally:
    driver.quit()