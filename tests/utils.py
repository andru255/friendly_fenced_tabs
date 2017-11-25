class Utils:
    def get_str_from_content(self, file_path):
        file_self = open(file_path)
        str_content = file_self.read()
        file_self.close()
        return str_content