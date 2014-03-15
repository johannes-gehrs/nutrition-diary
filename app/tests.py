from __future__ import absolute_import, division, unicode_literals
from decimal import Decimal
from app import factories
from django.test import TestCase


class FoodTypeTest(TestCase):
    # Currently assumes specific default values in Factory Class
    ft = factories.FoodTypeFactory()

    def test_points_base(self):
        self.assertEqual(self.ft.points(), Decimal(2))

    def test_points_unrounded_base(self):
        self.assertAlmostEqual(self.ft.points(rounded=False), Decimal('2.293'), places=3)

    def test_points_qty(self):
        self.assertEqual(self.ft.points(quantity=Decimal(300)), Decimal(7))

    def test_points_unrounded_qty(self):
        self.assertAlmostEqual(self.ft.points(rounded=False, quantity=Decimal(300)),
                               Decimal('6.880'), places=3)

    def test_values_base(self):
        self.assertEquals(self.ft.values(), {u'calories': Decimal('29.4'),
                                             'carbon': Decimal('0.9'),
                                             'fat': Decimal('1.2'),
                                             'fiber': Decimal('0.0'),
                                             'protein': Decimal('3.75')})

    def test_values_qty(self):
        self.assertEqual(self.ft.values(quantity=Decimal(300)),
                         {u'calories': Decimal('294'),
                          'carbon': Decimal('9'),
                          'fat': Decimal('12'),
                          'fiber': Decimal('0'),
                          'protein': Decimal('37.5')})

    def test_values_qty_fat(self):
        self.assertEqual(self.ft.values(quantity=Decimal(300), keys=['fat']),
                         {'fat': Decimal('12')})


class ServingTest(TestCase):
    # Currently assumes specific default values in Factory Class
    srv = factories.ServingFactory()

    def test_points(self):
        self.assertEqual(self.srv.points(), Decimal(1))

    def test_points_unrounded(self):
        self.assertAlmostEqual(self.srv.points(rounded=False), Decimal(0.69), places=2)
