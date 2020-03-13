class HBaseClient(object):
    """HBase数据库读取工具类
    """
    def __init__(self, connection):
        self.pool = connection

    def __init__(self, size, host, port):
        self.pool = happybase.ConnectionPool(size, host, port)

    def get(self, table_name, key_format, column_format=None, include_timestamp=False):
        """
        获取HBase数据库中的行记录数据
        :param table_name: 表名
        :param key_format: key格式字符串, 如表的'user:reco:1', 类型为bytes
        :param column_format: column, 列族字符串,如表的 column 'channel:18',类型为bytes
        :param include_timestamp: 是否包含时间戳
        :return: 返回数据库结果data
        """
        if not isinstance(key_format, bytes):
            raise KeyError("key_format or column type error")

        if not isinstance(table_name, str):
            raise KeyError("table_name should str type")

        with self.pool.connection() as conn:
            table = conn.table(table_name)

            if column_format:
                data = table.row(row=key_format, columns=[column_format], include_timestamp=include_timestamp)
            else:
                data = table.row(row=key_format)
            conn.close()

        if column_format:
            return data[column_format]
        else:
            # [(b'[141440,]', 1555519429582)]
            # {'[141440,]'}
            return data

    def get_cells(self, table_name, key_format, column_format=None,
                        timestamp=None, include_timestamp=False):
        """
        获取HBase数据库中多个版本数据
        :param table_name: 表名
        :param key_format: key格式字符串, 如表的'user:reco:1', 类型为bytes
        :param column_format: column, 列族字符串,如表的 column 'als:18',类型为bytes
        :param timestamp: 指定小于该时间戳的数据
        :param include_timestamp: 是否包含时间戳
        :return: 返回数据库结果data
        """
        if not isinstance(key_format, bytes) or not isinstance(column_format, bytes):
            raise KeyError("key_format or column type error")

        if not isinstance(table_name, str):
            raise KeyError("table_name should str type")

        with self.pool.connection() as conn:
            table = conn.table(table_name)

            data = table.cells(row=key_format, column=column_format,
                               timestamp=timestamp,
                               include_timestamp=include_timestamp)

            conn.close()
        # [(), ()]
        return data

    #插入某一个family下的column
    def put(self, table_name, key_format, column_format, data, timestamp=None):
        """

        :param table_name: 表名
        :param key_format: key格式字符串, 如表的'user:reco:1', 类型为bytes
        :param column_format: column, 列族字符串,如表的 column 'als:18',类型为bytes
        :param data: 插入的数据
        :param timestamp: 指定拆入数据的时间戳
        :return: None
        """
        if not isinstance(key_format, bytes) or not isinstance(column_format, bytes) or not isinstance(data, bytes):
            raise KeyError("key_format or column or data type error")

        if not isinstance(table_name, str):
            raise KeyError("table_name should str type")

        with self.pool.connection() as conn:
            table = conn.table(table_name)

            table.put(key_format, {column_format: data}, timestamp=timestamp)

            conn.close()
        return None

    #若干个不同family下的column更新数据存放在data_json中，一次性更新
    def put_json(self, table_name, key_format, data_json, timestamp=None):
        """

        :param table_name: 表名
        :param key_format: key格式字符串, 如表的'user:reco:1', 类型为bytes
        :param data_json: 插入的数据, column_format:data
        :param timestamp: 指定拆入数据的时间戳
        :return: None
        """
        if not isinstance(key_format, bytes) or not isinstance(column_format, bytes) or not isinstance(data, bytes):
            raise KeyError("key_format or column or data type error")

        if not isinstance(table_name, str):
            raise KeyError("table_name should str type")

        with self.pool.connection() as conn:
            table = conn.table(table_name)

            table.put(key_format, data_json, timestamp=timestamp)

            conn.close()
        return None

    def delete(self, table_name, key_format, column_format):
        """
        删除列族中的内容
        :param table_name: 表名称
        :param key_format: key
        :param column_format: 列格式
        :return:
        """
        if not isinstance(key_format, bytes) or not isinstance(column_format, bytes):
            raise KeyError("key_format or column type error")

        if not isinstance(table_name, str):
            raise KeyError("table_name should str type")
        with self.pool.connection() as conn:
            table = conn.table(table_name)
            table.delete(row=key_format, columns=[column_format])
            conn.close()
        return None