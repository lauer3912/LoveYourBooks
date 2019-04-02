# -*- coding: utf-8 -*-
import locale

print(locale.getdefaultlocale())

import argparse
import os
import random
import signal
import sys
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

# 日志
import logging.handlers

handler = logging.handlers.RotatingFileHandler(os.path.join(app_current_dir, 'vmid-{}-run.log'.format(app_args.vmid)),
                                               maxBytes=1024 * 1024 * 5, backupCount=5)  # 实例化 handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化 formatter
handler.setFormatter(formatter)  # 为 handler 添加 formatter
logger = logging.getLogger('tst')  # 获取名为 tst 的 logger
logger.addHandler(handler)  # 为 logger 添加 handler
logger.setLevel(logging.DEBUG)


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
            except Exception:
                logger.exception("Error:")

    @staticmethod
    def remove_can_stop_vm_flag_file(flag_file):
        if os.path.isfile(flag_file):
            try:
                os.remove(flag_file)
            except Exception:
                logger.exception("Error:")


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
    logger.info(message)
    logger.info("The system is about to exit ...")
    exit(0)


def sample_touch(driver):
    try:
        eye1 = TouchAction(driver)
        eye1.press(x=random.randint(100, 150),
                   y=random.randint(100, 150)).release()
        time.sleep(1)
    except Exception:
        logger.exception("Error:")
    finally:
        pass


def auto_scroll_page(driver):
    """
    自动从上到下滚动，处理页面滑动问题
    """
    try:
        logger.info("Start Auto Scroll")
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        logger.info("Total: ({0}, {1}), Viewport: ({2},{3})".format(
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

                logger.info("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width, top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        previous = None
        part = 0
        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                logger.info("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(round(random.uniform(0.2, 1.6), 2))

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            part = part + 1
            previous = rectangle

        logger.info("Finishing chrome full page scroll workaround...")
        return True
    except Exception:
        logger.exception("Error:")


def random_scroll_up(driver):
    """
    随机往上滚动
    :return:
    """
    try:
        if round(random.uniform(0.2, 0.9), 2) < 0.5:
            return

        logger.info("Start random_scroll_up")
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        logger.info("Total: ({0}, {1}), Viewport: ({2},{3})".format(
            total_width, total_height, viewport_width, viewport_height))

        # 先记录所有区间
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
                logger.info("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width, top_height))
                ii = ii + viewport_width
            i = i + viewport_height

        # 随机回滚的位置
        all_rectangle_count = len(rectangles)
        cur_index = 0
        max_rectangle_count = random.randint(0, all_rectangle_count)
        rectangles.reverse()
        for rectangle in rectangles:
            if cur_index >= max_rectangle_count:
                break
            cur_index += 1

            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            logger.info("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(round(random.uniform(0.2, 0.6), 2))

        logger.info("Finishing chrome random page scroll workaround...")
    except Exception:
        logger.exception("Error:")


def get_enable_click_ads():
    """
    检测是否可以点击广告
    （1）时间允许
    （2）随机告知是否可以
    :return:
    """

    # Step1: 检测时间是否在范围内
    time_enable = False
    cur_time = time.localtime()
    cur_time_hour = int(cur_time.tm_hour)
    # 上午的情况，对应为美国区的晚上
    if cur_time_hour in range(9, 18):
        time_enable = False

    # 凌晨的情况，对应美国区的下午
    if cur_time_hour in range(0, 9):
        time_enable = True

    # 下午晚上可以点击少量广告的情况下，对应美国区的上午到中午时段
    if cur_time_hour in range(18, 25):
        time_enable = True

    # Step2: 获取随机范围
    # return round(random.uniform(0.2, 0.9), 2) > 0.3 and time_enable
    return True
    # return time_enable


def _common_ads_try_move_and_click(driver):
    had_click_ads = False

    # 在这个frame中定位到谷歌广告
    # 找 a 元素，target="_blank" 类似的元素
    link_elements = driver.find_elements_by_xpath('//a[@target="_blank"]')
    count_link_elements = len(link_elements)

    logger.info("link_elements = {}".format(count_link_elements))

    if count_link_elements != 0:
        # 检查是否可见
        sort_indexs = []
        for index in range(count_link_elements):
            sort_indexs.append(index)
        # 让列表乱序处理
        random.shuffle(sort_indexs)

        # 随机找到可见的元素，再进行点击
        will_click_ads_ele = None
        for cur_index in sort_indexs:
            one_ads_element = link_elements[cur_index]
            if one_ads_element.is_displayed():
                will_click_ads_ele = one_ads_element
                break

        if will_click_ads_ele:
            logger.info("Found a ads element ...")
            try:
                if will_click_ads_ele.is_displayed():
                    x = will_click_ads_ele.get('x')
                    y = will_click_ads_ele.get('y')

                    logger.info("ads element x={}, y={}".format(x, y))
                    driver.execute_script("window.scrollTo({0}, {1})".format(0, y))
            except Exception:
                logger.exception("Error:")

            try:
                # No found the visual ads element
                if will_click_ads_ele.is_displayed():
                    logger.info("click ads: call element click")
                    will_click_ads_ele.click()

                    time.sleep(random.randint(10, 30))
                    had_click_ads = True
            except Exception:
                logger.exception("Error:")

    return had_click_ads


def _reunion_ads_try_find(driver, layer):
    # driver.implicitly_wait(5)
    ads_iframe_elements = driver.find_elements_by_xpath('//iframe')
    all_ads_count = len(ads_iframe_elements)
    logger.info("layer = {}, ads_iframe_elements = {}".format(layer, all_ads_count))

    # 检查是否可见
    sort_index_list = []
    for index in range(all_ads_count):
        sort_index_list.append(index)
    # 让列表乱序处理
    random.shuffle(sort_index_list)

    for index_frame in sort_index_list:
        ele_iframe = ads_iframe_elements[index_frame]

        is_displayed = False
        try:
            is_displayed = ele_iframe.is_displayed()
            logger.info("layer={}, index_frame={}, is_displayed={}".format(
                layer,
                index_frame,
                is_displayed
            ))

            try:
                if is_displayed:
                    x = ele_iframe.get('x')
                    y = ele_iframe.get('y')

                    logger.info("ads element x={}, y={}".format(x, y))
                    driver.execute_script("window.scrollTo({0}, {1})".format(0, y))
            except Exception:
                logger.exception("Error:")

        except Exception:
            logger.exception("Error:")

        # 只有页面有显示的情况下
        if is_displayed:
            driver.switch_to.frame(ele_iframe)
            had_click_ads = _common_ads_try_move_and_click(driver)
            if had_click_ads:
                return layer
            else:
                layer += 1
                _reunion_ads_try_find(driver, layer)


def auto_click_ads(driver):
    logger.info("Trying click ads...")
    if not get_enable_click_ads():
        logger.info("Disable click ads...")
        return

    logger.info("Enable click ads...")
    layer = 0
    try:
        # 获取广告的元素有哪些？然后随机找到一个元素，并且在可视范围内，然后点击
        layer = _reunion_ads_try_find(driver, layer)
    except Exception:
        logger.exception("Error:")
        for i in range(layer):
            driver.switch_to.parent_frame()
        driver.switch_to.default_content()


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

        logger.info("Starting webdriver ...")
        logger.info("remote server address : %s" % app_args.remote_server)

        globals_drivers[now_driver_id] = webdriver.Remote(app_args.remote_server, desired_caps)

        logger.info("Open %s" % want_open_url)

        global_config['run_to_get_urls_count'] = global_config['run_to_get_urls_count'] + 1
        logger.info("This is already an attempt to open a Web page = %d " % (global_config['run_to_get_urls_count']))

        # 设置加载时间超时处理
        max_page_load_timeout = random.randint(120, 180)
        max_script_timeout = random.randint(60, 90)

        globals_drivers[now_driver_id].set_page_load_timeout(max_page_load_timeout)
        globals_drivers[now_driver_id].set_script_timeout(max_script_timeout)

        # 打开网页
        try:
            # 移除可以停止的标志文件
            RunningHelper.remove_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))
            # 执行打开网页
            globals_drivers[now_driver_id].get(want_open_url)
        except Exception:
            logger.exception("Error:")
            logger.info('time out after %d seconds when loading page' % max_page_load_timeout)

            try:
                logger.info('call window.stop()')
                globals_drivers[now_driver_id].execute_script(
                    'window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
            except Exception:
                logger.exception("Error:")

        # print(u"正在获取当前环境 ...")
        # 获取当前上下文环境
        # current_context = driver.current_context
        # contexts = driver.contexts

        # 可以滚动一下
        logger.info("The Web page is ready, ready, you can scroll ...")
        sample_touch(globals_drivers[now_driver_id])
        auto_scroll_page(globals_drivers[now_driver_id])

        # 随机回滚一下
        min_sleep_secs = random.randint(2, 10)
        time.sleep(min_sleep_secs)
        random_scroll_up(globals_drivers[now_driver_id])

        # 休息一会
        logger.info("Take a break first, let the Web page itself quiet...")
        min_sleep_secs = random.randint(60, 150)
        time.sleep(min_sleep_secs)

        # 可以尝试点击广告了
        logger.info("Try click some ads element...")
        auto_click_ads(globals_drivers[now_driver_id])

        # 创建可以关闭VM的标记文件
        RunningHelper.create_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))

        # 浏览完成后，可以关闭了
        logger.info("After browsing is complete, you can close the page...")

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
    except Exception:
        logger.exception("Error:")
        has_error = True
    finally:
        logger.info("pages that are currently open count = %d" % global_config['run_count'])
        try:
            globals_drivers[now_driver_id].quit()
        except Exception:
            logger.exception("Error:")
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

        logger.info("Now process the web page count： %d" % len(sort_indexs))

        # 让列表乱序处理
        random.shuffle(sort_indexs)
        for cur_index in sort_indexs:
            cur_url = all_urls[cur_index]
            starup(cur_url)
            logger.info("Prepare the next web page url ... index=%d" % cur_index)
            time.sleep(random.randint(6, 12))


def keyboardInterruptHandler(signal, frame):
    logger.info("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        browser_boot()
    except Exception:
        logger.exception("Error:")
    finally:
        exit(0)
