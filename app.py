import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# ==========================================
# 1. APP CONFIGURATION & STYLE
# ==========================================
st.set_page_config(
    page_title="ONOE Voter Hub",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF9933; 
        color: white;
        border: none;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #138808;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 2. DATA & TRANSLATIONS (Hardcoded)
# ==========================================

# Mock Data: ECI Statistics for 5 Major States (Representative values)
@st.cache_data
def load_data():
    data = {
        'State': ['Uttar Pradesh', 'Maharashtra', 'West Bengal', 'Bihar', 'Tamil Nadu', 'NCT of Delhi'],
        'Voters (Cr)': [15.3, 9.2, 7.5, 7.6, 6.2, 1.5],
        'Est. Election Cost (₹ Cr)': [4500, 3200, 2800, 2500, 2100, 1500],
        'Turnout (%)': [59.2, 61.0, 82.0, 57.3, 72.0, 58.8],
        'Polling Stations': [163000, 96000, 78000, 72000, 68000, 13600]
    }
    return pd.DataFrame(data)

# Fact Repository for Misinformation Check
facts_db = {
    'cost': {
        'myth': "ONOE is too expensive to implement.",
        'fact': "ECI estimates ONOE saves ~₹4,500 Cr per cycle by avoiding repeated deployment of security and staff.",
        'source': "Law Commission Report, 2018"
    },
    'federalism': {
        'myth': "It destroys the federal structure of states.",
        'fact': "It requires constitutional amendments but does not dissolve state assemblies; they just sync timelines.",
        'source': "NITI Aayog Discussion Paper"
    },
    'evm': {
        'myth': "There aren't enough EVMs for simultaneous polls.",
        'fact': "ECI has projected a requirement of ₹10,000 Cr for new VVPATs/EVMs, which is a one-time capital cost.",
        'source': "ECI Submission to Govt"
    },
    'one nation one election':{
        'myth': "One Nation One Election means elections will happen only once and then stop for years.",
        'fact': "Elections will still be held every five years as per the Constitution; only their timing will be synchronized.",
        'source': "Election Commission of India"
    },
    'Voter Rights':{
        'myth': "Voters will lose their right to vote frequently under One Nation One Election.",
        'fact': "The frequency of voting remains the same; voters will still elect representatives for both Parliament and State Assemblies.",
        'source': "Election Commission of India"     
    },
    'Federal Structure':{
        'myth': "One Nation One Election removes power from state governments.",
        'fact': "State governments retain full constitutional powers; only the election schedule is proposed to be aligned.",
        'source': "NITI Aayog"
    },
    'Constitution':{
        'myth': "One Nation One Election violates the Constitution of India.",
        'fact': "The proposal can only be implemented through constitutional amendments and democratic procedures.",
        'source': "Constitution of India"
    },
    'Election Commission':{
        'myth': "The Election Commission will lose independence if elections are held together.",
        'fact': "The Election Commission will continue to function independently and conduct elections as per constitutional authority.",
        'source': "Election Commission of India"
    },
    'Election Expenditure':{
        'myth': "One Nation One Election benefits only politicians by saving money.",
        'fact': "Reduced election expenditure also saves public resources and administrative effort, benefiting governance and taxpayers.",
        'source': "Law Commission of India"
    },
    'Governance Efficiency':{
        'myth': "Governance quality will decrease due to simultaneous elections.",
        'fact': "Governance may improve because frequent enforcement of the Model Code of Conduct will reduce.",
        'source': "Election Commission of India"
    },
    'Voter Confusion':{
        'myth': "Voters will not understand whom they are voting for if elections are held together.",
        'fact': "Separate ballots, symbols, and EVM units are used, just like current elections, ensuring clarity.",
        'source': "Election Commission of India"
    },
    'Misinformation':{
        'myth': "Messages shared on social media about One Nation One Election are always trustworthy.",
        'fact': "Many viral claims are misleading; official sources and verified government publications should be consulted",
        'source': "Press Information Bureau"
    },
    'Political Neutrality':{
        'myth': "Discussing One Nation One Election means supporting a specific political party.",
        'fact': "One Nation One Election is a policy proposal and can be discussed objectively without political bias.",
        'source': "Civic Education Guidelines, Election Commission of India"
    },
    'Democracy':{
        'myth': "Simultaneous elections weaken democracy.",
        'fact': "Democracy depends on free and fair elections, not on how often they are held. These principles remain unchanged.",
        'source': "Constitution of India"
    }
}

# Translations Dictionary
translations = {
    'English': {
        'title': "One Nation One Election: Voter Hub",
        'subtitle': "Neutral • Educational • Data-Driven",
        'nav_home': "🏠 Home & Explainers",
        'nav_sim': "📊 Impact Simulator",
        'nav_quiz': "🧠 Voter Quiz",
        'nav_myth': "🛡️ Myth Buster",
        'welcome': "Welcome to the ONOE Voter Hub",
        'intro': "A student-led initiative to explain the 'One Nation One Election' proposal using data and facts.",
        'pros': "Potential Benefits",
        'cons': "Potential Challenges",
        'sim_title': "Policy Impact Simulator",
        'sim_desc': "Adjust sliders to see how ONOE could affect costs and voter turnout in your state.",
        'state_sel': "Select State",
        'freq_sel': "Election Frequency (Years)",
        'turnout_sel': "Projected Turnout Change (%)",
        'calc_save': "Calculate Savings",
        'quiz_title': "Test Your Knowledge",
        'check_btn': "Check Fact",
        'source': "Source"
    },
    'Hindi': {
        'title': "एक देश एक चुनाव: वोटर हब",
        'subtitle': "निष्पक्ष • शैक्षिक • डेटा-संचालित",
        'nav_home': "🏠 मुख्य पृष्ठ",
        'nav_sim': "📊 प्रभाव सिम्युलेटर",
        'nav_quiz': "🧠 प्रश्नोत्तरी",
        'nav_myth': "🛡️ मिथक निवारण",
        'welcome': "ONOE वोटर हब में आपका स्वागत है",
        'intro': "डेटा और तथ्यों का उपयोग करके 'एक देश एक चुनाव' प्रस्ताव को समझाने की एक छात्र पहल।",
        'pros': "संभावित लाभ",
        'cons': "संभावित चुनौतियां",
        'sim_title': "नीति प्रभाव सिम्युलेटर",
        'sim_desc': "यह देखने के लिए स्लाइडर्स समायोजित करें कि ONOE आपके राज्य में लागत और मतदान को कैसे प्रभावित कर सकता है।",
        'state_sel': "राज्य चुनें",
        'freq_sel': "चुनाव आवृत्ति (वर्ष)",
        'turnout_sel': "अनुमानित मतदान परिवर्तन (%)",
        'calc_save': "बचत की गणना करें",
        'quiz_title': "अपना ज्ञान परखें",
        'check_btn': "तथ्य जांचें",
        'source': "स्रोत"
    }
}

# ==========================================
# 3. SIDEBAR & NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/240px-Emblem_of_India.svg.png", width=200)
    st.title("Menu / मेन्यू")
    
    # Language Toggle
    lang_choice = st.radio("Language / भाषा", ["English", "Hindi"])
    t = translations[lang_choice]
    
    st.markdown("---")
    page = st.radio("Navigation", [
        t['nav_home'], 
        t['nav_sim'], 
        t['nav_myth'], 
        t['nav_quiz']
    ])
    
    st.info("Developed by Team TECHVISION")
    st.info("Voter Helpline Toll Free Number- 1950")

# Load Data
df = load_data()

# ==========================================
# 4. PAGE: HOME / EXPLAINER
# ==========================================
if page == t['nav_home']:
    st.title(t['title'])
    st.caption(t['subtitle'])
    
    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {t['welcome']}")
        st.write(t['intro'])
        st.markdown("""
        **What is ONOE?**  
        One Nation, One Election (ONOE) is a proposal to synchronize elections for the Lok Sabha (central parliament) and all State Assemblies so that voters cast ballots for both on the same day or within the same schedule once every five years.
        """)
    with col2:
        st.metric(label="Total Voters in India (2024)", value="96.8 Cr", delta="+6% vs 2019")

    st.divider()

    # Pros vs Cons Table
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"✅ {t['pros']}")
        st.success("""
        - **Cost Efficiency:** Massive reduction in recurring poll expenditure.
        - **Governance:** Govt focuses on work rather than constant 'Code of Conduct'.
        - **Voter Fatigue:** Reduces apathy from frequent voting.
        - **Reduced Financial Burden:** Synchronizing elections cuts the massive recurring costs of logistics, security, and administration.
        - **Continuity in Governance:** It limits the disruption of the Model Code of Conduct to once every five years.
        - **Increased Efficiency:** Essential staff like teachers and security forces remain focused on core duties instead of frequent election duty.
        - **Higher Voter Turnout:** Consolidating elections combats voter fatigue and may encourage more citizens to vote.
        - **Focus on Long-term Policy:** Governments can pursue structural reforms rather than short-term populist measures for frequent state polls.
        - **Reduced Social Polarization:** Limiting campaign periods reduces the frequency of divisive communal and caste-based rhetoric.
        - **Curbing Horse-Trading:** Simultaneous polls may stabilize coalitions and reduce unethical legislative trading.
         
        """)
    with c2:
        st.subheader(f"⚠️ {t['cons']}")
        st.error("""
        - **Federalism:** National issues might overshadow local state issues.
        - **Logistics:** Requires 2x EVMs and VVPATs instantly.
        - **Constitutional:** Requires amendments to Article 83, 172, etc.
        - **Threat to Federalism:** National issues may overshadow critical local and regional concerns during voting.
        - **Disadvantage to Regional Parties:** Smaller parties may struggle to compete with the resources and reach of national parties.
        - **Constitutional Challenges:** Implementation requires complex amendments regarding the tenure of houses and President's Rule.
        - **Logistical Nightmares:** Deploying security and EVMs for the entire country simultaneously creates immense operational pressure.
        - **Impact of "Wave" Voting:** Voters may mistakenly cast ballots for the same party at both levels, reducing regional checks and balances.
        - **Handling Hung Assemblies:** Mid-term government collapses create confusion on how to manage the remainder of the term.
        - **Reduced Accountability:** A five-year gap between elections may make representatives less responsive to public grievances.
                            
        """)

# ==========================================
# 5. PAGE: SIMULATOR
# ==========================================
elif page == t['nav_sim']:
    st.title(f"📊 {t['sim_title']}")
    st.write(t['sim_desc'])
    
    col_input, col_viz = st.columns([1, 2])
    
    with col_input:
        st.markdown("### Parameters")
        selected_state = st.selectbox(t['state_sel'], df['State'])
        
        # Scenario Sliders
        current_freq = 5 # Current system (approx every year somewhere)
        target_freq = st.slider(t['freq_sel'], 1, 5, 5, help="1 = Elections every year, 5 = Once in 5 years")
        turnout_impact = st.slider(t['turnout_sel'], -10, 20, 5)
        
        # Get State Data
        state_data = df[df['State'] == selected_state].iloc[0]
        base_cost = state_data['Est. Election Cost (₹ Cr)']
        
        # Calculation Logic
        # If freq increases (slider goes to 1), cost goes up. If freq goes to 5 (ONOE), cost reduces over time.
        # Simple Model: Cost over 5 years
        cost_current_5yr = base_cost * 1.5  # Approx separate elections cost more
        cost_onoe_5yr = base_cost * 1.1     # One time sync cost
        
        savings = cost_current_5yr - cost_onoe_5yr
        
    with col_viz:
        st.markdown(f"### Analysis for **{selected_state}**")
        
        # 1. Cost Comparison Chart
        fig, ax = plt.subplots(figsize=(6, 3))
        categories = ['Current System (5 Yrs)', 'ONOE System (5 Yrs)']
        costs = [cost_current_5yr, cost_onoe_5yr]
        colors = ['#ff9999', '#99ff99']
        
        ax.barh(categories, costs, color=colors)
        ax.set_xlabel('Expenditure (₹ Crores)')
        st.pyplot(fig)
        
        # 2. Metrics
        m1, m2 = st.columns(2)
        m1.metric("Est. Savings (5 Yrs)", f"₹{int(savings)} Cr", delta="Saved")
        m2.metric("Projected Turnout", f"{state_data['Turnout (%)'] + turnout_impact}%", delta=f"{turnout_impact}%")

    # Export Data Button
    st.markdown("### Export Simulation")
    if st.button("Download Report (Excel)"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        st.download_button(label="📥 Download .xlsx", data=processed_data, file_name=f'onoe_sim_{selected_state}.xlsx')

# ==========================================
# 6. PAGE: MYTH BUSTER
# ==========================================
elif page == t['nav_myth']:
    st.title(f"🛡️ {t['nav_myth']}")
    
    # Search Bar
    query = st.text_input("Search keywords (e.g., cost, evm, federal)...", "")
    
    # Myth Cards
    found = False
    for key, data in facts_db.items():
        if query.lower() in key or query.lower() in data['myth'].lower() or query == "":
            found = True
            with st.expander(f"🛑 MYTH: {data['myth']}", expanded=True):
                st.markdown(f"### ✅ FACT: {data['fact']}")
                st.caption(f"{t['source']}: {data['source']}")
    
    if not found:
        st.warning("No matching myths found. Try 'cost' or 'EVM'.")

    # Simple Reporter (No Backend)
    st.divider()
    st.subheader("Report Misinformation")
    uploaded_file = st.file_uploader("Upload screenshot of fake news", type=['png', 'jpg'])
    if uploaded_file:
        st.success("Image uploaded!")

# ==========================================
# 7. PAGE: QUIZ
# ==========================================
elif page == t['nav_quiz']:
    st.title(f"🧠 {t['quiz_title']}")
    st.markdown("Test your knowledge about the **One Nation One Election** proposal.")

    # ------------------------------------------
    # QUIZ DATA REPOSITORY
    # ------------------------------------------
    quiz_data = [
        {
            "question": "1. Who originally proposed the concept of simultaneous elections in India in 1983?",
            "options": ["NITI Aayog", "Election Commission of India", "Supreme Court", "Parliament"],
            "answer": "Election Commission of India",
            "explanation": "The Election Commission of India first proposed the idea in its Annual Report in 1983."
        },
        {
            "question": "2. When were simultaneous elections last held in India?",
            "options": ["1952", "1967", "1977", "2014"],
            "answer": "1967",
            "explanation": "Simultaneous elections were the norm in India until 1967, after which some state assemblies were dissolved prematurely."
        },
        {
            "question": "3. Which High Level Committee was constituted in 2023 to examine 'One Nation, One Election'?",
            "options": ["Ram Nath Kovind Committee", "Verma Committee", "Sarkaria Commission", "Punchhi Commission"],
            "answer": "Ram Nath Kovind Committee",
            "explanation": "A committee led by former President Ram Nath Kovind was set up to explore the feasibility."
        },
        {
            "question": "4. What is a major logistical requirement for holding simultaneous elections?",
            "options": ["Less Security Forces", "More EVMs and VVPATs", "Manual Paper Ballots", "Reducing Polling Stations"],
            "answer": "More EVMs and VVPATs",
            "explanation": "Simultaneous elections would require nearly double the number of EVMs and VVPATs to manage two concurrent polls."
        },
        {
            "question": "5. Which article of the Constitution deals with the duration of the Lok Sabha?",
            "options": ["Article 72", "Article 83", "Article 370", "Article 21"],
            "answer": "Article 83",
            "explanation": "Article 83(2) states that the House of the People (Lok Sabha) shall continue for five years unless dissolved sooner."
        },
        {
            "question": "6. According to the Law Commission (2018), approximately how much could be saved per cycle with ONOE?",
            "options": ["₹500 Cr", "₹4,500 Cr", "₹10,000 Cr", "₹100 Cr"],
            "answer": "₹4,500 Cr",
            "explanation": "The Law Commission estimated savings of roughly ₹4,500 Crores by avoiding separate election cycles."
        },
        {
            "question": "7. What is the primary impact of frequent elections on governance?",
            "options": ["Faster decisions", "Frequent Model Code of Conduct halts", "Better roads", "More holidays"],
            "answer": "Frequent Model Code of Conduct halts",
            "explanation": "Frequent elections lead to the frequent imposition of the Model Code of Conduct, which pauses new development projects."
        },
        {
            "question": "8. Which of the following is a concern regarding Federalism under ONOE?",
            "options": ["States get more power", "National issues might overshadow local issues", "No concern", "Local bodies get abolished"],
            "answer": "National issues might overshadow local issues",
            "explanation": "Critics argue that voters might vote on national issues for state elections if held simultaneously."
        },
        {
            "question": "9. Would implementing ONOE require Constitutional Amendments?",
            "options": ["No", "Yes, multiple articles", "Only if the President says so", "Only for State Assemblies"],
            "answer": "Yes, multiple articles",
            "explanation": "It requires amending Articles like 83, 85, 172, 174, and 356 to synchronize terms."
        },
        {
            "question": "10. Does ONOE imply that elections will only happen once and never again?",
            "options": ["Yes", "No, it means synchronized 5-year cycles", "Maybe", "Only for Lok Sabha"],
            "answer": "No, it means synchronized 5-year cycles",
            "explanation": "It simply aligns the schedules; democratic elections will still occur every 5 years."
        }
    ]

    # ------------------------------------------
    # QUIZ LOGIC & FORM
    # ------------------------------------------
    # Initialize dictionary to store user answers if not exists
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    score = 0
    
    with st.form("quiz_form"):
        for i, q in enumerate(quiz_data):
            st.subheader(q['question'])
            # Helper to get previous selection if available
            default_idx = None
            
            # Display Radio Button
            choice = st.radio(
                f"Select an option:", 
                q['options'], 
                key=f"q_{i}", 
                index=default_idx
            )
            st.session_state.user_answers[i] = choice
            st.markdown("---")
        
        submitted = st.form_submit_button("Submit Quiz")
        
        if submitted:
            st.write("## 📝 Quiz Results")
            for i, q in enumerate(quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                
                # Check Answer
                if user_ans == q['answer']:
                    score += 1
                    st.success(f"**Q{i+1}: Correct!** \n{q['explanation']}")
                else:
                    st.error(f"**Q{i+1}: Incorrect.** \nYour Answer: {user_ans} \nCorrect Answer: **{q['answer']}** \nExplanation: {q['explanation']}")
            
            # Final Score Display
            final_score_pct = (score / len(quiz_data)) * 100
            st.metric(label="Final Score", value=f"{score}/{len(quiz_data)}", delta=f"{final_score_pct}%")
            
            if score >= 7:
                st.balloons()
                st.success("🏆 **Excellent!** You are an ONOE Expert!")
            elif score >= 4:
                st.info("👍 **Good effort!** Review the Myth Buster section to learn more.")
            else:
                st.warning("📚 **Keep learning!** Check the Home page for more info.")


# ==========================================
# FOOTER
# ==========================================
st.markdown("""
    <div style='text-align: center; color: grey; padding-top: 50px;'>
    <p>Sources: ECI Reports, NITI Aayog Papers, Law Commission of India.</p>
    <p><i>Note: This is a simulation tool for educational purposes only.</i></p>
    </div>
    """, unsafe_allow_html=True)


