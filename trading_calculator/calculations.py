def calculate_asset_amount(operation_size, entry_price, leverage, operation_type ):
    if operation_type  == "Buy":
        return (operation_size * leverage) / entry_price
    elif operation_type  == "Sell":
        return (operation_size * leverage) / entry_price * -1
    else:
        return 0.0

def calculate_trade_result(entry_price, exit_price, asset_amount):
    return (exit_price - entry_price) * asset_amount

def get_leverage_value(leverage_selection):

    leverage_values = {
        "None": 1,
        "10x": 10,
        "20x": 20,
        "30x": 30,
        "50x": 50,
        "100x": 100
    }
    return leverage_values.get(leverage_selection, 1)
