import math

def norm_cdf(x:float)-> float:
    """Cumulative distribution function for the standard normal distribution."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_pdf(x:float)-> float:
    """Probability density function for the standard normal distribution. φ(x) = 1/sqrt(2π) * exp(-x²/2)"""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# Black-Scholes formula for European call and put options
def _validate_inputs(S:float, K:float, r:float, sigma:float, T:float)->None:
    """Validate input parameters for the Black-Scholes formula."""
    if S <= 0:
        raise ValueError("Stock price (S) must be positive.")
    if K <= 0:
        raise ValueError("Strike price (K) must be positive.")
    if r < 0:
        raise ValueError("Risk-free rate (r) cannot be negative.")
    if sigma <= 0:
        raise ValueError("Volatility (sigma) must be positive.")
    if T <= 0:
        raise ValueError("Time to maturity (T) must be positive.")
    
def d1(S:float, K:float, r:float, sigma:float, T:float)-> float:
    """Calculate d1 for the Black-Scholes formula."""
    _validate_inputs(S, K, r, sigma, T)
    return (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))

def d2(S:float, K:float, r:float, sigma:float, T:float)-> float:
    """Calculate d2 for the Black-Scholes formula."""
    return d1(S, K, r, sigma, T) - sigma * math.sqrt(T)

def bsm_call(S:float, K:float, r:float, sigma:float, T:float)->float:
    """
    Calculate the price of a European call option using the Black-Scholes formula.
    P = K e^{-rT} N(-d2) - S N(-d1)
    """
    _validate_inputs(S, K, r, sigma, T)
    d_1 = d1(S, K, r, sigma, T)
    d_2 = d2(S, K, r, sigma, T)
    return S * norm_cdf(d_1) - K * math.exp(-r * T) * norm_cdf(d_2)

def bsm_put(S:float, K:float, r:float, sigma:float, T:float)-> float:
    """
    Calculate the price of a European put option using the Black-Scholes formula.
    P = K e^{-rT} N(-d2) - S N(-d1)
    """
    _validate_inputs(S, K, r, sigma, T)
    d_1 = d1(S, K, r, sigma, T)
    d_2 = d2(S, K, r, sigma, T)
    return K * math.exp(-r * T) * norm_cdf(-d_2) - S * norm_cdf(-d_1)

def greek_call(S:float, K:float, r:float, sigma:float, T:float)-> dict[str, float]:
    """
    Main Greeks for a European call under BSM.
    Returns:
      - delta
      - gamma
      - vega   (per +1.00 in vol, i.e. 100% vol; for +1% multiply by 0.01)
      - theta  (per year)
      - rho    (per +1.00 in rate; for +1% multiply by 0.01)
    """
    _validate_inputs(S, K, r, sigma, T)
    d_1 = d1(S, K, r, sigma, T)
    d_2 = d2(S, K, r, sigma, T)

    delta = norm_cdf(d_1)
    gamma = norm_pdf(d_1) / (S * sigma * math.sqrt(T))
    vega = S * norm_pdf(d_1) * math.sqrt(T)
    theta = (-S * norm_pdf(d_1) * sigma / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm_cdf(d_2))
    rho = K * T * math.exp(-r * T) * norm_cdf(d_2)
    
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}