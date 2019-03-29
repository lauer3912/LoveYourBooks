import io
import os
import signal
import random
import sys
import subprocess

# libs
from libs.utils import Utils
from libs.vmsmodify import VMSModifyHandler


from curio import run, TaskGroup, Queue, sleep

print("The python path is '%s'" % sys.executable)

# 当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))

import argparse
app_parser = argparse.ArgumentParser(description='Handle some make stop file or clean stop file')
app_parser.add_argument('--m', dest='make', action='store', default=True,help='Make stop file')
app_parser.add_argument('--r', dest='clean', action='store', default=False,help='Remove all stop file')
# 解析参数步骤
app_args = app_parser.parse_args()


async def main():
    # 定义vmsH
    vmsH = VMSModifyHandler()

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

            if app_args.clean:
                if os.path.exists(stop_file):
                    try:
                        print('remove stop file:', stop_file)
                        os.remove(stop_file)
                    except Exception as err:
                        print('Error:', err)
            else:
                if not os.path.exists(stop_file):
                    try:
                        print('make stop file:', stop_file)
                        open(stop_file, "w+").close()
                    except Exception as err:
                        print('Error:', err)


if __name__ == "__main__":
    run(main)