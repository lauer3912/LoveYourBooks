# -*- coding: utf-8 -*-

"""
用来修改VMS文件的内容的，vms文件内容是xml格式，需要修改内部值来
"""
import os
import subprocess
import uuid
import xml.dom.minidom

from .utils import Utils


class VMSModifyHandler(object):

    def __init__(self, logger):
        self.logger = logger
        self.config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_xml_file = os.path.join(self.config_dir, 'vms.config.xml')
        self.print('The VMS Config XML Path: {}'.format(self.config_xml_file))
        self.configs = []  # config xml element

        for maybe_path in [
            'C:\Program Files\Microvirt\MEmu\memuc.exe',
            'D:\VMSMicrovirt\MEmu\memuc.exe'
        ]:
            if os.path.exists(maybe_path):
                self.vmcmd = maybe_path
                break

    def print(self, msg, is_exception=False):
        if self.logger:
            if is_exception:
                self.logger.exception('Error:')
            else:
                self.logger.info(msg)
        else:
            print(msg)

    @staticmethod
    def get_local_mac_address():
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

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
                machine_mac_address = one_machine.getAttribute('macAddress')
                self.print(
                    "Reading the '{0} - {1}' machine config information.".format(machine_name, machine_mac_address))

            configs = one_machine.getElementsByTagName('config')
            self.print("The config information count = %d" % len(configs))

            # 根据每一个config来处理内容
            for one_config in configs:
                if one_config.hasAttribute('enable') and \
                        one_config.hasAttribute('vmname'):
                    config_enable = one_config.getAttribute('enable')
                    config_vmname = one_config.getAttribute('vmname')
                    config_vmid = one_config.getAttribute('vmid')
                    config_enable_ads = one_config.getAttribute('enable_ads')
                    config_start_cmd = one_config.getAttribute('startCommand')
                    config_appium_cmd = one_config.getAttribute('appiumCommand')

                    extend_vm_info = {
                        'win_x': one_config.getAttribute('win_x'),
                        'win_y': one_config.getAttribute('win_y'),
                        'win_scaling_percent2': one_config.getAttribute('win_scaling_percent2'),
                        'resolution_width': one_config.getAttribute('resolution_width'),
                        'resolution_height': one_config.getAttribute('resolution_height'),
                    }

                    self.configs.append({
                        'macAddress': machine_mac_address,
                        'vmid': config_vmid,
                        'vmname': config_vmname,
                        'enable': config_enable,
                        'enable_ads': config_enable_ads,
                        'startCommand': config_start_cmd,
                        'appiumCommand': config_appium_cmd,
                        'extend_vm_info': extend_vm_info
                    })

                    if not config_enable or config_enable != 'true':
                        continue

    def modify_all_vms(self):
        if len(self.configs) == 0:
            self.print("The vms config file is invalid, please run reload_vms_config_info() function first.")
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
                self.print("vmid=%s, vmname=%s, vmsfile=%s" % (config_vmid, config_vmname, config_path))
                VMSModifyHandler.rebuild(config_path)

    def set_vm_config(self, vmid, extend_info):
        self.print('start setting vm new config...')
        new_gps_pos = Utils.generate_new_pos()
        config_info = {
            'macaddress': ":".join(Utils.generate_new_mac_address_list()).upper(),
            'linenum': str(Utils.generate_new_phone_number()),
            'latitude': str(new_gps_pos['latitude']),
            'longitude': str(new_gps_pos['longitude']),
            'simserial': str(Utils.generate_new_simserial()),
            'imei': str(Utils.generate_new_imei()),

            # 'bssid': Utils.generate_new_bssid().upper(),
            # 'cellid': Utils.generate_new_cellid(),
            # 'ssid': Utils.generate_new_wifi_id(),
        }

        # 兼容扩展属性
        for key in extend_info.keys():
            value = extend_info[key]
            config_info[key] = value

        for key in config_info.keys():
            value = config_info[key]
            obj = subprocess.Popen([self.vmcmd, 'setconfig', '-i', vmid, key, value], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            cmd_out = obj.stdout.read()
            obj.stdout.close()
            self.print(cmd_out)

        self.print('setting vm new config over ...')

    async def adb_devices(self):
        obj = subprocess.Popen(['adb', 'devices'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        self.print('CMD: adb devices')
        self.print(cmd_out)

    async def start_vm(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'start', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'SUCCESS: start vm finished.':
            return True

        return False

    async def stop_vm(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'stop', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'SUCCESS: stop vm finished.':
            return True

        return False

    async def vm_is_running(self, vmid):
        obj = subprocess.Popen([self.vmcmd, 'isvmrunning', '-i', vmid], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = obj.stdout.read()
        obj.stdout.close()

        if cmd_out.strip() == 'Running':
            return True

        return False
