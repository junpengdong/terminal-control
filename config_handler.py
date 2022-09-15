import json
import datetime
from read_module import ReadModule
from global_constant import *


class ConfigHandler:

    def __init__(self):
        self.run_cache_config_path = './config/run_cache_config.json'
        self.automated_process_config_path = './config/automated_process_config.json'

    def init_config(self):
        # 读取自动化流程配置
        processes = ReadModule.read_config(self.automated_process_config_path)
        if len(processes) == 0:
            return False
        # 读取启动缓存配置
        run_cache = ReadModule.read_config(self.run_cache_config_path)
        # 获取已初始化流程名列表
        init_processes = run_cache.get(init_processes_key)
        if init_processes is None:
            init_processes = []
        # 需初始化配置流程列表
        need_init_processes = []
        for process in processes:
            process_name = process.get(process_name_key)
            if process_name in init_processes:
                continue
            need_init_processes.append(process)

        if len(need_init_processes) == 0:
            return False

        self.__handle_init(processes)

    # 处理初始化配置
    def __handle_init(self, processes):
        for process in processes:
            process_type = process.get(process_type_key)
            if process_type == process_type_tb:
                self.__init_tb_config(process)

    # 初始化tb类型配置
    def __init_tb_config(self, process):
        print(process)
        total_equipment = process.get(tb_total_equipment_key)
        total_execution_days = process.get(tb_total_execution_days_key)
        daily_equipment = int(total_equipment / total_execution_days)
        today = datetime.date.today()
        config_dict = {}
        for i in range(1, total_execution_days + 1):
            date = str(today + datetime.timedelta(days=i))
            daily_config = {
                new_equipment_key: daily_equipment,
                active_equipment_key: 0,
                status_key: 0
            }
            config_dict[date] = daily_config
        print(config_dict)
        daily_active = process.get(tb_daily_active_key)
        tomorrow = today + datetime.timedelta(days=1)
        if daily_active:
            active_days = process.get(tb_active_days_key)
            if active_days is None or active_days < 1:
                return False
            last_retained = process.get(tb_last_retained_key) / 100
            # 根据最后留存计算每日启动设备数
            for j in range(1, active_days + 1):
                before_date = str(tomorrow + datetime.timedelta(days=j-1))
                before_config = config_dict.get(before_date)
                before_active_equipment = before_config.get(active_equipment_key)
                if before_active_equipment == 0:
                    before_active_equipment = before_config.get(new_equipment_key)
                date = str(tomorrow + datetime.timedelta(days=j))
                config = config_dict.get(date)
                if config is None:
                    config = {
                        new_equipment_key: daily_equipment,
                        active_equipment_key: int(before_active_equipment *
                                                  self.__calculation_equipment(active_days, last_retained)),
                        status_key: 0
                    }
                else:
                    config[active_equipment_key] = int(before_active_equipment *
                                                       self.__calculation_equipment(active_days, last_retained))
                config_dict[date] = config

        print(config_dict)

    def init_active_config(self, execution_days, equipment, active_days, last_retained, tomorrow):
        config_dict = {}
        last_date = None
        # 计算出活跃最后执行日期
        for i in range(1, execution_days):
            temp_date = tomorrow + datetime.timedelta(days=i)
            for j in range(1, active_days):
                last_date = temp_date + datetime.timedelta(days=j)

        # 再反向计算每日需要跑的日活
        temp_date = last_date
        for i in range(1, execution_days + active_days):
            config = {}
            temp_equipment = equipment
            for j in range(1, active_days + 1):
                date_b = temp_date - datetime.timedelta(days=j)
                temp_equipment = int(temp_equipment * self.__calculation_equipment(active_days, last_retained))
                config[str(date_b)] = temp_equipment
            config_dict[str(temp_date)] = config
            temp_date = last_date - datetime.timedelta(days=i)
        return config_dict

    # 计算每日启动设备数
    @staticmethod
    def __calculation_equipment(days, retained):
        return round(pow(retained, 1/days), 4)



if __name__ == '__main__':
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    obj = ConfigHandler()
    res = obj.init_active_config(7, 70000, 7, 0.05, tomorrow)
    print(json.dumps(res))
    # x = pow(0.05, 1/30)
    # x = round(x, 3)
    # y = 300000
    # for i in range(1, 31):
    #     y = y * x
    #     print(int(y))

