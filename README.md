# Exploratory Data Analysis (EDA) and Data Cleaning

## Project Overview
This project performs **Exploratory Data Analysis (EDA)** and **Data Cleaning** on [Amazon Sales 2025 Dataset](./data/raw/amazon_sales_2025_INR.csv) to gain insights and prepare the data for further analysis or modeling. The tasks completed include:
- Data quality assessment (checking for inconsistencies, outliers)
- Data cleaning (handling missing values, duplicates, fixing data types)
- Statistical Exploratory data analysis (visualizing distributions, relationships)
- Transformation (modifying or reshaping the data)

## Project Workflow

## Phase 1: Initial Exploration

- **Data Overview**: Key columns explored include **Product_Name**, **Review_Text**, **Delivery_Status**, **Payment_Method**, **Product_Category**, and **Total_Sales_INR**. No missing values found, but need for type conversion.

- **Key Decisions**:
   - Convert to categorical types: **Product_Name**, **Review_Text**, **Delivery_Status**, **Payment_Method**, **Product_Category**.
   - Verify **Total_Sales_INR** calculation. 

- **Hypothesis**:
  - **Relevant Variables**: **Product_Category**, **State**, **Total_Sales_INR**, **Date** (RQ1 & RQ4); **Review_Rating**, **Review_Text**, **Delivery_Status**, **Unit_Price_INR** (RQ2); **Payment_Method**, **Total_Sales_INR**, **Delivery_Status** (RQ3).
  - **Useful Relationships**: **State vs Total_Sales_INR**, **Delivery_Status vs Review_Rating**, **Payment Method vs Revenue**, **Date vs Seasonal Trends**.

## Phase 2: Data Quality Assessment

### Motivation:
- Assess the dataset for issues such as incorrect data types, missing values, duplicates, and outliers to ensure it can be trusted for analysis.

### Key Findings:
- **Data Types**: Columns like `Product_Name`, `Review_Text`, `Delivery_Status`, `Payment_Method`, and `Product_Category` need to be converted to categorical types.
- **Missing Values**: No missing values found (`.isna().sum()`).
- **Duplicates**: No duplicates found; customer IDs are unique.
- **Outliers**: `Unit_Price_INR` shows no outliers. Outliers in `Total_Sales_INR` appear to be legitimate high-value transactions, likely from premium or bulk purchases.
- **Value Range**: All numerical values fall within a reasonable range.

### Hypothesis:
- Outliers in `Total_Sales_INR` are likely due to premium or bulk items.
- **No Missing Values**: The dataset is complete with no missing values.
- All variables are within expected business domains.

### Iteration Signals:
- No need to revisit data loading since there are no missing values.

## Phase 3: Cleaning

### Key Findings:
- **Duplicates**: No duplicates found; no rows need to be removed.
- **Outliers**: Outliers in `Total_Sales_INR` were validated as legitimate high-value transactions and retained.
- **Missing Values**: No missing values found across the dataset.
- **Data Types**: Columns like `Product_Name`, `Review_Text`, `Delivery_Status`, `Payment_Method`, and `Product_Category` were converted to categorical types.

### Hypothesis Generation for Cleaning Decisions:
1. **Could type conversions introduce bias?**  
   No, converting category-like fields to category does not modify the meaning of the data.

2. **Are outliers legitimate or errors?**  
   Outliers represent legitimate high-value transactions and are kept in the dataset.

3. **What sensitivity analyses should be considered?**  
   Compare model performance with and without outliers to assess their impact.

4. **What assumptions are we making?**  
   - **Order_ID** uniquely identifies each transaction.
   - No hidden missing values beyond what was detected in **Phase 2**.
   - High-value purchases are permitted in the dataset.

### Iteration Signals:
- The cleaned dataset is now ready for **Phase 4**: Statistical Exploratory Data Analysis (EDA).

## Phase 4: Statistical Exploratory Data Analysis (EDA)

### Motivation:
Identify patterns and relationships in the **Amazon 2025 Diwali Sales** dataset.

### Key Findings:
- **High-value Electronics**: Electronics, particularly premium items, significantly contribute to the overall sales. The `Total_Sales_INR` distribution is skewed due to these high-value transactions.
- **Delivery Status vs Ratings**: The `Delivery_Status` affects customer ratings. Returns or pending orders tend to have lower ratings compared to delivered ones.
- **Regional Preferences**: Different states show preferences for specific product categories (e.g., electronics in some states, clothing/beauty in others), suggesting demographic or seasonal factors.
- **Payment Method and Revenue**: Customers using **UPI** and **Credit Cards** tend to make larger purchases compared to **COD** users.
- **Price vs Review Rating**: No direct relationship between `Unit_Price_INR` and `Review_Rating`. This indicates that customer satisfaction may be more influenced by delivery and product quality rather than the price itself.

### Hypothesis:
1. **High-value electronics** drive overall category dominance.
2. **Delivery_Status** may influence **Review_Rating**.
3. Regional preferences vary by state (e.g., electronics vs clothing).
4. **Payment method** (UPI/Credit Card) correlates with larger purchases.
5. **Price** appears independent of **Review_Rating**.

### Iteration Signals:
- **Right-skewed** `Total_Sales_INR`: Log-transform in Phase 5.
- **Delivery_Status** affects ratings: Consider binary variable in Phase 5.
- **State × Category** interactions: Explore segmentation in Phase 5.
- **Price vs Rating**: Suggests sentiment analysis for richer features.

## Phase 5: Feature Engineering & Transformation

### Motivation:
In this phase, we create transformed features to make patterns clearer, reduce skew, and support interactive dashboard exploration.

### Key Actions:
- **Transformed Features**: Created new features like `Delivery_Flag`, `Satisfied`, `Log_Total_Sales`, `Category_Avg_Price`, and payment-related dummy variables.
- **Skew Reduction**: Applied log-transformation to `Total_Sales_INR` to improve interpretability and reduce skew.
- **Temporal Features**: Added `Month` and `Quarter` for better time-based analysis.
- **Dashboard Enhancement**: Introduced dummy variables for improved filtering in dashboards.

### Conclusion:
- **New Variables**: Added features that support **RQ1–RQ4** and provide deeper insights into sales and customer satisfaction.
- **Skew Reduction**: Log-transformation of `Total_Sales_INR` clarifies the data and improves visualization.
- **Group-Level Features**: Enhanced with satisfaction and delivery flags for subgroup analysis.
- **Improved Dashboard**: Multi-filtering capability using dummy variables enhances interactive exploration.

### Hypothesis Generation:
1. **Credit Card / UPI customers** spend more than **COD** customers.
2. **Delivery_Flag** is a stronger predictor of satisfaction than `Unit_Price_INR`.
3. Categories with higher **Category_Avg_Price** show more stable sales patterns.
4. **Quarter** may predict demand spikes (e.g., Q4 = festival season).
5. **Satisfied customers** are more common in high-revenue regions.

### Iteration Signals:
- **Skew reduction** via `Log_Total_Sales` improves plot interpretation.
- **Dummy variables** enable advanced dashboard filtering.
- **Satisfaction flag** simplifies modeling and subgroup analysis.
- **Month/Quarter features** support deeper time-based analysis.

## Phase 6: Interactive Dashboard & Final Analysis

### Motivation:
In this phase, we build an interactive dashboard using **Streamlit** to allow users to explore key patterns and relationships in the **Amazon 2025 Diwali Sales** dataset. Here is the link: [**Streamlit Dashboard: Amazon 2025 Diwali Sales EDA**](https://deploy-project.streamlit.app/)

### Key Actions:
- **Streamlit Dashboard**: Developed a dashboard displaying visualizations like `Total_Sales_INR`, `Product_Category`, `Review_Rating`, and time-based trends.
- **Interactive Filters**: Implemented filters for product category, delivery status, payment method, and time-based analysis (month, quarter).

### Conclusion:
- **Interactive Exploration**: Users can explore and analyze the data in real-time.
- **User Engagement**: The dashboard supports detailed exploration of sales trends, customer behavior, and more.
- **Final Output**: A comprehensive tool for visualizing key insights from the dataset.

### Hypothesis Testing:
- **Credit Card / UPI customers spend more** than **COD** customers.
- **Delivery_Status** affects **Review_Rating**.
- **Category_Avg_Price** leads to more stable sales patterns.

### Iteration Signals:
- **User Feedback**: Continuously refine the dashboard based on user interaction.
- **Additional Features**: Add new features like predictive insights or advanced visualizations if needed.
- **Performance Optimization**: Ensure dashboard performs efficiently even with large datasets.

### Next Steps:
- Deploy the **Streamlit app** for interactive analysis.
- Continue refining the dashboard based on user feedback.
---



