# -*- coding: utf-8 -*
import json


class ReadModule:

    # 读取配置文件
    @staticmethod
    def read_config(file_path):
        return ReadModule.__read_data(file_path)

    @staticmethod
    def __read_data(file_path):
        try:
            # with open(file_path, 'r', encoding='utf=8') as content:
            with open(file_path, 'r') as content:
                return json.load(content)
        except Exception as e:
            return None


if __name__ == '__main__':
    # print(str(datetime.date.today()).replace("-", ""))
    # res = ReadModule.read_main_config()
    # print(res)
    count = 300000
    for i in range(1, 31):
        count = count * 0.901855372322704
        print(count)