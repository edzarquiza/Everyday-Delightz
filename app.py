import streamlit as st
import pandas as pd
from pathlib import Path
import math
from datetime import date, timedelta
import plotly.graph_objects as go
from data_manager import DataManager

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Everyday DelightZ",
    page_icon="🧁",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── Brand CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');

  /* ── Design tokens ───────────────────────────────────────────── */
  :root {
    --color-primary:     #204ce5;
    --color-primary-dk:  #0048aa;
    --color-primary-lt:  #eef2ff;
    --color-green:       #3aad2e;
    --color-red:         #e05555;
    --color-bg:          #f4f6ff;
    --color-surface:     #ffffff;
    --color-border:      #d0d8f0;
    --color-text:        #112337;
    --color-muted:       #686e77;
    --radius-sm:         8px;
    --radius-md:         12px;
    --radius-lg:         16px;
    --shadow-sm:         0 1px 4px rgba(32,76,229,0.06);
    --shadow-md:         0 4px 16px rgba(32,76,229,0.10);
    --transition:        all 0.18s ease;
  }

  /* ── Base ────────────────────────────────────────────────────── */
  html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    color: var(--color-text);
    font-size: 14px;
    line-height: 1.6;
  }

  /* ── Layout ──────────────────────────────────────────────────── */
  .stApp { background-color: var(--color-bg); }
  section[data-testid="stSidebar"] {
    background-color: var(--color-surface) !important;
    border-right: 1px solid var(--color-border);
  }
  header[data-testid="stHeader"] { background-color: var(--color-bg) !important; }
  .stDeployButton { display: none; }
  div[data-testid="stToolbar"] { display: none; }

  /* ── Metric cards ────────────────────────────────────────────── */
  .metric-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-top: 3px solid var(--color-primary);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
  }
  .metric-card:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
  .metric-label {
    color: var(--color-muted);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }
  .metric-value { font-size: 28px; font-weight: 800; margin: 0; line-height: 1.2; }
  .metric-sub { color: var(--color-muted); font-size: 12px; margin-top: 6px; }

  /* ── Stat colours ────────────────────────────────────────────── */
  .gold  { color: var(--color-primary) !important; }
  .green { color: var(--color-green) !important; }
  .red   { color: var(--color-red) !important; }
  .teal  { color: var(--color-primary-dk) !important; }
  .white { color: var(--color-text) !important; }

  /* ── Alert banners ───────────────────────────────────────────── */
  .alert-low {
    background: #e0555510;
    border-left: 4px solid var(--color-red);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    margin-bottom: 16px;
    color: var(--color-red);
    font-size: 14px;
    font-weight: 600;
  }
  .alert-ok {
    background: #3aad2e10;
    border-left: 4px solid var(--color-green);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    margin-bottom: 16px;
    color: var(--color-green);
    font-size: 14px;
    font-weight: 600;
  }

  /* ── Tables ──────────────────────────────────────────────────── */
  .dataframe { font-size: 13px !important; }
  div[data-testid="stDataFrame"] {
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
  }

  /* ── Section headers ─────────────────────────────────────────── */
  .section-header {
    color: var(--color-text);
    font-family: 'Montserrat', sans-serif;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 4px;
    border-left: 4px solid var(--color-primary);
    padding-left: 12px;
  }
  .section-sub {
    color: var(--color-muted);
    font-size: 13px;
    margin-bottom: 24px;
    padding-left: 16px;
  }

  /* ── Progress bars ───────────────────────────────────────────── */
  .prog-wrap { background: var(--color-primary-lt); border-radius: 6px; height: 8px; margin-top: 6px; overflow: hidden; }
  .prog-fill-ok  { background: var(--color-green); height: 8px; border-radius: 6px; }
  .prog-fill-low { background: var(--color-red);   height: 8px; border-radius: 6px; }

  /* ── Pill badges ─────────────────────────────────────────────── */
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; }
  .badge-gold  { background: #204ce512; color: var(--color-primary); border: 1px solid #204ce530; }
  .badge-green { background: #3aad2e12; color: var(--color-green);   border: 1px solid #3aad2e30; }
  .badge-red   { background: #e0555512; color: var(--color-red);     border: 1px solid #e0555530; }

  /* ── Sidebar nav buttons ─────────────────────────────────────── */
  .stButton > button {
    background: transparent;
    border: 1px solid var(--color-border);
    color: var(--color-muted);
    border-radius: 9999px;
    width: 100%;
    text-align: left;
    padding: 11px 20px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 6px;
    transition: var(--transition);
    cursor: pointer;
  }
  .stButton > button:hover {
    background: var(--color-primary);
    color: #ffffff;
    border-color: var(--color-primary);
    box-shadow: 0 4px 12px rgba(32,76,229,0.25);
    transform: translateY(-1px);
  }
  .stButton > button:active { transform: translateY(0); }

  /* ── Form inputs ─────────────────────────────────────────────── */
  .stTextInput input, .stNumberInput input, .stDateInput input {
    background: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
    color: var(--color-text) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.15s !important;
  }
  .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 3px rgba(32,76,229,0.12) !important;
    outline: none !important;
  }
  .stSelectbox > div > div {
    background: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--color-text) !important;
  }

  /* ── Expanders ───────────────────────────────────────────────── */
  .streamlit-expanderHeader {
    background: var(--color-primary-lt);
    border-radius: var(--radius-sm);
    color: var(--color-text);
    font-weight: 600;
    font-size: 14px;
    border: 1px solid var(--color-border);
  }
  .streamlit-expanderHeader:hover { background: #dde5ff; }

  /* ── Tabs ────────────────────────────────────────────────────── */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--color-primary-lt);
    border-radius: var(--radius-sm);
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--color-border);
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
    color: var(--color-muted);
    padding: 8px 16px;
  }
  .stTabs [aria-selected="true"] {
    background: var(--color-primary) !important;
    color: #ffffff !important;
  }

  /* ── Sliders ─────────────────────────────────────────────────── */
  .stSlider [data-baseweb="slider"] { padding: 0 4px; }

  /* ── Checkboxes ──────────────────────────────────────────────── */
  .stCheckbox label { font-size: 14px; color: var(--color-text); font-weight: 500; }

  /* ── Dividers ────────────────────────────────────────────────── */
  hr { border-color: var(--color-border) !important; margin: 24px 0 !important; }

  /* ── Scrollbar ───────────────────────────────────────────────── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--color-bg); }
  ::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #b0bcd8; }

  /* ── Reduce motion ───────────────────────────────────────────── */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { transition: none !important; animation: none !important; }
  }

  /* ── Mobile ──────────────────────────────────────────────────── */
  @media (max-width: 768px) {
    /* Reduce main block padding so content uses full width */
    .block-container {
      padding-left: 12px !important;
      padding-right: 12px !important;
      padding-top: 16px !important;
      max-width: 100% !important;
    }

    /* Section headers — smaller on mobile */
    .section-header {
      font-size: 18px !important;
      padding-left: 10px !important;
      margin-bottom: 2px !important;
    }
    .section-sub {
      font-size: 12px !important;
      margin-bottom: 16px !important;
    }

    /* Metric cards — tighter padding, smaller text */
    .metric-card {
      padding: 14px 16px !important;
      margin-bottom: 8px !important;
    }
    .metric-value { font-size: 22px !important; }
    .metric-label { font-size: 11px !important; }
    .metric-sub   { font-size: 11px !important; }

    /* Buttons — bigger touch target */
    .stButton > button {
      padding: 14px 20px !important;
      font-size: 15px !important;
      min-height: 48px !important;
    }

    /* Form inputs — bigger touch targets */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
      font-size: 16px !important;  /* prevents iOS zoom on focus */
      padding: 12px 14px !important;
      min-height: 48px !important;
    }
    .stSelectbox > div > div {
      font-size: 16px !important;
      min-height: 48px !important;
    }

    /* Tables — horizontal scroll instead of overflow */
    div[data-testid="stDataFrame"] {
      overflow-x: auto !important;
      -webkit-overflow-scrolling: touch;
    }

    /* Tabs — smaller, scrollable on mobile */
    .stTabs [data-baseweb="tab-list"] {
      overflow-x: auto !important;
      flex-wrap: nowrap !important;
      -webkit-overflow-scrolling: touch;
      padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
      font-size: 12px !important;
      padding: 8px 12px !important;
      white-space: nowrap !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
      font-size: 13px !important;
      padding: 12px 14px !important;
    }

    /* Dividers — less vertical space */
    hr { margin: 16px 0 !important; }

    /* Columns — ensure they stack cleanly */
    div[data-testid="column"] { padding: 0 4px !important; }
  }
</style>
""", unsafe_allow_html=True)

# ── Data manager ─────────────────────────────────────────────────────
@st.cache_resource
def get_data_manager():
    return DataManager()

dm = get_data_manager()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("Logo.jpg", use_container_width=True)
    st.markdown("""
    <div style='text-align:center; padding: 4px 0 16px;'>
      <div style='color: #686e77; font-size: 12px; letter-spacing: 1px;'>🧁 BAKING BUSINESS TOOL</div>
    </div>
    <hr style='border-color: #d0d8f0; margin-bottom: 16px;'>
    """, unsafe_allow_html=True)

    PAGES = {
        "📊 Dashboard": "dashboard",
        "🥚 Ingredient Costs": "ingredients",
        "📦 Inventory": "inventory",
        "🧾 Recipe Templates": "recipes",
        "⚙️ Yield & Cost Calc": "calculator",
        "📈 Sales Tracker": "sales",
        "💸 Expenses": "expenses",
        "🗓️ Batch Planner": "planner",
    }

    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    for label, key in PAGES.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key

    # Low stock alert in sidebar
    inv = dm.get_ingredients()
    low = inv[inv["stock"] <= inv["min_stock"]]
    if not low.empty:
        st.markdown(f"""
        <div style='background:#e0555518; border:1px solid #e0555555; border-radius:10px; padding:12px; margin-top:20px;'>
          <div style='color:#e05555; font-weight:700; font-size:13px;'>⚠️ {len(low)} Low Stock Item(s)</div>
          <div style='color:#686e77; font-size:12px; margin-top:4px;'>{"<br>".join(low["name"].tolist())}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Data Backup / Restore ─────────────────────────────────────
    st.markdown("---")
    st.markdown("<div style='font-size:12px; font-weight:700; color:#204ce5; margin-bottom:6px;'>💾 Data Backup</div>", unsafe_allow_html=True)

    db_path = Path("everyday_delightz_data.xlsx")
    if db_path.exists():
        with open(db_path, "rb") as f:
            st.download_button(
                label="⬇️ Download My Data",
                data=f,
                file_name="everyday_delightz_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    uploaded = st.file_uploader("⬆️ Restore from backup", type=["xlsx"], label_visibility="collapsed")
    if uploaded:
        with open(db_path, "wb") as f:
            f.write(uploaded.read())
        st.success("Data restored! Refreshing…")
        st.rerun()

    st.markdown(f"""
    <div style='color:#686e77; font-size:12px; text-align:center; margin-top:16px; padding-top:12px; border-top:1px solid #d0d8f0;'>
      🇵🇭 Made for Philippine bakers
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────────────
def peso(val):
    try:
        return f"₱{float(val):,.2f}"
    except:
        return "₱0.00"

def calc_recipe_cost(recipe_id, _items_cache=None, _ings_cache=None):
    """Return total batch cost for a recipe. Pass caches to avoid repeated DB reads."""
    items = _items_cache if _items_cache is not None else dm.get_recipe_items(recipe_id)
    ings  = _ings_cache  if _ings_cache  is not None else dm.get_ingredients()
    total = 0.0
    for _, row in items.iterrows():
        ing = ings[ings["id"] == row["ingredient_id"]]
        if not ing.empty:
            total += float(ing.iloc[0]["cost_per_unit"]) * float(row["qty"])
    return total

def calc_yield(dough_weight, portion, waste_pct):
    effective = dough_weight * (1 - waste_pct / 100)
    return max(0, math.floor(effective / portion)) if portion > 0 else 0

# ────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ────────────────────────────────────────────────────────────────────
if page == "dashboard":
    st.markdown('<div class="section-header">📊 Profit Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your baking business at a glance</div>', unsafe_allow_html=True)

    sales_all    = dm.get_sales()
    recipes      = dm.get_recipes()
    ings         = dm.get_ingredients()
    expenses_all = dm.get_expenses()
    today_dt     = date.today()

    # ── Period filter ─────────────────────────────────────────────
    period = st.radio(
        "Period", ["This Week", "This Month", "This Year", "All Time"],
        horizontal=True, index=1, label_visibility="collapsed"
    )

    def _filter_period(df, date_col="date"):
        if df.empty or period == "All Time":
            return df.copy()
        d = df.copy()
        d[date_col] = pd.to_datetime(d[date_col]).dt.date
        if period == "This Week":
            start = today_dt - timedelta(days=today_dt.weekday())
        elif period == "This Month":
            start = today_dt.replace(day=1)
        else:
            start = today_dt.replace(month=1, day=1)
        return d[d[date_col] >= start]

    sales    = _filter_period(sales_all)
    expenses = _filter_period(expenses_all)
    total_overhead = float(expenses["amount"].sum()) if not expenses.empty else 0.0

    # ── Compute KPIs ──────────────────────────────────────────────
    total_revenue = 0.0
    total_cost    = 0.0
    _cost_cache   = {}
    _all_items    = dm.get_recipe_items()
    if not sales.empty:
        for _, s in sales.iterrows():
            r = recipes[recipes["id"] == s["recipe_id"]]
            if r.empty:
                continue
            r   = r.iloc[0]
            rid = r["id"]
            if rid not in _cost_cache:
                _ri = _all_items[_all_items["recipe_id"] == rid]
                _cost_cache[rid] = calc_recipe_cost(rid, _items_cache=_ri, _ings_cache=ings)
            pieces      = calc_yield(float(r.get("dough_weight", 0) or 0), float(r["portion_size"]), float(r["waste_pct"]))
            cost_per_pc = _cost_cache[rid] / pieces if pieces > 0 else 0
            total_revenue += float(s["qty"]) * float(s["price_per_pc"])
            total_cost    += cost_per_pc * float(s["qty"])

    net_profit     = total_revenue - total_cost - total_overhead
    overall_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    low_count      = len(ings[ings["stock"] <= ings["min_stock"]]) if not ings.empty else 0

    # ── KPI cards ─────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Revenue</div><div class="metric-value gold">{peso(total_revenue)}</div><div class="metric-sub">{period}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Overhead</div><div class="metric-value white">{peso(total_overhead)}</div><div class="metric-sub">Expenses · {period}</div></div>', unsafe_allow_html=True)
    with c3:
        pc = "green" if net_profit >= 0 else "red"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Net Profit</div><div class="metric-value {pc}">{peso(net_profit)}</div><div class="metric-sub">After overhead</div></div>', unsafe_allow_html=True)
    with c4:
        mc = "green" if overall_margin >= 50 else ("gold" if overall_margin >= 30 else "red")
        lbl = f"⚠️ {low_count} low stock" if low_count > 0 else "✅ Stock OK"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Net Margin</div><div class="metric-value {mc}">{overall_margin:.1f}%</div><div class="metric-sub">{lbl}</div></div>', unsafe_allow_html=True)

    # ── Monthly goal progress bar ─────────────────────────────────
    monthly_goal = float(dm.get_setting("monthly_goal") or 0)
    this_month_rev = 0.0
    if not sales_all.empty:
        _sm = sales_all.copy()
        _sm["_d"] = pd.to_datetime(_sm["date"]).dt.date
        _sm = _sm[_sm["_d"] >= today_dt.replace(day=1)]
        if not _sm.empty:
            this_month_rev = float((_sm["qty"] * _sm["price_per_pc"]).sum())

    st.markdown("---")
    g_col, btn_col = st.columns([5, 1])
    with g_col:
        if monthly_goal > 0:
            pct = min(this_month_rev / monthly_goal * 100, 100)
            bar_color = "#3aad2e" if pct >= 100 else ("#204ce5" if pct >= 60 else "#e8a020")
            st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:12px; padding:16px 20px; box-shadow:0 1px 4px rgba(32,76,229,0.06);'>
              <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                <span style='font-size:13px; font-weight:700; color:#112337;'>🎯 Monthly Revenue Goal</span>
                <span style='font-size:13px; font-weight:800; color:{bar_color};'>{peso(this_month_rev)} / {peso(monthly_goal)} &nbsp;·&nbsp; {pct:.0f}%</span>
              </div>
              <div style='background:#eef2ff; border-radius:6px; height:10px; overflow:hidden;'>
                <div style='background:{bar_color}; height:10px; border-radius:6px; width:{pct:.1f}%;'></div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#686e77; font-size:13px; padding:10px 0;">No monthly goal set — click <strong>Set Goal</strong> to track your monthly revenue progress.</div>', unsafe_allow_html=True)
    with btn_col:
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🎯 Set Goal", use_container_width=True, key="btn_set_goal"):
            st.session_state["show_goal_input"] = not st.session_state.get("show_goal_input", False)

    if st.session_state.get("show_goal_input"):
        with st.form("set_goal_form"):
            new_goal = st.number_input("Monthly Revenue Goal (₱)", min_value=0.0, value=monthly_goal, step=100.0)
            if st.form_submit_button("✅ Save Goal", use_container_width=True):
                dm.set_setting("monthly_goal", str(new_goal))
                st.session_state.pop("show_goal_input", None)
                st.success("✅ Goal saved!")
                st.rerun()

    st.markdown("---")

    # ── Product performance ────────────────────────────────────────
    st.markdown("#### 📦 Product Performance")
    if not recipes.empty:
        perf_rows = []
        for _, r in recipes.iterrows():
            rid = r["id"]
            _ri = _all_items[_all_items["recipe_id"] == rid]
            batch_cost  = _cost_cache.get(rid) or calc_recipe_cost(rid, _items_cache=_ri, _ings_cache=ings)
            pieces      = calc_yield(float(r.get("dough_weight") or 0), float(r["portion_size"]), float(r["waste_pct"]))
            cost_per_pc = batch_cost / pieces if pieces > 0 else 0
            sell_price  = float(r["default_price"])
            margin      = ((sell_price - cost_per_pc) / sell_price * 100) if sell_price > 0 else 0

            rel_sales = sales[sales["recipe_id"] == r["id"]] if not sales.empty else pd.DataFrame()
            total_qty = rel_sales["qty"].sum() if not rel_sales.empty else 0
            rev       = (rel_sales["qty"] * rel_sales["price_per_pc"]).sum() if not rel_sales.empty else 0
            profit    = (rel_sales["qty"] * (rel_sales["price_per_pc"] - cost_per_pc)).sum() if not rel_sales.empty else 0

            perf_rows.append({
                "Product": r["name"], "Cost/pc": peso(cost_per_pc),
                "Sell Price": peso(sell_price), "Margin %": f"{margin:.1f}%",
                "Units Sold": int(total_qty), "Revenue": peso(rev), "Profit": peso(profit),
            })
        st.dataframe(pd.DataFrame(perf_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No recipes yet. Add some in Recipe Templates.")

    # ── Recent sales ──────────────────────────────────────────────
    if not sales.empty:
        st.markdown("#### 🧾 Recent Sales (Last 10)")
        recent = sales.sort_values("date", ascending=False).head(10).copy()
        recent["Recipe"] = recent["recipe_id"].apply(
            lambda rid: recipes[recipes["id"] == rid]["name"].values[0] if not recipes[recipes["id"] == rid].empty else "—"
        )
        recent["Revenue"] = (recent["qty"] * recent["price_per_pc"]).map(lambda x: peso(x))
        recent["Price/pc"] = recent["price_per_pc"].map(lambda x: peso(x))
        st.dataframe(
            recent[["date", "Recipe", "qty", "Price/pc", "Revenue"]].rename(columns={"date": "Date", "qty": "Qty"}),
            use_container_width=True, hide_index=True
        )

    # ── Charts ────────────────────────────────────────────────────
    if not sales.empty and not recipes.empty:
        _chart_layout = dict(
            paper_bgcolor="#f4f6ff", plot_bgcolor="#f4f6ff",
            font=dict(color="#686e77", family="Montserrat, sans-serif", size=12),
            xaxis=dict(gridcolor="#e0e6ff", linecolor="#e0e6ff", tickfont=dict(color="#686e77")),
            yaxis=dict(gridcolor="#e0e6ff", linecolor="#e0e6ff", tickfont=dict(color="#686e77")),
            margin=dict(l=10, r=10, t=24, b=10),
            showlegend=False,
        )
        st.markdown("---")
        st.markdown("#### 📈 Sales Trends")
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("**Daily Revenue (₱)**")
            daily = sales.copy()
            daily["revenue"] = daily["qty"] * daily["price_per_pc"]
            daily_grp = daily.groupby("date")["revenue"].sum().reset_index().sort_values("date")
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=daily_grp["date"], y=daily_grp["revenue"], mode="lines+markers",
                line=dict(color="#204ce5", width=2), marker=dict(color="#204ce5", size=6),
                fill="tozeroy", fillcolor="rgba(32,76,229,0.10)",
            ))
            fig1.update_layout(**_chart_layout, height=230)
            st.plotly_chart(fig1, use_container_width=True)
        with ch2:
            st.markdown("**Revenue by Product (₱)**")
            prod_rev = []
            for _, r in recipes.iterrows():
                rel = sales[sales["recipe_id"] == r["id"]]
                rev = (rel["qty"] * rel["price_per_pc"]).sum() if not rel.empty else 0
                if rev > 0:
                    prod_rev.append({"name": r["name"], "rev": round(rev, 2)})
            if prod_rev:
                fig2 = go.Figure(go.Bar(
                    x=[p["rev"] for p in prod_rev], y=[p["name"] for p in prod_rev],
                    orientation="h", marker_color="#3aad2e",
                    text=[f"₱{p['rev']:,.0f}" for p in prod_rev],
                    textposition="auto", textfont=dict(color="#112337"),
                ))
                fig2.update_layout(**_chart_layout, height=230)
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### 💰 Profit by Product (₱)")
        profit_rows = []
        for _, r in recipes.iterrows():
            rid = r["id"]
            _ri = _all_items[_all_items["recipe_id"] == rid]
            bc  = _cost_cache.get(rid) or calc_recipe_cost(rid, _items_cache=_ri, _ings_cache=ings)
            pcs = calc_yield(float(r.get("dough_weight") or 0), float(r["portion_size"]), float(r["waste_pct"]))
            cpc = bc / pcs if pcs > 0 else 0
            rel = sales[sales["recipe_id"] == rid]
            if not rel.empty:
                profit = round((rel["qty"] * (rel["price_per_pc"] - cpc)).sum(), 2)
                profit_rows.append({"name": r["name"], "profit": profit})
        if profit_rows:
            fig3 = go.Figure(go.Bar(
                x=[p["profit"] for p in profit_rows], y=[p["name"] for p in profit_rows],
                orientation="h",
                marker_color=["#3aad2e" if p["profit"] >= 0 else "#e05555" for p in profit_rows],
                text=[f"₱{p['profit']:,.0f}" for p in profit_rows],
                textposition="auto", textfont=dict(color="#112337"),
            ))
            fig3.update_layout(**_chart_layout, height=max(180, len(profit_rows) * 60))
            st.plotly_chart(fig3, use_container_width=True)

# ────────────────────────────────────────────────────────────────────
# PAGE: INGREDIENTS
# ────────────────────────────────────────────────────────────────────
elif page == "ingredients":
    st.markdown('<div class="section-header">🥚 Ingredient Cost Benchmark</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Master pricing reference — changes here update all recipe costs automatically</div>', unsafe_allow_html=True)

    ings = dm.get_ingredients()

    # Low stock banner
    if not ings.empty:
        low = ings[ings["stock"] <= ings["min_stock"]]
        if not low.empty:
            st.markdown(f'<div class="alert-low">⚠️ Low Stock: {", ".join(low["name"].tolist())}</div>', unsafe_allow_html=True)

    # ── Add / Edit form ────────────────────────────────────────────
    with st.expander("➕ Add New Ingredient", expanded=False):
        with st.form("add_ing", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input("Ingredient Name", placeholder="e.g. All-Purpose Flour")
            with c2:
                unit = st.text_input("Unit", placeholder="g, ml, pcs, kg, L, tbsp, cup, tsp…")
            with c3:
                cost = st.number_input("Cost per Unit (₱)", min_value=0.0, step=0.001, format="%.4f")
            c4, c5 = st.columns(2)
            with c4:
                stock = st.number_input("Current Stock", min_value=0.0, step=1.0)
            with c5:
                min_stock = st.number_input("Min Stock Threshold", min_value=0.0, step=1.0)
            if st.form_submit_button("💾 Save Ingredient", use_container_width=True):
                if name and unit:
                    dm.add_ingredient(name, unit.strip(), cost, stock, min_stock)
                    st.success(f"✅ {name} added!")
                    st.rerun()
                elif name and not unit:
                    st.error("Please enter a unit (e.g. g, ml, pcs).")

    # ── Ingredient table ───────────────────────────────────────────
    ings = dm.get_ingredients()
    if not ings.empty:
        st.markdown("#### All Ingredients")

        search = st.text_input("🔍 Search", placeholder="Filter by name...")
        if search:
            ings = ings[ings["name"].str.contains(search, case=False, na=False)]

        if ings.empty:
            st.info("No ingredients match your search.")
        else:
            # Display table
            display = ings[["name", "unit", "cost_per_unit", "stock", "min_stock", "updated_at"]].copy()
            display.columns = ["Name", "Unit", "Cost/Unit (₱)", "Stock", "Min Stock", "Updated"]
            display["Cost/Unit (₱)"] = display["Cost/Unit (₱)"].map(lambda x: f"₱{x:.4f}")
            display["Status"] = ings.apply(lambda r: "⚠️ LOW" if r["stock"] <= r["min_stock"] else "✅ OK", axis=1)
            st.dataframe(display, use_container_width=True, hide_index=True)

        if not ings.empty:
            # Edit section
            st.markdown("#### ✏️ Edit an Ingredient")
            ing_names = ings["name"].tolist()
            sel_name = st.selectbox("Select ingredient to edit", ing_names)
            sel_ing = ings[ings["name"] == sel_name].iloc[0]

            with st.form("edit_ing"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    new_name = st.text_input("Name", value=sel_ing["name"])
                with c2:
                    new_unit = st.text_input("Unit", value=sel_ing["unit"])
                with c3:
                    new_cost = st.number_input("Cost/Unit (₱)", value=float(sel_ing["cost_per_unit"]), step=0.001, format="%.4f")
                c4, c5 = st.columns(2)
                with c4:
                    new_stock = st.number_input("Current Stock", value=float(sel_ing["stock"]), step=1.0)
                with c5:
                    new_min = st.number_input("Min Stock", value=float(sel_ing["min_stock"]), step=1.0)

                col_save, col_del = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 Update", use_container_width=True):
                        if not new_unit.strip():
                            st.error("Unit cannot be empty.")
                        else:
                            dm.update_ingredient(int(sel_ing["id"]), new_name, new_unit.strip(), new_cost, new_stock, new_min)
                            st.success("✅ Updated!")
                            st.rerun()
                with col_del:
                    if st.form_submit_button("🗑️ Delete", use_container_width=True):
                        dm.delete_ingredient(int(sel_ing["id"]))
                        st.warning("Deleted.")
                        st.rerun()
    else:
        st.info("No ingredients yet. Add your first ingredient above.")

# ────────────────────────────────────────────────────────────────────
# PAGE: INVENTORY
# ────────────────────────────────────────────────────────────────────
elif page == "inventory":
    st.markdown('<div class="section-header">📦 Inventory</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Track and adjust your stock levels quickly</div>', unsafe_allow_html=True)

    ings = dm.get_ingredients()
    if ings.empty:
        st.info("No ingredients yet. Add some in Ingredient Costs.")
    else:
        low = ings[ings["stock"] <= ings["min_stock"]]

        if not low.empty:
            st.markdown(f'<div class="alert-low">⚠️ {len(low)} ingredient(s) below minimum threshold!</div>', unsafe_allow_html=True)

        # Quick adjust form
        st.markdown("#### ⚡ Quick Stock Adjustment")
        with st.form("quick_adj"):
            c1, c2, c3 = st.columns(3)
            with c1:
                sel = st.selectbox("Ingredient", ings["name"].tolist())
            with c2:
                amt = st.number_input("Amount", min_value=0.0, step=1.0)
            with c3:
                action = st.selectbox("Action", ["Add Stock", "Use / Deduct"])
            if st.form_submit_button("✅ Apply", use_container_width=True):
                ing_row = ings[ings["name"] == sel].iloc[0]
                delta = amt if action == "Add Stock" else -amt
                new_stock = max(0, float(ing_row["stock"]) + delta)
                dm.update_ingredient(int(ing_row["id"]), ing_row["name"], ing_row["unit"], float(ing_row["cost_per_unit"]), new_stock, float(ing_row["min_stock"]))
                st.success(f"✅ {sel} stock updated to {new_stock:.0f}{ing_row['unit']}")
                st.rerun()

        st.markdown("---")
        st.markdown("#### 📋 All Inventory")

        inv_display = ings[["name", "unit", "stock", "min_stock"]].copy()
        inv_display["Status"] = ings.apply(lambda r: "⚠️ LOW" if r["stock"] <= r["min_stock"] else "✅ OK", axis=1)
        inv_display["Stock Level"] = ings.apply(
            lambda r: f"{r['stock']:.0f} {r['unit']} (min: {r['min_stock']:.0f})", axis=1
        )
        inv_display = inv_display.rename(columns={"name": "Ingredient", "unit": "Unit", "stock": "Current Stock", "min_stock": "Min Stock"})
        st.dataframe(inv_display[["Ingredient", "Unit", "Current Stock", "Min Stock", "Status"]], use_container_width=True, hide_index=True)

        # ── Shopping list ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 🛒 Shopping List")
        low_items = ings[ings["stock"] < ings["min_stock"]]
        if low_items.empty:
            st.markdown('<div class="alert-ok">✅ All ingredients are sufficiently stocked — nothing to buy right now.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-low">⚠️ {len(low_items)} ingredient(s) need restocking.</div>', unsafe_allow_html=True)
            for _, item in low_items.iterrows():
                needed = item["min_stock"] - item["stock"]
                st.markdown(
                    f"<div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; "
                    f"padding:10px 16px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;'>"
                    f"<span style='font-weight:700; color:#112337;'>{item['name']}</span>"
                    f"<span style='color:#686e77; font-size:13px;'>Have: <strong>{item['stock']:.0f} {item['unit']}</strong> &nbsp;·&nbsp; "
                    f"Min: <strong>{item['min_stock']:.0f} {item['unit']}</strong></span>"
                    f"<span style='background:#e0555512; color:#e05555; border:1px solid #e0555530; "
                    f"border-radius:20px; font-size:12px; font-weight:700; padding:4px 12px;'>"
                    f"Buy ≥ {needed:.0f} {item['unit']}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

# ────────────────────────────────────────────────────────────────────
# PAGE: RECIPES
# ────────────────────────────────────────────────────────────────────
elif page == "recipes":
    st.markdown('<div class="section-header">🧾 Recipe Templates</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Build once, reuse forever. All costs update automatically.</div>', unsafe_allow_html=True)

    ings = dm.get_ingredients()
    recipes = dm.get_recipes()

    # ── Add Recipe ────────────────────────────────────────────────
    with st.expander("➕ Create New Recipe", expanded=False):
        if ings.empty:
            st.warning("Add ingredients first before creating recipes.")
        else:
            with st.form("new_recipe", clear_on_submit=False):
                c1, c2 = st.columns(2)
                with c1:
                    r_name = st.text_input("Product Name", placeholder="e.g. Chocolate Chip Cookies")
                    portion = st.number_input("Portion Size (g per piece)", min_value=1.0, value=40.0)
                    waste = st.number_input("Waste Buffer (%)", min_value=0.0, max_value=30.0, value=5.0)
                with c2:
                    default_price = st.number_input("Default Selling Price (₱/pc)", min_value=0.0, value=35.0)
                    target_margin = st.number_input("Target Profit Margin (%)", min_value=0.0, max_value=100.0, value=60.0)
                    pack_sizes_input = st.text_input("Pack Sizes (comma-separated)", value="1,5,10",
                        help="e.g. '1,5,10' → sell per piece, box of 5, or box of 10")

                st.markdown("**Ingredients:**")
                num_ings = st.number_input("Number of ingredients", min_value=1, max_value=20, value=3, step=1)

                ing_selections = []
                ing_qtys = []
                for i in range(int(num_ings)):
                    ca, cb = st.columns([3, 1])
                    with ca:
                        sel_ing = st.selectbox(f"Ingredient {i+1}", ings["name"].tolist(), key=f"ri_{i}")
                    with cb:
                        unit_label = ings[ings["name"] == sel_ing]["unit"].values[0] if not ings[ings["name"] == sel_ing].empty else "g"
                        sel_qty = st.number_input(f"Qty ({unit_label})", min_value=0.0, step=1.0, key=f"rq_{i}")
                    ing_selections.append(sel_ing)
                    ing_qtys.append(sel_qty)

                if st.form_submit_button("💾 Save Recipe", use_container_width=True):
                    if r_name:
                        # Calculate dough weight (sum of g ingredients)
                        dw = 0.0
                        for sn, sq in zip(ing_selections, ing_qtys):
                            row = ings[ings["name"] == sn]
                            if not row.empty and row.iloc[0]["unit"] == "g":
                                dw += sq
                        recipe_ings = []
                        for sn, sq in zip(ing_selections, ing_qtys):
                            row = ings[ings["name"] == sn]
                            if not row.empty:
                                recipe_ings.append({"ingredient_id": int(row.iloc[0]["id"]), "qty": sq})
                        dm.add_recipe(r_name, portion, waste, default_price, target_margin, dw, recipe_ings, pack_sizes=pack_sizes_input)
                        st.success(f"✅ {r_name} saved!")
                        st.rerun()

    # ── Recipe cards ──────────────────────────────────────────────
    recipes = dm.get_recipes()
    if not recipes.empty:
        for _, r in recipes.iterrows():
            batch_cost = calc_recipe_cost(r["id"])
            dw = float(r.get("dough_weight") or 0)
            pieces = calc_yield(dw, float(r["portion_size"]), float(r["waste_pct"]))
            cost_per_pc = batch_cost / pieces if pieces > 0 else 0
            sell_price = float(r["default_price"])
            margin = ((sell_price - cost_per_pc) / sell_price * 100) if sell_price > 0 else 0
            suggested = cost_per_pc / (1 - float(r["target_margin_pct"]) / 100) if float(r["target_margin_pct"]) < 100 else 0

            with st.expander(f"🧁 {r['name']}  |  Margin: {margin:.0f}%  |  Cost/pc: {peso(cost_per_pc)}  |  Suggested: {peso(suggested)}"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Batch Cost", peso(batch_cost))
                c2.metric("Yield", f"{pieces} pcs")
                c3.metric("Cost/Piece", peso(cost_per_pc))
                c4.metric(f"Suggested Price ({r['target_margin_pct']:.0f}%)", peso(suggested))

                # Ingredients table
                items = dm.get_recipe_items(r["id"])
                if not items.empty:
                    items_display = []
                    for _, item in items.iterrows():
                        ing = ings[ings["id"] == item["ingredient_id"]]
                        if not ing.empty:
                            ing = ing.iloc[0]
                            line_cost = float(ing["cost_per_unit"]) * float(item["qty"])
                            items_display.append({
                                "Ingredient": ing["name"],
                                "Qty": f"{item['qty']:.1f} {ing['unit']}",
                                "Cost": peso(line_cost)
                            })
                    if items_display:
                        st.dataframe(pd.DataFrame(items_display), hide_index=True, use_container_width=True)

                # Action buttons
                cd, cx = st.columns(2)
                with cd:
                    if st.button(f"📋 Duplicate", key=f"dup_{r['id']}"):
                        items = dm.get_recipe_items(r["id"])
                        ing_list = [{"ingredient_id": int(i["ingredient_id"]), "qty": float(i["qty"])} for _, i in items.iterrows()]
                        dm.add_recipe(r["name"] + " (Copy)", float(r["portion_size"]), float(r["waste_pct"]), float(r["default_price"]), float(r["target_margin_pct"]), float(r.get("dough_weight") or 0), ing_list, pack_sizes=str(r.get("pack_sizes") or "1,5,10"))
                        st.success("Duplicated!")
                        st.rerun()
                with cx:
                    if st.button(f"🗑️ Delete", key=f"del_{r['id']}"):
                        dm.delete_recipe(int(r["id"]))
                        st.warning("Recipe deleted.")
                        st.rerun()

                # Edit form
                with st.expander("✏️ Edit Recipe", expanded=False):
                    current_items = dm.get_recipe_items(r["id"])
                    ing_name_list = ings["name"].tolist()

                    # Ingredient count lives OUTSIDE the form so changing it rerenders rows
                    n_key = f"edit_n_{r['id']}"
                    if n_key not in st.session_state:
                        st.session_state[n_key] = max(1, len(current_items))
                    num_edit_ings = st.number_input(
                        "Number of ingredients", min_value=1, max_value=20,
                        step=1, key=n_key
                    )

                    with st.form(f"edit_recipe_{r['id']}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_name = st.text_input("Product Name", value=r["name"], key=f"en_{r['id']}")
                            e_portion = st.number_input("Portion Size (g/piece)", min_value=1.0, value=float(r["portion_size"]), key=f"ep_{r['id']}")
                            e_waste = st.number_input("Waste Buffer (%)", min_value=0.0, max_value=30.0, value=float(r["waste_pct"]), key=f"ew_{r['id']}")
                        with ec2:
                            e_price = st.number_input("Default Selling Price (₱/pc)", min_value=0.0, value=float(r["default_price"]), key=f"epr_{r['id']}")
                            e_margin = st.number_input("Target Profit Margin (%)", min_value=0.0, max_value=100.0, value=float(r["target_margin_pct"]), key=f"em_{r['id']}")
                            e_pack_sizes = st.text_input("Pack Sizes", value=str(r.get("pack_sizes") or "1,5,10"),
                                help="e.g. '1,5,10' → per piece, box of 5, box of 10", key=f"eps_{r['id']}")

                        st.markdown("**Ingredients:**")
                        edit_selections = []
                        edit_qtys = []
                        for i in range(int(num_edit_ings)):
                            # Pre-fill from existing items; blank defaults for new rows
                            if i < len(current_items):
                                item = current_items.iloc[i]
                                ing_match = ings[ings["id"] == item["ingredient_id"]]
                                default_name = ing_match.iloc[0]["name"] if not ing_match.empty else ing_name_list[0]
                                default_qty = float(item["qty"])
                            else:
                                default_name = ing_name_list[0]
                                default_qty = 0.0
                            default_idx = ing_name_list.index(default_name) if default_name in ing_name_list else 0
                            ca, cb = st.columns([3, 1])
                            with ca:
                                sel = st.selectbox(f"Ingredient {i+1}", ing_name_list, index=default_idx, key=f"ei_{r['id']}_{i}")
                            with cb:
                                unit_label = ings[ings["name"] == sel]["unit"].values[0] if not ings[ings["name"] == sel].empty else "g"
                                qty_val = st.number_input(f"Qty ({unit_label})", min_value=0.0, value=default_qty, step=1.0, key=f"eq_{r['id']}_{i}")
                            edit_selections.append(sel)
                            edit_qtys.append(qty_val)

                        if st.form_submit_button("💾 Save Changes", use_container_width=True):
                            e_dw = 0.0
                            recipe_ings = []
                            for sn, sq in zip(edit_selections, edit_qtys):
                                row = ings[ings["name"] == sn]
                                if not row.empty:
                                    if row.iloc[0]["unit"] == "g":
                                        e_dw += sq
                                    recipe_ings.append({"ingredient_id": int(row.iloc[0]["id"]), "qty": sq})
                            dm.update_recipe(int(r["id"]), e_name, e_portion, e_waste, e_price, e_margin, e_dw, recipe_ings, pack_sizes=e_pack_sizes)
                            # Delete key so it reinitializes from saved item count on next rerun
                            if n_key in st.session_state:
                                del st.session_state[n_key]
                            st.success("✅ Recipe updated!")
                            st.rerun()
    else:
        st.info("No recipes yet. Create your first recipe above.")

# ────────────────────────────────────────────────────────────────────
# PAGE: CALCULATOR
# ────────────────────────────────────────────────────────────────────
elif page == "calculator":
    st.markdown('<div class="section-header">⚙️ Yield & Cost Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All values update live — pick a margin tier or set your own price</div>', unsafe_allow_html=True)

    recipes = dm.get_recipes()
    ings = dm.get_ingredients()

    if recipes.empty:
        st.info("No recipes yet. Add some in Recipe Templates.")
    else:
        # ── Recipe selection ──────────────────────────────────────
        sel_recipe_name = st.selectbox("Select Recipe", recipes["name"].tolist())
        sel_r = recipes[recipes["name"] == sel_recipe_name].iloc[0]

        # Reset all calc state when recipe changes
        if st.session_state.get("calc_last_recipe") != int(sel_r["id"]):
            st.session_state.calc_last_recipe = int(sel_r["id"])
            st.session_state.pop("calc_sell_pc", None)
            st.session_state.pop("calc_sell_box", None)
            st.session_state.pop("calc_dough_w", None)
            st.session_state.pop("calc_portion", None)
            st.session_state.pop("calc_waste", None)
            st.session_state.pop("calc_pack_sel", None)

        # Apply tier button overrides BEFORE price widgets are rendered
        if "calc_price_override_pc" in st.session_state:
            st.session_state["calc_sell_pc"] = st.session_state.pop("calc_price_override_pc")
        if "calc_price_override_box" in st.session_state:
            st.session_state["calc_sell_box"] = st.session_state.pop("calc_price_override_box")

        # Initialize batch input defaults if not already set
        if "calc_dough_w" not in st.session_state:
            st.session_state["calc_dough_w"] = float(sel_r.get("dough_weight") or 0)
        if "calc_portion" not in st.session_state:
            st.session_state["calc_portion"] = float(sel_r["portion_size"])
        if "calc_waste" not in st.session_state:
            st.session_state["calc_waste"] = int(sel_r["waste_pct"])

        # ── Batch inputs ──────────────────────────────────────────
        batch_cost = calc_recipe_cost(sel_r["id"])
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### Batch Settings")
            dough_weight = st.number_input("Total Dough Weight (g)", min_value=0.0, step=10.0, key="calc_dough_w")
            portion = st.number_input("Portion Size (g/piece)", min_value=1.0, step=5.0, key="calc_portion")
            waste = st.slider("Waste Buffer (%)", 0, 20, key="calc_waste")
            if st.button("💾 Save Batch Settings", use_container_width=True):
                recipe_id = int(sel_r["id"])
                items = dm.get_recipe_items(recipe_id)
                ing_list = [{"ingredient_id": int(r["ingredient_id"]), "qty": float(r["qty"])} for _, r in items.iterrows()]
                dm.update_recipe(
                    recipe_id,
                    str(sel_r["name"]),
                    portion,
                    waste,
                    float(sel_r["default_price"]),
                    float(sel_r["target_margin_pct"]),
                    dough_weight,
                    ing_list,
                )
                st.success("✅ Batch settings saved!")
        with col_b:
            st.markdown("##### Pack / Box Size")
            _ps_raw    = str(sel_r.get("pack_sizes") or "1,5,10")
            _ps_list   = [int(x.strip()) for x in _ps_raw.split(",") if x.strip().isdigit()]
            if not _ps_list:
                _ps_list = [1, 6, 12]
            def _ps_lbl(n): return "Per Piece" if n == 1 else f"Box of {n}"
            _ps_labels = [_ps_lbl(p) for p in _ps_list]
            _ps_sel    = st.selectbox("Pack / Box Size", _ps_labels, key="calc_pack_sel")
            pack_size  = _ps_list[_ps_labels.index(_ps_sel)]
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(32,76,229,0.07);'>
              <div style='color:#686e77; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.8px;'>Batch Cost</div>
              <div style='color:#204ce5; font-size:22px; font-weight:800; margin-top:2px;'>{peso(batch_cost)}</div>
            </div>""", unsafe_allow_html=True)

        # ── Core yield & cost ─────────────────────────────────────
        pieces = calc_yield(dough_weight, portion, waste)
        cost_per_pc = batch_cost / pieces if pieces > 0 else 0
        full_boxes = pieces // pack_size
        leftover_pcs = pieces % pack_size

        # ── Margin Guide ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 🎯 Margin Guide")
        st.markdown('<div class="section-sub">Based on your actual batch cost — click any tier to apply those prices</div>', unsafe_allow_html=True)

        TIERS = [
            ("🔴", "Low",    30, "#e05555", "Pushing it low — only if you need volume"),
            ("🟡", "Fair",   45, "#e8a020", "Decent — covers costs with some room"),
            ("🟢", "Good",   60, "#3aad2e", "Sweet spot — solid profit, recommended"),
            ("⭐", "Best",   70, "#204ce5", "Premium — great if your product stands out"),
        ]

        tier_cols = st.columns(len(TIERS))
        for col, (icon, label, margin, color, tip) in zip(tier_cols, TIERS):
            sug_pc  = cost_per_pc / (1 - margin / 100) if cost_per_pc > 0 else 0.0
            sug_box = sug_pc * pack_size
            with col:
                st.markdown(f"""
                <div style='background:#ffffff; border:2px solid {color}44; border-radius:12px;
                            padding:14px 10px; text-align:center; margin-bottom:6px; box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
                  <div style='font-size:20px;'>{icon}</div>
                  <div style='color:{color}; font-weight:800; font-size:13px;'>{label} · {margin}%</div>
                  <div style='color:#112337; font-weight:700; font-size:17px; margin:6px 0 2px;'>
                    {peso(sug_pc)}<span style='color:#686e77; font-size:11px;'>/pc</span>
                  </div>
                  <div style='color:#686e77; font-size:12px;'>{peso(sug_box)} / box of {pack_size}</div>
                  <div style='color:{color}; font-size:12px; margin-top:6px; line-height:1.4;'>{tip}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Use {label}", key=f"tier_{margin}", use_container_width=True):
                    st.session_state["calc_price_override_pc"]  = round(sug_pc, 2)
                    st.session_state["calc_price_override_box"] = round(sug_box, 2)
                    st.rerun()

        # ── Price inputs ──────────────────────────────────────────
        st.markdown("---")
        if "calc_sell_pc" not in st.session_state:
            st.session_state["calc_sell_pc"] = float(sel_r["default_price"])
        if "calc_sell_box" not in st.session_state:
            st.session_state["calc_sell_box"] = float(sel_r["default_price"]) * pack_size

        p1, p2 = st.columns(2)
        with p1:
            sell_price = st.number_input("Your Selling Price / Piece (₱)", min_value=0.0, step=0.50, key="calc_sell_pc")
        with p2:
            box_price = st.number_input(f"Your Selling Price / Box of {pack_size} (₱)", min_value=0.0, step=1.0, key="calc_sell_box")

        # ── Current margin indicator ──────────────────────────────
        if cost_per_pc > 0:
            cur_margin = (sell_price - cost_per_pc) / sell_price * 100 if sell_price > 0 else 0
            if cur_margin < 20:
                t_label, t_color = "⚠️ Danger Zone — barely covers costs, raise your price", "#e05555"
            elif cur_margin < 35:
                t_label, t_color = "🔴 Low Profit — you're working hard for little return", "#e05555"
            elif cur_margin < 50:
                t_label, t_color = "🟡 Fair — decent, but you can probably do better", "#e8a020"
            elif cur_margin < 65:
                t_label, t_color = "🟢 Good — solid profit margin, keep it here", "#3aad2e"
            else:
                t_label, t_color = "⭐ Best — premium margin, excellent work!", "#204ce5"
            st.markdown(f"""
            <div style='background:{t_color}18; border:1px solid {t_color}55; border-radius:10px;
                        padding:12px 18px; margin:10px 0 4px;'>
              <div style='color:{t_color}; font-weight:800; font-size:14px;'>{t_label}</div>
              <div style='color:#686e77; font-size:12px; margin-top:4px;'>
                Margin: <strong style='color:#112337;'>{cur_margin:.1f}%</strong>
                &nbsp;·&nbsp; Cost/pc: <strong style='color:#112337;'>{peso(cost_per_pc)}</strong>
                &nbsp;·&nbsp; Profit/pc: <strong style='color:#112337;'>{peso(sell_price - cost_per_pc)}</strong>
                &nbsp;·&nbsp; Profit/box: <strong style='color:#112337;'>{peso(box_price - cost_per_pc * pack_size)}</strong>
              </div>
            </div>""", unsafe_allow_html=True)

        # ── Results ───────────────────────────────────────────────
        st.markdown("---")
        profit_per_pc  = sell_price - cost_per_pc
        margin_pct     = (profit_per_pc / sell_price * 100) if sell_price > 0 else 0
        cost_per_box   = cost_per_pc * pack_size
        profit_per_box = box_price - cost_per_box
        margin_box     = (profit_per_box / box_price * 100) if box_price > 0 else 0
        total_rev_pcs  = sell_price * pieces
        total_rev_box  = box_price * full_boxes + sell_price * leftover_pcs
        total_cost_val = cost_per_pc * pieces
        total_prof_pcs = total_rev_pcs - total_cost_val
        total_prof_box = total_rev_box - total_cost_val

        def result_row(label, value, color="white"):
            return (f"<div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; padding:11px 16px; margin-bottom:7px;"
                    f"display:flex; justify-content:space-between; align-items:center;'>"
                    f"<span style='color:#686e77; font-size:13px;'>{label}</span>"
                    f"<span class='{color}' style='font-weight:800; font-size:15px;'>{value}</span></div>")

        r_left, r_right = st.columns(2)
        with r_left:
            st.markdown("#### 🍪 Per Piece")
            st.markdown(
                result_row("Batch Cost", peso(batch_cost)) +
                result_row("Pieces Yielded", f"{pieces} pcs", "teal") +
                result_row("Cost per Piece", peso(cost_per_pc)) +
                result_row("Sell Price / Piece", peso(sell_price), "gold") +
                result_row("Profit / Piece", peso(profit_per_pc), "green" if profit_per_pc >= 0 else "red") +
                result_row("Margin", f"{margin_pct:.1f}%", "green" if margin_pct >= 50 else ("gold" if margin_pct >= 30 else "red")) +
                result_row("Total Revenue (all pcs)", peso(total_rev_pcs), "gold") +
                result_row("Total Profit (all pcs)", peso(total_prof_pcs), "green" if total_prof_pcs >= 0 else "red"),
                unsafe_allow_html=True)

        with r_right:
            st.markdown(f"#### 📦 Per Box ({pack_size} pcs)")
            st.markdown(
                result_row("Full Boxes per Batch", f"{full_boxes} boxes", "teal") +
                result_row("Leftover Pieces", f"{leftover_pcs} pcs") +
                result_row("Cost per Box", peso(cost_per_box)) +
                result_row("Sell Price / Box", peso(box_price), "gold") +
                result_row("Profit / Box", peso(profit_per_box), "green" if profit_per_box >= 0 else "red") +
                result_row("Margin per Box", f"{margin_box:.1f}%", "green" if margin_box >= 50 else ("gold" if margin_box >= 30 else "red")) +
                result_row("Total Revenue (boxes + loose)", peso(total_rev_box), "gold") +
                result_row("Total Profit (boxes + loose)", peso(total_prof_box), "green" if total_prof_box >= 0 else "red"),
                unsafe_allow_html=True)

        # ── Save to Recipe ────────────────────────────────────────
        st.markdown("---")
        if st.button("💾 Save These Values to Recipe", use_container_width=True):
            saved_margin = (sell_price - cost_per_pc) / sell_price * 100 if sell_price > 0 else 0
            dm.update_recipe(
                int(sel_r["id"]), sel_r["name"], portion, waste, sell_price,
                saved_margin, dough_weight,
                [{"ingredient_id": int(i["ingredient_id"]), "qty": float(i["qty"])}
                 for _, i in dm.get_recipe_items(sel_r["id"]).iterrows()]
            )
            st.success(f"✅ '{sel_r['name']}' defaults updated!")

        # ── Ingredient breakdown ──────────────────────────────────
        st.markdown("#### 📋 Ingredient Cost Breakdown")
        items = dm.get_recipe_items(sel_r["id"])
        if not items.empty:
            breakdown = []
            for _, item in items.iterrows():
                ing = ings[ings["id"] == item["ingredient_id"]]
                if not ing.empty:
                    ing = ing.iloc[0]
                    line_cost = float(ing["cost_per_unit"]) * float(item["qty"])
                    pct_of_batch = (line_cost / batch_cost * 100) if batch_cost > 0 else 0
                    breakdown.append({
                        "Ingredient": ing["name"],
                        "Qty": f"{item['qty']:.1f} {ing['unit']}",
                        "Unit Cost": f"₱{ing['cost_per_unit']:.4f}",
                        "Line Cost": peso(line_cost),
                        "% of Batch": f"{pct_of_batch:.1f}%"
                    })
            st.dataframe(pd.DataFrame(breakdown), hide_index=True, use_container_width=True)

# ────────────────────────────────────────────────────────────────────
# PAGE: SALES
# ────────────────────────────────────────────────────────────────────
elif page == "sales":
    st.markdown('<div class="section-header">📈 Sales Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Record every sale and watch your profit grow</div>', unsafe_allow_html=True)

    recipes = dm.get_recipes()
    ings = dm.get_ingredients()
    sales = dm.get_sales()

    # ── KPIs ──────────────────────────────────────────────────────
    total_revenue = 0.0
    total_cost_all = 0.0
    _all_items_s = dm.get_recipe_items()
    _cost_cache_s = {}
    if not sales.empty and not recipes.empty:
        for _, s in sales.iterrows():
            r = recipes[recipes["id"] == s["recipe_id"]]
            if r.empty:
                continue
            r = r.iloc[0]
            rid = r["id"]
            if rid not in _cost_cache_s:
                _ri = _all_items_s[_all_items_s["recipe_id"] == rid]
                _cost_cache_s[rid] = calc_recipe_cost(rid, _items_cache=_ri, _ings_cache=ings)
            bc = _cost_cache_s[rid]
            pcs = calc_yield(float(r.get("dough_weight") or 0), float(r["portion_size"]), float(r["waste_pct"]))
            cpc = bc / pcs if pcs > 0 else 0
            total_revenue += float(s["qty"]) * float(s["price_per_pc"])
            total_cost_all += cpc * float(s["qty"])

    total_profit = total_revenue - total_cost_all
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Revenue</div><div class="metric-value gold">{peso(total_revenue)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Cost</div><div class="metric-value white">{peso(total_cost_all)}</div></div>', unsafe_allow_html=True)
    with c3:
        profit_color = "green" if total_profit >= 0 else "red"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Profit</div><div class="metric-value {profit_color}">{peso(total_profit)}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Sales Records</div><div class="metric-value teal">{len(sales)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Record sale ───────────────────────────────────────────────
    if recipes.empty:
        st.warning("Add recipes first before recording sales.")
    else:
        st.markdown("#### ➕ Record a Sale")

        # Product & sell mode outside form so labels/defaults react to changes
        pre1, pre2 = st.columns(2)
        with pre1:
            sel_r_name = st.selectbox("Product", recipes["name"].tolist(), key="sale_product")
            sel_r = recipes[recipes["name"] == sel_r_name].iloc[0]
        with pre2:
            _r_ps_raw    = str(sel_r.get("pack_sizes") or "1,5,10")
            _r_ps_list   = [int(x.strip()) for x in _r_ps_raw.split(",") if x.strip().isdigit()]
            if not _r_ps_list:
                _r_ps_list = [1, 6, 12]
            def _sale_lbl(n): return "Per Piece" if n == 1 else f"Box of {n} pcs"
            _sale_labels = [_sale_lbl(p) for p in _r_ps_list]
            sell_mode    = st.selectbox("Sell as", _sale_labels, key="sale_mode")
            pack         = _r_ps_list[_sale_labels.index(sell_mode)]

        with st.form("add_sale", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                qty_label = "Quantity (pieces)" if pack == 1 else f"Quantity (boxes of {pack})"
                qty_input = st.number_input(qty_label, min_value=1, step=1, value=1)
                customer_input = st.text_input("Sold To", placeholder="e.g. Tita Cora, Walk-in, Online Order")
            with c2:
                price_label = "Price per Piece (₱)" if pack == 1 else f"Price per Box of {pack} (₱)"
                default_price = round(float(sel_r["default_price"]) * pack, 2)
                price_input = st.number_input(price_label, min_value=0.0, value=default_price, step=1.0)
                sale_date = st.date_input("Date", value=date.today())

            deduct = st.checkbox("Auto-deduct ingredients from inventory", value=False)

            if st.form_submit_button("✅ Record Sale", use_container_width=True):
                total_pieces = qty_input * pack
                price_per_pc = price_input / pack if pack > 1 else float(price_input)
                dm.add_sale(int(sel_r["id"]), total_pieces, price_per_pc, str(sale_date), pack, customer=customer_input)
                if deduct:
                    items = dm.get_recipe_items(int(sel_r["id"]))
                    pcs_per_batch = calc_yield(
                        float(sel_r.get("dough_weight") or 0),
                        float(sel_r["portion_size"]),
                        float(sel_r["waste_pct"])
                    )
                    for _, item in items.iterrows():
                        ing = ings[ings["id"] == item["ingredient_id"]]
                        if not ing.empty:
                            ing_row = ing.iloc[0]
                            deduct_qty = (float(item["qty"]) / pcs_per_batch * total_pieces) if pcs_per_batch > 0 else 0
                            new_stock = max(0, float(ing_row["stock"]) - deduct_qty)
                            dm.update_ingredient(int(ing_row["id"]), ing_row["name"], ing_row["unit"], float(ing_row["cost_per_unit"]), new_stock, float(ing_row["min_stock"]))
                total_rev = total_pieces * price_per_pc
                st.success(f"✅ Sale recorded! {total_pieces} pcs — Revenue: {peso(total_rev)}")
                st.rerun()

        # ── Sales table ───────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📋 Sales History")
        if not sales.empty and not recipes.empty:
            # Date range filter — work on a copy so KPI data above is unaffected
            sales_dated = sales.copy()
            sales_dated["date"] = pd.to_datetime(sales_dated["date"]).dt.date
            min_date = sales_dated["date"].min()
            max_date = sales["date"].max()
            fc1, fc2, fc3 = st.columns([2, 2, 3])
            with fc1:
                filter_from = st.date_input("From", value=min_date, key="sale_from")
            with fc2:
                filter_to = st.date_input("To", value=date.today(), key="sale_to")
            with fc3:
                st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)

            sales_view = sales_dated[(sales_dated["date"] >= filter_from) & (sales_dated["date"] <= filter_to)]

            rows = []
            for _, s in sales_view.sort_values("date", ascending=False).iterrows():
                r = recipes[recipes["id"] == s["recipe_id"]]
                if r.empty:
                    continue
                r = r.iloc[0]
                rid = r["id"]
                if rid not in _cost_cache_s:
                    _ri = _all_items_s[_all_items_s["recipe_id"] == rid]
                    _cost_cache_s[rid] = calc_recipe_cost(rid, _items_cache=_ri, _ings_cache=ings)
                bc = _cost_cache_s[rid]
                pcs = calc_yield(float(r.get("dough_weight") or 0), float(r["portion_size"]), float(r["waste_pct"]))
                cpc = bc / pcs if pcs > 0 else 0
                rev = float(s["qty"]) * float(s["price_per_pc"])
                cost = cpc * float(s["qty"])
                profit = rev - cost
                ps = int(s.get("pack_size", 1))
                total_qty = int(s["qty"])
                if ps > 1:
                    boxes = total_qty // ps
                    loose = total_qty % ps
                    qty_str = f"{total_qty} pcs ({boxes} box{'es' if boxes != 1 else ''} of {ps}" + (f" + {loose} loose" if loose else "") + ")"
                else:
                    qty_str = f"{total_qty} pcs"
                rows.append({
                    "Date": str(s["date"]), "Customer": str(s.get("customer") or "—"),
                    "Product": r["name"], "Qty": qty_str,
                    "Price/pc": peso(s["price_per_pc"]), "Revenue": peso(rev),
                    "Cost": peso(cost), "Profit": peso(profit),
                    "_id": int(s["id"]), "_rev": rev, "_cost": cost, "_profit": profit,
                    "_qty": total_qty, "_date": s["date"],
                })

            if not rows:
                st.info("No sales records in this date range.")
            else:
                tab_rec, tab_wk, tab_mo = st.tabs(["📋 All Records", "📅 Weekly", "📅 Monthly"])

                with tab_rec:
                    sales_df = pd.DataFrame(rows)
                    display_cols = ["Date", "Customer", "Product", "Qty", "Price/pc", "Revenue", "Cost", "Profit"]
                    st.dataframe(sales_df[display_cols], use_container_width=True, hide_index=True)

                    csv_data = sales_df[display_cols].to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="⬇️ Download as CSV",
                        data=csv_data,
                        file_name=f"sales_{filter_from}_to_{filter_to}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

                    st.markdown("##### 🗑️ Delete a Record")
                    for row in rows:
                        profit_color = "#3aad2e" if row["_profit"] >= 0 else "#e05555"
                        col_info, col_del = st.columns([6, 1])
                        with col_info:
                            _cust_tag = f"&nbsp;&nbsp;<span style='color:#686e77; font-size:12px;'>· {row['Customer']}</span>" if row['Customer'] != '—' else ""
                            st.markdown(
                                f"<div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; padding:8px 14px; margin-bottom:4px;'>"
                                f"<span style='color:#686e77; font-size:12px;'>{row['Date']}</span>&nbsp;&nbsp;"
                                f"<strong style='color:#112337;'>{row['Product']}</strong>&nbsp;&nbsp;"
                                f"<span style='color:#686e77;'>{row['Qty']}</span>&nbsp;&nbsp;"
                                f"<span style='color:#204ce5;'>{row['Revenue']}</span>&nbsp;&nbsp;"
                                f"<span style='color:{profit_color};'>Profit: {row['Profit']}</span>"
                                f"{_cust_tag}</div>",
                                unsafe_allow_html=True
                            )
                        with col_del:
                            if st.button("🗑️", key=f"del_sale_{row['_id']}", help="Delete this record"):
                                st.session_state["confirm_delete_sale"] = row["_id"]
                                st.rerun()
                        if st.session_state.get("confirm_delete_sale") == row["_id"]:
                            cc1, cc2, cc3 = st.columns([4, 1, 1])
                            with cc1:
                                st.markdown("<span style='color:#e05555; font-size:13px;'>⚠️ Delete this record? This cannot be undone.</span>", unsafe_allow_html=True)
                            with cc2:
                                if st.button("Yes, delete", key=f"yes_del_{row['_id']}", type="primary"):
                                    dm.delete_sale(row["_id"])
                                    st.session_state.pop("confirm_delete_sale", None)
                                    st.rerun()
                            with cc3:
                                if st.button("Cancel", key=f"cancel_del_{row['_id']}"):
                                    st.session_state.pop("confirm_delete_sale", None)
                                    st.rerun()

                def summary_table(grouped_rows, period_label):
                    summary = {}
                    for row in grouped_rows:
                        key = row[period_label]
                        if key not in summary:
                            summary[key] = {"Revenue": 0, "Cost": 0, "Profit": 0, "Sales": 0}
                        summary[key]["Revenue"] += row["_rev"]
                        summary[key]["Cost"]    += row["_cost"]
                        summary[key]["Profit"]  += row["_profit"]
                        summary[key]["Sales"]   += 1
                    rows_out = []
                    for k in sorted(summary.keys(), reverse=True):
                        v = summary[k]
                        margin = (v["Profit"] / v["Revenue"] * 100) if v["Revenue"] > 0 else 0
                        rows_out.append({
                            period_label: k,
                            "Revenue": peso(v["Revenue"]),
                            "Cost": peso(v["Cost"]),
                            "Profit": peso(v["Profit"]),
                            "Margin": f"{margin:.1f}%",
                            "# Sales": v["Sales"],
                        })
                    return rows_out

                with tab_wk:
                    wk_rows = []
                    for row in rows:
                        dt = pd.to_datetime(row["_date"])
                        week_start = (dt - pd.Timedelta(days=dt.weekday())).strftime("%Y-%m-%d")
                        wk_rows.append({**row, "Week": f"Week of {week_start}"})
                    wk_summary = summary_table(wk_rows, "Week")
                    if wk_summary:
                        st.dataframe(pd.DataFrame(wk_summary), use_container_width=True, hide_index=True)

                with tab_mo:
                    mo_rows = []
                    for row in rows:
                        dt = pd.to_datetime(row["_date"])
                        mo_rows.append({**row, "Month": dt.strftime("%B %Y")})
                    mo_summary = summary_table(mo_rows, "Month")
                    if mo_summary:
                        st.dataframe(pd.DataFrame(mo_summary), use_container_width=True, hide_index=True)

        else:
            st.info("No sales recorded yet.")

# ────────────────────────────────────────────────────────────────────
# PAGE: EXPENSES
# ────────────────────────────────────────────────────────────────────
elif page == "expenses":
    st.markdown('<div class="section-header">💸 Expenses</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Track overhead costs — packaging, gas, delivery, and more</div>', unsafe_allow_html=True)

    EXPENSE_CATEGORIES = ["Packaging", "Gas / Electricity", "Delivery", "Marketing", "Equipment", "Supplies", "Other"]

    with st.expander("➕ Add Expense", expanded=False):
        with st.form("add_expense", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                exp_desc = st.text_input("Description", placeholder="e.g. Cookie boxes (50 pcs)")
                exp_cat  = st.selectbox("Category", EXPENSE_CATEGORIES)
            with c2:
                exp_amt  = st.number_input("Amount (₱)", min_value=0.0, step=1.0)
                exp_date = st.date_input("Date", value=date.today())
            if st.form_submit_button("💾 Save Expense", use_container_width=True):
                if exp_desc and exp_amt > 0:
                    dm.add_expense(exp_desc, exp_cat, float(exp_amt), str(exp_date))
                    st.success(f"✅ Expense added: {peso(exp_amt)}")
                    st.rerun()
                else:
                    st.error("Please enter a description and an amount greater than 0.")

    expenses = dm.get_expenses()

    if not expenses.empty:
        total_exp = float(expenses["amount"].sum())
        cat_sum   = expenses.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)

        e1, e2 = st.columns(2)
        with e1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Expenses</div><div class="metric-value red">{peso(total_exp)}</div><div class="metric-sub">All time</div></div>', unsafe_allow_html=True)
        with e2:
            top_cat = cat_sum.iloc[0]["category"] if not cat_sum.empty else "—"
            top_amt = cat_sum.iloc[0]["amount"]   if not cat_sum.empty else 0
            st.markdown(f'<div class="metric-card"><div class="metric-label">Biggest Category</div><div class="metric-value white">{top_cat}</div><div class="metric-sub">{peso(top_amt)}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📊 By Category")
        cat_display = cat_sum.copy()
        cat_display["Amount"] = cat_display["amount"].map(lambda x: peso(x))
        cat_display["Share"]  = cat_display["amount"].map(lambda x: f"{x / total_exp * 100:.1f}%" if total_exp > 0 else "0%")
        st.dataframe(cat_display[["category", "Amount", "Share"]].rename(columns={"category": "Category"}),
                     use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("#### 📋 All Expenses")

        exp_dates = pd.to_datetime(expenses["date"]).dt.date
        ef1, ef2 = st.columns(2)
        with ef1:
            efrom = st.date_input("From", value=exp_dates.min(), key="exp_from")
        with ef2:
            eto   = st.date_input("To",   value=date.today(),   key="exp_to")

        exp_view = expenses.copy()
        exp_view["_date"] = pd.to_datetime(exp_view["date"]).dt.date
        exp_view = exp_view[(exp_view["_date"] >= efrom) & (exp_view["_date"] <= eto)]

        if exp_view.empty:
            st.info("No expenses in this date range.")
        else:
            for _, row in exp_view.sort_values("date", ascending=False).iterrows():
                col_info, col_del = st.columns([6, 1])
                with col_info:
                    st.markdown(
                        f"<div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; padding:8px 14px; margin-bottom:4px;'>"
                        f"<span style='color:#686e77; font-size:12px;'>{row['date']}</span>&nbsp;&nbsp;"
                        f"<span style='background:#e0555512; color:#e05555; border:1px solid #e0555530; border-radius:20px; font-size:11px; font-weight:700; padding:2px 8px;'>{row['category']}</span>&nbsp;&nbsp;"
                        f"<strong style='color:#112337;'>{row['description']}</strong>&nbsp;&nbsp;"
                        f"<span style='color:#e05555; font-weight:700;'>{peso(row['amount'])}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col_del:
                    if st.button("🗑️", key=f"del_exp_{int(row['id'])}", help="Delete expense"):
                        st.session_state["confirm_delete_exp"] = int(row["id"])
                        st.rerun()

                if st.session_state.get("confirm_delete_exp") == int(row["id"]):
                    dc1, dc2, dc3 = st.columns([4, 1, 1])
                    with dc1:
                        st.markdown("<span style='color:#e05555; font-size:13px;'>⚠️ Delete this expense? Cannot be undone.</span>", unsafe_allow_html=True)
                    with dc2:
                        if st.button("Yes, delete", key=f"yes_exp_{int(row['id'])}", type="primary"):
                            dm.delete_expense(int(row["id"]))
                            st.session_state.pop("confirm_delete_exp", None)
                            st.rerun()
                    with dc3:
                        if st.button("Cancel", key=f"cancel_exp_{int(row['id'])}"):
                            st.session_state.pop("confirm_delete_exp", None)
                            st.rerun()
    else:
        st.info("No expenses recorded yet. Add your first overhead cost above.")

# ────────────────────────────────────────────────────────────────────
# PAGE: BATCH PLANNER
# ────────────────────────────────────────────────────────────────────
elif page == "planner":
    st.markdown('<div class="section-header">🗓️ Batch Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Plan your bake session — see if your stock can cover the planned batches</div>', unsafe_allow_html=True)

    recipes = dm.get_recipes()
    ings    = dm.get_ingredients()

    if recipes.empty:
        st.info("No recipes yet. Add some in Recipe Templates first.")
    elif ings.empty:
        st.info("No ingredients yet. Add some in Ingredient Costs first.")
    else:
        pc1, pc2 = st.columns(2)
        with pc1:
            sel_name = st.selectbox("Recipe", recipes["name"].tolist())
            sel_r    = recipes[recipes["name"] == sel_name].iloc[0]
        with pc2:
            num_batches = st.number_input("Number of Batches", min_value=1, max_value=50, value=1, step=1)

        items = dm.get_recipe_items(int(sel_r["id"]))

        if items.empty:
            st.warning("This recipe has no ingredients configured yet.")
        else:
            batch_cost       = calc_recipe_cost(int(sel_r["id"]))
            pieces_per_batch = calc_yield(
                float(sel_r.get("dough_weight") or 0),
                float(sel_r["portion_size"]),
                float(sel_r["waste_pct"])
            )
            total_pieces = pieces_per_batch * num_batches
            total_cost   = batch_cost * num_batches
            cost_per_pc  = batch_cost / pieces_per_batch if pieces_per_batch > 0 else 0

            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Total Pieces</div><div class="metric-value teal">{total_pieces} pcs</div><div class="metric-sub">{pieces_per_batch} pcs/batch × {num_batches}</div></div>', unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Total Batch Cost</div><div class="metric-value white">{peso(total_cost)}</div><div class="metric-sub">{peso(batch_cost)} / batch</div></div>', unsafe_allow_html=True)
            with sc3:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Cost per Piece</div><div class="metric-value gold">{peso(cost_per_pc)}</div><div class="metric-sub">Ingredient cost only</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🧂 Ingredient Requirements vs Stock")

            plan_rows  = []
            has_short  = False
            shop_items = []

            for _, item in items.iterrows():
                ing = ings[ings["id"] == item["ingredient_id"]]
                if ing.empty:
                    continue
                ing     = ing.iloc[0]
                needed  = float(item["qty"]) * num_batches
                on_hand = float(ing["stock"])
                short   = max(0.0, needed - on_hand)
                status  = "⚠️ SHORT" if short > 0 else "✅ OK"
                if short > 0:
                    has_short = True
                    shop_items.append({"Ingredient": ing["name"], "Buy": f"{short:.1f} {ing['unit']}"})
                plan_rows.append({
                    "Ingredient":     ing["name"],
                    "Per Batch":      f"{item['qty']:.1f} {ing['unit']}",
                    "Total Needed":   f"{needed:.1f} {ing['unit']}",
                    "On Hand":        f"{on_hand:.1f} {ing['unit']}",
                    "Short By":       f"{short:.1f} {ing['unit']}" if short > 0 else "—",
                    "Status":         status,
                })

            if plan_rows:
                st.dataframe(pd.DataFrame(plan_rows), use_container_width=True, hide_index=True)

            if has_short:
                st.markdown('<div class="alert-low">⚠️ Stock is insufficient for this plan. Shopping list below.</div>', unsafe_allow_html=True)
                st.markdown("#### 🛒 Shopping List for This Plan")
                for s in shop_items:
                    st.markdown(
                        f"<div style='background:#ffffff; border:1px solid #d0d8f0; border-radius:8px; "
                        f"padding:10px 16px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;'>"
                        f"<span style='font-weight:700; color:#112337;'>{s['Ingredient']}</span>"
                        f"<span style='background:#e0555512; color:#e05555; border:1px solid #e0555530; "
                        f"border-radius:20px; font-size:12px; font-weight:700; padding:4px 12px;'>Buy: {s['Buy']}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown('<div class="alert-ok">✅ You have enough stock for all planned batches!</div>', unsafe_allow_html=True)
