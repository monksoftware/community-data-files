# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Numérigraphe SARL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    main_nace_id = fields.Many2one(
        'res.partner.category', string='Main economical activity')


class PartnerCategory(models.Model):
    """Let users search on code without a dot"""
    _inherit = 'res.partner.category'

    is_nace_category = fields.Boolean(default=False)

    @api.multi
    def name_get(self):
        """
        Always use short name for NACE categories,
        as they usually are very long
        """
        nace_categories = self.filtered('is_nace_category').with_context(
            partner_category_display='short')
        res_nace = super(PartnerCategory, nace_categories).name_get()
        non_nace_categories = self - nace_categories
        res_non_nace = super(PartnerCategory, non_nace_categories).name_get()
        return res_nace + res_non_nace

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """When no results are found, try again with an additional "."."""
        results = super(PartnerCategory, self).name_search(
            name, args=args, operator=operator, limit=limit)
        if not results and name and len(name) > 2:
            # Add a "." after the 2nd character, in case that makes a NACE code
            results = super(PartnerCategory, self).name_search(
                '%s.%s' % (name[:2], name[2:]), args=args, operator=operator,
                limit=limit)
        return results
