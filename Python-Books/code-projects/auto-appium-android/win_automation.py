# -*- coding: utf-8 -*-
# PYTHON_VERSION=3.6

import locale
print(locale.getdefaultlocale())

import os
import random
import signal
import subprocess
import sys

import psutil
from curio import run, TaskGroup, Queue, sleep

# libs
from libs.utils import Utils
from libs.vmsmodify import VMSModifyHandler

print("The python path is '%s'" % sys.executable)

# 定义vmsH
vmsH = VMSModifyHandler()


class VMJob(object):
    def __init__(self, vmid, vmname, config_path, enable, start_cmd, appium_cmd, max_run_time):
        object.__init__(self)
        self.vmid = vmid
        self.vmname = vmname
        self.config_path = config_path
        self.enable = enable
        self.start_cmd = start_cmd
        self.start_time = Utils.get_now_time()
        self.appium_cmd = appium_cmd
        self.appium_cmd_handler = None
        self.max_run_time = max_run_time
        self.back_proc = None
        self.startingVM = False

    async def is_running(self):
        is_runnig = await vmsH.vm_is_running(self.vmid)
        return is_runnig

    async def is_starting(self):
        return self.startingVM

    async def is_overtime(self):
        is_running = await self.is_running()
        is_starting = await self.is_starting()
        if not is_running or is_starting:
            return False

        running_time = Utils.get_now_time() - self.start_time

        # 判断时候有VM可以停止的标记文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        flag_file = os.path.join(current_dir, 'can-stop-vmid-{}-f.flag'.format(self.vmid))

        if running_time >= self.max_run_time and os.path.exists(flag_file):
            return True

        return False

    def _get_proc_is_running(self, proc_name, proc_handler):
        is_running = False
        if proc_handler:
            try:
                all_pids = psutil.pids()
                if all_pids.index(proc_handler.pid) >= 0:
                    is_running = True
                elif len(all_pids) > 0:
                    is_running = False
            except Exception as e:
                print("Error:", e)

        msg = '[X] [%s] is not running ... vmid=%s' % (proc_name, self.vmid)
        if is_running:
            msg = '[Y] [%s] is running ... vmid=%s' % (proc_name, self.vmid)
        print(msg)
        return is_running

    def get_back_proc_is_running(self):
        return self._get_proc_is_running('PythonRun', self.back_proc)

    async def create_sub_process(self):
        print('call create_sub_process ... vmid=', self.vmid)
        try:
            self.start_time = Utils.get_now_time()

            # 后台进程正在运行中，只记录一个
            if self.get_back_proc_is_running():
                return

            print('Must create a new process back handler ... vmid=', self.vmid)

            # 根据只创建一个后台跟踪的方式
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print('current dir path = ', current_dir)
            proc = subprocess.Popen(self.start_cmd,
                                    cwd=current_dir,
                                    shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            if proc:
                self.back_proc = proc
        except Exception as err:
            print('ERROR:', err)

    async def start_back_handler(self):
        try:
            self.startingVM = True
            print('call adb_devices')
            await vmsH.adb_devices()
            print('call vmsH.set_vm_config')
            vmsH.set_vm_config(self.vmid)
            print("call vmsH.start_vm(self.vmid)")
            await vmsH.start_vm(self.vmid)
            await sleep(10)
            is_running = await self.is_running()
            if not is_running:
                self.startingVM = False
                print('Start vm failed ... vmid=', self.vmid)
            else:
                await sleep(3)
                print('call adb_devices again ...')
                await vmsH.adb_devices()
                await sleep(5)
                print("call create_sub_process")
                await self.create_sub_process()

        except Exception as e:
            print(e)
        finally:
            self.startingVM = False
            print("start_back_handler end ...")

    async def stop_all_back_procs(self):
        # 尝试terminate
        try:
            self.back_proc.kill()
            psutil.Process(self.back_proc.pid).terminate()
        except Exception as err:
            print('Error:', err)

    async def stop_back_handler(self):
        await sleep(1)
        await vmsH.stop_vm(self.vmid)
        await sleep(5)
        is_running = await self.is_running()
        if is_running:
            self.startingVM = False
            print('Close VM failed ... vmid=', self.vmid)
        else:
            self.start_time = Utils.get_now_time() * 10  # 表示不会被重新启动

    def free(self):
        self.stop_all_back_procs()
        self.stop_back_handler()
        print('call free .....')


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
            print(name, 'got', vmjob.vmid, vmjob.vmname)

            if not vmjob.enable:
                continue
            print(name, 'watching', vmjob.vmid, vmjob.vmname)

            is_running = await vmjob.is_running()
            is_starting = await vmjob.is_starting()
            is_overtime = await vmjob.is_overtime()
            is_back_proc_running = vmjob.get_back_proc_is_running()

            print('is_running={},'
                  'is_starting={},'
                  'is_overtime={}, '
                  'is_back_proc_running={}'.format(is_running, is_starting, is_overtime, is_back_proc_running))

            if not is_running:
                if not is_starting:
                    await vmjob.start_back_handler()
            elif is_running:
                if is_overtime:
                    await vmjob.stop_back_handler()
                else:
                    print('VM-IS-RUNNING  vmid={}, vmname={}, max_run_time={} ms.'.format(vmjob.vmid, vmjob.vmname,
                                                                                          vmjob.max_run_time))
            # 检测后台正在运行
            if not is_back_proc_running:
                await vmjob.create_sub_process()

    finally:
        subscribers.discard(queue)


# A sample producer task
async def producer():
    while True:
        # 准备发送相关的VMJOB数据
        for vmjob in app_vmjob_list:
            if not vmjob.enable:
                continue

            await publish(vmjob)
            await sleep(5)

        await sleep(15)


def exit_callback():
    print('exit is done')
    for vmjob in app_vmjob_list:
        vmjob.free()
    print('exit ....')


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit_callback()
    exit(0)


async def make_stop_flag_file_first():
    # 当前路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 加载配置
    await vmsH.reload_vms_config_info()

    all_configs = vmsH.get_vms_configs()

    # 生成配置
    for one_config in all_configs:
        vmid = one_config.get('vmid')
        vmname = one_config.get('vmname')
        config_path = one_config.get('path')
        enable = one_config.get('enable') == 'true'

        if enable:
            stop_file = os.path.join(current_dir, 'vmid-{}-stop.flag'.format(vmid))
            print(stop_file)

            if not os.path.exists(stop_file):
                try:
                    print('make stop file:', stop_file)
                    open(stop_file, "w+").close()
                except Exception as err:
                    print('Error:', err)


async def main():
    print("Start make_stop_flag_file_first.....")
    await make_stop_flag_file_first()
    await sleep(5)
    # 重新加载vms 的配置文件
    await vmsH.reload_vms_config_info()
    # 动态获取VMS的配置内容
    app_vmjob_list.clear()
    for one_config in vmsH.get_vms_configs():
        app_vmjob_list.add(VMJob(
            vmid=one_config['vmid'],
            vmname=one_config['vmname'],
            config_path=one_config['path'],
            enable=one_config['enable'] == 'true',
            start_cmd=one_config['startCommand'],
            appium_cmd=one_config['appiumCommand'],
            max_run_time=random.randint(35, 60) * 60 * 1000  # 60 * 5 * 1000 # 毫秒
        ))

    print("Start working.....")
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
