# This file is part product_purchase_homologation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import doctest
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class ProductPurchaseHomologationTestCase(ModuleTestCase):
    'Test Product Purchase Homologation module'
    module = 'product_purchase_homologation'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductPurchaseHomologationTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_purchase.rst',
            tearDown=doctest_teardown, encoding='UTF-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
