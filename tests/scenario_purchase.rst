======================================
Product Purchase Homologation Scenario
======================================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import Model, Wizard, Report
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term

Install product_purchase_homologation::

    >>> config = activate_modules('product_purchase_homologation')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()

Create account categories::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.save()

    >>> account_category_tax, = account_category.duplicate()
    >>> account_category_tax.supplier_taxes.append(tax)
    >>> account_category_tax.save()

Create product with ProductSupplier and Purchase Homologation Required = True::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')

    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.list_price = Decimal(10)
    >>> template.cost_price_method = 'fixed'
    >>> template.account_category = account_category
    >>> template.purchase_homologation_required = True
    >>> product, = template.products
    >>> product.cost_price = Decimal(5)
    >>> template.save()
    >>> product, = template.products

    >>> ProductSupplier = Model.get('purchase.product_supplier')
    >>> ps = ProductSupplier()
    >>> ps.product = template
    >>> ps.party = supplier
    >>> ps.save()

    >>> SupplierPrice = Model.get('purchase.product_supplier.price')
    >>> price1 = SupplierPrice()
    >>> price1.product_supplier = ps
    >>> price1.quantity = 0
    >>> price1.unit_price = Decimal(10)
    >>> price1.save()

Create product without ProductSupplier and Purchase Homologation Required = True::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')

    >>> template2 = ProductTemplate()
    >>> template2.name = 'product2'
    >>> template2.default_uom = unit
    >>> template2.type = 'goods'
    >>> template2.purchasable = True
    >>> template2.list_price = Decimal(10)
    >>> template2.cost_price_method = 'fixed'
    >>> template2.account_category = account_category
    >>> template2.purchase_homologation_required = True
    >>> product2, = template2.products
    >>> product2.cost_price = Decimal(5)
    >>> template2.save()
    >>> product2, = template2.products

Create product without ProductSupplier and Purchase Homologation Required = True::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')

    >>> template3 = ProductTemplate()
    >>> template3.name = 'product3'
    >>> template3.default_uom = unit
    >>> template3.type = 'goods'
    >>> template3.purchasable = True
    >>> template3.list_price = Decimal(10)
    >>> template3.cost_price_method = 'fixed'
    >>> template3.account_category = account_category
    >>> template3.purchase_homologation_required = False
    >>> product3, = template3.products
    >>> product3.cost_price = Decimal(5)
    >>> template3.save()
    >>> product3, = template3.products

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Purchase with ProductSupplier and Purchase Homologation Required = True::

    >>> Purchase = Model.get('purchase.purchase')
    >>> PurchaseLine = Model.get('purchase.line')
    >>> purchase = Purchase()
    >>> purchase.party = supplier
    >>> purchase.payment_term = payment_term
    >>> purchase_line = PurchaseLine()
    >>> purchase.lines.append(purchase_line)
    >>> purchase_line.product = product
    >>> purchase_line.quantity = 1.0
    >>> purchase_line.unit_price = Decimal(10)
    >>> purchase.save()
    >>> purchase.click('quote')
    >>> purchase.click('confirm')
    >>> purchase.state
    'processing'

Purchase without ProductSupplier and Purchase Homologation Required = False::

    >>> Purchase = Model.get('purchase.purchase')
    >>> PurchaseLine = Model.get('purchase.line')
    >>> purchase2 = Purchase()
    >>> purchase2.party = supplier
    >>> purchase2.payment_term = payment_term
    >>> purchase2_line = PurchaseLine()
    >>> purchase2.lines.append(purchase2_line)
    >>> purchase2_line.product = product2
    >>> purchase2_line.quantity = 1.0
    >>> purchase2_line.unit_price = Decimal(10)
    >>> purchase2.save()
    >>> purchase2.click('quote') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    UserError: ('UserError', (u'UserError: Cannot end the purchase "2" because the line "product2 @ 2" needs a supplier.', ''))

Purchase without ProductSupplier and Purchase Homologation Required = False::

    >>> Purchase = Model.get('purchase.purchase')
    >>> PurchaseLine = Model.get('purchase.line')
    >>> purchase3 = Purchase()
    >>> purchase3.party = supplier
    >>> purchase3.payment_term = payment_term
    >>> purchase3_line = PurchaseLine()
    >>> purchase3.lines.append(purchase3_line)
    >>> purchase3_line.product = product3
    >>> purchase3_line.quantity = 1.0
    >>> purchase3_line.unit_price = Decimal(10)
    >>> purchase3.save()
    >>> purchase3.click('quote')
    >>> purchase3.click('confirm')
    >>> purchase3.state
    'processing'