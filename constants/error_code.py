class ErrorNode:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def unpack(self):
        return self.code, self.msg


class Error:
    success = ErrorNode("0000", "success")
    timeout_error = ErrorNode("9999", "请求超时")
    third_party_error = ErrorNode("FFFF", "第三方错误")
    request_error = ErrorNode("FFFF", "请求第三方发生内部错误")
    inter_error = ErrorNode("FFFF", "系统内部错误")