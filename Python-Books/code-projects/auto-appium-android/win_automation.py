# -*- coding: utf-8 -*-
# PYTHON_VERSION=3.6
import datetime
import locale

print(locale.getdefaultlocale())

import os
import random
import signal
import subprocess
import sys
import time

app_current_dir = os.path.dirname(os.path.abspath(__file__))

import logging.handlers

log_file_path = os.path.join(app_current_dir, 'win_auto.log')
if os.path.isfile(log_file_path):
    try:
        os.remove(log_file_path)
    except:
        pass
handler = logging.StreamHandler()
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化 formatter
handler.setFormatter(formatter)  # 为 handler 添加 formatter
logger = logging.getLogger('tst')  # 获取名为 tst 的 logger
logger.addHandler(handler)  # 为 logger 添加 handler
logger.setLevel(logging.DEBUG)

import psutil
from curio import run, TaskGroup, Queue, sleep

# libs
from libs.utils import Utils
from libs.vmsmodify import VMSModifyHandler

print("The python path is '%s'" % sys.executable)

# 定义vmsH
vmsH = VMSModifyHandler(logger=logger)


class VMJob(object):
    def __init__(self, vmid, vmname, enable, enable_ads, start_cmd, appium_cmd, max_run_time, extend_vm_info):
        object.__init__(self)
        self.vmid = vmid
        self.vmname = vmname
        self.enable = enable
        self.enable_ads = enable_ads
        self.start_cmd = start_cmd
        self.start_time = Utils.get_now_time()
        self.appium_cmd = appium_cmd
        self.appium_cmd_handler = None
        self.max_run_time = max_run_time
        self.extend_vm_info = extend_vm_info
        self.back_proc = None
        self.startingVM = False
        self.busy = False

    async def is_vm_running(self):
        is_runnig = await vmsH.vm_is_running(self.vmid)
        return is_runnig

    async def is_vm_starting(self):
        return self.startingVM

    async def is_job_overtime(self):
        is_running = await self.is_vm_running()
        is_starting = await self.is_vm_starting()
        if not is_running or is_starting:
            return False

        running_time = Utils.get_now_time() - self.start_time

        # 判断时候有VM可以停止的标记文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        flag_file = os.path.join(current_dir, 'can-stop-vmid-{}-f.flag'.format(self.vmid))

        run_overtime_case1 = running_time >= self.max_run_time and os.path.exists(flag_file)
        run_overtime_case2 = (running_time - self.max_run_time) >= 8 * 60 * 1000  # 严重超时8分钟
        if run_overtime_case1 or run_overtime_case2:
            return True

        return False

    def _get_proc_is_running(self, proc_name, proc_handler=None):
        is_running = False
        if proc_handler:
            try:
                all_pids = psutil.pids()
                if all_pids.index(proc_handler.pid) >= 0:
                    is_running = True
                elif len(all_pids) > 0:
                    is_running = False
            except Exception:
                logger.exception("Error:")

        msg = '[X] [%s] is not running ... vmid=%s' % (proc_name, self.vmid)
        if is_running:
            msg = '[Y] [%s] is running ... vmid=%s' % (proc_name, self.vmid)
        logger.info(msg)
        return is_running

    def get_back_proc_is_running(self):
        return self._get_proc_is_running('PythonRun', self.back_proc)

    async def create_sub_process(self):
        logger.info('call create_sub_process ... vmid={}'.format(self.vmid))
        try:
            # 后台进程正在运行中，关闭掉
            if self.get_back_proc_is_running():
                logger.info('Found back_proc is running, must check stop it ... vmid={}'.format(self.vmid))
                if (Utils.get_now_time() - self.start_time) < 10 * 1000:
                    return  # 如果当前时间和最开始的启动时间只是差10秒钟，那么直接返回，不关闭后台进程
                self.stop_all_back_procs()

            self.start_time = Utils.get_now_time()
            logger.info('Must create a new process back handler ... vmid={}'.format(self.vmid))

            # 根据只创建一个后台跟踪的方式
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logger.info('current dir path = {}'.format(current_dir))

            enable_ads_flag = 'false'
            if self.enable_ads:
                enable_ads_flag = 'true'
            cmd = "{0} --enableads {1}".format(self.start_cmd, enable_ads_flag)
            logger.info('cmd = {}'.format(cmd))
            proc = subprocess.Popen(cmd,
                                    cwd=current_dir,
                                    shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            if proc:
                self.back_proc = proc
        except Exception:
            logger.exception('ERROR:')

    async def start_back_handler(self):
        try:
            self.startingVM = True
            logger.info('call adb_devices')
            await vmsH.adb_devices()
            logger.info('call vmsH.set_vm_config')
            vmsH.set_vm_config(self.vmid, self.extend_vm_info)
            logger.info("call vmsH.start_vm(self.vmid)")
            await vmsH.start_vm(self.vmid)

            tmp_vm_start_time = Utils.get_now_time()
            tmp_vm_max_start_use_time = 300*1000  # 最大的运行检测时间
            while Utils.get_now_time() - tmp_vm_start_time <= tmp_vm_max_start_use_time:
                await sleep(2)
                is_running = await self.is_vm_running()
                if is_running:
                    break

            # 再次判断是否正在运行
            is_running = await self.is_vm_running()
            if not is_running:
                self.startingVM = False
                await self.stop_back_handler(force=True)
            else:
                await sleep(3)
                logger.info('call adb_devices again ...')
                await vmsH.adb_devices()
                await sleep(5)
                logger.info("call create_sub_process")
                await self.create_sub_process()

        except Exception:
            logger.exception("Error:")
        finally:
            self.startingVM = False
            logger.info("start_back_handler end ...")

    def stop_all_back_procs(self):
        # (1)尝试terminate
        try:
            if self.back_proc:
                self.back_proc.kill()
        except Exception:
            logger.exception('Error:')

        # (2)尝试使用psutil来处理
        try:
            if self.back_proc:
                psutil.Process(self.back_proc.pid).terminate()
        except Exception:
            logger.exception('Error:')
        finally:
            self.back_proc = None

    async def stop_back_handler(self, force=False):
        """
        关闭VM
        :param force: 是否强制关闭，默认：非强制
        :return:
        """
        await sleep(1)
        await vmsH.stop_vm(self.vmid)
        await sleep(5)
        is_running = await self.is_vm_running()
        if is_running or force:
            self.startingVM = False
            logger.info('Close VM failed ... vmid={}'.format(self.vmid))
        else:
            self.start_time = Utils.get_now_time() * 10  # 表示不会被重新启动

    def free(self):
        self.stop_all_back_procs()
        self.stop_back_handler(force=True)
        logger.info('call free .....')


# 定义队列及关键共享数据
messages = Queue()
subscribers = set()
app_vmjob_list = set()


# Dispatch task that forwards incoming messages to subscribers
async def dispatcher():
    async for msg in messages:
        for q in list(subscribers):
            await q.put(msg)


# Publish a message
async def publish(msg):
    await messages.put(msg)


# A sample subscriber task
async def subscriber(name):
    queue = Queue()
    subscribers.add(queue)
    try:
        async for msg in queue:
            vmjob = msg
            logger.info("{} got vmid={} vmname={}".format(name, vmjob.vmid, vmjob.vmname))
            if not vmjob.enable:
                continue
            logger.info("{} watching vmid={} vmname={}".format(name, vmjob.vmid, vmjob.vmname))
            await sleep(5)

            # 这里设置一个快捷判断状态的处理 标明VMJOB 正在处理中
            if vmjob.busy:
                continue
            vmjob.busy = True  # 表明vmjob现在很忙

            # 获取相关状态进行处理
            is_vm_running = await vmjob.is_vm_running()
            is_vm_starting = await vmjob.is_vm_starting()
            is_job_overtime = await vmjob.is_job_overtime()
            is_back_proc_running = vmjob.get_back_proc_is_running()

            logger.info('is_vm_running={},'
                        'is_vm_starting={},'
                        'is_job_overtime={}, '
                        'is_back_proc_running={}'.format(is_vm_running, is_vm_starting, is_job_overtime,
                                                         is_back_proc_running))

            if not is_vm_running:
                if not is_vm_starting:
                    await vmjob.start_back_handler()
            elif is_vm_running:
                if is_job_overtime:
                    logger.info("VMJOB is overtime ....")
                    vmjob.stop_all_back_procs()
                    await vmjob.stop_back_handler()
                else:
                    logger.info(
                        'VM-IS-RUNNING  vmid={}, vmname={}, max_run_time={} ms.'.format(vmjob.vmid, vmjob.vmname,
                                                                                        vmjob.max_run_time))
            # 检测后台正在运行
            if not is_back_proc_running:
                await vmjob.create_sub_process()

            # 将vmjob状态赋值为空闲
            vmjob.busy = False

    finally:
        subscribers.discard(queue)


def git_pull_update():
    logger.info('call git_pull_update')
    try:
        print(datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'))
        # 根据只创建一个后台跟踪的方式
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info('current dir path = {}'.format(current_dir))
        proc = subprocess.Popen(['git', 'pull'],
                                cwd=current_dir,
                                shell=True,
                                universal_newlines=True)
        proc.wait()
    except Exception:
        logger.exception('ERROR:')
    finally:
        print("-------------------------------------------------")


# A sample producer task
async def producer():
    num_git_pull_check = 0
    while True:
        # 先更新一下，看看子模块是否有更新
        if num_git_pull_check > 5:  # 首次及1分钟后，检查更新
            git_pull_update()
            num_git_pull_check = 0
        num_git_pull_check += 1

        # 准备发送相关的VMJOB数据
        for vmjob in app_vmjob_list:
            if not vmjob.enable:
                continue
            await publish(vmjob)
            await sleep(5)  # 每隔10秒再发布，让系统稳定下来

        # 需要系统等待30秒，再发送，不能太快
        await sleep(10)


def exit_callback():
    logger.info('exit is done')
    for vmjob in app_vmjob_list:
        vmjob.free()
    logger.info('exit ....')


def find_process_id_by_name(process_name):
    """
    Get a list of all the PIDs of a all the running process whose name contains the given string process name
    :param process_name:
    :return:
    """

    list_of_process_objects = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if process_name.lower() in pinfo['name'].lower():
                list_of_process_objects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception:
            pass
    return list_of_process_objects


def close_all_ahk_process():
    list_of_process_objects = find_process_id_by_name('AutoHotkey')
    for proc in list_of_process_objects:
        try:
            psutil.Process(proc['pid']).terminate()
        except Exception:
            pass


def keyboardInterruptHandler(signal, frame):
    logger.info("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    close_all_ahk_process()
    exit_callback()
    exit(0)


def get_best_max_run_time():
    """
    获取美国区合适的处理模拟器启动的时间
    :return:
    """
    cur_time = time.localtime()
    cur_time_hour = int(cur_time.tm_hour)

    # 凌晨的情况，对应美国区的下午
    if cur_time_hour in range(0, 8):
        return random.randint(15, 30) * 60 * 1000

    # 上午的情况，对应为美国区的晚上
    if cur_time_hour in range(9, 17):
        return random.randint(10, 25) * 60 * 1000

    # 下午晚上可以点击少量广告的情况下，对应美国区的上午到中午时段
    if cur_time_hour in range(18, 25):
        return random.randint(15, 30) * 60 * 1000

    # 普通情况下
    return random.randint(30, 48) * 60 * 1000


def find_in_record_mac_address_list(config_mac_address, had_record_mac_address_list):
    in_list = False
    all_config_mac_address = config_mac_address.split(';')
    for iter_mac_address in all_config_mac_address:
        if iter_mac_address != '':
            if iter_mac_address in had_record_mac_address_list:
                in_list = True
                break

    return in_list


async def main():
    logger.info("Start make_stop_flag_file_first.....")
    await sleep(5)
    # 重新加载vms 的配置文件
    await vmsH.reload_vms_config_info()
    # 动态获取VMS的配置内容
    app_vmjob_list.clear()

    local_mac_address = VMSModifyHandler.get_local_mac_address()

    had_record_mac_address_list = []
    for one_config in vmsH.get_vms_configs():
        config_mac_address = one_config['macAddress']
        logger.info('localMacAddress={0}, configMacAddress={1}'.format(local_mac_address, config_mac_address))
        if config_mac_address != '':
            # config_mac_address 现在接受多mac地址情况
            all_config_mac_address = config_mac_address.split(';')
            for iter_mac_address in all_config_mac_address:
                if iter_mac_address != '':
                    if iter_mac_address not in had_record_mac_address_list \
                            and iter_mac_address == local_mac_address:
                        had_record_mac_address_list.append(iter_mac_address)

    logger.info('had_record_mac_address_list = {0}'.format(had_record_mac_address_list))

    for one_config in vmsH.get_vms_configs():
        config_mac_address = one_config['macAddress']

        enable_add = False
        if local_mac_address in had_record_mac_address_list:
            enable_add = find_in_record_mac_address_list(config_mac_address, had_record_mac_address_list)
        elif config_mac_address == '':
            enable_add = local_mac_address not in had_record_mac_address_list

        if enable_add:
            logger.info('call app_vmjob_list.add function')
            app_vmjob_list.add(VMJob(
                vmid=one_config['vmid'],
                vmname=one_config['vmname'],
                enable=one_config['enable'] == 'true',
                enable_ads=one_config['enable_ads'] == 'true',
                start_cmd=one_config['startCommand'],
                appium_cmd=one_config['appiumCommand'],
                max_run_time=get_best_max_run_time(),  # 60 * 5 * 1000 # 毫秒
                extend_vm_info=one_config['extend_vm_info']
            ))

    if len(app_vmjob_list) == 0:
        logger.info('No have vmjob ...')
        exit(9)

    logger.info("Start working..... vmjob count = {0}".format(len(app_vmjob_list)))
    async with TaskGroup() as g:
        await g.spawn(dispatcher)
        # await g.spawn(subscriber, 'child1')
        # await g.spawn(subscriber, 'child2')
        await g.spawn(subscriber, 'VMS-Monitor')
        ptask = await g.spawn(producer)
        await ptask.join()
        await g.cancel_remaining()



if __name__ == '__main__':
    sys.exitfunc = exit_callback
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    run(main)
