def format_portfolio(portfolio: dict) -> str:
    """
    Format portfolio data into a human-readable string.
    
    Args:
        portfolio (dict): Portfolio data grouped by asset class
        
    Returns:
        str: Formatted portfolio string
    """
    formatted = []
    
    for asset_class, holdings in portfolio.items():
        total = sum(item['amount'] for item in holdings)
        
        # Format sub-categories
        sub_cats = []
        for holding in holdings:
            percentage = (holding['amount'] / total) * 100
            sub_cats.append(f"{holding['sub_category']} {percentage:.0f}%")
        
        sub_categories = f"({', '.join(sub_cats)})" if sub_cats else ""
        
        # Format amount in a readable way (using Indian numbering system as per example)
        amount_str = format_indian_currency(total)
        
        formatted.append(f"- {asset_class}: ₹{amount_str} {sub_categories}")
    
    return "\n".join(formatted)

def format_indian_currency(amount: float) -> str:
    """
    Format amount in Indian numbering system (with commas).
    Example: 800000 -> 8,00,000
    
    Args:
        amount (float): The amount to format
        
    Returns:
        str: Formatted amount string
    """
    amount_str = str(int(amount))
    result = ""
    
    if len(amount_str) <= 3:
        return amount_str
    
    # Handle last 3 digits
    result = amount_str[-3:]
    amount_str = amount_str[:-3]
    
    # Handle remaining digits in groups of 2
    while amount_str:
        if len(amount_str) >= 2:
            result = amount_str[-2:] + "," + result
            amount_str = amount_str[:-2]
        else:
            result = amount_str + "," + result
            amount_str = ""
            
    return result
