import os

class Utils:
    @staticmethod
    def get_str_from_content(file_path):
        pwd = Utils.get_current_path(__file__)
        file_path = os.path.join(pwd, file_path)
        file_self = open(file_path)
        str_content = file_self.read()
        file_self.close()
        return str_content

    @staticmethod
    def get_current_path(path):
        current_path = os.path.dirname(path)
        return current_path