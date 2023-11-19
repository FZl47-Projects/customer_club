import json


class UserDetail:

    def __init__(self, user):
        self.user = user

    @property
    def data(self):
        user = self.user
        user_data = {
            'id': user.id,
            'number_id': user.get_number_id(),
            'phonenumber': str(user.phonenumber),
            'full_name': user.get_full_name(),
            'wallet_amount': user.get_wallet().amount,
        }

        transactions_data = {
            'transactions': []
        }
        for transaction in user.get_transactions():
            transactions_data['transactions'].append({
                'number_id': transaction.number_id,
                'created_at': str(transaction.created_at),
                'amount': transaction.amount,
                'amount_refund': transaction.amount_refund,
                'discount_percentage': transaction.discount_percentage
            })

        data = {**user_data, **transactions_data}
        return json.dumps(data)
