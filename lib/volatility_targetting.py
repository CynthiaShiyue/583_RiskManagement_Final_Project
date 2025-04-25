def rebalance_portfolio(
    predicted_volatility,
    portfolio_value,
    target_annualized_volatility=0.20,
    max_leverage=2.0,
    trading_days=252,
):
    """
    Rebalance the QQQ portfolio based on predicted next-day volatility (Volatility Targeting approach).

    Parameters:
        predicted_volatility (float): Predicted next-day daily volatility (standard deviation).
        portfolio_value (float): Current total value of the portfolio (e.g., $1,000,000).
        target_annualized_volatility (float): Target annualized volatility (default is 20%).
        max_leverage (float): Maximum allowed leverage (default is 2.0x).
        trading_days (int): Number of trading days in a year (default is 252).

    Returns:
        position_value (float): Dollar amount to allocate to QQQ.
        cash_value (float): Dollar amount to hold in cash.
        target_weight (float): Target portfolio weight allocated to QQQ.
    """

    if predicted_volatility <= 0:
        raise ValueError("Predicted volatility must be positive.")

    # 1. Calculate target daily volatility
    target_daily_volatility = target_annualized_volatility / (trading_days**0.5)

    # 2. Calculate target portfolio weight
    target_weight = target_daily_volatility / predicted_volatility

    # 3. Cap the maximum leverage
    target_weight = min(target_weight, max_leverage)

    # 4. Calculate allocation amounts
    position_value = target_weight * portfolio_value
    cash_value = portfolio_value - position_value

    return position_value, cash_value, target_weight
