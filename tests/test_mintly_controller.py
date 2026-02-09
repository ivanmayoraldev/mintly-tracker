import unittest
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.transaction import Transaction, TransactionType
from src.models.savings_goal import SavingsGoal
from src.models.database import Database
from src.controllers.mintly import Mintly


class TestTransaction(unittest.TestCase):
    def test_create_income_transaction(self):
        trans = Transaction(
            transaction_type=TransactionType.INCOME,
            amount=1000.0,
            category="💼 Salario",
            description="Salario mensual",
            date="2024-01-15"
        )

        self.assertEqual(trans.transaction_type, TransactionType.INCOME)
        self.assertEqual(trans.amount, 1000.0)
        self.assertEqual(trans.category, "💼 Salario")
        self.assertTrue(trans.is_income())
        self.assertFalse(trans.is_expense())

    def test_create_expense_transaction(self):
        trans = Transaction(
            transaction_type=TransactionType.EXPENSE,
            amount=50.0,
            category="🛒 Alimentación",
            description="Compra supermercado",
            date="2024-01-16"
        )

        self.assertEqual(trans.transaction_type, TransactionType.EXPENSE)
        self.assertTrue(trans.is_expense())
        self.assertFalse(trans.is_income())

    def test_create_savings_transaction(self):
        trans = Transaction(
            transaction_type=TransactionType.SAVINGS,
            amount=200.0,
            category="💰 Auto-Ahorro",
            description="Ahorro automático",
            date="2024-01-17"
        )

        self.assertEqual(trans.transaction_type, TransactionType.SAVINGS)
        self.assertTrue(trans.is_savings())


class TestSavingsGoal(unittest.TestCase):
    def test_create_savings_goal(self):
        goal = SavingsGoal(
            name="Vacaciones",
            target_amount=3000.0,
            current_amount=500.0,
            deadline="2024-12-31",
            description="Viaje a Europa"
        )

        self.assertEqual(goal.name, "Vacaciones")
        self.assertEqual(goal.target_amount, 3000.0)
        self.assertEqual(goal.current_amount, 500.0)
        self.assertIsNone(goal.id)

    def test_progress_percentage_calculation(self):
        goal = SavingsGoal(
            name="Laptop",
            target_amount=1000.0,
            current_amount=250.0
        )

        self.assertEqual(goal.progress_percentage, 25.0)

    def test_progress_percentage_zero_target(self):
        goal = SavingsGoal(
            name="Test",
            target_amount=0.0,
            current_amount=100.0
        )

        self.assertEqual(goal.progress_percentage, 0.0)

    def test_progress_percentage_over_100(self):
        goal = SavingsGoal(
            name="Exceso",
            target_amount=100.0,
            current_amount=150.0
        )

        self.assertEqual(goal.progress_percentage, 100.0)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_mintly.db")

    def tearDown(self):
        try:
            os.remove("test_mintly.db")
        except:
            pass

    def test_add_transaction(self):
        trans = Transaction(
            transaction_type=TransactionType.INCOME,
            amount=500.0,
            category="💼 Salario",
            description="Test",
            date="2024-01-20"
        )

        trans_id = self.db.add_transaction(trans)
        self.assertIsNotNone(trans_id)
        self.assertGreater(trans_id, 0)

    def test_add_and_retrieve_savings_goal(self):
        goal = SavingsGoal(
            name="Test Goal",
            target_amount=1000.0,
            current_amount=0.0,
            deadline="2024-12-31"
        )

        goal_id = self.db.add_savings_goal(goal)
        self.assertIsNotNone(goal_id)

        goals = self.db.get_all_savings_goals()
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0].name, "Test Goal")

    def test_update_savings_goal_amount(self):
        goal = SavingsGoal(
            name="Update Test",
            target_amount=1000.0,
            current_amount=100.0
        )

        goal_id = self.db.add_savings_goal(goal)
        self.db.update_savings_goal_amount(goal_id, 200.0)

        goals = self.db.get_all_savings_goals()
        self.assertEqual(goals[0].current_amount, 300.0)


class TestMintlyController(unittest.TestCase):

    def setUp(self):
        self.controller = Mintly()
        self.controller.db = Database("test_controller.db")

    def tearDown(self):
        try:
            os.remove("test_controller.db")
        except:
            pass

    def test_create_simple_transaction(self):
        trans_id = self.controller.create_transaction(
            t_type=TransactionType.INCOME,
            amount=1000.0,
            category="💼 Salario",
            description="Test",
            date="2024-01-20"
        )

        self.assertIsNotNone(trans_id)

    def test_monthly_balance_calculation(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.controller.create_transaction(
            t_type=TransactionType.INCOME,
            amount=2000.0,
            category="💼 Salario",
            description="Salario",
            date=today
        )

        self.controller.create_transaction(
            t_type=TransactionType.EXPENSE,
            amount=500.0,
            category="🛒 Alimentación",
            description="Compras",
            date=today
        )

        balance = self.controller.get_monthly_balance()

        self.assertEqual(balance['total_income'], 2000.0)
        self.assertEqual(balance['total_expense'], 500.0)
        self.assertEqual(balance['balance'], 1500.0)

    def test_auto_savings_creation(self):
        goal_id = self.controller.create_savings_goal(
            name="Test Auto-Save",
            target_amount=1000.0,
            current_amount=0.0,
            deadline="2024-12-31",
            description="Test"
        )

        today = datetime.now().strftime("%Y-%m-%d")

        self.controller.create_transaction(
            t_type=TransactionType.INCOME,
            amount=1000.0,
            category="💼 Salario",
            description="Test",
            date=today,
            goal_id=goal_id,
            save_pct=20
        )

        savings_trans = self.controller.get_transactions_by_type(TransactionType.SAVINGS)
        self.assertEqual(len(savings_trans), 1)
        self.assertEqual(savings_trans[0].amount, 200.0)

        goals = self.controller.get_all_savings_goals()
        self.assertEqual(goals[0].current_amount, 200.0)

    def test_manual_savings_addition(self):
        goal_id = self.controller.create_savings_goal(
            name="Manual Save Test",
            target_amount=1000.0,
            current_amount=100.0,
            deadline="2024-12-31",
            description="Test"
        )

        self.controller.add_to_savings_goal(goal_id, 250.0)

        goals = self.controller.get_all_savings_goals()
        self.assertEqual(goals[0].current_amount, 350.0)

    def test_financial_health_score(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.controller.create_transaction(
            t_type=TransactionType.INCOME,
            amount=2000.0,
            category="💼 Salario",
            description="Salario",
            date=today
        )

        self.controller.create_transaction(
            t_type=TransactionType.EXPENSE,
            amount=600.0,
            category="🛒 Alimentación",
            description="Gastos",
            date=today
        )

        health = self.controller.get_financial_health_score()

        self.assertIn('score', health)
        self.assertIn('level', health)
        self.assertIn('message', health)
        self.assertGreaterEqual(health['score'], 0)
        self.assertLessEqual(health['score'], 100)

    def test_delete_transaction(self):
        trans_id = self.controller.create_transaction(
            t_type=TransactionType.EXPENSE,
            amount=100.0,
            category="🎬 Ocio",
            description="Cine",
            date=datetime.now().strftime("%Y-%m-%d")
        )

        all_trans = self.controller.get_all_transactions()
        initial_count = len(all_trans)

        self.controller.delete_transaction(trans_id)

        all_trans = self.controller.get_all_transactions()
        self.assertEqual(len(all_trans), initial_count - 1)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestTransaction))
    suite.addTests(loader.loadTestsFromTestCase(TestSavingsGoal))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestMintlyController))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())