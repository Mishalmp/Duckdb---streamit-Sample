import duckdb
import pandas as pd
import polars as pl
import plotly_express as px
import numpy as np
from tabulate import tabulate

# df = pd.DataFrame({
#     'column1': [1, 2, 3, 4, 5,6], 
#     'column2': ['a', 'b', 'c', 'd', 'e',"f"], 
# })

data = {
    'operating_datetime_utc': pd.date_range(start='2024-01-01', periods=1000, freq='h'),
    'state': np.random.choice(['CO', 'TX', 'CA'], size=1000),
    'co2_mass_tons': np.random.rand(1000) * 100
}



df = pd.DataFrame(data)

# df.head()


# dash = duckdb.sql('''
# SELECT * 
# FROM df
# ''')

# dash1 = duckdb.sql(''' FROM df ''')

query1 = """
SELECT 
    DATE_PART('year', operating_datetime_utc) AS year,
    DATE_PART('hour', operating_datetime_utc) AS hour,
    SUM(co2_mass_tons) AS total_co2
FROM df
WHERE state =  'CO'
GROUP BY year, hour
"""


query2 = """

SELECT
    COUNT(*) AS total_rows,
    MIN(co2_mass_tons) AS min_co2,
    MAX(co2_mass_tons) AS max_co2,
    AVG(co2_mass_tons) AS avg_co2,
    STDDEV(co2_mass_tons) AS stddev_co2
FROM df
WHERE state = 'CO'
"""


query3 = """
SELECT
    AVG(co2_mass_tons) AS avg_emission,
    MAX(co2_mass_tons) AS max_emission,

FROM df
WHERE state = 'CO'
"""


result1 = duckdb.query(query1).to_df()
result2 = duckdb.query(query2).to_df()
result3 = duckdb.query(query3).to_df()

result = duckdb.query("""
    SELECT *
    FROM 'hourly_emissions_epacems.parquet'
    WHERE state = 'CO'
    LIMIT 5
""").df()
print(result)


# print(result1.head())

# print(tabulate(result1.head(), headers='keys', tablefmt='pretty'))
# print(tabulate(result2.head(), headers='keys', tablefmt='pretty'))
# print(tabulate(result3.head(), headers='keys', tablefmt='pretty'))


# print(dash)




import time

start = time.time()

# Your DuckDB query
duckdb.query("SELECT AVG(co2_mass_tons) FROM df WHERE state='CO'").df()

end = time.time()
print("Elapsed time:", end - start, "seconds")


#  Save and Reuse DataFrames


result = duckdb.query("SELECT * FROM df WHERE state = 'TX'").df()
result.to_parquet("filtered_tx.parquet")