# # bq_integration.py
# from google.cloud import bigquery
# import pandas as pd

# class CREDataAnalyzer:
#     def __init__(self):
#         self.client = bigquery.Client()
#         self.dataset = "cre_data"
        
#     def get_property_details(self, address):
#         """Fetch property details from BigQuery"""
#         query = f"""
#         SELECT 
#             p.address,
#             p.sq_ft,
#             p.year_built,
#             p.zoning_code,
#             p.last_sale_price,
#             p.current_owner,
#             p.zip_code,
#             m.vacancy_rate,
#             m.market_rent_per_sqft,
#             m.cap_rate_avg,
#             m.absorption_rate,
#             d.population_growth_3yr,
#             d.median_household_income,
#             d.unemployment_rate,
#             r.flood_zone_risk,
#             r.crime_score,
#             r.regulatory_changes_flag
#         FROM `{self.dataset}.properties` p
#         LEFT JOIN `{self.dataset}.market_trends` m 
#             ON p.zip_code = m.zip_code
#         LEFT JOIN `{self.dataset}.demographics` d 
#             ON p.zip_code = d.zip_code
#         LEFT JOIN `{self.dataset}.risks` r 
#             ON p.zip_code = r.zip_code
#         WHERE LOWER(p.address) LIKE LOWER('%{address}%')
#         """
        
#         return self.client.query(query).to_dataframe()
    
#     def calculate_valuation(self, property_data):
#         """Calculate property valuation metrics"""
#         sq_ft = property_data['sq_ft'].iloc[0]
#         market_rent = property_data['market_rent_per_sqft'].iloc[0]
#         cap_rate = property_data['cap_rate_avg'].iloc[0]
        
#         # Calculate Gross Potential Income
#         gpi = sq_ft * market_rent * 12
        
#         # Adjust for vacancy
#         vacancy_rate = property_data['vacancy_rate'].iloc[0]
#         egi = gpi * (1 - vacancy_rate)
        
#         # Calculate property value using cap rate
#         if cap_rate > 0:
#             property_value = egi / cap_rate
#         else:
#             property_value = property_data['last_sale_price'].iloc[0]
        
#         return {
#             "gross_potential_income": gpi,
#             "effective_gross_income": egi,
#             "estimated_property_value": property_value,
#             "cap_rate": cap_rate,
#             "price_per_sqft": property_value / sq_ft
#         }
    
#     def analyze_risk_score(self, property_data):
#         """Calculate comprehensive risk score"""
#         risk_factors = {
#             "market_risk": property_data['vacancy_rate'].iloc[0] * 100,
#             "economic_risk": (1 - (property_data['population_growth_3yr'].iloc[0] * 100)) * 10,
#             "crime_risk": property_data['crime_score'].iloc[0] / 10,
#             "flood_risk": {"Low": 10, "Medium": 50, "High": 100}[property_data['flood_zone_risk'].iloc[0]],
#             "regulatory_risk": property_data['regulatory_changes_flag'].iloc[0] * 50
#         }
        
#         total_risk = sum(risk_factors.values()) / len(risk_factors)
        
#         if total_risk <= 30:
#             risk_level = "Low"
#         elif total_risk <= 60:
#             risk_level = "Moderate"
#         else:
#             risk_level = "High"
            
#         return {
#             "risk_score": total_risk,
#             "risk_level": risk_level,
#             "risk_factors": risk_factors
#         }