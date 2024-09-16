from odoo import models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _create_packed_picking(self, operation_type, stock_move_data, owner=None,
                               location=None, location_dest_id=None, package_name=None,
                               create_lots=False, set_ready=False):
        
        picking_vals = {
            'picking_type_id': operation_type.id,
            'owner_id': owner.id if owner else False,
            'location_id': location.id if location else operation_type.default_location_src_id.id,
            'location_dest_id': location_dest_id.id if location_dest_id else operation_type.default_location_dest_id.id,
        }
        picking = self.create(picking_vals)

        for product_id, qty_done, serial in stock_move_data:
            product = self.env['product.product'].browse(product_id)
            move_vals = {
                'name': product.display_name,
                'product_id': product.id,
                'product_uom_qty': qty_done,
                'product_uom': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
            }
            move = self.env['stock.move'].create(move_vals)
            
            move_line_vals = {
                'move_id': move.id,
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'qty_done': qty_done,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'picking_id': picking.id,
            }

            if create_lots:
                move_line_vals.update({'lot_name': serial})

            self.env['stock.move.line'].create(move_line_vals)

        picking.action_confirm()

        if set_ready:
            picking.action_assign()

        package = picking._put_in_pack(picking.move_line_ids)
        
        if package_name:
            package.write({'name': package_name})

        return picking
