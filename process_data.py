import pandas as pd

# Read Maddison Historical Statistics csv
df = pd.read_csv('USA vs Russia GDP data.csv')
# Fix data types
df['GDP per Capita'] = df['GDP per Capita'].str.replace(',', '').astype(float)
# Handle missing data
df = df.fillna(0)
# Subset by selected columns
df = df[['Country', 'Year', 'Percentage of Global GDP', 'GDP per Capita', 'Total Country GDP (in billions of dollars)', 'World GDP(billions of dollars']]
# Filter by year
df_mhs = df[df['Year'] >= 1960]

# Read International Monetary Fund csv
df = pd.read_csv('imf-inflation-rate.csv')
# Transpose
df = df.T
# Fix columns
df.columns = df.iloc[0]
df = df.drop(df.index[0])
df = df.reset_index()
df = df.rename(columns={'index': 'Year'})
# Fix data types
df['Year'] = df['Year'].astype(int)
# Filter by year
df_imf = df[df['Year'] <= 2022]

# Helper functions
def _filter_dataframe(dataset, df, country, label):
  # Conditionally select rows and columns
  if dataset == 'mhs':
    if country == 'WORLD':
      filtered = df[df[f'{label}'] != 0][['Year', f'{label}']]
      return filtered
    else:
      filtered = df[df['Country'] == f'{country}'][['Year', f'{label}']]
      return filtered
  elif dataset == 'imf':
    filtered = df[['Year', f'{label}']]
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

def _process_data(dataset, chart, df, country, label, file_name):
  # Filter by country
  filtered = _filter_dataframe(dataset, df, f'{country}', f'{label}')
  # Conditionally calculate
  if chart == 'percentage_gdp' and country == 'WORLD':
    filtered = _calculate_avg_percentage_global_gdp(filtered, f'{label}')
  elif chart == 'growth_rate_gdp':
    filtered = _calculate_gdp_growth_rate(filtered, f'{label}')
  # Convert to json
  _convert_to_json(filtered, f'{country.lower()}', f'{file_name}')

# % of Global GDP
# USA
_process_data('mhs', 'percentage_gdp', df_mhs, 'USA', 'Percentage of Global GDP', 'percentage_gdp')
# RUS
_process_data('mhs', 'percentage_gdp', df_mhs, 'RUS', 'Percentage of Global GDP', 'percentage_gdp')
# WORLD
_process_data('mhs', 'percentage_gdp', df_mhs, 'WORLD', 'World GDP(billions of dollars', 'avg_percentage_gdp')

# GDP per Capita (USD)
# USA
_process_data('mhs', 'capita_gdp', df_mhs, 'USA', 'GDP per Capita', 'capita_gdp')
# RUS
_process_data('mhs', 'capita_gdp', df_mhs, 'RUS', 'GDP per Capita', 'capita_gdp')

# GDP Growth Rate (%)
# USA
_process_data('mhs', 'growth_rate_gdp', df_mhs, 'USA', 'Total Country GDP (in billions of dollars)', 'growth_rate_gdp')
# RUS
_process_data('mhs', 'growth_rate_gdp', df_mhs, 'RUS', 'Total Country GDP (in billions of dollars)', 'growth_rate_gdp')
# WORLD
_process_data('mhs', 'growth_rate_gdp', df_mhs, 'WORLD', 'World GDP(billions of dollars', 'avg_growth_rate_gdp')

# Inflation Rate (%)
# USA
_process_data('imf', 'inflation_rate', df_imf, 'USA', 'United States', 'inflation_rate')
# RUS
_process_data('imf', 'inflation_rate', df_imf, 'RUS', 'Russian Federation', 'inflation_rate')
# WORLD
_process_data('imf', 'inflation_rate', df_imf, 'WORLD', 'World', 'avg_inflation_rate')
