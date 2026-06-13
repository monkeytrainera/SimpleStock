import datetime

import pytz

from src.data.db_connection import DBConnection


def get_current_time():
    """获取东八区当前时间"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


class StockDAO:
    @staticmethod
    def add_stock_in_record(product_id, quantity, remark, operator_id):
        db = DBConnection()
        sql = '''
        INSERT INTO stock_in_records (product_id, quantity, remark, operator_id, created_at)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor = db.execute(sql, (product_id, quantity, remark, operator_id, get_current_time()))
        return cursor.lastrowid

    @staticmethod
    def add_stock_out_record(product_id, quantity, remark, operator_id):
        db = DBConnection()
        sql = '''
        INSERT INTO stock_out_records (product_id, quantity, remark, operator_id, created_at)
        VALUES (?, ?, ?, ?, ?)
        '''
        cursor = db.execute(sql, (product_id, quantity, remark, operator_id, get_current_time()))
        return cursor.lastrowid

    @staticmethod
    def get_stock_in_records(start_date=None, end_date=None):
        db = DBConnection()
        sql = '''
        SELECT r.*, p.name as product_name, u.username as operator_name
        FROM stock_in_records r
        JOIN products p ON r.product_id = p.id
        JOIN users u ON r.operator_id = u.id
        '''
        params = []

        if start_date and end_date:
            sql += " WHERE r.created_at >= ? AND r.created_at <= ?"
            params.extend([start_date, end_date + " 23:59:59"])

        sql += " ORDER BY r.created_at DESC"
        results = db.query(sql, params)
        return [dict(row) for row in results]

    @staticmethod
    def get_stock_out_records(start_date=None, end_date=None):
        db = DBConnection()
        sql = '''
        SELECT r.*, p.name as product_name, u.username as operator_name
        FROM stock_out_records r
        JOIN products p ON r.product_id = p.id
        JOIN users u ON r.operator_id = u.id
        '''
        params = []

        if start_date and end_date:
            sql += " WHERE r.created_at >= ? AND r.created_at <= ?"
            params.extend([start_date, end_date + " 23:59:59"])

        sql += " ORDER BY r.created_at DESC"
        results = db.query(sql, params)
        return [dict(row) for row in results]

    @staticmethod
    def get_all_records(start_date=None, end_date=None):
        in_records = StockDAO.get_stock_in_records(start_date, end_date)
        out_records = StockDAO.get_stock_out_records(start_date, end_date)

        all_records = []
        for record in in_records:
            record['type'] = '入库'
            all_records.append(record)
        for record in out_records:
            record['type'] = '出库'
            all_records.append(record)

        all_records.sort(key=lambda x: x['created_at'], reverse=True)
        return all_records
