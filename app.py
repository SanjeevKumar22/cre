# # app.py - Streamlit Application
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime
# from bq_integration import CREDataAnalyzer
# import google.generativeai as genai

# # Configure Streamlit page
# st.set_page_config(
#     page_title="AI CRE Loan Analyzer",
#     page_icon="🏢",
#     layout="wide"
# )

# # Initialize analyzer
# analyzer = CREDataAnalyzer()

# # Configure Gemini AI
# genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# model = genai.GenerativeModel('gemini-2.0-flash')

# # Custom CSS for professional look
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         color: #1E3A8A;
#         font-weight: bold;
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         color: #374151;
#         margin-top: 1rem;
#     }
#     .metric-card {
#         background: white;
#         border-radius: 10px;
#         padding: 1rem;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         border-left: 4px solid #3B82F6;
#     }
#     .risk-low {
#         color: #10B981;
#         font-weight: bold;
#     }
#     .risk-moderate {
#         color: #F59E0B;
#         font-weight: bold;
#     }
#     .risk-high {
#         color: #EF4444;
#         font-weight: bold;
#     }
#     .chat-message {
#         padding: 1rem;
#         border-radius: 10px;
#         margin-bottom: 1rem;
#     }
#     .user-message {
#         background-color: #EFF6FF;
#         border-left: 4px solid #3B82F6;
#     }
#     .assistant-message {
#         background-color: #F3F4F6;
#         border-left: 4px solid #10B981;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown('<h1 class="main-header">🏢 AI Commercial Real Estate Loan Analyzer</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-header">Automated Deal Memo Generation in Minutes</p>', unsafe_allow_html=True)

# # Initialize session state
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'analysis_data' not in st.session_state:
#     st.session_state.analysis_data = None

# # Sidebar for property input
# with st.sidebar:
#     st.markdown("### 📍 Property Search")
#     address_input = st.text_input(
#         "Enter Property Address:",
#         placeholder="e.g., 123 Main St, New York, NY 10001",
#         key="address_input"
#     )
    
#     analyze_btn = st.button("🚀 Analyze Property", type="primary", use_container_width=True)
    
#     if analyze_btn and address_input:
#         with st.spinner("🔍 Analyzing property data..."):
#             try:
#                 # Fetch data from BigQuery
#                 property_data = analyzer.get_property_details(address_input)
                
#                 if property_data.empty:
#                     st.error("Property not found in database")
#                 else:
#                     # Calculate metrics
#                     valuation = analyzer.calculate_valuation(property_data)
#                     risk_analysis = analyzer.analyze_risk_score(property_data)
                    
#                     # Store in session state
#                     st.session_state.analysis_data = {
#                         "property": property_data.iloc[0].to_dict(),
#                         "valuation": valuation,
#                         "risk": risk_analysis
#                     }
                    
#                     st.success("✅ Analysis complete!")
                    
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")
    
#     st.markdown("---")
#     st.markdown("### 📊 Quick Metrics")
#     if st.session_state.analysis_data:
#         data = st.session_state.analysis_data
#         st.metric("Estimated Value", f"${data['valuation']['estimated_property_value']:,.0f}")
#         st.metric("Risk Level", data['risk']['risk_level'])
#         st.metric("Cap Rate", f"{data['valuation']['cap_rate']*100:.2f}%")

# # Main chat interface
# st.markdown("### 💬 CRE Analysis Assistant")

# # Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Chat input
# if prompt := st.chat_input("Ask about the property analysis..."):
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Generate AI response
#     with st.chat_message("assistant"):
#         if st.session_state.analysis_data:
#             # Create context from analysis data
#             context = f"""
#             Property Analysis Data:
#             {st.session_state.analysis_data}
            
#             User Question: {prompt}
            
#             Please provide a detailed analysis based on the data above.
#             """
            
#             response = model.generate_content(context)
#             print(response.text)
#             st.markdown(response.text)
#         else:
#             st.info("Please enter a property address to begin analysis.")
    
#     st.session_state.messages.append({"role": "assistant", "content": response.text if st.session_state.analysis_data else "Please enter a property address to begin analysis."})

# # Display detailed analysis if available
# if st.session_state.analysis_data:
#     data = st.session_state.analysis_data
    
#     st.markdown("---")
#     st.markdown("## 📋 Comprehensive Loan Memo")
    
#     # Create tabs for different sections
#     tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#         "📊 Executive Summary",
#         "🏢 Property Overview",
#         "📈 Market Analysis",
#         "👥 Demographics",
#         "⚠️ Risk Assessment",
#         "💰 Valuation"
#     ])
    
#     with tab1:
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Property Value", f"${data['valuation']['estimated_property_value']:,.0f}")
#         with col2:
#             st.metric("Loan Recommendation", "Approved" if data['risk']['risk_score'] <= 60 else "Review")
#         with col3:
#             st.metric("Processing Time", "2 minutes")
        
#         st.markdown("### Key Highlights")
#         st.markdown(f"""
#         - **Property**: {data['property']['address']}
#         - **Market**: Strong fundamentals with {data['property']['absorption_rate']*100:.1f}% absorption rate
#         - **Risk**: {data['risk']['risk_level']} risk profile
#         - **Recommendation**: {"Recommended for approval" if data['risk']['risk_score'] <= 60 else "Requires additional review"}
#         """)
    
#     with tab2:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Property Details**")
#             st.write(f"**Address**: {data['property']['address']}")
#             st.write(f"**Square Feet**: {data['property']['sq_ft']:,.0f}")
#             st.write(f"**Year Built**: {data['property']['year_built']}")
#             st.write(f"**Zoning**: {data['property']['zoning_code']}")
#             st.write(f"**Last Sale**: ${data['property']['last_sale_price']:,.0f}")
        
#         with col2:
#             st.markdown("**Owner Information**")
#             st.write(f"**Current Owner**: {data['property']['current_owner']}")
#             st.write(f"**Zip Code**: {data['property']['zip_code']}")
    
#     with tab3:
#         fig1 = go.Figure()
#         fig1.add_trace(go.Indicator(
#             mode = "gauge+number+delta",
#             value = data['property']['vacancy_rate'] * 100,
#             title = {'text': "Vacancy Rate %"},
#             delta = {'reference': 10},
#             gauge = {'axis': {'range': [0, 20]},
#                      'steps': [
#                          {'range': [0, 5], 'color': "green"},
#                          {'range': [5, 15], 'color': "yellow"},
#                          {'range': [15, 20], 'color': "red"}]
#                     }
#         ))
#         st.plotly_chart(fig1, use_container_width=True)
    
#     with tab4:
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Population Growth", f"{data['property']['population_growth_3yr']*100:.1f}%")
#         with col2:
#             st.metric("Median Income", f"${data['property']['median_household_income']:,.0f}")
#         with col3:
#             st.metric("Unemployment", f"{data['property']['unemployment_rate']*100:.1f}%")
    
#     with tab5:
#         # Risk factors visualization
#         risk_df = pd.DataFrame.from_dict(data['risk']['risk_factors'], orient='index', columns=['Score'])
#         fig2 = px.bar(risk_df, y=risk_df.index, x='Score', orientation='h',
#                      title="Risk Factor Analysis", color='Score',
#                      color_continuous_scale='RdYlGn_r')
#         st.plotly_chart(fig2, use_container_width=True)
        
#         st.markdown(f"**Overall Risk Score**: {data['risk']['risk_score']:.1f} - **{data['risk']['risk_level']}**")
    
#     with tab6:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("**Valuation Metrics**")
#             for key, value in data['valuation'].items():
#                 if isinstance(value, (int, float)):
#                     if key in ['estimated_property_value', 'gross_potential_income', 'effective_gross_income']:
#                         st.write(f"**{key.replace('_', ' ').title()}**: ${value:,.0f}")
#                     elif key in ['cap_rate']:
#                         st.write(f"**{key.replace('_', ' ').title()}**: {value*100:.2f}%")
#                     else:
#                         st.write(f"**{key.replace('_', ' ').title()}**: {value:,.2f}")
        
#         with col2:
#             # Download button for report
#             report_text = f"""
#             COMMERCIAL REAL ESTATE LOAN ANALYSIS REPORT
#             ===========================================
            
#             Property: {data['property']['address']}
#             Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
#             EXECUTIVE SUMMARY:
#             - Estimated Value: ${data['valuation']['estimated_property_value']:,.0f}
#             - Risk Level: {data['risk']['risk_level']}
#             - Recommendation: {"APPROVE" if data['risk']['risk_score'] <= 60 else "REVIEW REQUIRED"}
            
#             PROPERTY DETAILS:
#             - Square Feet: {data['property']['sq_ft']:,.0f}
#             - Year Built: {data['property']['year_built']}
#             - Zoning: {data['property']['zoning_code']}
            
#             MARKET ANALYSIS:
#             - Vacancy Rate: {data['property']['vacancy_rate']*100:.1f}%
#             - Market Rent: ${data['property']['market_rent_per_sqft']:.2f}/sqft
#             - Cap Rate: {data['valuation']['cap_rate']*100:.2f}%
            
#             RISK ASSESSMENT:
#             - Overall Risk Score: {data['risk']['risk_score']:.1f}
#             - Flood Zone: {data['property']['flood_zone_risk']}
#             - Crime Score: {data['property']['crime_score']}
#             """
            
#             st.download_button(
#                 label="📥 Download Full Report",
#                 data=report_text,
#                 file_name=f"CRE_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#                 mime="text/plain"
#             )


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io
import base64
from enhanced_bq_integration import EnhancedCREDataAnalyzer
import google.generativeai as genai


def get_zone_risk_description(zone):
    """Get risk level description for flood zone"""
    risk_descriptions = {
        'V': 'Coastal High Hazard Area - Subject to high velocity wave action. Severe risk requiring special construction.',
        'A': 'Special Flood Hazard Area - High risk of flooding. Base flood elevation not determined.',
        'AE': 'Special Flood Hazard Area - Moderate to high risk with determined base flood elevation.',
        'X': 'Moderate to Minimal Risk Area - Outside 500-year flood plain. Lower insurance rates.',
        'VE': 'Coastal High Hazard Area - Subject to high velocity wave action with determined base flood elevation.'
    }
    return risk_descriptions.get(zone, 'Standard flood zone')


def generate_comprehensive_report(analysis_data, flood_data, report_format='txt'):
    """Generate comprehensive report in specified format"""
    
    data = analysis_data
    property_info = data['property']
    valuation = data['valuation']
    risk = data['risk']
    
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if report_format == 'txt':
        report_content = generate_txt_report(property_info, valuation, risk, flood_data, report_date)
        filename = f"CRE_Analysis_{property_info['address'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    elif report_format == 'json':
        report_content = generate_json_report(property_info, valuation, risk, flood_data, report_date)
        filename = f"CRE_Analysis_{property_info['address'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    elif report_format == 'html':
        report_content = generate_html_report(property_info, valuation, risk, flood_data, report_date)
        filename = f"CRE_Analysis_{property_info['address'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    elif report_format == 'pdf':
        # For PDF, we generate HTML first and let user convert
        report_content = generate_html_report(property_info, valuation, risk, flood_data, report_date)
        filename = f"CRE_Analysis_{property_info['address'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    return {
        "content": report_content,
        "filename": filename,
        "format": report_format
    }
def generate_txt_report(property_info, valuation, risk, flood_data, report_date):
    """Generate text format report"""
    
    report = f"""
    ================================================================================
                     COMMERCIAL REAL ESTATE LOAN ANALYSIS REPORT
    ================================================================================
    Report Date: {report_date}
    Generated By: AI CRE Loan Analyzer with Flood Risk Assessment
    ================================================================================

    1. PROPERTY INFORMATION
    =======================
    Address:          {property_info['address']}
    Zip Code:         {property_info['zip_code']}
    Square Feet:      {property_info['sq_ft']:,.0f}
    Year Built:       {property_info['year_built']}
    Zoning:           {property_info['zoning_code']}
    Current Owner:    {property_info['current_owner']}
    Last Sale Price:  ${property_info['last_sale_price']:,.0f}

    2. VALUATION SUMMARY
    ====================
    Gross Potential Income:    ${valuation['gross_potential_income']:,.0f}/year
    Effective Gross Income:    ${valuation['effective_gross_income']:,.0f}/year
    Net Operating Income:      ${valuation['net_operating_income']:,.0f}/year
    NOI Margin:                {valuation['noi_margin_used']:.1f}%
    
    Estimated Property Value:  ${valuation['estimated_property_value']:,.0f}
    Flood Risk Adjustment:     -{valuation['flood_risk_adjustment_pct']:.1f}%
    Adjusted Property Value:   ${valuation['adjusted_property_value']:,.0f}
    Price per Sq Ft:           ${valuation['price_per_sqft']:,.2f}
    Cap Rate:                  {valuation['cap_rate']*100:.2f}%

    3. FLOOD RISK ASSESSMENT
    =========================
    Flood Zone Risk:           {property_info['flood_zone_risk']}
    """
    
    if flood_data:
        report += f"""
    Identified Flood Zones:    {flood_data.get('flood_zones_present', 'Unknown')}
    Historical Loss Count:     {flood_data.get('historical_loss_count', 0):,}
    Historical Payments:       {flood_data.get('historical_payment_total', 'Not Available')}
    Average Loss Severity:     {flood_data.get('avg_loss_severity', 'Not Available')}
    Flood Insurance Required:  {flood_data.get('flood_insurance_required', 'Unknown')}
    Recommended Coverage:      {flood_data.get('recommended_insurance_coverage', 'Not Available')}
    """
    
    report += f"""
    4. RISK ASSESSMENT
    ==================
    Overall Risk Score:        {risk['risk_score']:.1f}/100
    Risk Level:                {risk['risk_level']}
    
    Risk Factors:
    """
    
    for factor, score in risk['risk_factors'].items():
        report += f"    • {factor.replace('_', ' ').title()}: {score:.1f}\n"
    
    report += f"""
    5. MARKET ANALYSIS
    ==================
    Market Rent:               ${property_info['market_rent_per_sqft']:.2f}/sq ft/month
    Vacancy Rate:              {property_info['vacancy_rate']*100:.1f}%
    Absorption Rate:           {property_info['absorption_rate']*100:.1f}%
    
    Demographic Data:
    • Population Growth (3yr): {property_info['population_growth_3yr']*100:.1f}%
    • Median Household Income: ${property_info['median_household_income']:,.0f}
    • Unemployment Rate:       {property_info['unemployment_rate']*100:.1f}%
    • Crime Score:             {property_info['crime_score']}/100
    • Regulatory Risk Flag:    {'Yes' if property_info['regulatory_changes_flag'] else 'No'}

    6. LOAN RECOMMENDATION
    ======================
    """
    
    if risk['risk_score'] <= 30:
        recommendation = "STRONGLY RECOMMEND APPROVAL"
        terms = "Standard terms, 70-75% LTV, competitive interest rate"
    elif risk['risk_score'] <= 60:
        recommendation = "RECOMMEND APPROVAL"
        terms = "65-70% LTV, standard interest rate with flood risk premium"
    else:
        recommendation = "REQUIRES FURTHER REVIEW"
        terms = "Maximum 60% LTV, higher interest rate, additional flood insurance required"
    
    report += f"""
    Recommendation:            {recommendation}
    Suggested Terms:           {terms}
    
    Decision Rationale:
    • Overall Risk Score: {risk['risk_score']:.1f} ({risk['risk_level']})
    • Flood Risk Impact: {valuation['flood_risk_adjustment_pct']:.1f}% value adjustment
    • Market Conditions: {property_info['vacancy_rate']*100:.1f}% vacancy rate
    • Financial Metrics: {valuation['cap_rate']*100:.2f}% cap rate, {valuation['noi_margin_used']:.1f}% NOI margin

    7. CONDITIONS & COVENANTS
    =========================
    1. Flood insurance required: {flood_data.get('flood_insurance_required', 'Yes, based on risk assessment') if flood_data else 'To be determined'}
    2. Minimum insurance coverage: {flood_data.get('recommended_insurance_coverage', 'Based on property value') if flood_data else 'Standard coverage required'}
    3. Annual property condition review required
    4. Debt Service Coverage Ratio maintained at 1.25x minimum
    5. Quarterly financial reporting required

    8. DISCLAIMERS
    ==============
    • This analysis is based on available data and AI algorithms
    • Flood risk assessment uses NFIP historical data
    • Actual flood risk may vary based on climate projections
    • Property inspection recommended for final underwriting
    • Market conditions subject to change

    ================================================================================
                              END OF REPORT
    ================================================================================
    """
    
    return report

def generate_json_report(property_info, valuation, risk, flood_data, report_date):
    """Generate JSON format report"""
    
    report_data = {
        "report_metadata": {
            "generated_date": report_date,
            "tool": "AI CRE Loan Analyzer",
            "version": "2.0"
        },
        "property_information": {
            "address": property_info['address'],
            "zip_code": property_info['zip_code'],
            "square_feet": property_info['sq_ft'],
            "year_built": property_info['year_built'],
            "zoning_code": property_info['zoning_code'],
            "current_owner": property_info['current_owner'],
            "last_sale_price": property_info['last_sale_price']
        },
        "valuation": {
            "gross_potential_income": valuation['gross_potential_income'],
            "effective_gross_income": valuation['effective_gross_income'],
            "net_operating_income": valuation['net_operating_income'],
            "noi_margin": valuation['noi_margin_used'],
            "estimated_property_value": valuation['estimated_property_value'],
            "flood_risk_adjustment_pct": valuation['flood_risk_adjustment_pct'],
            "adjusted_property_value": valuation['adjusted_property_value'],
            "price_per_sqft": valuation['price_per_sqft'],
            "cap_rate": valuation['cap_rate']
        },
        "risk_assessment": {
            "overall_risk_score": risk['risk_score'],
            "risk_level": risk['risk_level'],
            "risk_factors": risk['risk_factors']
        },
        "market_analysis": {
            "market_rent_per_sqft": property_info['market_rent_per_sqft'],
            "vacancy_rate": property_info['vacancy_rate'],
            "absorption_rate": property_info['absorption_rate'],
            "demographics": {
                "population_growth_3yr": property_info['population_growth_3yr'],
                "median_household_income": property_info['median_household_income'],
                "unemployment_rate": property_info['unemployment_rate'],
                "crime_score": property_info['crime_score'],
                "regulatory_changes_flag": bool(property_info['regulatory_changes_flag'])
            }
        },
        "flood_risk_assessment": flood_data if flood_data else {},
        "loan_recommendation": {
            "decision": "APPROVE" if risk['risk_score'] <= 60 else "REVIEW_REQUIRED",
            "risk_category": risk['risk_level'],
            "suggested_ltv": "70%" if risk['risk_score'] <= 30 else "65%" if risk['risk_score'] <= 60 else "60%",
            "flood_insurance_required": flood_data.get('flood_insurance_required', 'Yes') if flood_data else 'To be determined'
        }
    }
    
    return json.dumps(report_data, indent=2)

def generate_html_report(property_info, valuation, risk, flood_data, report_date):
    """Generate HTML format report"""
    
    risk_color = {
        "Low": "#10B981",
        "Moderate": "#F59E0B",
        "High": "#EF4444"
    }.get(risk['risk_level'], "#6B7280")
    
    html_report = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRE Loan Analysis Report - {property_info['address']}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8fafc;
            }}
            .report-header {{
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                text-align: center;
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }}
            .report-title {{
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 10px;
            }}
            .report-subtitle {{
                font-size: 18px;
                opacity: 0.9;
            }}
            .section {{
                background: white;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }}
            .section-title {{
                color: #1E3A8A;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #3B82F6;
            }}
            .data-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .data-card {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #3B82F6;
            }}
            .data-label {{
                font-weight: 600;
                color: #4B5563;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .data-value {{
                font-weight: 700;
                color: #1F2937;
                font-size: 18px;
            }}
            .metric-highlight {{
                background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #3B82F6;
            }}
            .metric-value {{
                font-size: 36px;
                font-weight: 800;
                color: #1E3A8A;
                margin: 10px 0;
            }}
            .metric-label {{
                font-size: 16px;
                color: #6B7280;
            }}
            .risk-badge {{
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: 700;
                font-size: 16px;
                margin: 10px 0;
            }}
            .recommendation-box {{
                background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
                padding: 25px;
                border-radius: 12px;
                border: 2px solid #10B981;
            }}
            .warning-box {{
                background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                padding: 25px;
                border-radius: 12px;
                border: 2px solid #F59E0B;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #E5E7EB;
                color: #6B7280;
                font-size: 14px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #E5E7EB;
            }}
            th {{
                background-color: #F9FAFB;
                font-weight: 600;
                color: #374151;
            }}
            tr:hover {{
                background-color: #F9FAFB;
            }}
        </style>
    </head>
    <body>
        <div class="report-header">
            <div class="report-title">🏢 Commercial Real Estate Loan Analysis Report</div>
            <div class="report-subtitle">AI-Powered Analysis with Flood Risk Assessment</div>
            <div style="margin-top: 15px; opacity: 0.8;">Generated on {report_date}</div>
        </div>

        <div class="section">
            <div class="section-title">📊 Executive Summary</div>
            <div class="data-grid">
                <div class="metric-highlight">
                    <div class="metric-label">Adjusted Property Value</div>
                    <div class="metric-value">${valuation['adjusted_property_value']:,.0f}</div>
                    <div style="font-size: 14px; color: #6B7280;">Flood-adjusted valuation</div>
                </div>
                
                <div class="metric-highlight">
                    <div class="metric-label">Loan Recommendation</div>
                    <div class="metric-value">{'APPROVE' if risk['risk_score'] <= 60 else 'REVIEW REQUIRED'}</div>
                    <div class="risk-badge" style="background-color: {risk_color}; color: white;">
                        {risk['risk_level']} Risk
                    </div>
                </div>
                
                <div class="metric-highlight">
                    <div class="metric-label">Flood Risk Impact</div>
                    <div class="metric-value">-{valuation['flood_risk_adjustment_pct']:.1f}%</div>
                    <div style="font-size: 14px; color: #6B7280;">Value adjustment</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🏢 Property Information</div>
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Property Address</div>
                    <div class="data-value">{property_info['address']}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Square Feet</div>
                    <div class="data-value">{property_info['sq_ft']:,.0f} sq ft</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Year Built</div>
                    <div class="data-value">{property_info['year_built']}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Zoning Code</div>
                    <div class="data-value">{property_info['zoning_code']}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Last Sale Price</div>
                    <div class="data-value">${property_info['last_sale_price']:,.0f}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Current Owner</div>
                    <div class="data-value">{property_info['current_owner']}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">💰 Financial Analysis</div>
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Gross Potential Income</div>
                    <div class="data-value">${valuation['gross_potential_income']:,.0f}/year</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Net Operating Income</div>
                    <div class="data-value">${valuation['net_operating_income']:,.0f}/year</div>
                </div>
                <div class="data-card">
                    <div class="data-label">NOI Margin</div>
                    <div class="data-value">{valuation['noi_margin_used']:.1f}%</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Cap Rate</div>
                    <div class="data-value">{valuation['cap_rate']*100:.2f}%</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Price per Sq Ft</div>
                    <div class="data-value">${valuation['price_per_sqft']:,.2f}</div>
                </div>
            </div>
            
            <table>
                <tr>
                    <th>Valuation Component</th>
                    <th>Amount</th>
                    <th>Details</th>
                </tr>
                <tr>
                    <td>Estimated Property Value</td>
                    <td><strong>${valuation['estimated_property_value']:,.0f}</strong></td>
                    <td>Before flood adjustment</td>
                </tr>
                <tr>
                    <td>Flood Risk Adjustment</td>
                    <td><strong>-{valuation['flood_risk_adjustment_pct']:.1f}%</strong></td>
                    <td>Based on NFIP historical data</td>
                </tr>
                <tr>
                    <td>Adjusted Property Value</td>
                    <td><strong>${valuation['adjusted_property_value']:,.0f}</strong></td>
                    <td>Final valuation for loan underwriting</td>
                </tr>
            </table>
        </div>
    """
    
    if flood_data:
        html_report += f"""
        <div class="section">
            <div class="section-title">🌊 Flood Risk Assessment</div>
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Flood Zone Risk Level</div>
                    <div class="data-value">{property_info['flood_zone_risk']}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Identified Flood Zones</div>
                    <div class="data-value">{flood_data.get('flood_zones_present', 'Unknown')}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Historical Loss Count</div>
                    <div class="data-value">{flood_data.get('historical_loss_count', 0):,}</div>
                </div>
            </div>
            
            <div class="warning-box">
                <h3 style="margin-top: 0; color: #92400E;">🛡️ Flood Insurance Requirements</h3>
                <p><strong>Insurance Required:</strong> {flood_data.get('flood_insurance_required', 'Unknown')}</p>
                <p><strong>Recommended Coverage:</strong> {flood_data.get('recommended_insurance_coverage', 'Not Available')}</p>
                <p><strong>Historical Payments:</strong> {flood_data.get('historical_payment_total', 'Not Available')}</p>
                <p><strong>Average Loss Severity:</strong> {flood_data.get('avg_loss_severity', 'Not Available')}</p>
            </div>
        </div>
        """
    
    html_report += f"""
        <div class="section">
            <div class="section-title">⚠️ Risk Assessment</div>
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Overall Risk Score</div>
                    <div class="data-value">{risk['risk_score']:.1f}/100</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Risk Level</div>
                    <div class="risk-badge" style="background-color: {risk_color}; color: white;">
                        {risk['risk_level']}
                    </div>
                </div>
            </div>
            
            <table>
                <tr>
                    <th>Risk Factor</th>
                    <th>Score</th>
                    <th>Risk Level</th>
                </tr>
    """
    
    for factor, score in risk['risk_factors'].items():
        factor_risk = "Low" if score <= 30 else "Moderate" if score <= 60 else "High"
        factor_color = "#10B981" if factor_risk == "Low" else "#F59E0B" if factor_risk == "Moderate" else "#EF4444"
        html_report += f"""
                <tr>
                    <td>{factor.replace('_', ' ').title()}</td>
                    <td>{score:.1f}</td>
                    <td><span style="color: {factor_color}; font-weight: 600;">{factor_risk}</span></td>
                </tr>
        """
    
    html_report += f"""
            </table>
        </div>

        <div class="section">
            <div class="section-title">📈 Market & Demographic Analysis</div>
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Market Rent</div>
                    <div class="data-value">${property_info['market_rent_per_sqft']:.2f}/sq ft</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Vacancy Rate</div>
                    <div class="data-value">{property_info['vacancy_rate']*100:.1f}%</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Absorption Rate</div>
                    <div class="data-value">{property_info['absorption_rate']*100:.1f}%</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Population Growth (3yr)</div>
                    <div class="data-value">{property_info['population_growth_3yr']*100:.1f}%</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Median Household Income</div>
                    <div class="data-value">${property_info['median_household_income']:,.0f}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Unemployment Rate</div>
                    <div class="data-value">{property_info['unemployment_rate']*100:.1f}%</div>
                </div>
            </div>
        </div>

        <div class="{'recommendation-box' if risk['risk_score'] <= 60 else 'warning-box'}">
            <div class="section-title">{'✅ Loan Recommendation' if risk['risk_score'] <= 60 else '⚠️ Loan Recommendation'}</div>
            <h3 style="margin-top: 0; {'color: #065F46;' if risk['risk_score'] <= 60 else 'color: #92400E;'}">
                {'APPROVE' if risk['risk_score'] <= 60 else 'REQUIRES FURTHER REVIEW'}
            </h3>
            
            <div class="data-grid">
                <div class="data-card">
                    <div class="data-label">Suggested LTV</div>
                    <div class="data-value">{'70%' if risk['risk_score'] <= 30 else '65%' if risk['risk_score'] <= 60 else '60%'}</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Interest Rate Premium</div>
                    <div class="data-value">+{valuation['flood_risk_adjustment_pct']/2:.1f}% for flood risk</div>
                </div>
                <div class="data-card">
                    <div class="data-label">Debt Service Coverage Ratio</div>
                    <div class="data-value">Minimum 1.25x</div>
                </div>
            </div>
            
            <h4>Conditions & Covenants:</h4>
            <ol>
                <li>Flood insurance required as recommended</li>
                <li>Annual property condition review</li>
                <li>Quarterly financial reporting</li>
                <li>Maintain minimum DSCR of 1.25x</li>
                <li>Property insurance with agreed value coverage</li>
            </ol>
        </div>

        <div class="footer">
            <p><strong>Disclaimer:</strong> This report is generated by AI algorithms based on available data. 
            Actual conditions may vary. Professional inspection and verification recommended for final underwriting decisions.</p>
            <p>© {datetime.now().year} AI CRE Loan Analyzer - All rights reserved</p>
        </div>
    </body>
    </html>
    """
    
    return html_report

# Configure Streamlit page
st.set_page_config(
    page_title="AI CRE Loan Analyzer with Flood Risk Assessment",
    page_icon="🏢🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1E3A8A;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.6rem;
        color: #374151;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3B82F6;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    .risk-low {
        color: #10B981;
        font-weight: 700;
        background-color: #D1FAE5;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .risk-moderate {
        color: #F59E0B;
        font-weight: 700;
        background-color: #FEF3C7;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .risk-high {
        color: #EF4444;
        font-weight: 700;
        background-color: #FEE2E2;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .flood-risk-high {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 5px solid #EF4444;
    }
    .flood-risk-medium {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 5px solid #F59E0B;
    }
    .flood-risk-low {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 5px solid #10B981;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .user-message {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 4px solid #3B82F6;
    }
    .assistant-message {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        border-left: 4px solid #10B981;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .download-btn {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    .download-btn:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        text-decoration: none;
        color: white;
    }
    .tab-content {
        padding: 1.5rem 0;
    }
    .data-point {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .data-point:last-child {
        border-bottom: none;
    }
    .data-label {
        font-weight: 600;
        color: #4B5563;
    }
    .data-value {
        font-weight: 700;
        color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzer
analyzer = EnhancedCREDataAnalyzer()

# Configure Gemini AI
try:
    genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY", "demo-key"))
    model = genai.GenerativeModel('gemini-pro')
except:
    model = None

# Header
st.markdown('<h1 class="main-header">🏢🌊 AI Commercial Real Estate Loan Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automated Deal Memo Generation with Flood Risk Assessment</p>', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'flood_data' not in st.session_state:
    st.session_state.flood_data = None
if 'report_format' not in st.session_state:
    st.session_state.report_format = 'txt'
if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None

# Sidebar for property input and controls
with st.sidebar:
    st.markdown("### 📍 Property Search")
    
    # Property address input
    address_input = st.text_input(
        "Enter Property Address:",
        placeholder="e.g., 123 Main St, New York, NY 10001",
        key="address_input",
        help="Enter the complete property address for analysis"
    )
    
    # Analysis options
    st.markdown("### ⚙️ Analysis Options")
    include_flood_analysis = st.checkbox("Include Flood Risk Analysis", value=True)
    include_rental_comps = st.checkbox("Include Rental Comparables", value=True)
    
    # Report format selection
    st.markdown("### 📄 Report Format")
    report_format = st.radio(
        "Select Report Format:",
        ["TXT (Text)", "PDF", "JSON", "HTML"],
        horizontal=True,
        index=0
    )
    
    # Map format to file extension
    format_map = {
        "TXT (Text)": "txt",
        "PDF": "pdf",
        "JSON": "json",
        "HTML": "html"
    }
    st.session_state.report_format = format_map[report_format]
    
    # Analyze button
    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("🚀 Analyze Property", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Clear Analysis", use_container_width=True)
    
    if clear_btn:
        st.session_state.analysis_data = None
        st.session_state.flood_data = None
        st.session_state.generated_report = None
        st.session_state.messages = []
        st.rerun()
    
    if analyze_btn and address_input:
        with st.spinner("🔍 Analyzing property data..."):
            try:
                # Fetch data from BigQuery
                property_data = analyzer.get_comprehensive_property_details(address_input)
                
                if property_data.empty:
                    st.error("❌ Property not found in database. Please check the address.")
                else:
                    # Calculate metrics
                    valuation = analyzer.calculate_enhanced_valuation(property_data)
                    risk_analysis = analyzer.analyze_risk_score(property_data)
                    flood_analysis = analyzer.generate_flood_risk_analysis(property_data) if include_flood_analysis else {}
                    
                    # Store in session state
                    st.session_state.analysis_data = {
                        "property": property_data.iloc[0].to_dict(),
                        "valuation": valuation,
                        "risk": risk_analysis
                    }
                    st.session_state.flood_data = flood_analysis
                    
                    st.success("✅ Analysis complete!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please ensure the property exists in the database and all tables are properly loaded.")
    
    # Quick metrics display
    st.markdown("---")
    st.markdown("### 📊 Quick Metrics")
    
    if st.session_state.analysis_data:
        data = st.session_state.analysis_data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Estimated Value",
                f"${data['valuation']['adjusted_property_value']:,.0f}",
                delta=f"-{data['valuation']['flood_risk_adjustment_pct']:.1f}% flood adj"
            )
        
        with col2:
            risk_level = data['risk']['risk_level']
            risk_color = {
                "Low": "#10B981",
                "Moderate": "#F59E0B",
                "High": "#EF4444"
            }
            st.markdown(f"""
            <div style='text-align: center;'>
                <div style='font-size: 0.9rem; color: #6B7280;'>Risk Level</div>
                <div style='color: {risk_color[risk_level]}; font-weight: 700; font-size: 1.2rem;'>{risk_level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.metric(
                "Cap Rate",
                f"{data['valuation']['cap_rate']*100:.2f}%"
            )
    else:
        st.info("👈 Enter a property address to begin analysis")

# Main chat interface
st.markdown("### 💬 CRE Analysis Assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the property analysis..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        if st.session_state.analysis_data:
            # Create context from analysis data
            context = f"""
            Property Analysis Data:
            Address: {st.session_state.analysis_data['property']['address']}
            Property Value: ${st.session_state.analysis_data['valuation']['adjusted_property_value']:,.0f}
            Risk Level: {st.session_state.analysis_data['risk']['risk_level']}
            Flood Risk Adjustment: {st.session_state.analysis_data['valuation']['flood_risk_adjustment_pct']:.1f}%
            
            User Question: {prompt}
            
            Please provide a detailed, professional analysis based on the data above.
            Include specific recommendations and data points.
            """
            
            if model:
                try:
                    response = model.generate_content(context)
                    response_text = response.text
                except:
                    response_text = f"""Based on the property analysis:
                    
                    **Property**: {st.session_state.analysis_data['property']['address']}
                    **Value**: ${st.session_state.analysis_data['valuation']['adjusted_property_value']:,.0f}
                    **Risk**: {st.session_state.analysis_data['risk']['risk_level']} level
                    **Flood Adjustment**: {st.session_state.analysis_data['valuation']['flood_risk_adjustment_pct']:.1f}%
                    
                    The property shows {st.session_state.analysis_data['risk']['risk_level'].lower()} risk characteristics.
                    {f"Flood risk contributes {st.session_state.analysis_data['valuation']['flood_risk_adjustment_pct']:.1f}% value adjustment." if st.session_state.flood_data else ""}
                    
                    Recommendation: {"Approved with standard terms" if st.session_state.analysis_data['risk']['risk_score'] <= 60 else "Requires additional review and potential adjustments."}
                    """
            else:
                response_text = f"""Analysis for {st.session_state.analysis_data['property']['address']}:
                
                • Value: ${st.session_state.analysis_data['valuation']['adjusted_property_value']:,.0f}
                • Risk: {st.session_state.analysis_data['risk']['risk_level']}
                • Flood Adjustment: {st.session_state.analysis_data['valuation']['flood_risk_adjustment_pct']:.1f}%
                • Recommendation: {"APPROVE" if st.session_state.analysis_data['risk']['risk_score'] <= 60 else "REVIEW REQUIRED"}
                """
            
            st.markdown(response_text)
        else:
            response_text = "Please enter a property address and click 'Analyze Property' to begin analysis."
            st.info(response_text)
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Report Generation Section
if st.session_state.analysis_data:
    st.markdown("---")
    
    # Report generation controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("## 📋 Generate Comprehensive Report")
    with col2:
        generate_report = st.button("🔄 Generate Report", type="secondary", use_container_width=True)
    with col3:
        if st.session_state.generated_report:
            download_disabled = False
        else:
            download_disabled = True
        download_report = st.button("📥 Download Report", disabled=download_disabled, use_container_width=True)    
    if generate_report:
        with st.spinner("📝 Generating comprehensive report..."):
            st.session_state.generated_report = generate_comprehensive_report(
                st.session_state.analysis_data,
                st.session_state.flood_data,
                st.session_state.report_format
            )
        st.success("✅ Report generated successfully!")
    
    # Display report preview
    if st.session_state.generated_report:
        st.markdown("### 👁️ Report Preview")
        ...
        
        # Download button (replace manual base64 anchor with st.download_button)
        # ...existing code...
        st.download_button(
            label=f"⬇️ Download {st.session_state.generated_report['filename']}",
            data=st.session_state.generated_report['content'].encode(),
            file_name=st.session_state.generated_report['filename'],
            mime="application/octet-stream",
            use_container_width=True
        )
        st.markdown("### 👁️ Report Preview")
        
        if st.session_state.report_format == 'txt':
            st.text_area("Report Content", st.session_state.generated_report['content'], height=300)
        elif st.session_state.report_format == 'json':
            st.json(json.loads(st.session_state.generated_report['content']))
        elif st.session_state.report_format == 'html':
            st.components.v1.html(st.session_state.generated_report['content'], height=400, scrolling=True)
        
        # Download button
        if download_report:
            b64 = base64.b64encode(st.session_state.generated_report['content'].encode()).decode()
            href = f'data:application/octet-stream;base64,{b64}'
            st.markdown(f'<a href="{href}" download="{st.session_state.generated_report["filename"]}" class="download-btn">⬇️ Download {st.session_state.generated_report["filename"]}</a>', unsafe_allow_html=True)

# Display detailed analysis if available
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    flood_data = st.session_state.flood_data
    
    st.markdown("---")
    st.markdown("## 📊 Detailed Analysis Dashboard")
    
    # Create tabs for different sections
    tabs = st.tabs([
        "📈 Executive Summary",
        "🏢 Property Details",
        "💰 Financial Analysis",
        "⚠️ Risk Assessment",
        "🌊 Flood Risk",
        "📊 Market Analysis"
    ])
    
    with tabs[0]:  # Executive Summary
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Executive Summary")
            st.markdown("""
            This comprehensive analysis provides a detailed assessment of the commercial property 
            for loan underwriting purposes. The analysis includes property valuation, risk assessment, 
            market conditions, and flood risk evaluation using NFIP historical data.
            """)
            
            # Key highlights
            st.markdown("#### 📌 Key Highlights")
            highlights = [
                f"**Property Value**: ${data['valuation']['adjusted_property_value']:,.0f} (flood-adjusted)",
                f"**Loan Recommendation**: {'✅ APPROVE' if data['risk']['risk_score'] <= 60 else '⚠️ REVIEW REQUIRED'}",
                f"**Risk Level**: <span class='risk-{data['risk']['risk_level'].lower()}'>{data['risk']['risk_level']}</span>",
                f"**Flood Risk Impact**: {data['valuation']['flood_risk_adjustment_pct']:.1f}% value adjustment",
                f"**Processing Time**: 2 minutes (vs. 4+ hours manual)"
            ]
            
            for highlight in highlights:
                st.markdown(f"- {highlight}", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚡ Quick Facts")
            quick_facts = {
                "Address": data['property']['address'],
                "Square Feet": f"{data['property']['sq_ft']:,.0f}",
                "Year Built": data['property']['year_built'],
                "Zoning": data['property']['zoning_code'],
                "Zip Code": data['property']['zip_code']
            }
            
            for label, value in quick_facts.items():
                st.markdown(f"**{label}**: {value}")
    
    with tabs[1]:  # Property Details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📍 Property Information")
            property_info = [
                ("Address", data['property']['address']),
                ("Square Feet", f"{data['property']['sq_ft']:,.0f}"),
                ("Year Built", data['property']['year_built']),
                ("Zoning Code", data['property']['zoning_code']),
                ("Last Sale Price", f"${data['property']['last_sale_price']:,.0f}"),
                ("Current Owner", data['property']['current_owner'])
            ]
            
            for label, value in property_info:
                st.markdown(f"""
                <div class="data-point">
                    <span class="data-label">{label}</span>
                    <span class="data-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🏙️ Location Details")
            location_info = [
                ("Zip Code", data['property']['zip_code']),
                ("Population Growth (3yr)", f"{data['property']['population_growth_3yr']*100:.1f}%"),
                ("Median Income", f"${data['property']['median_household_income']:,.0f}"),
                ("Unemployment Rate", f"{data['property']['unemployment_rate']*100:.1f}%"),
                ("Crime Score", f"{data['property']['crime_score']}/100"),
                ("Regulatory Risk", "⚠️ Flagged" if data['property']['regulatory_changes_flag'] else "✅ Clear")
            ]
            
            for label, value in location_info:
                st.markdown(f"""
                <div class="data-point">
                    <span class="data-label">{label}</span>
                    <span class="data-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[2]:  # Financial Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Income Analysis")
            income_metrics = [
                ("Gross Potential Income", f"${data['valuation']['gross_potential_income']:,.0f}"),
                ("Effective Gross Income", f"${data['valuation']['effective_gross_income']:,.0f}"),
                ("Net Operating Income", f"${data['valuation']['net_operating_income']:,.0f}"),
                ("NOI Margin", f"{data['valuation']['noi_margin_used']:.1f}%"),
                ("Market Rent", f"${data['property']['market_rent_per_sqft']:.2f}/sq ft")
            ]
            
            for label, value in income_metrics:
                st.metric(label, value)
        
        with col2:
            st.markdown("#### 🏦 Valuation Metrics")
            valuation_metrics = [
                ("Estimated Value", f"${data['valuation']['estimated_property_value']:,.0f}"),
                ("Flood Adjustment", f"-{data['valuation']['flood_risk_adjustment_pct']:.1f}%"),
                ("Adjusted Value", f"${data['valuation']['adjusted_property_value']:,.0f}"),
                ("Price per Sq Ft", f"${data['valuation']['price_per_sqft']:,.2f}"),
                ("Cap Rate", f"{data['valuation']['cap_rate']*100:.2f}%")
            ]
            
            for label, value in valuation_metrics:
                st.metric(label, value)
            
            # Value comparison chart
            fig = go.Figure(data=[
                go.Bar(name='Estimated Value', 
                      x=['Property Value'], 
                      y=[data['valuation']['estimated_property_value']],
                      marker_color='#3B82F6'),
                go.Bar(name='Flood Adjusted', 
                      x=['Property Value'], 
                      y=[data['valuation']['adjusted_property_value']],
                      marker_color='#10B981')
            ])
            fig.update_layout(
                title="Flood Risk Impact on Valuation",
                yaxis_title="Value ($)",
                showlegend=True,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:  # Risk Assessment
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Risk Score Analysis")
            
            # Risk score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=data['risk']['risk_score'],
                title={'text': "Overall Risk Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "green"},
                        {'range': [30, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 60
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⚠️ Risk Factors")
            risk_factors = data['risk']['risk_factors']
            
            risk_df = pd.DataFrame.from_dict(risk_factors, orient='index', columns=['Score'])
            risk_df['Factor'] = risk_df.index
            risk_df['Risk Level'] = pd.cut(risk_df['Score'], 
                                          bins=[0, 30, 60, 100],
                                          labels=['Low', 'Moderate', 'High'])
            
            fig2 = px.bar(risk_df, x='Score', y='Factor', orientation='h',
                         color='Risk Level',
                         color_discrete_map={'Low': '#10B981', 'Moderate': '#F59E0B', 'High': '#EF4444'},
                         title="Risk Factor Breakdown")
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tabs[4]:  # Flood Risk
        if flood_data:
            st.markdown("### 🌊 Comprehensive Flood Risk Assessment")
            
            # Flood risk summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                flood_risk_class = data['property']['flood_zone_risk']
                risk_class_card = f"""
                <div class="metric-card flood-risk-{flood_risk_class.lower()}">
                    <h4 style="margin: 0 0 10px 0; color: #1F2937;">Flood Zone Risk</h4>
                    <div style="font-size: 2rem; font-weight: 700; color: #1F2937;">{flood_risk_class}</div>
                    <div style="font-size: 0.9rem; color: #6B7280;">Primary Risk Classification</div>
                </div>
                """
                st.markdown(risk_class_card, unsafe_allow_html=True)
            
            with col2:
                flood_zones = flood_data.get('flood_zones_present', 'Unknown')
                st.metric("Identified Flood Zones", flood_zones)
            
            with col3:
                insurance_req = flood_data.get('flood_insurance_required', 'Unknown')
                st.metric("Insurance Required", insurance_req)
            
            # Historical flood data
            st.markdown("#### 📜 Historical Flood Data")
            hist_col1, hist_col2, hist_col3 = st.columns(3)
            
            with hist_col1:
                st.metric("Historical Losses", f"{flood_data.get('historical_loss_count', 0):,}")
            
            with hist_col2:
                payments = flood_data.get('historical_payment_total', 'Not Available')
                st.metric("Total Payments", payments)
            
            with hist_col3:
                severity = flood_data.get('avg_loss_severity', 'Not Available')
                st.metric("Average Loss Severity", severity)
            
            # Insurance recommendations
            st.markdown("#### 🛡️ Insurance Recommendations")
            
            rec_col1, rec_col2 = st.columns(2)
            
            with rec_col1:
                st.info(f"""
                **Recommended Coverage**: {flood_data.get('recommended_insurance_coverage', 'Not Available')}
                
                **Coverage Details**:
                - Based on {data['valuation']['flood_risk_adjustment_pct']:.1f}% flood risk adjustment
                - Property value: ${data['valuation']['estimated_property_value']:,.0f}
                - Adjusted value: ${data['valuation']['adjusted_property_value']:,.0f}
                """)
            
            with rec_col2:
                st.warning(f"""
                **Important Notes**:
                - {flood_data.get('flood_insurance_required', 'Check required')}
                - Flood risk contributes {data['valuation']['flood_risk_adjustment_pct']:.1f}% to property value adjustment
                - NFIP historical data shows {flood_data.get('historical_loss_count', 0)} claims in this area
                """)
            
            # Flood zone details
            st.markdown("#### 🗺️ Flood Zone Details")
            if flood_data.get('flood_zones_present') and flood_data['flood_zones_present'] != "Unknown":
                zones = flood_data['flood_zones_present'].split(', ')
                for zone in zones:
                    risk_desc = get_zone_risk_description(zone)
                    st.markdown(f"**Zone {zone}**: {risk_desc}")
        else:
            st.info("Flood risk analysis was not included in this analysis. Enable it in the sidebar options.")
    
    with tabs[5]:  # Market Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Market Trends")
            market_metrics = [
                ("Vacancy Rate", f"{data['property']['vacancy_rate']*100:.1f}%"),
                ("Market Rent", f"${data['property']['market_rent_per_sqft']:.2f}/sq ft"),
                ("Absorption Rate", f"{data['property']['absorption_rate']*100:.1f}%"),
                ("Cap Rate Avg", f"{data['property']['cap_rate_avg']*100:.2f}%")
            ]
            
            for label, value in market_metrics:
                st.metric(label, value)
        
        with col2:
            st.markdown("#### 🏘️ Demographic Trends")
            demo_metrics = [
                ("Population Growth", f"{data['property']['population_growth_3yr']*100:.1f}%"),
                ("Median Income", f"${data['property']['median_household_income']:,.0f}"),
                ("Unemployment", f"{data['property']['unemployment_rate']*100:.1f}%")
            ]
            
            for label, value in demo_metrics:
                st.metric(label, value)
            
            # Vacancy rate gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=data['property']['vacancy_rate'] * 100,
                title={'text': "Vacancy Rate"},
                gauge={
                    'axis': {'range': [0, 20]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 5], 'color': "green"},
                        {'range': [5, 10], 'color': "yellow"},
                        {'range': [10, 20], 'color': "red"}
                    ]
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)


# Main application logic
if __name__ == "__main__":
    # Display instructions if no analysis
    if not st.session_state.analysis_data:
        st.markdown("---")
        st.markdown("## 🚀 Getting Started")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📋 How to Use
            1. **Enter Property Address** in the sidebar
            2. **Configure Analysis Options** (flood risk, rental comps)
            3. **Select Report Format** (TXT, PDF, JSON, HTML)
            4. **Click "Analyze Property"** to begin analysis
            5. **Review Results** in the dashboard
            6. **Generate Report** for download
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 Key Features
            • **Automated Data Collection** from BigQuery
            • **Flood Risk Assessment** using NFIP historical data
            • **Comprehensive Valuation** with risk adjustments
            • **AI-Powered Insights** using Gemini AI
            • **Multiple Report Formats** for different needs
            • **Interactive Visualizations** for better insights
            """)
        
        st.markdown("---")
        st.markdown("### 📊 Sample Analysis Results")
        
        # Show sample data for demonstration
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        with sample_col1:
            st.metric("Property Value", "$12,450,000")
            st.metric("Risk Level", "Moderate")
        
        with sample_col2:
            st.metric("Flood Adjustment", "-3.2%")
            st.metric("Cap Rate", "7.4%")
        
        with sample_col3:
            st.metric("Vacancy Rate", "9.9%")
            st.metric("NOI Margin", "62.8%")