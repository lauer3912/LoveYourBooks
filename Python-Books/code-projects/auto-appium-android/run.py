# -*- coding: utf-8 -*-
import locale
print(locale.getdefaultlocale())

import argparse
import os
import random
import signal
import sys
import threading
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

print("The Python path used = %s" % sys.executable)

# 创建解析步骤
app_parser = argparse.ArgumentParser(description='Process some args.')
app_parser.add_argument('--s', dest='remote_server', action='store', default='http://127.0.0.1:4723/wd/hub',
                        help='The Appium server')
app_parser.add_argument('--d', dest='dest_device', action='store', default='127.0.0.1:21523',
                        help='The device, Use: adb devices to list')
app_parser.add_argument('--v', dest='vmid', action='store', default=0,
                        help='Assign the vms id')

# 解析参数步骤
app_args = app_parser.parse_args()
app_current_dir = os.path.dirname(os.path.abspath(__file__))

class RunningHelper(object):
    @staticmethod
    def get_flag_file(vmid):
        flag_file = os.path.join(app_current_dir, 'can-stop-vmid-{}-f.flag'.format(vmid))
        return flag_file

    @staticmethod
    def create_can_stop_vm_flag_file(flag_file):
        if not os.path.isfile(flag_file):
            try:
                open(flag_file, "w+").close()
            except Exception as err:
                print(err)

    @staticmethod
    def remove_can_stop_vm_flag_file(flag_file):
        if os.path.isfile(flag_file):
            try:
                os.remove(flag_file)
            except Exception as err:
                print(err)


# 全局配置
global_config = {
    # 'max_urls_count': random.randint(12, 24),  # 一般情况下， 持续2个小时，是相当长的了
    'max_urls_count': random.randint(20 * 24 * 3, 20 * 24 * 7),  # 一般情况下， 1小时，最多生产20，一般要求3天，查看一次
    'run_count': 0,
    'run_to_get_urls_count': 0,  # 运行获取url的机器运行计数
}

globals_drivers = {}


def get_now_time():
    millis = int(round(time.time() * 1000))
    return millis


def get_random_driver_id():
    """
    获取随机的driver_id
    :return:
    """
    new_id = '+{}{}'.format("".join(random.sample("abcdefghijklmnopqrstuvwxyz", 2)), get_now_time())
    return new_id


def sys_exit(message):
    """
    系统退出
    """
    print(message)
    print("The system is about to exit ...")
    exit(0)


def siample_touch(driver):
    try:
        eye1 = TouchAction(driver)
        eye1.press(x=random.randint(100, 150),
                   y=random.randint(100, 150)).release()
        time.sleep(1)
    except Exception as err:
        print(err)
    finally:
        pass


def auto_up_scroll_page(driver):
    pass


def auto_scroll_page(driver):
    """
    自动从上到下滚动，处理页面滑动问题
    """
    print("Start Auto Scroll")
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script(
        "return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    print("Total: ({0}, {1}), Viewport: ({2},{3})".format(
        total_width, total_height, viewport_width, viewport_height))

    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(round(random.uniform(0.2, 1.6), 2))

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        part = part + 1
        previous = rectangle

    print("Finishing chrome full page scroll workaround...")
    return True


def starup(want_open_url):
    has_error = False
    now_driver_id = get_random_driver_id()
    try:
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '5.1.1',
            'deviceName': app_args.dest_device,
            "udid": app_args.dest_device,  # "127.0.0.1:21533",
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'browserName': 'Chrome',
            'nativeWebScreenshot': True,
            'androidScreenshotPath': 'target/screenshots',
            # 'appPackage': 'com.android.chrome',
            'clearSystemFiles': True,
            'avdLaunchTimeout': 60000,
            'avdReadyTimeout': 60000,
            # 'noReset': True,
            # 'appActivity': 'BrowserActivity',
            'newCommandTimeout': 60000,
            'autoWebviewTimeout': 60000,
            # 'appWaitDuration': 30000,
            'chromeOptions': {
                # 为了防止出现Chrome的欢迎界面，你需要开启模拟器或者真机的开发者Debug选项。这个选项在手机或者模拟器的“设置”中
                'args': [
                    '--disable-fre',
                    '--disable-popup-blocking',
                    '--disable-infobars',
                    '--allow-running-insecure-content',
                    '--no-first-run',
                    '--disable-web-security',
                    # '--user-data-dir=/data/data/com.android.chrome/cache',
                    '--test-type'
                ]
            },
        }

        # expressVPN:
        # app.romanysoft@gmail.com
        # hGFjNk5R
        # EUONFNPKASP5WXYVCEVOUEA

        print("Starting webdriver ...")
        print("remote server address : %s" % app_args.remote_server)

        globals_drivers[now_driver_id] = webdriver.Remote(app_args.remote_server, desired_caps)

        print("Open %s" % want_open_url)

        global_config['run_to_get_urls_count'] = global_config['run_to_get_urls_count'] + 1
        print("This is already an attempt to open a Web page = %d " % (global_config['run_to_get_urls_count']))

        # 设置加载时间超时处理
        max_page_load_timeout = random.randint(90, 120)
        max_script_timeout = 30

        globals_drivers[now_driver_id].set_page_load_timeout(max_page_load_timeout)
        globals_drivers[now_driver_id].set_script_timeout(max_script_timeout)

        # 打开网页
        try:
            # 移除可以停止的标志文件
            RunningHelper.remove_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))
            # 执行打开网页
            globals_drivers[now_driver_id].get(want_open_url)
        except Exception as e:
            print(e)
            print('time out after %d seconds when loading page' % max_page_load_timeout)

            try:
                print('call window.stop()')
                globals_drivers[now_driver_id].execute_script(
                    'window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except Exception as jsErr:
                print(jsErr)

        # print(u"正在获取当前环境 ...")
        # 获取当前上下文环境
        # current_context = driver.current_context
        # contexts = driver.contexts

        # 可以滚动一下
        print("The Web page is ready, ready, you can scroll ...")
        siample_touch(globals_drivers[now_driver_id])
        auto_scroll_page(globals_drivers[now_driver_id])

        # 休息一会
        print("Take a break first, let the Web page itself quiet...")
        min_sleep_secs = random.randint(75, 180)
        time.sleep(min_sleep_secs)

        # 创建可以关闭VM的标记文件
        RunningHelper.create_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))

        # 浏览完成后，可以关闭了
        print("After browsing is complete, you can close the page...")

        # print(contexts)
        # print(current_context)

        # # 切换上下文
        # driver.switch_to.context("NATIVE_APP")

        # at = driver.current_context

        # print(at)

        # driver.find_element_by_id('com.android.browser:id/search_box_collapsed').click()
        # search_box = driver.find_element_by_id('com.android.browser:id/search_view')
        # search_box.click()
        # search_box.send_keys('hello toby')
        has_error = False
        global_config['run_count'] = global_config['run_count'] + 1
    except Exception as e:
        print(e)
        has_error = True
    finally:
        print("pages that are currently open count = %d" % global_config['run_count'])
        try:
            globals_drivers[now_driver_id].quit()
        except Exception as e:
            print(e)
        if has_error:
            # 重新开启刷屏处理
            time.sleep(random.randint(10, 15))
            browser_boot()
        if global_config['run_count'] > global_config['max_urls_count']:
            sys_exit("The number of pages opened has reached the maximum requirement")


def browser_boot():
    with open("urls.txt", "r+") as fhandler:

        all_urls = []
        while True:
            file_url = fhandler.readline()
            if not file_url:
                break
            format_url = file_url.replace('\n', '')
            all_urls.append(format_url)

        sort_indexs = []
        for index in range(len(all_urls)):
            sort_indexs.append(index)

        print("Now process the web page count： %d" % len(sort_indexs))

        # 让列表乱序处理
        random.shuffle(sort_indexs)
        for cur_index in sort_indexs:
            cur_url = all_urls[cur_index]
            starup(cur_url)
            print("Prepare the next web page url ... index=%d" % cur_index)
            time.sleep(random.randint(6, 12))


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        browser_boot()
    except Exception as e:
        print(e)
    finally:
        exit(0)
