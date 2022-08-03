""" Tests for arithmetic operations. Intention is to verify that gurobipy
objects correctly defer to Series for arithmetic operations. """

import unittest

import gurobipy as gp
import gurobipy_pandas
import pandas as pd


class GurobiTestCase(unittest.TestCase):
    def setUp(self):
        self.env = gp.Env()
        self.model = gp.Model(env=self.env)

    def tearDown(self):
        self.model.close()
        self.env.close()

    def assert_expression_equal(self, expr1, expr2):
        if isinstance(expr1, gp.LinExpr):
            self.assertIsInstance(expr2, gp.LinExpr)
            self.assertEqual(expr1.getConstant(), expr2.getConstant())
            self.assertEqual(expr1.size(), expr2.size())
            for i in range(expr1.size()):
                self.assertTrue(expr1.getVar(i).sameAs(expr2.getVar(i)))
                self.assertEqual(expr1.getCoeff(i), expr2.getCoeff(i))
        elif isinstance(expr1, gp.QuadExpr):
            self.assertIsInstance(expr2, gp.QuadExpr)
            self.assert_expression_equal(expr1.getLinExpr(), expr2.getLinExpr())
            self.assertEqual(expr1.size(), expr2.size())
            for i in range(expr1.size()):
                self.assertTrue(expr1.getVar1(i).sameAs(expr2.getVar1(i)))
                self.assertTrue(expr1.getVar2(i).sameAs(expr2.getVar2(i)))
                self.assertEqual(expr1.getCoeff(i), expr2.getCoeff(i))
        else:
            raise TypeError(f"{type(expr1)} not handled")


class TestAdd(GurobiTestCase):
    def test_varseries_var(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        self.model.update()
        result = x + y
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x[i] + y)

    @unittest.expectedFailure
    def test_var_varseries(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        self.model.update()
        result = y + x
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], y + x[i])

    def test_dataseries_var(self):
        x = self.model.addVar(name="x")
        self.model.update()
        result = pd.Series(list(range(5))) + x
        self.assertIsInstance(result, pd.Series)
        # Note if we use extension types in future, this would not
        # come out as an extension type.
        for i in range(5):
            self.assert_expression_equal(result[i], i + x)

    @unittest.expectedFailure
    def test_var_dataseries(self):
        x = self.model.addVar(name="x")
        self.model.update()
        result = x + pd.Series(list(range(5)))
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x + i)

    def test_varseries_linexpr(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        le = 2 * y + 1
        self.model.update()
        result = x + le
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x[i] + 2 * y + 1)

    @unittest.expectedFailure
    def test_linexpr_varseries(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        le = 2 * y + 1
        self.model.update()
        result = le + x
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], 2 * y + 1 + x[i])

    def test_varseries_quadexpr(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        qe = y * y + 2 * y + 3
        self.model.update()
        result = x + qe
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x[i] + y * y + 2 * y + 3)

    @unittest.expectedFailure
    def test_quadexpr_varseries(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        qe = y * y + 2 * y + 3
        self.model.update()
        result = qe + x
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], y * y + 2 * y + 3 + x[i])


class TestIadd(GurobiTestCase):
    def test_varseries_var(self):
        # Make series manually here so original isn't changed.
        x0 = list(self.model.addVars(3).values())
        x = pd.Series(x0)
        y = self.model.addVar(name="y")
        self.model.update()
        x += y
        self.assertIsInstance(x, pd.Series)
        for i in range(3):
            self.assert_expression_equal(x[i], x0[i] + y)

    def test_linexprseries_var(self):
        x = pd.RangeIndex(3).grb.pd_add_vars(self.model, name="x")
        le = x * 1
        y = self.model.addVar(name="y")
        self.model.update()
        le += y
        self.assertIsInstance(le, pd.Series)
        for i in range(3):
            self.assert_expression_equal(le[i], x[i] + y)

    def test_quadexprseries_var(self):
        x = pd.RangeIndex(3).grb.pd_add_vars(self.model, name="x")
        qe = x * x
        y = self.model.addVar(name="y")
        self.model.update()
        qe += y
        self.assertIsInstance(qe, pd.Series)
        for i in range(3):
            self.assert_expression_equal(qe[i], x[i] * x[i] + y)

    @unittest.expectedFailure
    def test_var_varseries(self):
        # Type uplift to Series (reassignment)
        x = pd.RangeIndex(3).grb.pd_add_vars(self.model, name="x")
        y0 = self.model.addVar(name="y")
        y = y0
        self.model.update()
        y += x
        self.assertIsInstance(y, pd.Series)
        for i in range(3):
            self.assert_expression_equal(y[i], y0 + x[i])

    @unittest.expectedFailure
    def test_linexpr_varseries(self):
        # Type uplift to Series (reassignment)
        # Expected call chain:
        #   1. LinExpr.__iadd__(Series) -> return NotImplemented
        #   2. Series.__radd__(LinExpr) -> expanded along series
        #   3. LinExpr.__add__(Var) -> new LinExpr for each in series
        #   4. New series reassigned over le
        x = pd.RangeIndex(3).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        le = 2 * y
        self.model.update()
        le += x
        self.assertIsInstance(le, pd.Series)
        for i in range(3):
            self.assert_expression_equal(le[i], 2 * y + x[i])

    @unittest.expectedFailure
    def test_quadexpr_varseries(self):
        # Type uplift to Series (reassignment)
        x = pd.RangeIndex(3).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        qe = y * y
        self.model.update()
        qe += x
        self.assertIsInstance(qe, pd.Series)
        for i in range(3):
            self.assert_expression_equal(qe[i], y * y + x[i])


class TestMul(GurobiTestCase):
    def test_varseries_var(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        self.model.update()
        result = x * y
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x[i] * y)

    @unittest.expectedFailure
    def test_var_varseries(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        self.model.update()
        result = y * x
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], y * x[i])

    def test_varseries_linexpr(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        le = 2 * y
        self.model.update()
        result = x * le
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], x[i] * 2 * y)

    @unittest.expectedFailure
    def test_linexpr_varseries(self):
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        le = 2 * y
        self.model.update()
        result = le * x
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], 2 * y * x[i])

    def test_dataseries_quadexpr(self):
        s = pd.Series(list(range(5)))
        y = self.model.addVar(name="y")
        qe = y * y
        self.model.update()
        result = s * qe
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], i * y * y)

    @unittest.expectedFailure
    def test_quadexpr_dataseries(self):
        s = pd.Series(list(range(5)))
        y = self.model.addVar(name="y")
        qe = y * y
        self.model.update()
        result = qe * s
        self.assertIsInstance(result, pd.Series)
        for i in range(5):
            self.assert_expression_equal(result[i], i * y * y)

    @unittest.expectedFailure
    def test_varseries_quadexpr(self):
        # Cannot multiply, should get a python TypeError
        x = pd.RangeIndex(5).grb.pd_add_vars(self.model, name="x")
        y = self.model.addVar(name="y")
        qe = y * y
        self.model.update()
        with self.assertRaises(TypeError):
            x * qe
