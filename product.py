# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    purchase_homologation_required = fields.Boolean('Purchase Homologation '
        'Required')
