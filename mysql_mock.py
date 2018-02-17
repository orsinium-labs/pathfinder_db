import pymysql.cursors

conv = pymysql.converters.conversions

class Connection(pymysql.connections.Connection):  # noQA
    encoders = dict([(k, v) for (k, v) in conv.items() if type(k) is not int])
    encoding = 'utf8'
    charset = 'utf8_general_ci'
    server_status = 64

    def __init__(self):
        pass


cursor = pymysql.cursors.Cursor(Connection())
