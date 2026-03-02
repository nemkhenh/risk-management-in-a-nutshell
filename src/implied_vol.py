from .pricing import bsm_call, _validate_inputs

def implied_vol_call(
        market_price: float, 
        S: float, 
        K: float, 
        r: float, 
        T: float,
        sigma_low: float = 1e-6,
        sigma_high: float = 5.0,
        tol: float = 1e-8, 
        max_iter: int = 1000
) -> float:
    """
    Calculate the implied volatility of a European call option using the bisection method.
    
    We solve: bsm_call(S,K,r,sigma,T) - market_price = 0

    Parameters:
    - market_price: The observed market price of the call option.
    - S: Current stock price.
    - K: Strike price.
    - r: Risk-free interest rate (annualized).
    - T: Time to maturity (in years).
    - sigma_low: Lower bound for volatility search (default: 1e-6).
    - sigma_high: Upper bound for volatility search (default: 5.0).
    - tol: Tolerance for convergence (default: 1e-8).
    - max_iter: Maximum number of iterations to prevent infinite loops (default: 1000).
    
    Returns:
    - Implied volatility as a decimal (e.g., 0.2 for 20%).
    
    Raises:
    - ValueError if the market price is out of bounds or if convergence fails.
    """
    
    # Check if market price is within bounds
    if market_price < 0:
        raise ValueError("Market price cannot be negative.")
    
    _validate_inputs(S, K, r, sigma_low, T)

    def f(sig:float) -> float:return bsm_call(S, K, r, sig, T) - market_price

    f_low=f(sigma_low); f_high=f(sigma_high)

    if f_low * f_high > 0:
        raise ValueError("Market price is out of bounds for the given parameters. Try adjusting sigma_low and sigma_high.")
    
    low = sigma_low
    high = sigma_high
    
    for i in range(max_iter):
        mid = (low + high) / 2
        price = bsm_call(S, K, r, mid, T)
        
        if abs(price - market_price) < tol:
            return mid
        elif price < market_price:
            low = mid
        else:
            high = mid
            
    raise ValueError("Implied volatility did not converge within the maximum number of iterations.")