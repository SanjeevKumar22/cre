# enhanced_bq_integration.py
from google.cloud import bigquery
import pandas as pd
import numpy as np

class EnhancedCREDataAnalyzer:
    def __init__(self):
        self.client = bigquery.Client()
        self.dataset = "cre_data"
        
    def get_comprehensive_property_details(self, address):
        """Fetch comprehensive property details including new datasets"""
        query = f"""
        WITH property_base AS (
            SELECT 
                p.address,
                p.sq_ft,
                p.year_built,
                p.zoning_code,
                p.last_sale_price,
                p.current_owner,
                p.zip_code,
                m.vacancy_rate,
                m.market_rent_per_sqft,
                m.cap_rate_avg,
                m.absorption_rate,
                d.population_growth_3yr,
                d.median_household_income,
                d.unemployment_rate,
                r.flood_zone_risk,
                r.crime_score,
                r.regulatory_changes_flag
            FROM `{self.dataset}.properties` p
            LEFT JOIN `{self.dataset}.market_trends` m 
                ON p.zip_code = m.zip_code
            LEFT JOIN `{self.dataset}.demographics` d 
                ON p.zip_code = d.zip_code
            LEFT JOIN `{self.dataset}.risks` r 
                ON p.zip_code = r.zip_code
            WHERE LOWER(p.address) LIKE LOWER('%{address}%')
        ),
        rental_data AS (
            SELECT 
                ri.zip_code,
                AVG(ri.avg_monthly_rent) as avg_rent_all_types,
                MAX(CASE WHEN ri.property_type = 'Office' THEN ri.avg_monthly_rent END) as office_rent,
                MAX(CASE WHEN ri.property_type = 'Retail' THEN ri.avg_monthly_rent END) as retail_rent,
                MAX(CASE WHEN ri.property_type = 'Industrial' THEN ri.avg_monthly_rent END) as industrial_rent,
                MAX(CASE WHEN ri.property_type = 'Multifamily' THEN ri.avg_monthly_rent END) as multifamily_rent,
                AVG(ri.net_operating_income_margin) as avg_noi_margin
            FROM `{self.dataset}.rental_inc` ri
            WHERE ri.zip_code = (SELECT zip_code FROM property_base)
            GROUP BY ri.zip_code
        ),
        flood_risk_summary AS (
            SELECT 
                nf.Zip_Code,
                STRING_AGG(DISTINCT nf.Rated_Flood_Zones, ', ') as flood_zones,
                SUM(nf.Total_Losses) as total_flood_losses,
                SUM(nf.Total_Payments) as total_flood_payments,
                AVG(nf.Total_Payments / NULLIF(nf.Total_Losses, 0)) as avg_loss_severity
            FROM `{self.dataset}.nfip_policy` nf
            WHERE nf.Zip_Code = (SELECT zip_code FROM property_base)
            GROUP BY nf.Zip_Code
        )
        SELECT 
            pb.*,
            rd.avg_rent_all_types,
            rd.office_rent,
            rd.retail_rent,
            rd.industrial_rent,
            rd.multifamily_rent,
            rd.avg_noi_margin,
            frs.flood_zones,
            frs.total_flood_losses,
            frs.total_flood_payments,
            frs.avg_loss_severity
        FROM property_base pb
        LEFT JOIN rental_data rd ON pb.zip_code = rd.zip_code
        LEFT JOIN flood_risk_summary frs ON pb.zip_code = frs.Zip_Code
        """
        
        return self.client.query(query).to_dataframe()
    
    def calculate_enhanced_valuation(self, property_data):
        """Calculate enhanced valuation with flood risk adjustment"""
        sq_ft = property_data['sq_ft'].iloc[0]
        market_rent = property_data['market_rent_per_sqft'].iloc[0]
        cap_rate = property_data['cap_rate_avg'].iloc[0]
        avg_noi_margin = property_data['avg_noi_margin'].iloc[0]
        
        # Calculate Gross Potential Income
        gpi = sq_ft * market_rent * 12
        
        # Adjust for vacancy
        vacancy_rate = property_data['vacancy_rate'].iloc[0]
        egi = gpi * (1 - vacancy_rate)
        
        # Calculate NOI using industry-specific margin
        noi = egi * (avg_noi_margin / 100) if pd.notna(avg_noi_margin) else egi * 0.65
        
        # Calculate property value using cap rate
        if cap_rate > 0:
            property_value = noi / cap_rate
        else:
            property_value = property_data['last_sale_price'].iloc[0]
        
        # Apply flood risk adjustment
        flood_adjustment = self.calculate_flood_risk_adjustment(property_data)
        adjusted_property_value = property_value * (1 - flood_adjustment)
        
        return {
            "gross_potential_income": gpi,
            "effective_gross_income": egi,
            "net_operating_income": noi,
            "estimated_property_value": property_value,
            "flood_risk_adjustment_pct": flood_adjustment * 100,
            "adjusted_property_value": adjusted_property_value,
            "cap_rate": cap_rate,
            "price_per_sqft": adjusted_property_value / sq_ft,
            "noi_margin_used": avg_noi_margin if pd.notna(avg_noi_margin) else 65.0
        }
    
    def calculate_flood_risk_adjustment(self, property_data):
        """Calculate flood risk adjustment based on NFIP data"""
        flood_zone = property_data['flood_zone_risk'].iloc[0]
        flood_zones = property_data['flood_zones'].iloc[0] if pd.notna(property_data['flood_zones'].iloc[0]) else ""
        total_payments = property_data['total_flood_payments'].iloc[0]
        
        # Base adjustment by flood zone
        zone_adjustments = {
            'Low': 0.01,
            'Medium': 0.05,
            'High': 0.15
        }
        
        base_adjustment = zone_adjustments.get(flood_zone, 0.03)
        
        # Additional adjustment for specific flood zones
        zone_risk_multipliers = {
            'V': 2.0,  # Coastal high hazard
            'A': 1.5,  # Special flood hazard
            'AE': 1.3, # Base flood elevation
            'X': 0.7   # Minimal risk
        }
        
        for zone, multiplier in zone_risk_multipliers.items():
            if zone in flood_zones:
                base_adjustment *= multiplier
                break
        
        # Adjustment based on historical payments
        if pd.notna(total_payments):
            if total_payments > 50000000:  # > $50M
                base_adjustment += 0.05
            elif total_payments > 10000000:  # > $10M
                base_adjustment += 0.02
        
        return min(base_adjustment, 0.25)  # Cap at 25% adjustment
    
    def generate_flood_risk_analysis(self, property_data):
        """Generate detailed flood risk analysis"""
        flood_zones = property_data['flood_zones'].iloc[0]
        total_losses = property_data['total_flood_losses'].iloc[0]
        total_payments = property_data['total_flood_payments'].iloc[0]
        avg_loss_severity = property_data['avg_loss_severity'].iloc[0]
        
        analysis = {
            "flood_zones_present": flood_zones if pd.notna(flood_zones) else "Unknown",
            "historical_loss_count": int(total_losses) if pd.notna(total_losses) else 0,
            "historical_payment_total": f"${total_payments:,.0f}" if pd.notna(total_payments) else "Not Available",
            "avg_loss_severity": f"${avg_loss_severity:,.0f}" if pd.notna(avg_loss_severity) else "Not Available",
            "flood_insurance_required": self.is_flood_insurance_required(property_data),
            "recommended_insurance_coverage": self.calculate_recommended_coverage(property_data)
        }
        
        return analysis
    
    def is_flood_insurance_required(self, property_data):
        """Determine if flood insurance is required"""
        flood_zones = property_data['flood_zones'].iloc[0]
        if pd.isna(flood_zones):
            return "Unknown - Further assessment needed"
        
        high_risk_zones = ['V', 'A', 'AE']
        for zone in high_risk_zones:
            if zone in flood_zones:
                return "Yes - Required for lenders in high-risk zones"
        
        return "Not required but recommended"
    
    def calculate_recommended_coverage(self, property_data):
        """Calculate recommended flood insurance coverage"""
        property_value = property_data['last_sale_price'].iloc[0]
        flood_zone = property_data['flood_zone_risk'].iloc[0]
        
        coverage_percentages = {
            'High': 0.80,  # 80% of property value
            'Medium': 0.60, # 60% of property value
            'Low': 0.40    # 40% of property value
        }
        
        percentage = coverage_percentages.get(flood_zone, 0.50)
        coverage = property_value * percentage
        
        return f"${coverage:,.0f} ({percentage*100:.0f}% of property value)"
    def analyze_risk_score(self, property_data):
            """Calculate comprehensive risk score"""
            risk_factors = {
                "market_risk": property_data['vacancy_rate'].iloc[0] * 100,
                "economic_risk": (1 - (property_data['population_growth_3yr'].iloc[0] * 100)) * 10,
                "crime_risk": property_data['crime_score'].iloc[0] / 10,
                "flood_risk": {"Low": 10, "Medium": 50, "High": 100}[property_data['flood_zone_risk'].iloc[0]],
                "regulatory_risk": property_data['regulatory_changes_flag'].iloc[0] * 50
            }
            
            total_risk = sum(risk_factors.values()) / len(risk_factors)
            
            if total_risk <= 30:
                risk_level = "Low"
            elif total_risk <= 60:
                risk_level = "Moderate"
            else:
                risk_level = "High"
                
            return {
                "risk_score": total_risk,
                "risk_level": risk_level,
                "risk_factors": risk_factors
            }