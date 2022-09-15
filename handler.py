from read_module import ReadModule


class Handler:

    @staticmethod
    def init_main_process_data():
        data = ReadModule.read_main_config()
        print(data)

    @staticmethod
    def __init_execute_process_data():
        data = ReadModule.read_execute_config()
        print(data)


if __name__ == '__main__':
    Handler.init_main_process_data()