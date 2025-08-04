def get_advisor_prompt(portfolio: str, user_query: str) -> str:
    """
    Generate a prompt for the financial advisor AI model.
    
    Args:
        portfolio (str): Formatted portfolio data
        user_query (str): User's question or request
        
    Returns:
        str: Complete prompt for the AI model
    """
    return f"""You are a professional financial advisor. Please provide advice based on the following portfolio:

{portfolio}

Customer asks: "{user_query}"

Please provide clear, compliant, and actionable suggestions. Consider:
1. Current market conditions
2. Risk management
3. Portfolio diversification
4. Long-term investment goals

Response should be:
- Professional and clear
- Regulatory compliant
- Based on the portfolio data
- Actionable but not overly prescriptive
"""
