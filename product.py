# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields, ModelSQL, ModelView, Unique, Check

__all__ = ['Template']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    purchase_homologation_required = fields.Boolean('Purchase Homologation Required')