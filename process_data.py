import pandas as pd

# Read csv
df = pd.read_csv('USA vs Russia GDP data.csv')
# Fix data types
df['GDP per Capita'] = df['GDP per Capita'].str.replace(',', '').astype(float)
# Handle missing data
df = df.fillna(0)
# Subset by selected columns
df = df[['Country', 'Year', 'Percentage of Global GDP', 'GDP per Capita', 'Total Country GDP (in billions of dollars)', 'World GDP(billions of dollars']]
# Filter by year
df = df[df['Year'] >= 1960]

# Helper functions
def _filter_dataframe(df, country, label):
  # Conditionally select rows and columns
  if country == 'WORLD':
    filtered = df[df[f'{label}'] != 0][['Year', f'{label}']]
    return filtered
  else:
    filtered = df[df['Country'] == f'{country}'][['Year', f'{label}']]
    return filtered

def _calculate_avg_percentage_global_gdp(filtered, label):
  # Calculate percentage
  filtered[f'{label}'] = ((filtered[f'{label}'] / 195) / filtered[f'{label}']) * 100
  # Rename column
  filtered = filtered.rename(columns={f'{label}': 'AVG Percentage of Global GDP'})
  return filtered

def _calculate_gdp_growth_rate(filtered, label):
  # Add new column
  filtered['GDP Growth Rate (%)'] = (filtered[f'{label}'] / filtered[f'{label}'].shift(1) - 1) * 100
  # Handle missing data
  filtered = filtered.fillna(0)
  # Select columns
  filtered = filtered[['Year', 'GDP Growth Rate (%)']]
  return filtered

def _convert_to_json(filtered, country, file_name):
  filtered.to_json(f'data/{country}/{file_name}.json', orient='records', indent=2)

def _process_data(chart, df, country, label, file_name):
  # Filter by country
  filtered = _filter_dataframe(df, f'{country}', f'{label}')
  # Conditionally calculate
  if chart == 'percentage_gdp' and country == 'WORLD':
    filtered = _calculate_avg_percentage_global_gdp(filtered, f'{label}')
  elif chart == 'growth_rate_gdp':
    filtered = _calculate_gdp_growth_rate(filtered, f'{label}')
  # Convert to json
  _convert_to_json(filtered, f'{country.lower()}', f'{file_name}')

# % of Global GDP
# USA
_process_data('percentage_gdp', df, 'USA', 'Percentage of Global GDP', 'percentage_gdp')
# RUS
_process_data('percentage_gdp', df, 'RUS', 'Percentage of Global GDP', 'percentage_gdp')
# WORLD
_process_data('percentage_gdp', df, 'WORLD', 'World GDP(billions of dollars', 'avg_percentage_gdp')

# GDP per Capita (USD)
# USA
_process_data('capita_gdp', df, 'USA', 'GDP per Capita', 'capita_gdp')
# RUS
_process_data('capita_gdp', df, 'RUS', 'GDP per Capita', 'capita_gdp')

# GDP Growth Rate (%)
# USA
_process_data('growth_rate_gdp', df, 'USA', 'Total Country GDP (in billions of dollars)', 'growth_rate_gdp')
# RUS
_process_data('growth_rate_gdp', df, 'RUS', 'Total Country GDP (in billions of dollars)', 'growth_rate_gdp')
# WORLD
_process_data('growth_rate_gdp', df, 'WORLD', 'World GDP(billions of dollars', 'avg_growth_rate_gdp')
