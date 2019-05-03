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

from libs.vmsmodify import VMSModifyHandler

print("The Python path used = %s" % sys.executable)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


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
app_parser.add_argument('--enableads', dest='enable_ads', action='store', type=str2bool,
    nargs='?', help='enable click ads')

# 解析参数步骤
app_args = app_parser.parse_args()
app_current_dir = os.path.dirname(os.path.abspath(__file__))

# 日志
import logging.handlers

log_file_path = os.path.join(app_current_dir, 'vmid-{}-run.log'.format(app_args.vmid))
if os.path.isfile(log_file_path):
    try:
        os.remove(log_file_path)
    except:
        pass

handler = logging.handlers.RotatingFileHandler(log_file_path,
                                               maxBytes=1024 * 1024 * 50, backupCount=1)  # 实例化 handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化 formatter
handler.setFormatter(formatter)  # 为 handler 添加 formatter
logger = logging.getLogger('tst')  # 获取名为 tst 的 logger
logger.addHandler(handler)  # 为 logger 添加 handler
logger.setLevel(logging.DEBUG)

vmsH = VMSModifyHandler(logger=logger)


class RunningHelper(object):
    @staticmethod
    def get_flag_file(vmid):
        flag_file = os.path.join(app_current_dir, 'can-stop-vmid-{}-f.flag'.format(vmid))
        return flag_file

    @staticmethod
    def is_vm_is_running(vmid):
        return vmsH.vm_is_running(vmid)

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

global_use_buildin_vpn = True  # 是否使用VM中内置的VPN


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
        time_enable = round(random.uniform(0.2, 12), 2) >= 4.8

    # 凌晨的情况，对应美国区的下午
    if cur_time_hour in range(0, 11):
        time_enable = True and round(random.uniform(0.2, 12), 2) >= 1

    # 下午晚上可以点击少量广告的情况下，对应美国区的上午到中午时段
    if cur_time_hour in range(18, 25):
        time_enable = True and round(random.uniform(0.2, 12), 2) >= 1.8

    # Step2: 获取随机范围
    return time_enable


def common_process_call(loginfo='', commandList=[]):
    '''
    公共调用子进程函数
    :param loginfo:
    :param commandList:
    :return:
    '''
    try:
        proc = subprocess.Popen(commandList,
                                cwd=os.path.join(app_current_dir, 'scripts', app_args.auto_ahk_file_prex),
                                shell=True)
        all_sub_process.append(proc)
        return_code = proc.wait()
        logger.info(return_code)
        return 1

    except Exception:
        logger.exception("Error:")
    finally:
        time.sleep(5)

    return 0


def start_scroll_up_to_down():
    return common_process_call("Trying start_scroll_up_to_down...", ['AutoHotkey', 'scrolluptodown.ahk'])


def start_auto_scroll_up_or_down():
    return common_process_call("Trying start_auto_scroll_up_or_down...", ['AutoHotkey', 'scrollupordown.ahk'])


def start_vpn():
    return common_process_call("Trying start_vpn...", ['AutoHotkey', 'runvpn.ahk'])


def auto_click_ads():
    return common_process_call("Trying click ads...", ['AutoHotkey', 'clickads.ahk'])


def auto_close_tab_page():
    return common_process_call("Trying auto_close_tab_page...", ['AutoHotkey', 'closetab.ahk'])


def starup(want_open_url, app_args):
    has_error = False
    now_driver_id = get_random_driver_id()
    try:
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '5.1.1',
            'deviceName': app_args.dest_device,
            "udid": app_args.dest_device,  # "127.0.0.1:21533", 查看：设备通讯端口，adb devices。  https://www.cnblogs.com/Nefeltari/p/5603163.html
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'browserName': 'Chrome',
            'nativeWebScreenshot': True,
            'androidScreenshotPath': 'target/screenshots',
            # 'appPackage': 'com.android.chrome',
            'clearSystemFiles': True,
            'avdLaunchTimeout': 60000,
            'avdReadyTimeout': 60000,
            # 'noReset': False,
            'gpsEnabled': True,
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
        max_page_load_timeout = random.randint(90, 180)  # 加大支持timeout的时间, 让浏览更逼真
        max_script_timeout = random.randint(60, 90)  # 加大支持脚本执行的timeout时间，让浏览更逼真

        # 是否开启快速浏览模式
        # 快速浏览模式，将降低很多指标参数，不点击广告等等
        # enable_quick_browser_mode = round(random.uniform(0.1, 12), 2) <= random.randint(3, 6)
        enable_quick_browser_mode = get_enable_quick_browser_mode()
        if enable_quick_browser_mode:
            logger.info("开启快速浏览模式 ....")
            max_page_load_timeout = random.randint(60, 90)
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
            time.sleep(random.randint(15, 30))

        # 随机回滚一下
        cfg_enable_scroll_up = True and round(random.uniform(1, 12), 2) >= 3
        if cfg_enable_scroll_up:
            time.sleep(random.randint(3, 5))
            logger.info("现在可以向上滚动页面了 ...")
            start_auto_scroll_up_or_down()

        # 让网页自己休息一会
        cfg_enable_web_wait = 1
        if cfg_enable_web_wait == 1:
            logger.info("让网页自己先安静一下...")
            min_sleep_secs = random.randint(5, 30)
            time.sleep(min_sleep_secs)

        # 判断是否为快速浏览模式
        if enable_quick_browser_mode:
            start_auto_scroll_up_or_down()
            time.sleep(3)

            if round(random.uniform(1, 12), 2) >= 5:
                start_auto_scroll_up_or_down()
                time.sleep(3)

            if app_args.enalbe_ads:  # 如果可以点击
                auto_click_ads()

            start_auto_scroll_up_or_down()
            time.sleep(random.randint(5, 25))

        # 非快速浏览模式，可以尝试点击广告
        else:
            # 可以尝试点击广告了
            logger.info("尝试点击广告...")
            start_auto_scroll_up_or_down()
            auto_click_ads()
            cfg_enable_web_wait_after_ads = 1

            if cfg_enable_web_wait_after_ads == 1:
                logger.info("点击广告后，需要等待一会...")
                if round(random.uniform(1, 12), 2) >= 5:
                    time.sleep(10)

                start_auto_scroll_up_or_down()

                if round(random.uniform(1, 12), 2) >= 5:
                    time.sleep(5)
                    start_auto_scroll_up_or_down()
                    auto_click_ads()

                if round(random.uniform(1, 12), 2) >= 5:
                    min_sleep_secs = random.randint(15, 30)
                    time.sleep(min_sleep_secs)
                    start_auto_scroll_up_or_down()

            # 停顿后，可以执行点击操作广告工作，也可以点击关闭标签的操作
            if round(random.uniform(1, 12), 2) >= 3:
                time.sleep(random.randint(1, 10))
                auto_click_ads()
                start_auto_scroll_up_or_down()

            if round(random.uniform(1, 12), 2) >= 4:
                time.sleep(random.randint(1, 10))
                auto_click_ads()
                start_auto_scroll_up_or_down()

            if round(random.uniform(1, 12), 2) >= 5:
                time.sleep(random.randint(1, 10))
                start_auto_scroll_up_or_down()

            if round(random.uniform(1, 12), 2) >= 6:
                time.sleep(random.randint(1, 10))
                auto_click_ads()
                start_auto_scroll_up_or_down()

        # 自动关闭标签页面
        auto_close_tab_page()
        if round(random.uniform(1, 12), 2) >= 5:
            time.sleep(random.randint(2, 5))

        # 关闭后台进程
        stop_all_back_procs(all_sub_process)

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
            # 创建可以关闭VM的标记文件
            RunningHelper.create_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))
        except Exception:
            logger.exception("Error:")
        if has_error:
            # 重新开启刷屏处理
            browser_boot(app_args)
        if global_config['run_count'] > global_config['max_urls_count']:
            sys_exit("The number of pages opened has reached the maximum requirement")


def get_enable_quick_browser_mode():
    # Step1: 检测时间是否在范围内
    time_enable_ads_browser = False
    cur_time = time.localtime()
    cur_time_hour = int(cur_time.tm_hour)

    # 中国晚上的情况，美国区的上午到中午
    if cur_time_hour in range(18, 25):
        time_enable_ads_browser = True and round(random.uniform(1, 12), 2) >= 2

    # 中国凌晨的情况，美国中午到下午
    elif cur_time_hour in range(0, 12):
        time_enable_ads_browser = True and round(random.uniform(1, 12), 2) >= 1.5

    # 中国下午的情况，美国凌晨到上午
    elif cur_time_hour in range(12, 18):
        time_enable_ads_browser = True and round(random.uniform(1, 12), 2) >= 9

    try:
        if not app_args.enable_ads:  # 如果系统要求不能使用点击广告，启动快速浏览模式
            return True
    finally:
        pass

    # Step2: 获取随机范围
    enable_quick_browser_mode = not time_enable_ads_browser
    return enable_quick_browser_mode


def browser_boot(app_args):
    sort_indexs = []
    with open("urls.txt", "r") as fhandler:
        all_urls = []
        while True:
            file_url = fhandler.readline()
            if not file_url:
                break
            format_url = file_url.replace('\n', '')
            all_urls.append(format_url)

        for index in range(len(all_urls)):
            sort_indexs.append(index)

        logger.info("Now process the web page count： %d" % len(sort_indexs))

    # 让列表乱序处理
    random.shuffle(sort_indexs)
    for cur_index in sort_indexs:
        cur_url = all_urls[cur_index]
        cur_url = cur_url.strip()
        if cur_url != '':
            # must check vm is running
            vm_is_running = RunningHelper.is_vm_is_running(app_args.vmid)
            while not vm_is_running:
                vm_is_running = RunningHelper.is_vm_is_running(app_args.vmid)
                time.sleep(2)

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

        # 移除可以停止的标志文件
        RunningHelper.remove_can_stop_vm_flag_file(RunningHelper.get_flag_file(app_args.vmid))

        # must check vm is running
        vm_is_running = RunningHelper.is_vm_is_running(app_args.vmid)
        while not vm_is_running:
            vm_is_running = RunningHelper.is_vm_is_running(app_args.vmid)
            time.sleep(2)

        if global_use_buildin_vpn:
            start_vpn()
        browser_boot(app_args)
    except Exception:
        logger.exception("Error:")
    finally:
        stop_all_back_procs(all_sub_process)
        exit(0)
