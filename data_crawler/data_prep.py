import re


class CodePreprocess:
    def __init__(self):
        pass

    @staticmethod
    def remove_comment(code):
        return re.sub(r"(\/\/.+)|(#.+)|('.+)|(\/\*[^(\*\/)]+?\*\/)|(\"{3}[^(\"{3})]+?\"{3})", ' ', code)

    @staticmethod
    def remove_space(code):
        return re.sub("\s+", ' ', code.strip())

    def preprocess(self, code):
        code = self.remove_comment(code)
        code = self.remove_space(code)
        return code
