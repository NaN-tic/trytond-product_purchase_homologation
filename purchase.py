# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.exceptions import UserError
from trytond.i18n import gettext


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    @classmethod
    def quote(cls, purchases):
        pool = Pool()
        PProductSupplier = pool.get('purchase.product_supplier')

        super(Purchase, cls).quote(purchases)
        for purchase in purchases:
            for line in purchase.lines:
                if (line.product and
                        not line.product_supplier and
                        line.product.purchase_homologation_required):
                    raise UserError(gettext(
                        'product_purchase_homologation.cannot_end_purchase',
                        purchase=purchase.id,
                        line=line.rec_name))
                if (line.product and
                        line.product.purchase_homologation_required and
                        line.product_supplier and
                        line.product_supplier.active == False and
                        line.type == 'line'):
                    raise UserError(gettext(
                        'product_purchase_homologation.product_purchase_deactivate',
                        purchase=purchase.id,
                    ))
