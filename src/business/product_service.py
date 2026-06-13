from src.data.product_dao import ProductDAO


class ProductService:
    @staticmethod
    def add_product(name, spec, unit, initial_quantity, remark):
        if not name or not unit:
            raise ValueError("商品名称和单位不能为空")

        if initial_quantity < 0:
            raise ValueError("初始库存不能为负数")

        return ProductDAO.add_product(name, spec, unit, initial_quantity, remark)

    @staticmethod
    def update_product(product_id, name, spec, unit, remark):
        if not name or not unit:
            raise ValueError("商品名称和单位不能为空")

        return ProductDAO.update_product(product_id, name, spec, unit, remark)

    @staticmethod
    def delete_product(product_id):
        if ProductDAO.has_stock_or_records(product_id):
            raise ValueError("该商品有库存或操作记录，无法删除")

        return ProductDAO.delete_product(product_id)

    @staticmethod
    def get_product_by_id(product_id):
        return ProductDAO.get_product_by_id(product_id)

    @staticmethod
    def search_products(keyword):
        return ProductDAO.search_products(keyword)

    @staticmethod
    def get_all_products():
        return ProductDAO.get_all_products()

    @staticmethod
    def get_product_count():
        return ProductDAO.get_product_count()
