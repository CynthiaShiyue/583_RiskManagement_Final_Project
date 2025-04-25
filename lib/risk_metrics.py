# risk_metrics.py

import numpy as np
import pandas as pd


def calculate_qqq_risk_metrics(df, return_col="QQQ_Return", alpha=0.05):
    """
    Calculate Value at Risk (VaR) and Expected Shortfall (ES)
    for a given return series (e.g., QQQ returns).

    Parameters:
        df (pd.DataFrame): DataFrame containing the return column
        return_col (str): Name of the column containing daily returns
        alpha (float): Significance level (e.g., 0.05 for 95% VaR)

    Returns:
        dict: Dictionary with keys: 'VaR', 'ES', 'Confidence_Level'
    """
    if return_col not in df.columns:
        raise ValueError(f"'{return_col}' not found in DataFrame columns.")

    returns = df[return_col].dropna()

    # Value at Risk (VaR)
    var = np.percentile(returns, 100 * alpha)

    # Expected Shortfall (ES)
    es = returns[returns <= var].mean()

    return {"VaR": var, "ES": es, "Confidence_Level": f"{int((1 - alpha) * 100)}%"}
