from odoo.tests import TransactionCase


class TestStockPicking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ResCompany = cls.env["res.company"]
        cls.StockPicking = cls.env["stock.picking"]
        cls.StockPackage = cls.env["stock.quant.package"]
        cls.StockQuant = cls.env["stock.quant"]
        cls.Product = cls.env["product.product"]
        cls.PackageLevel = cls.env["stock.package_level"]
        cls.StockMoveLine = cls.env["stock.move.line"]
        cls.company = cls.ResCompany.create({"name": "Company A"})
        cls.user_demo = cls.env["res.users"].create(
            {
                "login": "firstnametest",
                "name": "User Demo",
                "email": "firstnametest@example.org",
                "groups_id": [
                    (4, cls.env.ref("base.group_user").id),
                    (4, cls.env.ref("stock.group_stock_user").id),
                ],
            }
        )
        group_stock_multi_locations = cls.env.ref("stock.group_stock_multi_locations")
        group_stock_adv_location = cls.env.ref("stock.group_adv_location")
        cls.user_demo.write(
            {
                "company_id": cls.company.id,
                "company_ids": [(4, cls.company.id)],
                "groups_id": [
                    (4, group_stock_multi_locations.id, 0),
                    (4, group_stock_adv_location.id, 0),
                ],
            }
        )
        cls.stock_location = (
            cls.env["stock.location"]
            .sudo()
            .search(
                [("name", "=", "Stock"), ("company_id", "=", cls.company.id)], limit=1
            )
        )
        cls.warehouse = cls.stock_location.warehouse_id
        cls.warehouse.write({"reception_steps": "two_steps"})
        cls.input_location = cls.warehouse.wh_input_stock_loc_id
        cls.in_type = cls.warehouse.in_type_id
        cls.in_type.write({"show_entire_packs": True})
        cls.int_type = cls.warehouse.int_type_id
        cls.int_type.write({"show_entire_packs": True})
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")

    