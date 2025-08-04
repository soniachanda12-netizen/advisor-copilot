from google.cloud import bigquery
import os

def get_customer_portfolio(customer_id: str) -> dict:
    """
    Fetch customer portfolio data from BigQuery.
    
    Args:
        customer_id (str): Customer's unique identifier
        
    Returns:
        dict: Portfolio data grouped by asset class
    """
    client = bigquery.Client()
    dataset = os.getenv('BQ_DATASET')
    
    query = f"""
    SELECT
        asset_class,
        sub_category,
        SUM(amount) as total_amount
    FROM
        `{dataset}.customer_portfolio`
    WHERE
        customer_id = @customer_id
    GROUP BY
        asset_class,
        sub_category
    ORDER BY
        asset_class,
        sub_category
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    # Group results by asset class
    portfolio = {}
    for row in results:
        if row.asset_class not in portfolio:
            portfolio[row.asset_class] = []
        portfolio[row.asset_class].append({
            'sub_category': row.sub_category,
            'amount': row.total_amount
        })
    
    return portfolio
