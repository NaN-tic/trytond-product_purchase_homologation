# This file is part product_purchase_homologation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import purchase

def register():
    Pool.register(
        product.Template,
        purchase.Purchase,
        module='product_purchase_homologation', type_='model')
