# -*- coding: utf-8 -*-
import locale
import subprocess

import psutil

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
app_parser.add_argument('--a', dest='auto_ahk_file_prex', action='store', default='',
                        help='Assign the auto hot key file')
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
all_sub_process = []

global_use_buildin_vpn = random.randint(0, 1) == 1  # 是否使用VM中内置的VPN


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


class OldToolHelper(object):
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
            max_rectangle_count = max(0, random.randint(0, all_rectangle_count) - 1)
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
    if cur_time_hour in range(11, 18):
        time_enable = round(random.uniform(0.2, 10), 2) <= 1

    # 凌晨的情况，对应美国区的下午
    if cur_time_hour in range(0, 11):
        time_enable = True and round(random.uniform(0.2, 12), 2) >= 2

    # 下午晚上可以点击少量广告的情况下，对应美国区的上午到中午时段
    if cur_time_hour in range(18, 25):
        time_enable = True and round(random.uniform(0.2, 12), 2) >= 3

    # Step2: 获取随机范围
    return time_enable


def start_scroll_up_to_down():
    try:
        logger.info("Trying start_scroll_up_to_down...")
        proc = subprocess.Popen(['AutoHotkey', 'scrolluptodown.ahk'],
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        proc.wait()
        logger.info(proc.returncode)
        return 1

    except Exception:
        logger.exception("Error:")

    return 0


def start_auto_scroll_up_or_down():
    try:
        logger.info("Trying start_auto_scroll_up_or_down...")
        proc = subprocess.Popen(['AutoHotkey', 'scrollupordown.ahk'],
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        proc.wait()
        logger.info(proc.returncode)
        return 1

    except Exception:
        logger.exception("Error:")

    return 0


def start_vpn():
    try:
        logger.info("Trying start_vpn...")
        proc = subprocess.Popen(['AutoHotkey', 'runvpn.ahk'],
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        proc.wait()
        logger.info(proc.returncode)
        return 1

    except Exception:
        logger.exception("Error:")

    return 0


def auto_click_ads():
    try:
        logger.info("Trying click ads...")
        if not get_enable_click_ads():
            logger.info("Disable click ads...")
            return 0
        logger.info("Enable click ads...")

        proc = subprocess.Popen(['AutoHotkey', 'clickads.ahk'],
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        proc.wait()
        logger.info(proc.returncode)
        return 1

    except Exception:
        logger.exception("Error:")

    return 0


def auto_close_tab_page():
    try:
        logger.info("Trying auto_close_tab_page...")
        proc = subprocess.Popen(['AutoHotkey', 'closetab.ahk'],
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        proc.wait()
        logger.info(proc.returncode)
        return 1

    except Exception:
        logger.exception("Error:")

    return 0


def starup(want_open_url, app_args):
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
        cur_driver = globals_drivers[now_driver_id]

        # 获取屏幕的size
        try:
            size = cur_driver.get_window_size()
            logger.info("Device Size = {}".format(size))
        except Exception:
            pass

        logger.info("Open %s" % want_open_url)

        global_config['run_to_get_urls_count'] = global_config['run_to_get_urls_count'] + 1
        logger.info("This is already an attempt to open a Web page = %d " % (global_config['run_to_get_urls_count']))

        # 设置加载时间超时处理
        max_page_load_timeout = random.randint(180, 360)  # 加大支持timeout的时间, 让浏览更逼真
        max_script_timeout = random.randint(60, 120)  # 加大支持脚本执行的timeout时间，让浏览更逼真

        # 是否开启快速浏览模式
        # 快速浏览模式，将降低很多指标参数，不点击广告等等
        # enable_quick_browser_mode = round(random.uniform(0.1, 12), 2) <= random.randint(3, 6)
        enable_quick_browser_mode = (not global_use_buildin_vpn) or (
                    round(random.uniform(0.1, 12), 2) <= random.randint(6, 8))
        if enable_quick_browser_mode:
            logger.info("开启快速浏览模式 ....")
            max_page_load_timeout = random.randint(90, 150)
            max_script_timeout = random.randint(30, 60)

        # 设置加载及延时时间控制
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

        # print(u"正在获取当前环境 ...")
        # 获取当前上下文环境
        # current_context = driver.current_context
        # contexts = driver.contexts

        # 可以滚动一下
        cfg_enable_auto_scroll = True
        if cfg_enable_auto_scroll:
            logger.info("网页已经加载完成，可以从上到下滚动了 ...")
            start_scroll_up_to_down()

        # 随机回滚一下
        cfg_enable_scroll_up = random.randint(0, 1)
        if cfg_enable_scroll_up == 1:
            time.sleep(random.randint(3, 5))
            logger.info("现在可以向上滚动页面了 ...")
            start_auto_scroll_up_or_down()

        # 让网页自己休息一会
        cfg_enable_web_wait = 1
        if cfg_enable_web_wait == 1:
            logger.info("让网页自己先安静一下...")
            min_sleep_secs = random.randint(15, 35)
            time.sleep(min_sleep_secs)

        # 判断是否为快速浏览模式
        if enable_quick_browser_mode:
            start_auto_scroll_up_or_down()
            if random.randint(0, 1) == 1:
                time.sleep(3)
                start_auto_scroll_up_or_down()
            time.sleep(random.randint(3, 15))
            start_auto_scroll_up_or_down()
            time.sleep(random.randint(30, 50))
        # 非快速浏览模式，可以尝试点击广告
        else:
            # 可以尝试点击广告了
            logger.info("尝试点击广告...")
            cfg_enable_web_wait_after_ads = auto_click_ads()

            if cfg_enable_web_wait_after_ads == 1:
                logger.info("点击广告后，需要等待一会...")
                time.sleep(10)
                start_auto_scroll_up_or_down()
                if random.randint(0, 1) == 1:
                    time.sleep(5)
                    start_auto_scroll_up_or_down()
                min_sleep_secs = random.randint(30, 60)
                time.sleep(min_sleep_secs)

            # 停顿后，可以执行点击操作广告工作，也可以点击关闭标签的操作
            auto_click_ads()
            time.sleep(random.randint(15, 30))
            auto_click_ads()
            time.sleep(random.randint(3, 10))
            start_auto_scroll_up_or_down()

        # 自动关闭标签页面
        auto_close_tab_page()
        time.sleep(random.randint(2, 5))

        # 创建可以关闭VM的标记文件
        RunningHelper.create_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))

        # 浏览完成后，可以关闭了
        logger.info("浏览网页完成，即将关闭该网页...")

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
            browser_boot(app_args)
        if global_config['run_count'] > global_config['max_urls_count']:
            sys_exit("The number of pages opened has reached the maximum requirement")


def browser_boot(app_args):
    with open("urls.txt", "r") as fhandler:
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
            cur_url = cur_url.strip()
            if cur_url != '':
                starup(cur_url, app_args)
                logger.info("Prepare the next web page url ... index=%d" % cur_index)
                time.sleep(random.randint(6, 12))
            else:
                continue


def stop_all_back_procs(proc_list):
    for proc in proc_list:
        # (1)尝试terminate
        try:
            if proc:
                proc.kill()
        except Exception:
            logger.exception('Error:')

        # (2)尝试使用psutil来处理
        try:
            if proc:
                psutil.Process(proc.pid).terminate()
        except Exception:
            logger.exception('Error:')


def keyboardInterruptHandler(signal, frame):
    logger.info("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))

    exit(0)


def exit_callback():
    logger.info('exit is done')
    stop_all_back_procs(all_sub_process)
    logger.info('exit ....')


if __name__ == "__main__":
    try:
        sys.exitfunc = exit_callback
        signal.signal(signal.SIGINT, keyboardInterruptHandler)
        if global_use_buildin_vpn:
            start_vpn()
        browser_boot(app_args)
    except Exception:
        logger.exception("Error:")
    finally:
        stop_all_back_procs(all_sub_process)
        exit(0)
