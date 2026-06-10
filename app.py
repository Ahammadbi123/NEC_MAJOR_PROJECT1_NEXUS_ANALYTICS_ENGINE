import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import numpy as np
import os
from src.genai_utils import get_ai_advice

# --- 1. PREMIUM GLASS UI CONFIG ---
st.set_page_config(page_title="Nexus Analytics Engine Pro", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    .main { background: #0b0e14; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #161b22; min-width: 300px; border-right: 2px solid #38bdf8; }
    .stMetric { background: #1c2128; border-radius: 12px; padding: 20px; border-left: 5px solid #38bdf8; }
    h1, h2, h3 { color: #38bdf8; font-weight: 800; }
    .stButton>button { background: linear-gradient(90deg, #38bdf8, #2563eb); color: white; font-weight: bold; border-radius: 10px; width: 100%; border: none; }
    
    /* Unique Offer Card Style */
    .loyalty-card { 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
        padding: 30px; border-radius: 20px; border: 2px solid #38bdf8; 
        text-align: center; box-shadow: 0 10px 30px rgba(0,212,255,0.2);
    }
    .badge { font-size: 24px; font-weight: bold; color: #00d4ff; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('data/customer_data.csv')

def save_db():
    st.session_state.df.to_csv('data/customer_data.csv', index=False)

# Models
with open('models/kmeans_model.pkl', 'rb') as f: kmeans = pickle.load(f)
with open('models/churn_model.pkl', 'rb') as f: churn_model = pickle.load(f)

# --- 3. SIDEBAR NAVIGATION (1-9 FIXED ORDER) ---
st.sidebar.title("🌐 NEXUS ENGINE")
st.sidebar.markdown("---")
page = st.sidebar.radio("📡 CONTROL CENTER", 
    ["1. Executive Dashboard", 
     "2. Customer Data Management", 
     "3. Churn Analysis Radar", 
     "4. Predictive Hub", 
     "5. Smart Recommendations",
     "6. Behavioral Segmentation",
     "7. Unique Offers & Rewards",
     "8. System Reports (CRUD & Search)",
     "9. AI Strategic Advisor"])
st.sidebar.markdown("---")
st.sidebar.success("v16.0 Ultimate Loyalty Build")

# --- 4. MODULES ---

# --- PAGE 1: DASHBOARD ---
if page == "1. Executive Dashboard":
    st.title("📈 Executive Command Dashboard")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Base", len(st.session_state.df), "+15%")
    m2.metric("Annual Revenue", f"${(st.session_state.df['Annual_Income'].sum()*0.1):,.0f}")
    m3.metric("Retention Index", "8.9/10")
    m4.metric("Market Status", "Bullish")
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.pie(st.session_state.df, names='City', hole=0.5, template="plotly_dark"), use_container_width=True)
    with c2: st.plotly_chart(px.bar(st.session_state.df.groupby('Preferred_Category')['Annual_Income'].sum().reset_index(), x='Preferred_Category', y='Annual_Income', color='Preferred_Category'), use_container_width=True)
    st.table(st.session_state.df.groupby('City')[['Annual_Income', 'Spending_Score']].mean().reset_index())

# --- PAGE 2: CRUD ---
elif page == "2. Customer Data Management":
    st.title("🛠️ Customer Database Control")
    t1, t2, t3 = st.tabs(["➕ Add Entry", "📝 Edit Details", "🗑️ Delete Record"])
    with t1:
        with st.form("add"):
            c1, c2 = st.columns(2)
            nid = c1.number_input("ID", value=int(st.session_state.df['CustomerID'].max()+1))
            ncity = c2.selectbox("City", st.session_state.df['City'].unique())
            ninc = c2.number_input("Income", 30000, 200000, 60000)
            if st.form_submit_button("ADD"):
                new = pd.DataFrame([[nid, 35, 'Male', ncity, ninc, 50, 5, 'Electronics', 3, 0, 0]], columns=st.session_state.df.columns)
                st.session_state.df = pd.concat([st.session_state.df, new], ignore_index=True); save_db(); st.success("Database Updated!")
    st.divider()
    gc1, gc2 = st.columns(2)
    with gc1: st.plotly_chart(px.pie(st.session_state.df, names='Gender'), use_container_width=True)
    with gc2: 
        cnts = st.session_state.df['City'].value_counts().reset_index(); cnts.columns=['City','Count']
        st.plotly_chart(px.bar(cnts, x='City', y='Count', color='City'), use_container_width=True)
    st.dataframe(st.session_state.df, use_container_width=True)

# --- PAGE 3: CHURN ---
elif page == "3. Churn Analysis Radar":
    st.title("🚨 Churn Radar")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.pie(st.session_state.df, names='Churn', hole=0.5, color_discrete_sequence=['cyan', 'red']), use_container_width=True)
    with c2: st.plotly_chart(px.bar(st.session_state.df.groupby('City')['Churn'].mean().reset_index(), x='City', y='Churn', color='Churn'), use_container_width=True)
    st.table(st.session_state.df[st.session_state.df['Churn']==1].head(10))

# --- PAGE 4: PREDICTIVE HUB ---
elif page == "4. Predictive Hub":
    st.title("🔮 Predictive Intelligence")
    cp1, cp2 = st.columns([4,6])
    with cp1:
        a=st.slider("Age",18,80,35); i=st.number_input("Inc",10000,200000,75000); s=st.slider("Score",1,100,50); t=st.slider("Ten",0,15,3)
        if st.button("RUN ML"):
            st.session_state['v16_p'] = churn_model.predict_proba([[a,i,s,t]])[0][1]
    with cp2:
        if 'v16_p' in st.session_state:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=st.session_state['v16_p']*100, title={'text':"Risk %"}, gauge={'bar':{'color':"red"}}))
            st.plotly_chart(fig, use_container_width=True)
    st.divider()
    pg1, pg2 = st.columns(2)
    with pg1: st.plotly_chart(px.pie(st.session_state.df, names='Churn'), use_container_width=True)
    with pg2: st.plotly_chart(px.bar(st.session_state.df.groupby('Churn')['Spending_Score'].mean().reset_index(), x='Churn', y='Spending_Score'), use_container_width=True)
    st.table(st.session_state.df.head(5))

# --- PAGE 5: RECOMMENDATIONS ---
elif page == "5. Smart Recommendations":
    st.title("🎯 Hyper-Personalized targeting")
    sid = st.selectbox("Customer ID", st.session_state.df['CustomerID'].unique())
    user = st.session_state.df[st.session_state.df['CustomerID'] == sid].iloc[0]
    rc1, rc2 = st.columns(2)
    with rc1: st.plotly_chart(go.Figure(go.Scatterpolar(r=[user['Annual_Income']/2000, user['Spending_Score'], user['Tenure']*5], theta=['Inc','Spend','Loyalty'], fill='toself')), use_container_width=True)
    with rc2: st.plotly_chart(px.pie(st.session_state.df[st.session_state.df['Segment']==user['Segment']], names='Preferred_Category'), use_container_width=True)
    st.table(pd.DataFrame({"Rec": ["Diamond Card", "Luxury Travel"], "Confidence": ["98%", "91%"]}))
    st.plotly_chart(px.bar(st.session_state.df.groupby('Preferred_Category')['Spending_Score'].mean().reset_index(), x='Preferred_Category', y='Spending_Score'), use_container_width=True)

# --- PAGE 6: SEGMENTATION ---
elif page == "6. Behavioral Segmentation":
    st.title("🧬 AI Clusters")
    st.plotly_chart(px.scatter_3d(st.session_state.df, x='Annual_Income', y='Spending_Score', z='Age', color='Segment', height=750), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(px.pie(st.session_state.df, names='Segment', hole=0.5), use_container_width=True)
    with c2: st.table(st.session_state.df.groupby('Segment')[['Annual_Income', 'Spending_Score']].mean())
    st.plotly_chart(px.bar(st.session_state.df.groupby('Segment')['Annual_Income'].mean().reset_index(), x='Segment', y='Annual_Income'), use_container_width=True)

# --- PAGE 7: UNIQUE OFFERS & REWARDS (MEGA UNIQUE BUILD) ---
elif page == "7. Unique Offers & Rewards":
    st.title("🎁 AI Loyalty Vault & Rewards")
    
    # 1. Customer Context
    sel_id = st.selectbox("Identify Customer Portfolio", st.session_state.df['CustomerID'].unique())
    user = st.session_state.df[st.session_state.df['CustomerID'] == sel_id].iloc[0]
    seg = user['Segment']
    
    # 2. Dynamic Gamified Card (Unique UI)
    badge = "🏆 PLATINUM ELITE" if seg == 0 else "🥇 GOLD PREFERRED" if seg == 1 else "🥈 SILVER SAVER"
    st.markdown(f"""
        <div class='loyalty-card'>
            <div class='badge'>{badge}</div>
            <p style='color: #94a3b8;'>Customer ID: #{sel_id} | Member Since: {2024 - user['Tenure']}</p>
            <h2 style='color: white;'>Available Credit: ${user['Annual_Income']//12:,}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # 3. Tables + Pie + Bar
    oc1, oc2 = st.columns(2)
    with oc1:
        st.subheader("🎯 Personalized Reward Matrix")
        # UNIQUE TABLE
        rewards = pd.DataFrame({
            "Reward Type": ["Financial Perk", "Lifestyle", "Digital"],
            "Offer Details": ["No-Cost EMI Level 1" if seg==3 else "Unlimited Credit", "Lounge Access", "Premium Subscription"],
            "Activation Code": ["NEXUS_START", "NEXUS_VIP", "NEXUS_PRO"][:3],
            "Match": ["High", "Very High", "Medium"]
        })
        st.table(rewards)
        
    with oc2:
        st.subheader("🔥 Offer Popularity by Segment")
        # UNIQUE PIE
        st.plotly_chart(px.pie(st.session_state.df, names='Segment', hole=0.6, title="Segment Reach"), use_container_width=True)

    st.subheader("📊 Projected Spending Lift with Rewards (Unique Bar)")
    # UNIQUE BAR: Comparing current spend vs projected
    fig_impact = go.Figure(data=[
        go.Bar(name='Current Spend Score', x=['This Customer', 'Segment Avg'], y=[user['Spending_Score'], st.session_state.df[st.session_state.df['Segment']==seg]['Spending_Score'].mean()]),
        go.Bar(name='Projected with Rewards', x=['This Customer', 'Segment Avg'], y=[min(100, user['Spending_Score']+20), min(100, st.session_state.df[st.session_state.df['Segment']==seg]['Spending_Score'].mean()+15)])
    ])
    fig_impact.update_layout(barmode='group', template="plotly_dark")
    st.plotly_chart(fig_impact, use_container_width=True)

    st.subheader("🌍 Regional Reward Effectiveness (Treemap)")
    # UNIQUE TREEMAP
    st.plotly_chart(px.treemap(st.session_state.df, path=['City', 'Preferred_Category'], values='Spending_Score', color='Spending_Score', color_continuous_scale='GnBu'), use_container_width=True)

# --- PAGE 8: REPORTS ---
elif page == "8. System Reports (CRUD & Search)":
    st.title("🗂️ Search & Master Reports")
    q = st.text_input("Global Search (ID, City...):")
    res = st.session_state.df[st.session_state.df['City'].str.contains(q, case=False) | st.session_state.df['CustomerID'].astype(str).str.contains(q)]
    if q:
        sc1, sc2 = st.columns(2)
        with sc1: st.plotly_chart(px.pie(res, names='Gender'), use_container_width=True)
        with sc2: st.table(res.head(5))
    cnts = st.session_state.df['City'].value_counts().reset_index(); cnts.columns=['City','Count']
    st.plotly_chart(px.bar(cnts, x='City', y='Count', color='City'), use_container_width=True)
    st.dataframe(st.session_state.df, use_container_width=True)

# --- PAGE 9: AI STRATEGIES ---
elif page == "9. AI Strategic Advisor":
    st.title("🤖 AI Strategy Advisor")
    user_q = st.text_input("Consult AI Strategist:")
    if st.button("EXECUTE"):
        st.info(get_ai_advice(user_q, f"Rev: {st.session_state.df['Annual_Income'].sum()}"))
    st.table(st.session_state.df.groupby('City')['Annual_Income'].mean().reset_index())
    st.plotly_chart(px.line(st.session_state.df.groupby('Age')['Annual_Income'].mean().reset_index(), x='Age', y='Annual_Income'), use_container_width=True)