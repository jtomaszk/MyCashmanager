from account_model.account import Account
from account_model.cycle import Cycle

__author__ = 'jtomaszk'


def save_cycle_execution(cycle_id, amount, execution_date, account_id=None):
    cycle = Cycle.get(cycle_id)

    if account_id is None:
        account = Account.get(cycle.account_id)
    else:
        account = Account.get(account_id)

    cycle.date_next = cycle.calculate_next()
    cycle.save_execute(execution_date)

    if cycle.transaction_type == 'INCOME':
        return account.add_income(amount, cycle.category_id, str(cycle.count + 1), execution_date)
    else:
        return account.add_outcome(amount, cycle.category_id, str(cycle.count + 1), execution_date)
