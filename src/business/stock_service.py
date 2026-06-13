from src.data.product_dao import ProductDAO
from src.data.stock_dao import StockDAO


class StockService:
    @staticmethod
    def stock_in(product_id, quantity, remark, operator_id):
        if quantity <= 0:
            raise ValueError("入库数量必须大于0")

        current_stock = ProductDAO.get_stock_by_product_id(product_id)
        new_stock = current_stock + quantity

        ProductDAO.update_stock(product_id, new_stock)
        StockDAO.add_stock_in_record(product_id, quantity, remark, operator_id)

        return True

    @staticmethod
    def stock_out(product_id, quantity, remark, operator_id):
        if quantity <= 0:
            raise ValueError("出库数量必须大于0")

        current_stock = ProductDAO.get_stock_by_product_id(product_id)

        if current_stock < quantity:
            raise ValueError("库存不足，无法出库")

        new_stock = current_stock - quantity

        ProductDAO.update_stock(product_id, new_stock)
        StockDAO.add_stock_out_record(product_id, quantity, remark, operator_id)

        return True

    @staticmethod
    def get_stock_by_product_id(product_id):
        return ProductDAO.get_stock_by_product_id(product_id)

    @staticmethod
    def get_stock_in_records(start_date=None, end_date=None):
        return StockDAO.get_stock_in_records(start_date, end_date)

    @staticmethod
    def get_stock_out_records(start_date=None, end_date=None):
        return StockDAO.get_stock_out_records(start_date, end_date)

    @staticmethod
    def get_all_records(start_date=None, end_date=None):
        return StockDAO.get_all_records(start_date, end_date)

    @staticmethod
    def get_stock_records(start_date=None, end_date=None, keyword=None):
        records = StockDAO.get_all_records(start_date, end_date)

        if keyword:
            keyword = keyword.lower()
            records = [
                record
                for record in records
                if (
                    record.get("product_name")
                    and keyword in record["product_name"].lower()
                )
                or (record.get("remark") and keyword in record["remark"].lower())
            ]

        for record in records:
            record["operator"] = record.get("operator_name", "")

        return records

    @staticmethod
    def export_records_to_excel(start_date, end_date, file_path):
        records = StockDAO.get_all_records(start_date, end_date)

        try:
            from openpyxl import Workbook

            wb = Workbook()
            ws = wb.active
            ws.title = "库存台账"

            headers = ["日期", "商品名称", "类型", "数量", "操作员", "备注"]
            ws.append(headers)

            for record in records:
                row = [
                    record["created_at"],
                    record.get("product_name", ""),
                    record["type"],
                    record["quantity"],
                    record.get("operator_name", ""),
                    record.get("remark", ""),
                ]
                ws.append(row)

            wb.save(file_path)
            return True
        except Exception as e:
            raise ValueError(f"导出失败: {str(e)}")
