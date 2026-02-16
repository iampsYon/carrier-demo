import streamlit as st
import time
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Carrier Partner Portal", page_icon="🛡️", layout="wide")

# --- BRANDING & CSS (The "Skin") ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* FORCE LIGHT MODE OVERRIDES */
    /* This forces the app to look "Light" even if your Mac is in "Dark Mode" */
    
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #EAEAEA !important;
    }
    
    /* Header (Top Bar) Background */
    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0) !important;
    }
    
    /* All Text Colors */
    h1, h2, h3, h4, h5, h6, p, li, span, div, label {
        color: #1A1A1A !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Specific Header Font */
    h1, h2, h3 {
        font-family: 'Merriweather', serif !important;
        color: #002b36 !important;
        font-weight: 700 !important;
    }
    
    /* Input Fields (Text Input, TextArea, NumberInput) - Force Light Background */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #E0E0E0 !important;
    }
    
    /* --- FIX FOR DROPDOWNS (Selectbox) --- */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border-color: #E0E0E0 !important;
    }
    div[data-baseweb="select"] span {
        color: #1A1A1A !important;
    }
    div[data-baseweb="select"] svg {
        fill: #1A1A1A !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }
    li[data-baseweb="option"] {
        color: #1A1A1A !important;
    }

    /* --- FIX FOR CHECKBOXES --- */
    /* Unchecked */
    [data-testid="stCheckbox"] label span[role="checkbox"] {
        background-color: #FFFFFF !important;
        border-color: #31333F !important;
    }
    /* Checked (Using your Teal color #57CFCF) */
    [data-testid="stCheckbox"] label span[role="checkbox"][aria-checked="true"] {
        background-color: #57CFCF !important;
        border-color: #57CFCF !important;
    }

    /* --- FIX FOR RADIO BUTTONS --- */
    /* Unchecked Ring */
    [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        background-color: #FFFFFF !important;
        border-color: #31333F !important;
    }
    /* Checked Circle Background */
    [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
         background-color: #FFFFFF !important;
    }
    
    /* FORCE BUTTON STYLING */
    div.stButton > button {
        background-color: #57CFCF !important; /* Teal */
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1) !important;
    }
    div.stButton > button:hover {
        background-color: #4BBDBD !important;
        color: white !important;
    }
    div.stButton > button:active {
        background-color: #3AA8A8 !important;
    }
    
    /* Secondary/Ghost Buttons (Previous Step) */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #57CFCF !important;
        border: 1px solid #57CFCF !important;
    }

    /* Success/Referral/Decline Box Styling */
    .bind-box {padding:20px; background-color:#e6fffa; border-left: 5px solid #00A6A6; color:#004d40; border-radius: 4px; margin-bottom: 20px;}
    .refer-box {padding:20px; background-color:#fffbea; border-left: 5px solid #d97706; color:#78350f; border-radius: 4px; margin-bottom: 20px;}
    .decline-box {padding:20px; background-color:#fef2f2; border-left: 5px solid #ef4444; color:#991b1b; border-radius: 4px; margin-bottom: 20px;}
    
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {
        'company': 'EverPeak Flower Shop',
        'address': '775 Battery Avenue Southeast, Atlanta, GA',
        'class_code': 'Florist (Retail) - 8017',
        'premium': '$1,250.00'
    }
if 'decline_reason' not in st.session_state:
    st.session_state.decline_reason = ""

# --- HELPER FUNCTIONS ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    st.session_state.step -= 1
    st.rerun()

def reset():
    st.session_state.step = 1
    if 'validation_started' in st.session_state:
        del st.session_state.validation_started
    st.session_state.decline_reason = ""
    st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://via.placeholder.com/50x50.png?text=WC", width=50) 
    st.markdown("### New quote")
    st.caption("EverPeak Flower Shop")
    
    st.markdown("---")
    
    # Navigation Visual
    steps = {
        1: "Start", 
        2: "Account", 
        3: "Guidelines", 
        4: "Eligibility", 
        5: "Operations",
        6: "Industry",
        7: "Basic info", 
        8: "Details", 
        9: "Quote", 
        10: "Quote", 
        11: "Bound", 
        12: "Decline"
    }
    
    max_range = 12 if st.session_state.step < 12 else 6

    for i in range(2, max_range):
        display_label = steps.get(i, '')
        if i == 9 and st.session_state.step == 10: 
            continue 
        if i == 10 and st.session_state.step == 9:
            continue
            
        if st.session_state.step == i:
            st.markdown(f"**🟢 {display_label}**") 
        elif i < st.session_state.step:
            st.markdown(f"✔ {display_label}") 
        else:
            st.markdown(f"⚪ {display_label}") 
            
    st.markdown("---")
    st.markdown("### 🛠️ Demo Controller")
    st.info("Hidden from agent view")
    scenario = st.radio(
        "Select Outcome:",
        ("5a. Clean Bind (STP)", "5b. Data Mismatch (Referral)")
    )
    
    if st.button("Reset Demo", key="reset_btn"):
        reset()

# --- PAGE 1: START ---
if st.session_state.step == 1:
    col1, col2 = st.columns([1, 2])
    st.markdown("# Workers' Compensation")
    st.markdown("### Start a new quote")
    st.write("Fast, automated, and easy.")
    st.write("")
    if st.button("Start New Quote"):
        next_step()

# --- PAGE 2: ACCOUNT (Zip/Class Kickout) ---
elif st.session_state.step == 2:
    st.markdown("# New insured account")
    
    company = st.text_input("Company name", "EverPeak Flower Shop")
    st.session_state.data['company'] = company
    
    st.text_input("DBA or Operating Name")
    st.text_input("Address Line 1", "775 Battery Avenue Southeast", label_visibility="collapsed")
    st.text_input("Address Line 2", placeholder="Address 2", label_visibility="collapsed")
    
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1: st.text_input("City", "Atlanta", label_visibility="collapsed")
    with c2: st.selectbox("State", ["GA", "CA", "TX"], label_visibility="collapsed")
    zip_input = c3.text_input("Zip", "30339", label_visibility="collapsed")
    
    st.text_area("Detailed description of operations", "Flower Shop")
    
    st.markdown("### Description of business")
    class_code = st.selectbox(
        "Choose one",
        [
            "Florist (Retail) - 8017",
            "Restaurant - 9079",
            "Masonry: High Wage - 5027",
            "Plumbing (Residential) - 5183",
            "Computer/Telephone Install/Repair - 5193",
            "Auto Repair Shop - 8380",
            "Roofing (Contractor) - 5551"
        ]
    )
    st.session_state.data['class_code'] = class_code
    
    st.write("")
    if st.button("Next"):
        # 1. Zip Code Check
        zip_kickout = False
        try:
            zip_val = int(zip_input)
            if 90000 <= zip_val <= 91099:
                zip_kickout = True
        except:
            pass 

        # 2. Class Code Check (IMMEDIATE KICKOUT FOR ROOFING ONLY)
        class_kickout = "Roofing" in class_code

        if zip_kickout:
            st.session_state.decline_reason = f"Location (Zip {zip_input}) is within a restricted moratorium zone (LA County)."
            st.session_state.step = 12 # Jump to Decline
            st.rerun()
        elif class_kickout:
            st.session_state.decline_reason = "Class Code 5551 (Roofing) is outside of our current appetite."
            st.session_state.step = 12 # Jump to Decline
            st.rerun()
        else:
            next_step()

# --- PAGE 3: GUIDELINES (UPDATED) ---
elif st.session_state.step == 3:
    if st.button("← Previous step"):
        prev_step()
        
    st.markdown("## California Workers' Compensation Eligibility Attestation")
    st.write("Please review the following eligibility criteria. By proceeding, you attest that the applicant does not engage in any of the prohibited operations or meet the ineligible criteria listed below.")
    
    st.markdown("### Prohibited Operations & Risk Exposures")
    st.write("By checking the box below, you certify that the applicant:")
    
    st.markdown("""
    * **Labor & Staffing:** Does not utilize interchange of labor between separate legal entities and is not involved in staffing, PEO, or labor-hire operations.
    * **High-Risk Specialized Services:** Is not involved in Emergency Services (Ambulance, Fire, Police, Private EMS), Logging, Tree Trimming, Deforestation, or Disaster Cleanup.
    * **Industrial & Heavy Ops:** Has no involvement in Crane Operations (unless 100% subcontracted), Railroad, Coal, Foundry, Mining, or the manufacturing of Oil, Gas, Asbestos, or Chemicals.
    * **Hazardous Materials:** Does not handle firearms, ammunition, fireworks, or explosive materials.
    * **Aviation & Maritime:** Has no aircraft/piloting exposure and does not require Maritime Liability (Jones Act, USL&H, DBA, or FELA).
    * **Transportation & Travel:** Does not provide group transportation (4+ employees in a single vehicle) and has no international travel or foreign coverage requirements.
    * **Special Classes:** Does not request coverage for volunteers.
    * **Height Exposure:** Does not perform any work at heights exceeding 40 feet.
    """)
    
    st.markdown("**Fraud Warning:** TBD")
    st.markdown("**Confirmation**")
    
    agree = st.checkbox("I attest that I have reviewed the applicant’s operations and confirm they do not engage in any of the ineligible activities listed above.")
    
    st.write("")
    if st.button("Next"):
        if agree:
            next_step()
        else:
            st.error("You must attest to the eligibility criteria to proceed.")

# --- PAGE 4: ELIGIBILITY ---
elif st.session_state.step == 4:
    if st.button("← Previous step"):
        prev_step()
    
    st.markdown("# General Eligibility")
    st.write("Please answer the following regarding the applicant's operations:")
    st.write("---")

    st.write("**Does the applicant have any 24-hour operations?** (excluding hotels, motels)")
    q_24hr = st.radio("24hr Ops", ["No", "Yes"], horizontal=True, label_visibility="collapsed", index=0)
    
    st.write("")
    
    st.write("**Does the insured currently have a policy with Benchmark?**")
    q_benchmark = st.radio("Benchmark Policy", ["No", "Yes"], horizontal=True, label_visibility="collapsed", index=0)

    st.write("")
    st.write("")
    if st.button("Next"):
        # KICKOUT LOGIC
        if q_24hr == "Yes":
            st.session_state.decline_reason = "24-hour operations are outside of program appetite."
            st.session_state.step = 12
            st.rerun()
        elif q_benchmark == "Yes":
            st.session_state.decline_reason = "Applicant already has active coverage with Benchmark (Duplicate Submission)."
            st.session_state.step = 12
            st.rerun()
        else:
            next_step()

# --- PAGE 5: CLASS CODE SPECIFIC OPERATIONS ---
elif st.session_state.step == 5:
    if st.button("← Previous step"):
        prev_step()
    
    code = st.session_state.data.get('class_code', '')
    
    # DETERMINE FLAGS
    is_masonry = "5027" in code
    is_tech = "5193" in code
    
    # If no specific class questions, skip to next step
    if not is_masonry and not is_tech:
        next_step()
    
    st.markdown(f"# Class Specific Questions: {code}")
    st.write("---")
    
    kickout = False
    
    # MASONRY (5027)
    if is_masonry:
        m_q1 = st.radio("Does the applicant perform any work on chimneys or flues (rebuilding, repointing, relining, capping, flashing)?", ["No", "Yes"])
        if m_q1 == "Yes": kickout = True

    # TECH (5193)
    elif is_tech:
        t_q1 = st.radio("Does the applicant perform work on power poles, transmission lines, street lights, or high voltage?", ["No", "Yes"])
        if t_q1 == "Yes": kickout = True
        
    st.write("")
    if st.button("Next"):
        if kickout:
            st.session_state.decline_reason = "Selected operations (Chimneys/High Voltage) are prohibited for this class code."
            st.session_state.step = 12
            st.rerun()
        else:
            next_step()

# --- PAGE 6: INDUSTRY GROUP OPERATIONS ---
elif st.session_state.step == 6:
    if st.button("← Previous step"):
        prev_step()
    
    code = st.session_state.data.get('class_code', '')
    
    # DETERMINE INDUSTRY GROUPS
    # Contractor = Masonry, Plumbing, Tech, Roofing
    is_contractor = "5027" in code or "5183" in code or "5193" in code or "5551" in code
    is_auto = "8380" in code
    
    if not is_contractor and not is_auto:
        next_step()
        
    reason = None

    # --- ARTISAN CONTRACTOR GROUP ---
    if is_contractor:
        st.markdown("# Industry Supplement: Artisan Contractors")
        st.write("---")
        
        c_q1 = st.radio("Does the applicant perform any work on rooftops?", ["No", "Yes"])
        st.write("")
        c_q2 = st.number_input("Percentage of labor performed by uninsured subcontractors (%)", 0, 100, 0)
        st.write("")
        c_q3 = st.radio("Does any work take place at heights exceeding 40 feet?", ["No", "Yes"])
        st.write("")
        c_q4 = st.radio("Does any work take place at depths exceeding 15 feet?", ["No", "Yes"])
        st.write("")
        c_q5 = st.radio("Are employees required to use fall protection at heights above 10 feet?", ["Yes", "No"]) # Yes is good
        st.write("")
        c_q6 = st.radio("Does the applicant perform trenching deeper than 8 feet?", ["No", "Yes"])
        st.write("")
        c_q7 = st.radio("Any current or requested OCIP exposure?", ["No", "Yes"])
        st.write("")
        c_q8 = st.radio("Does the applicant perform any demolition or wrecking?", ["No", "Yes"])
        st.write("")
        c_q9 = st.radio("Installation/repair of solar panels on elevated surfaces?", ["No", "Yes"])

        # Kickout Logic
        if c_q1 == "Yes": reason = "Rooftop work is prohibited."
        elif c_q2 > 25: reason = f"Uninsured subcontractor usage ({c_q2}%) exceeds maximum of 25%."
        elif c_q3 == "Yes": reason = "Work at heights > 40ft is prohibited."
        elif c_q4 == "Yes": reason = "Work at depths > 15ft is prohibited."
        elif c_q5 == "No": reason = "Fall protection required for heights > 10ft."
        elif c_q6 == "Yes": reason = "Trenching > 8ft is prohibited."
        elif c_q7 == "Yes": reason = "OCIP exposure is outside of appetite."
        elif c_q8 == "Yes": reason = "Demolition/Wrecking operations are prohibited."
        elif c_q9 == "Yes": reason = "Solar panel installation on rooftops is prohibited."

    # --- AUTOMOTIVE GROUP ---
    elif is_auto:
        st.markdown("# Industry Supplement: Automotive")
        st.write("---")
        a_q1 = st.radio("Is towing performed for any reason other than incidental transport?", ["No", "Yes"])
        st.write("")
        a_q2 = st.radio("Any operations dedicated to motorcycles (repair/sales/storage)?", ["No", "Yes"])
        
        if a_q1 == "Yes": reason = "Non-incidental towing is prohibited."
        elif a_q2 == "Yes": reason = "Motorcycle operations are prohibited."

    st.write("")
    if st.button("Next"):
        if reason:
            st.session_state.decline_reason = reason
            st.session_state.step = 12
            st.rerun()
        else:
            next_step()

# --- PAGE 7: BASIC INFO PART A ---
elif st.session_state.step == 7:
    if st.button("← Previous step"):
        prev_step()

    st.markdown("# Basic info (1/2)")
    
    st.text_input("Effective Date", "11/01/2025")
    
    c1, c2 = st.columns(2)
    with c1: st.text_input("FEIN", "48-4924562")
    with c2: st.text_input("Years in business", "50")
    
    st.write("")
    if st.button("Next"):
        next_step()

# --- PAGE 8: BASIC INFO PART B ---
elif st.session_state.step == 8:
    if st.button("← Previous step"):
        prev_step()

    st.markdown("# Basic info (2/2)")

    c1, c2 = st.columns(2)
    with c1: st.selectbox("Organization type", ["Corporation", "LLC", "Sole Proprietorship"])
    with c2: st.selectbox("Employer's Liability Limits", ["$1M / $1M / $1M", "$500k / $500k / $500k"])

    st.write("---")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Waiver of Subrogation?**")
        st.radio("Waiver", ["Yes", "No"], horizontal=True, label_visibility="collapsed")
    with c2:
        st.write("**100% Ownership?**")
        st.radio("Ownership", ["Yes", "No"], horizontal=True, label_visibility="collapsed", index=0)
    with c3:
        st.write("**Bankruptcy?**")
        st.radio("Bankruptcy", ["Yes", "No"], horizontal=True, label_visibility="collapsed", index=1)
        
    st.write("---")
    
    st.write("**Number of locations?**")
    cols = st.columns(12)
    cols[0].button("1", key="l1")
    cols[1].button("2", key="l2")
    cols[2].button("3", key="l3")
    
    st.write("")
    st.write("")
    if st.button("Get Quote"):
        next_step()

# --- PAGE 9: PROCESSING SCREEN ---
elif st.session_state.step == 9:
    
    if 'validation_started' not in st.session_state:
        st.markdown("# Validating Data...")
        st.session_state.validation_started = True
        st.rerun() 

    st.markdown("# Validating Data...")
    
    my_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Connecting to Secretary of State API...",
        "Verifying Business Licenses...",
        "Checking OSHA records...",
        "Analyzing Digital Footprint (Carpe Data)...",
        "Finalizing Pricing..."
    ]
    
    for i, step_text in enumerate(steps):
        status_text.text(step_text)
        time.sleep(0.5) 
        my_bar.progress((i + 1) * 20)
        
    del st.session_state.validation_started
    st.session_state.step = 10
    st.rerun()

# --- PAGE 10: RESULT SCREEN ---
elif st.session_state.step == 10:
    st.markdown("## Quote Generated")
    st.markdown("---")
    
    is_referral = "Data Mismatch" in scenario
    
    if is_referral:
        st.markdown("""
        <div class="refer-box">
            <h3>⚠️ Quote Generated - Referral Required</h3>
            <p>We successfully rated this account, but external data validation found a discrepancy that requires Underwriter review.</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.error("⛔ **Validation Alert:** Digital footprint analysis (Yelp/Google) indicates 'Delivery Services' are advertised, but 'No Delivery' was selected.")
        with c2:
            st.metric(label="Indicative Premium", value="$3,450.00")
            
        st.button("Start a new Quote", on_click=reset)
        
    else:
        st.markdown("""
        <div class="bind-box">
            <h3>✅ Bindable Quote</h3>
            <p>All data validated. This account is eligible for straight-through processing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("✔ State License: Active")
            st.success("✔ OSHA History: Clean")
            st.success("✔ Digital Footprint: Consistent")
        with c2:
            st.metric(label="Total Premium", value="$1,250.00")
        
        if st.button("BIND POLICY NOW"):
            next_step()

# --- PAGE 11: BOUND SUMMARY ---
elif st.session_state.step == 11:
    st.balloons() 
    
    st.markdown("""
    <div class="bind-box">
        <center>
            <h2>🎉 Policy Bound Successfully!</h2>
            <p>Policy Number: <b>WC-2025-99824X</b></p>
        </center>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Policy Summary")
    
    # Define summary columns with unique names
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.markdown("**Insured:**")
        st.write(st.session_state.data.get('company'))
        st.write("775 Battery Avenue Southeast")
        st.write("Atlanta, GA 30339")
        
        st.markdown("**Coverage:**")
        st.write("Workers' Compensation")
        st.write("Limits: $1M / $1M / $1M")
    
    with summary_col2:
        st.markdown("**Classification:**")
        st.write(st.session_state.data.get('class_code'))
        
        st.markdown("**Total Premium:**")
        st.metric("Annual Premium", "$1,250.00")
    
    st.markdown("---")
    
    b1, b2, b3 = st.columns(3)
    b1.button("📄 Download Policy Packet")
    b2.button("📧 Email to Insured")
    b3.button("Start New Quote", on_click=reset)

# --- PAGE 12: DECLINE SCREEN ---
elif st.session_state.step == 12:
    st.markdown("## Application Declined")
    st.markdown("---")
    
    reason = st.session_state.decline_reason
    
    st.markdown(f"""
    <div class="decline-box">
        <h3>⛔ Decline: Outside of Appetite</h3>
        <p>We are unable to offer coverage for this risk based on the information provided.</p>
        <p><b>Reason:</b> {reason}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("If you believe this determination was made in error, please contact your territory manager.")
    st.write("")
    st.button("Start New Quote", on_click=reset)
