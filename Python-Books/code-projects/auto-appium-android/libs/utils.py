# -*- coding: utf-8 -*-

import random
import string
import time

class Utils(object):
    """
    工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def get_now_time():
        millis = int(round(time.time() * 1000))
        return millis

    @staticmethod
    def generate_new_phone_number(country='US'):
        """
        生成新的模拟手机电话号码
        :param country:
        :return:
        """
        N = 11
        part = ''.join(str(random.randrange(0, 9)) for _ in range(N - 1))
        new_phone_number = '+{}{}'.format(1, part)
        return new_phone_number

    @staticmethod
    def generate_new_mac_address():
        """
        生成新的MAC地址
        :param self:
        :return:
        """
        new_mac_address = ":".join(Utils.generate_new_mac_address_list())
        return new_mac_address.upper()

    @staticmethod
    def generate_new_mac_address_list():
        """
        生成新的MAC地址的列表，方便后面格式化
        :return:
        """
        mac_list = []
        for i in range(1,7):
            rand_str = "".join(random.sample("0123456789abcdef",2))
            mac_list.append(rand_str)
        return mac_list


    @staticmethod
    def generate_new_simserial():
        """
        获取新的simserial
        :return:
        """
        N = 20
        part1 = ''.join(random.sample("123456789",1))
        part2 = ''.join(str(random.randrange(1, 9)) for _ in range(N - 1))
        new_simserial = '{}{}'.format(part1, part2)
        return new_simserial

    @staticmethod
    def generate_new_bssid():
        """
        获取bssid
        :return:
        """
        bssid_list = []
        for i in range(1,7):
            rand_str = "".join(random.sample("0123456789abcdef",2))
            bssid_list.append(rand_str)
        return ":".join(bssid_list)

    @staticmethod
    def generate_new_cellid():
        N = 10
        part = ''.join(str(random.randrange(1, 9)) for _ in range(N - 1))
        new_cellid = '{}'.format(part)
        return new_cellid


    @staticmethod
    def generate_new_wifi_id():
        """
        生成新的wifi_id
        :param self:
        :return:
        """
        new_wifi_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        return new_wifi_id

    @staticmethod
    def _luhn_residue(digits):
        return sum(sum(divmod(int(d) * (1 + i % 2), 10))
                   for i, d in enumerate(digits[::-1])) % 10

    @staticmethod
    def _getImei(N):
        part = ''.join(str(random.randrange(0, 9)) for _ in range(N - 1))
        res = Utils._luhn_residue('{}{}'.format(part, 0))
        return '{}{}'.format(part, -res % 10)

    @staticmethod
    def generate_new_imei(country='US'):
        """
        生成新的imei
        IMEI为15位数字
        格式为AAAAAAAA BBBBBB C
        AAAAAAAA 为 Type Allocation Code
        BBBBBB 为 Serial Number
        C 为 Check Digit
        IMEI校验码算法：
        (1).将偶数位数字分别乘以2，分别计算个位数和十位数之和
        (2).将奇数位数字相加，再加上上一步算得的值
        (3).如果得出的数个位是0则校验位为0，否则为10减去个位数
        :param self:
        :return:
        """
        return Utils._getImei(15)

    @staticmethod
    def generate_new_pos(country='US'):
        """
        获取新的地理位置
        :param country:
        :return:
        """
        latitude_maps = {
            ''
        }

        long_part_float = round(random.uniform(0, 1), 6)
        long_part_int = random.randint(73, 120)
        longitude = "-{}".format(long_part_int + abs(long_part_float))

        # 计算范围，防止越界
        max_lat = 45
        min_lat = 25
        if long_part_int <= 75:
            min_lat = 39
            max_lat = 43
        elif long_part_int > 75 and long_part_int <= 77:
            min_lat = 35
            max_lat = 42
        elif long_part_int > 77 and long_part_int <= 110:
            min_lat = 30
            max_lat = 41
        elif long_part_int > 110:
            min_lat = 38
            max_lat = 45

        lat_part_float = round(random.uniform(0, 1), 6)
        lat_part_int = random.randint(min_lat, max_lat)
        latitude = "{}".format(lat_part_int + abs(lat_part_float))

        return {
            'latitude': latitude,
            'longitude': longitude,
        }