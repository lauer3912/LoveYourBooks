# -*- coding: utf-8 -*-

"""
用来修改VMS文件的内容的，vms文件内容是xml格式，需要修改内部值来
"""
import os
import subprocess
from pprint import pprint
import xml.dom.minidom
from xml import etree

from .utils import Utils


class VMSModifyHandler(object):

    def __init__(self):
        self.config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_xml_file = os.path.join(self.config_dir, 'vms.config.xml')
        print('The VMS Config XML Path: ', self.config_xml_file)

        self.vmcmd = 'C:\Program Files\Microvirt\MEmu\memuc.exe'
        self.configs = []  # config xml element

    def get_vms_configs(self):
        return self.configs

    async def reload_vms_config_info(self):
        """
        更新、重载VMS的配置信息
        :return:
        """

        self.configs = []
        dom = xml.dom.minidom.parse(self.config_xml_file)
        root = dom.documentElement

        machines = root.getElementsByTagName('machine')
        for one_machine in machines:
            if one_machine.hasAttribute('name'):
                machine_name = one_machine.getAttribute('name')
                print("Reading the '%s' machine config information." % machine_name)

            configs = one_machine.getElementsByTagName('config')
            print("The config information count = %d" % len(configs))

            # 根据每一个config来处理内容
            for one_config in configs:
                if one_config.hasAttribute('enable') and \
                        one_config.hasAttribute('path') and \
                        one_config.hasAttribute('vmname'):
                    config_enable = one_config.getAttribute('enable')
                    config_path = one_config.getAttribute('path')
                    config_vmname = one_config.getAttribute('vmname')
                    config_vmid = one_config.getAttribute('vmid')
                    config_start_cmd = one_config.getAttribute('startCommand')

                    self.configs.append({
                        'vmid': config_vmid,
                        'vmname': config_vmname,
                        'enable': config_enable,
                        'path': config_path,
                        'startCommand': config_start_cmd,
                    })

                    if not config_enable or config_enable != 'true':
                        continue

    def modify_all_vms(self):
        if len(self.configs) == 0:
            print("The vms config file is invalid, please run reload_vms_config_info() function first.")
            return

        for one_config in self.configs:
            config_enable = one_config['enable']
            config_vmname = one_config['vmname']
            config_vmid = one_config['vmid']
            config_path = one_config['path']

            if not config_enable or config_enable != 'true':
                continue

            # 判断配置是否是文件，并且具有可读写操作
            if os.path.isfile(config_path):
                print("vmid=%s, vmname=%s, vmsfile=%s" % (config_vmid, config_vmname, config_path))
                VMSModifyHandler.rebuild(config_path)

    def set_vm_config(self, vmid):
        print('start setting vm new config...')
        new_gps_pos = Utils.generate_new_pos()
        config_info = {
            'macaddress': ":".join(Utils.generate_new_mac_address_list()).upper(),
            'linenum': str(Utils.generate_new_phone_number()),
            'latitude': str(new_gps_pos['latitude']),
            'longitude': str(new_gps_pos['longitude']),
            'simserial': str(Utils.generate_new_simserial()),
            'imei': str(Utils.generate_new_imei()),
        
            #'bssid': Utils.generate_new_bssid().upper(),
            #'cellid': Utils.generate_new_cellid(),
            #'ssid': Utils.generate_new_wifi_id(),

        }
        for key in config_info.keys():
            value = config_info[key]
            obj = subprocess.Popen([self.vmcmd, 'setconfig', '-i', vmid, key, value], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            cmd_out = obj.stdout.read()
            obj.stdout.close()
            print(cmd_out)

        print('setting vm new config over ...')

    async def adb_devices(self):
        obj = subprocess.Popen(['adb','devices'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        print('CMD: adb devices')
        print(cmd_out)

    async def start_vm(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'start', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'SUCCESS: start vm finished.':
            return True

        return False

    async def stop_vm(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'stop', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'SUCCESS: stop vm finished.':
            return True

        return False

    async def vm_is_running(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'isvmrunning', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'Running':
            return True

        return False


    @staticmethod
    def rebuild(vms_file=''):

        if not os.path.isfile(vms_file):
            print("Can't location the vms_file = ", vms_file)
            return

        print("Now rebuilding ...")

        # 获取文件所在路径
        vmsDirectory = os.path.dirname(vms_file)
        vmsFileName = os.path.basename(vms_file)

        # 将获得的xml文件送入到dom来解析
        dom = xml.dom.minidom.parse(vms_file)
        root = dom.documentElement  # 根节点 为 <MemuHyperv xmlns="http://www.memuhyperv.org/" version="1.12-windows">

        Machine = root.getElementsByTagName('Machine')[0]

        # 获得Hardware的配置
        Hardware = Machine.getElementsByTagName('Hardware')[0]

        # 获取Hardware > Network
        Network = Hardware.getElementsByTagName('Network')[0]

        # 修改MAC地址
        Network_Adapters = Network.getElementsByTagName('Adapter')
        for adapter in Network_Adapters:
            if adapter.hasAttribute('enabled') and adapter.hasAttribute('MACAddress'):
                enabled = adapter.getAttribute('enabled')
                if enabled:
                    mac_address = "".join(Utils.generate_new_mac_address_list()).upper()
                    adapter.setAttribute('MACAddress', mac_address)
                    print("[%s] = %s" % ('MACAddress', mac_address))

        # 获取 GuestProperties
        GuestProperties = Hardware.getElementsByTagName('GuestProperties')[0].getElementsByTagName('GuestProperty')

        # 定义需要更新的内容
        new_gps_pos = Utils.generate_new_pos()
        win_update_map = {
            'bssid': Utils.generate_new_bssid().upper(),
            'cellid': Utils.generate_new_cellid(),
            'imei': Utils.generate_new_imei(),
            'linenum': Utils.generate_new_phone_number(),
            'latitude': new_gps_pos['latitude'],
            'longitude': new_gps_pos['longitude'],
            'ssid': Utils.generate_new_wifi_id(),
            'simserial': Utils.generate_new_simserial(),
        }

        # 循环查找，开始更新
        for one_GuestProperty in GuestProperties:
            if one_GuestProperty.hasAttribute('name') and one_GuestProperty.hasAttribute('value'):
                name = one_GuestProperty.getAttribute('name')

                # 根据name的不同，来更新value
                if name in win_update_map:
                    one_GuestProperty.setAttribute('value', win_update_map[name])
                    print("[%s] = %s" % (name, win_update_map[name]))

        # SharedFolders 需要重新整理为公共可用值
        # 由于SharedFolder 默认是不挂载的。autoMount = false, 所以暂时不启动

        # 尝试源路径存储
        save_vms_config_files = [
            os.path.join(vmsDirectory, vmsFileName),
            os.path.join(vmsDirectory, '{}-prev'.format(vmsFileName))
        ]
        for vms_file in save_vms_config_files:
            with open(file=vms_file, mode='w', encoding='utf-8') as fh:
                try:
                    dom.writexml(fh)
                    print('The new contents are saved, the file path = ', vms_file)
                except Exception as err:
                    print('Save file Error:', err)
