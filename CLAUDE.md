Project Overview

A Baking Business Costing, Inventory, and Profit Tracking Tool designed for a home-based baking side hustle.

The system helps track ingredient costs, manage inventory, calculate recipe costs, compute yield based on dough weight, and analyze profit per product and per sale.

Stack
Frontend: Streamlit (Python)
Backend: Python
Database: Excel file (local storage using pandas)
Architecture Rules
Keep the system modular and simple
Separate logic into:
UI layer (Streamlit views)
Business logic layer (costing, yield, profit calculations)
Data layer (Excel read/write)
All calculations must be handled in a dedicated logic/service layer
Avoid mixing UI code with computation logic
Coding Standards
Use clean and readable Python code
Use functions for each major feature
Use pandas for Excel operations
Use clear variable naming (snake_case)
Handle errors using try/except
Avoid overly complex abstractions
Core Features
1. Ingredient Cost Benchmark System
Store ingredient name, unit type, and cost per unit
Allow editing prices
Updating price should affect all recipe calculations
2. Inventory System (Lightweight)
Track current stock per ingredient
Allow manual updates
Optional auto-deduction when sales are recorded
Show low stock warnings
3. Recipe Template System
Create reusable recipe templates
Store:
Ingredients and quantities
Total dough weight
Portion size
Default selling price
Allow editing and duplication of templates
4. Dough Yield Calculator
Input:
Total dough weight
Portion size
Output:
Number of pieces
Cost per piece
Total batch cost
Include:
Rounding logic
Waste buffer option
5. Pricing & Profit System
Compute:
Cost per piece
Suggested price based on margin %
Profit per piece
Total batch profit
Profit margin %
Support:
Target margin mode
Target profit mode
6. Sales Tracker
Record:
Product
Quantity sold
Date
Compute:
Revenue
Cost
Profit
7. Profit Dashboard
Show:
Total revenue
Total profit
Best-selling products
Highest margin products
Folder Structure
/app.py → main Streamlit app
/services/
costing.py → ingredient & recipe cost calculations
yield.py → dough weight and portion calculations
profit.py → pricing and profit logic
/data/
excel_handler.py → read/write Excel files
/models/
ingredient_model.py
recipe_model.py
sales_model.py
/utils/
helpers.py
Data Structure (Excel)

Single Excel file with sheets:

Ingredients
name
unit
cost_per_unit
last_updated
Inventory
ingredient_name
stock_quantity
min_threshold
Recipes
recipe_name
ingredient_name
quantity
portion_size
dough_weight
selling_price
Sales
date
product_name
quantity
revenue
cost
profit
Do
Keep the UI simple and fast
Optimize for daily usage
Make calculations accurate and transparent
Ensure all values auto-update dynamically
Focus on profitability insights
Don't
Do not overengineer the system
Do not add unnecessary complexity
Do not mix UI and business logic
Do not require advanced setup
Example Pattern
UI Layer (Streamlit)
Takes user input
Calls service functions
Displays results
Service Layer
Handles:
Cost calculations
Yield computation
Profit logic
Data Layer
Reads/writes Excel
Ensures data consistency

## Available Skills

Skills are in `.claude/skills/`. Activate by invoking the skill name.

| Skill | Trigger |
|-------|---------|
| ckm:design | logo, banner, CIP, slides, icons, social photos |
| ckm:brand | brand voice, style guide, visual identity |
| ckm:ui-styling | shadcn/ui components, Tailwind layouts |
| ckm:design-system | design tokens, CSS variables |
| ckm:slides | HTML presentations, Chart.js |
| ckm:banner-design | social media banners, ad creatives |