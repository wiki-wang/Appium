from appium import webdriver
import traceback

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4'
desired_caps['deviceName'] = 'wiki'
# desired_caps['app'] = r'e:\apk\toutiao.apk'
desired_caps['appPackage'] = 'com.sqauto'   # app名字
desired_caps['appActivity'] = 'com.sqauto.MainActivity'     # launchable activity
# desired_caps['appWaitActivity'] = 'com.ibox.calculators.CalculatorActivity'

# desired_caps['unicodeKeyboard']  = True
# desired_caps['resetKeyboard']  = True
desired_caps['noReset'] = True
desired_caps['newCommandTimeout'] = 6000

#启动Remote RPC
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


'''
思路：
找到squato app，进入首屏后，计算 两个bar条y轴的差m
1）check 页面第一个bar条的文字是否为口碑最佳，
    1.1 如果不是，继续滑动，重复步骤2
    1.2 如果是，判断y轴位置：
        如果在 1/3屏幕高度 下方，则往上移动到第一个bar的左上角位置，确保5个app全部显示出来
        打印app名字        
2）从下往上滑动，滑动的距离为m，重复步骤1
'''
try:
    driver.implicitly_wait(10)
    bestApps = []   #存储口碑最佳的5个app的名字

    # 存储两个bar条的高度，为滑动的距离
    bar1 = 0
    bar2 = 0
    for bar in driver.find_elements_by_xpath('//*[@class="android.widget.ScrollView"]//*[@class="android.widget.TextView"]'):

        # bar的content-desc不为空
        if bar.text in ['松勤推荐', '上升最快', '最新上架', '口碑最佳', '用户最爱']:
            if bar1 == 0:
                bar1 = bar.location['y']
                continue
            if bar2 == 0:
                bar2 = bar.location['y']
                distance = bar2 - bar1
                break


    x_start = int(driver.get_window_size()['width']*0.5)
    y_start = int(driver.get_window_size()['height']*0.8)
    y_end = y_start - distance + 10


    while True:
        for bar in driver.find_elements_by_xpath('//*[@class="android.widget.ScrollView"]//*[@class="android.widget.TextView"]'):

            # 判断文本是不是为 口碑最佳
            if bar.text == '口碑最佳':

                #判断当前bar的位置，如果在 1/3屏幕高度 下面，则滑动到 bar1 位置
                if bar.location['y'] > int(driver.get_window_size()['width']*0.3):
                    driver.swipe(x_start, y_start, x_start, y_end, 3000)

                # 把口碑最佳的5个app名字保存到bestApps变量中,它们是每个android.widget.ImageView的下一个元素；
                # 由于xpath不支持从当前元素查找，只能从根节点查找，这里只能取出 口碑最佳 后续所有的文本，再做字符串处理
                eles = driver.find_elements_by_xpath('//android.widget.ScrollView//android.widget.TextView[@text="口碑最佳"]'
                                              '/following-sibling::android.widget.ImageView'
                                              '/following-sibling::android.widget.TextView')

                bestApps = [ele.text for ele in eles[:10]]

                # 结束循环，跳出内层循环
                break

        # 如果bestApps不为空，则说明找到口碑最佳的app，跳出while循环
        if bestApps:
            break

        # 没有找到，继续 从下往上 滑动
        driver.swipe(x_start, y_start, x_start, y_end, 3000)


    # 打印app，由于取出的是app名字和描述，只打印索引为偶数的内容
    i = 0
    for app in bestApps:
        if i % 2 == 0:
            print(app, end = '\t')
        i += 1

except:
    print(traceback.format_exc())
finally:
    driver.quit()