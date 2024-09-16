from odoo import models, fields, api

class PackProductsWizard(models.TransientModel):
    _name = 'pack.products.wizard'
    _description = 'Pack Products Wizard'

    operation_type_id = fields.Many2one(
        'stock.picking.type', string='Operation Type', required=True)
    owner_id = fields.Many2one('res.partner', string='Owner')
    location_id = fields.Many2one(
        'stock.location', string='Source Location')
    location_dest_id = fields.Many2one(
        'stock.location', string='Destination Location')
    package_name = fields.Char(string='Package Name')
    create_lots = fields.Boolean(string='Create Lots')
    set_ready = fields.Boolean(string='Set Ready')
    product_ids = fields.One2many(
        'pack.products.wizard.line', 'wizard_id', string='Products')

    @api.onchange('operation_type_id')
    def _onchange_operation_type_id(self):
        if self.operation_type_id:
            self.location_id = self.operation_type_id.default_location_src_id
            self.location_dest_id = self.operation_type_id.default_location_dest_id

    def action_create_picking(self):
        stock_move_data = []
        for line in self.product_ids:
            stock_move_data.append(
                (line.product_id.id, line.qty_done, line.serial))
        picking = self.env['stock.picking']._create_packed_picking(
            operation_type=self.operation_type_id,
            stock_move_data=stock_move_data,
            owner=self.owner_id,
            location=self.location_id,
            location_dest_id=self.location_dest_id,
            package_name=self.package_name,
            create_lots=self.create_lots,
            set_ready=self.set_ready,
        )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Picking',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': picking.id,
        }

class PackProductsWizardLine(models.TransientModel):
    _name = 'pack.products.wizard.line'
    _description = 'Pack Products Wizard Line'

    wizard_id = fields.Many2one(
        'pack.products.wizard', string='Wizard', required=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    qty_done = fields.Float(string='Quantity Done', required=True, default=1.0)
    serial = fields.Char(string='Serial Number')
