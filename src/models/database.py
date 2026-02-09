import sqlite3
from src.models.transaction import Transaction, TransactionType
from src.models.savings_goal import SavingsGoal


class Database:
    # No ha sido nada facil trabajar con esto la verdad, me ha dado muchos problemas pero finalmente la aplicación para la version en la que esta
    # está totalmente funcional.
    _instance = None

    def __new__(cls, db_name="mintly.db"):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_name="mintly.db"):
        if self._initialized:
            return
        self.db_name = db_name
        self._initialized = True
        self._create_tables()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        with self._get_connection() as conn:
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS transactions
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             type
                             TEXT
                             NOT
                             NULL
                             CHECK (
                             type
                             IN
                         (
                             'ingreso',
                             'gasto',
                             'ahorro'
                         )),
                             amount REAL NOT NULL,
                             category TEXT NOT NULL,
                             description TEXT,
                             date TEXT NOT NULL
                             )
                         """)

            conn.execute("""
                         CREATE TABLE IF NOT EXISTS savings_goals
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             name
                             TEXT
                             NOT
                             NULL,
                             target_amount
                             REAL
                             NOT
                             NULL,
                             current_amount
                             REAL
                             DEFAULT
                             0,
                             deadline
                             TEXT,
                             description
                             TEXT
                         )
                         """)

    def _get_type_string(self, t_type):
        mapping = {
            TransactionType.INCOME: 'ingreso',
            TransactionType.EXPENSE: 'gasto',
            TransactionType.SAVINGS: 'ahorro',
            'INCOME': 'ingreso',
            'EXPENSE': 'gasto',
            'SAVINGS': 'ahorro',
            'ingreso': 'ingreso',
            'gasto': 'gasto',
            'ahorro': 'ahorro'
        }
        return mapping.get(t_type, 'gasto')

    def add_transaction(self, t: Transaction) -> int:
        tipo_db = self._get_type_string(t.transaction_type)

        query = """
                INSERT INTO transactions (type, amount, category, description, date)
                VALUES (?, ?, ?, ?, ?) \
                """
        with self._get_connection() as conn:
            cursor = conn.execute(
                query,
                (tipo_db, t.amount, t.category, t.description, t.date)
            )
            return cursor.lastrowid

    def delete_transaction(self, t_id: int) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (t_id,))
            return True

    def get_all_transactions(self, limit: int = None) -> list:
        query = "SELECT * FROM transactions ORDER BY date DESC, id DESC"
        if limit:
            query += f" LIMIT {limit}"
        with self._get_connection() as conn:
            rows = conn.execute(query).fetchall()
            return [self._row_to_transaction(r) for r in rows]

    def get_transactions_by_type(self, t_type, limit: int = None) -> list:
        tipo_db = self._get_type_string(t_type)
        query = "SELECT * FROM transactions WHERE type = ? ORDER BY date DESC, id DESC"
        if limit:
            query += f" LIMIT {limit}"
        with self._get_connection() as conn:
            rows = conn.execute(query, (tipo_db,)).fetchall()
            return [self._row_to_transaction(r) for r in rows]

    def get_balance_by_period(self, start: str, end: str) -> dict:
        query = """
                SELECT type, SUM(amount) as total
                FROM transactions
                WHERE date BETWEEN ? AND ?
                GROUP BY type \
                """
        result = {"ingreso": 0.0, "gasto": 0.0, "ahorro": 0.0}
        with self._get_connection() as conn:
            rows = conn.execute(query, (start, end)).fetchall()
            for r in rows:
                result[r['type']] = float(r['total'] or 0.0)

        return {
            'total_income': result['ingreso'],
            'total_expense': result['gasto'],
            'total_savings': result['ahorro']
        }

    def get_expenses_by_category(self) -> dict:
        return self._get_category_totals('gasto')

    def get_income_by_category(self) -> dict:
        return self._get_category_totals('ingreso')

    def get_savings_by_category(self) -> dict:
        return self._get_category_totals('ahorro')

    def _get_category_totals(self, t_type: str) -> dict:
        query = "SELECT category, SUM(amount) as total FROM transactions WHERE type = ? GROUP BY category"
        with self._get_connection() as conn:
            rows = conn.execute(query, (t_type,)).fetchall()
            return {r['category']: float(r['total']) for r in rows}

    @staticmethod
    def _row_to_transaction(r) -> Transaction:
        type_map = {
            'ingreso': TransactionType.INCOME,
            'gasto': TransactionType.EXPENSE,
            'ahorro': TransactionType.SAVINGS
        }
        return Transaction(
            transaction_type=type_map.get(r['type'], TransactionType.EXPENSE),
            amount=r['amount'],
            category=r['category'],
            description=r['description'],
            date=r['date'],
            transaction_id=r['id']
        )

    def add_savings_goal(self, goal: SavingsGoal) -> int:
        query = "INSERT INTO savings_goals (name, target_amount, current_amount, deadline, description) VALUES (?, ?, ?, ?, ?)"
        params = (goal.name, goal.target_amount, goal.current_amount, goal.deadline, goal.description)
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid

    def update_savings_goal_amount(self, goal_id: int, amount: float) -> bool:
        query = "UPDATE savings_goals SET current_amount = current_amount + ? WHERE id = ?"
        with self._get_connection() as conn:
            conn.execute(query, (amount, goal_id))
            return True

    def get_all_savings_goals(self) -> list:
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM savings_goals ORDER BY id DESC").fetchall()
            return [SavingsGoal(name=r['name'], target_amount=r['target_amount'],
                                current_amount=r['current_amount'], deadline=r['deadline'],
                                description=r['description'], goal_id=r['id']) for r in rows]

    def delete_savings_goal(self, g_id: int) -> bool:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM savings_goals WHERE id = ?", (g_id,))
            return True