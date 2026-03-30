import streamlit as st

st.set_page_config(page_title="🏊 Pool Script Assistant", layout="wide")

# -----------------------------------------------------------------------
# 🔐 GOOGLE SSO AUTH
# -----------------------------------------------------------------------
ALLOWED_DOMAIN = "lawnstarter.com"

if st.user.is_logged_in:
    st.session_state['_auth_email'] = (st.user.email or "").strip()

_is_authed = st.session_state.get('_auth_email', '')

if not _is_authed:
    st.markdown(
        """
        <div style='text-align:center; padding: 80px 20px;'>
            <div style='font-size:48px;'>🏊</div>
            <h1 style='font-size:36px; font-weight:900;'>Pool Script Assistant</h1>
            <p style='font-size:18px; color:#aaa; margin-bottom:32px;'>
                Sign in with your LawnStarter Google account to continue.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.login("google")
    st.stop()

user_email = st.session_state['_auth_email']

if not user_email.lower().endswith(f"@{ALLOWED_DOMAIN}"):
    st.error(f"❌ Access restricted to @{ALLOWED_DOMAIN} accounts. You're signed in as **{user_email}**.")
    st.session_state.pop('_auth_email', None)
    st.logout()
    st.stop()

# -----------------------------------------------------------------------
# -----------------------------
# RESPONSE LIBRARY
# -----------------------------
RESPONSES = {
    "Green Pool / Urgent": {
        "response": (
            "Yeah — that’s exactly when most people call us. "
            "We’ll start with a deep clean to get everything reset and balanced, "
            "then maintain it so it stays clean and you don’t have to deal with it again."
        ),
        "why": "Matches urgency and clearly explains the reset → maintain model."
    },
    "Only Wants One Clean": {
        "response": (
            "Totally get that — we’ll start with the deep clean to get everything cleaned up, "
            "then do a few maintenance visits to keep it from going right back. "
            "After that, you’re completely flexible."
        ),
        "why": "Avoids saying no directly while reframing the follow-up visits as part of the solution."
    },
    "Price Too High": {
        "response": (
            "Yeah — totally fair. What most customers like is that everything’s included — "
            "cleaning, chemicals, balancing, and filter care — so there are no surprise costs."
        ),
        "why": "Acknowledges the objection and shifts the focus to value."
    },
    "Just Shopping Around": {
        "response": (
            "Totally makes sense — most people we talk to are comparing options. What we focus on is making it simple and consistent" 
             "— everything’s included, and you can see exactly what’s being done after each visit. "
        ),
        "why": "Keeps the rep calm and confident without sounding pushy."
    },
    "Does That Include Chemicals?": {
        "response": "Yes — chemicals are included. You don’t need to provide anything.",
        "why": "Directly removes one of the most common friction points."
    },
    "Who Is Coming?": {
        "response": (
            "We connect you with a vetted local pool pro. Once they pick up the job, "
            "you’ll see their info and be able to message them directly."
        ),
        "why": "Builds trust and transparency."
    },
    "I’ve Been Ghosted Before": {
        "response": (
            "Yeah — we hear that a lot. That’s actually one of the biggest reasons customers like using us. "
            "If you’re ever not happy for any reason, we handle switching you to a new pro, "
            "so you don’t have to start all over again."
        ),
        "why": "Turns a pain point into one of your strongest competitive advantages."
    },
    "I Don’t Want Ongoing Service": {
        "response": (
            "Totally get that — we do a few follow-up maintenance visits up front to keep the pool stable "
            "after the clean. After that, you’re completely flexible."
        ),
        "why": "Keeps the explanation honest without sounding rigid or contractual."
    },
    "Can I Skip or Pause?": {
        "response": (
            "Absolutely — you’re never locked into the schedule. "
            "You can skip or pause anytime as long as you let us know at least 48 hours ahead."
        ),
        "why": "Gives the customer control and reduces fear of overpaying."
    },
    "Trust / Wants to Try Us First": {
        "response": (
            "Totally fair — a lot of people feel that way at first. "
            "That’s why we make it simple and consistent, and if you’re ever not happy for any reason, "
            "we handle switching you to a new pro so you don’t have to start over."
        ),
        "why": "Acknowledges trust hesitation and uses your strongest service advantage to reduce risk."
    },
    "Selling Home": {
        "response": (
            "That actually works really well for this. We’ll get it cleaned up, "
            "then keep it maintained while the home is being shown so you don’t have to worry about it."
        ),
        "why": "Frames service as a simple solution for sellers."
    },
    "New Pool Owner / Needs Guidance": {
        "response": (
            "Yeah — that’s super common. We handle the cleaning, chemicals, and balancing for you, "
            "so you don’t have to figure it all out yourself."
        ),
        "why": "Reduces overwhelm and positions the service as easy."
    },
    "Wants to Think About It": {
        "response": (
            "Totally — what part are you still deciding on? "
            "Is it the pricing, the schedule, or just wanting to compare options?"
        ),
        "why": "Helps uncover the real objection instead of accepting a soft no."
    },
    "Why Do I Need Weekly?": {
        "response": (
            "The deep clean gets it fixed — the next few visits are what keep it from going right back. "
            "That’s what keeps the pool stable."
        ),
        "why": "Explains the logic behind recurring in a simple, confident way."
    },
    "Assumptive Close": {
        "response": (
            "Let’s get that taken care of — I have the earliest 2-day window of Thursday or Friday available. "
            "Which works better for you?"
        ),
        "why": "Keeps momentum moving and guides the customer into the next step."
    },
}

TOP_10_LINES = [
    "What’s the pool looking like right now?",
    "We start with a deep clean, then maintain it so it stays that way.",
    "Chemicals are included.",
    "Each visit includes cleaning, balancing, and filter care.",
    "Most customers are around $150/month.",
    "We do a few maintenance visits up front to keep everything stable.",
    "You can skip or pause anytime with 48 hours’ notice.",
    "If you’re not happy, we’ll switch you to a new pro.",
    "We connect you with a vetted local pool pro.",
    "I have Thursday or Friday available — which works better for you?",
]

# -----------------------------
# HELPERS
# -----------------------------
def show_response(label: str) -> None:
    result = RESPONSES[label]
    st.subheader("🎯 Suggested Response")
    st.success(result["response"])

    st.subheader("💡 Why This Works")
    st.info(result["why"])


def info_card(title: str, body: str, highlight: bool = False) -> None:
    bg_color = "#dbeafe" if highlight else "#f8fafc"   # active vs normal
    border_color = "#2563eb" if highlight else "#cbd5e1"
    title_color = "#0f172a"
    body_color = "#111827"

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            border-left: 6px solid {border_color};
            padding: 14px 16px;
            border-radius: 10px;
            margin-bottom: 10px;
        ">
            <div style="
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 10px;
                color: {title_color};
            ">
                {title}
            </div>
            <div style="
                white-space: pre-line;
                line-height: 1.6;
                font-size: 1.05rem;
                color: {body_color};
            ">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def monthly_estimate_from_visit_price(frequency: str, per_visit_price: float) -> float:
    if frequency == "Twice a Week":
        return per_visit_price * 8
    if frequency == "Weekly":
        return per_visit_price * 4
    if frequency == "Every Two Weeks":
        return per_visit_price * 2
    return per_visit_price

def get_pricing_strings():
    deep = st.session_state.get("deep_clean", 300)
    visit = st.session_state.get("per_visit", 38)
    monthly = st.session_state.get("monthly", 152)
    freq = st.session_state.get("frequency", "weekly")

    return (
        f"\\${deep:,.0f}",
        f"\\${monthly:,.0f}",
        f"\\${visit:,.0f}",
        freq.lower()
    )

def show_step_hint(current_key: str, active_key: str, active_label: str) -> None:
    if current_key == active_key and active_label:
        st.caption(f"➡️ Next Step: {active_label}")

def show_active_marker(current_key: str, active_key: str) -> None:
    if current_key == active_key:
        st.info("🔵 Current Step")

# -----------------------------
# HEADER
# -----------------------------
st.title("🏊 Pool Sales Script Assistant")
st.caption("Built for live rep support, objection handling, and fast pool call guidance.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📞 Full Call Flow",
    "⚡ Objection Assistant",
    "🎭 Scenario Mode",
    "❓ FAQs"
])

# -----------------------------
# TAB 1: FULL CALL FLOW
# -----------------------------
with tab1:
    st.subheader("Full Pool Call Flow")
    st.caption("Simple, trustworthy guide-to-sale from greeting to close.")

    st.info("""
    🔥 Live Call Reminders
    • Keep it simple
    • Don’t introduce objections early
    • Guide → price → close
    • If resistance appears, go to Tab 2
    """)

    step_order = [
        ("chk_service", "Service Explained"),
        ("chk_contact", "Contact Info"),
        ("chk_price", "Pricing"),
        ("chk_serviceincl", "What's Included"),
        ("chk_close", "Attempted Close"),
        ("chk_email", "Email"),
        ("chk_recap", "Recap"),
        ("chk_policy", "Policy"),
        ("chk_payment", "Payment"),
        ("chk_expectation", "Expectation Set"),
        ("chk_nextdoor", "Nextdoor Promo"),

    ]

    missing_steps = []
    active_step_key = None
    active_step_label = None

    for key, label in step_order:
        if not st.session_state.get(key, False):
            missing_steps.append(label)
            if active_step_key is None:
                active_step_key = key
                active_step_label = label

    if active_step_label:
        st.info(f"➡️ Current Focus: {active_step_label}")
    else:
        st.success("🎉 All key steps completed — ready to wrap up the call.")

    if missing_steps:
        st.caption(f"Missing: {', '.join(missing_steps)}")

    # -----------------------------
    # LIVE QUOTE BUILDER INPUTS
    # -----------------------------
    st.subheader("💰 Live Quote Builder")
    st.caption("Enter the prices from the sales tool and let the app build the talk track.")

    q1, q2, q3 = st.columns(3)

    with q1:
        deep_clean_input = st.number_input(
            "One-Time Deep Clean Price",
            min_value=0.0,
            step=1.0,
            value=300.0,
            key="deep_clean_input"
        )

    with q2:
        recurring_visit_input = st.number_input(
            "Standard Maintenance Price",
            min_value=0.0,
            step=1.0,
            value=38.0,
            key="recurring_visit_input"
        )

    with q3:
        recurring_frequency = st.selectbox(
            "Frequency of Standard Maintenance",
            ["Weekly", "Twice a Week", "Every Two Weeks"],
            key="recurring_frequency"
        )

    monthly_quote = monthly_estimate_from_visit_price(recurring_frequency, recurring_visit_input)

    deep_clean_display = f"{deep_clean_input:,.0f}"
    monthly_display = f"{monthly_quote:,.0f}"
    recurring_display = f"{recurring_visit_input:,.0f}"

    st.session_state["deep_clean"] = deep_clean_input
    st.session_state["per_visit"] = recurring_visit_input
    st.session_state["monthly"] = monthly_quote
    st.session_state["frequency"] = recurring_frequency

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        info_card(
            "1. Normal Call Greeting",
            "Hey this is Heather with Home Gnome — I can help you get your pool taken care of today.\n\n"
            "What’s the pool looking like right now, is it clear, cloudy, or starting to turn green?"
        )

        info_card(
            "2. SMS Follow-Up Call Greeting",
            "Hey this is Heather with Home Gnome — you were just texting us about pool service.\n\n"
            "I can get you a quote and walk you through everything real quick.\n\n"
            "What’s the pool looking like right now, is it clear, cloudy, or starting to turn green?"
        )

        show_active_marker("chk_service", active_step_key)

        info_card(
            "3. Position the Service",
            "Got it! What we’ll do is start with a deep clean to get everything reset and balanced, "
            "then maintain it so it stays clean.\n\n"
            "Our goal is simple, every visit, we leave your pool better than we found it.",
            highlight=(active_step_key == "chk_service")
        )

        st.checkbox("✔️ Service Explained", key="chk_service")
        show_step_hint("chk_service", active_step_key, active_step_label)

        show_active_marker("chk_contact", active_step_key)

        info_card(
            "4. Verify Customer Information Early",
            "Before I pull exact pricing, let me just make sure I’ve got the right info.\n\n"
            "I have your (NAME) as — did I get that right?\n"
            "And I have the service address as (ADDRESS) — is that correct?\n"
            "And is (PHONE) still the best number for you?",
            highlight=(active_step_key == "chk_contact")
        )

        st.checkbox("✔️ Contact Info Verified", key="chk_contact")
        show_step_hint("chk_contact", active_step_key, active_step_label)

        info_card(
            "5. Lead Source",
            "And how did you find out about us?"
        )

        show_active_marker("chk_price", active_step_key)

        info_card(
            "6. Pricing Language That Converts",
            f"To get it cleaned up, it’s \\${deep_clean_display} for the first visit based on the condition.\n\n"
            f"After that, it’s \\${recurring_display} per visit for weekly maintenance — so you’re only paying for completed service.\n\n"
            f"📌 If they ask about monthly: \"Most customers are around \\${monthly_display} per month — it’s billed per visit so you only pay for what’s completed.\"",
            highlight=(active_step_key == "chk_price")
        )

        st.checkbox("✔️ Pricing Clearly Explained", key="chk_price")
        show_step_hint("chk_price", active_step_key, active_step_label)

        show_active_marker("chk_serviceincl", active_step_key)

        info_card(
            "7. Explain What’s Included",
            "**Standard Maintenance** — every visit includes:\n\n"
            "• tile brushing & skimming\n"
            "• vacuuming\n"
            "• chemical testing\n"
            "• filter cleaning to keep your pool crystal clear year-round\n\n"
            "---\n\n"
            "**One-Time Deep Clean** — your first visit includes:\n\n"
            "• shock the pool\n"
            "• vacuum the pool floor\n"
            "• brush the walls and tile\n"
            "• skim surface debris\n"
            "• clean the skimmer and pump baskets\n"
            "• inspect and clean the filter\n"
            "• balance your pool’s water chemistry\n"
            "• apply algae treatment if needed\n\n"
            "We’re committed to leaving your pool in pristine condition, so you can spend more time enjoying it and less time maintaining it.",
            highlight=(active_step_key == "chk_serviceincl")
        )
        st.checkbox("✔️ What's Included", key="chk_serviceincl")
        show_step_hint("chk_serviceincl", active_step_key, active_step_label)

        show_active_marker("chk_close", active_step_key)

        info_card(
            "8. Assumptive Close",
            "Let’s get that pool taken care of — I have Thursday or Friday available as our first 2-day window. Does that work for you?",
            highlight=(active_step_key == "chk_close")
        )

        st.checkbox("✔️ Attempted Close", key="chk_close")
        show_step_hint("chk_close", active_step_key, active_step_label)

    with col2:

        show_active_marker("chk_email", active_step_key)

        info_card(
            "9. Email Verification",
            "Great — what’s the best email for your account?\n\n"
            "I have your email as (PHONETICALLY SPELLED OUT @ ALWAYS.com).\n\n"
            "To confirm, just in case we have it wrong, your phone number is (___) ___-____.",
            highlight=(active_step_key == "chk_email")
        )

        st.checkbox("✔️ Email Verified", key="chk_email")
        show_step_hint("chk_email", active_step_key, active_step_label)

        show_active_marker("chk_recap", active_step_key)

        info_card(
            "11. Order Recap",
            f"To confirm, we’re scheduling you for "
            f"{'weekly maintenance only' if deep_clean_input == 0 else 'deep cleaning + weekly maintenance'}.\n\n"
            f"Your first visit is \\${deep_clean_display if deep_clean_input > 0 else recurring_display}, "
            f"and ongoing service is billed at \\${recurring_display} per visit.",
            highlight=(active_step_key == "chk_recap")
        )

        st.checkbox("✔️ Recap", key="chk_recap")
        show_step_hint("chk_recap", active_step_key, active_step_label)


        show_active_marker("chk_policy", active_step_key)

        info_card(
            "12. Policy Disclosure (Verbatim)",
            "Quick heads-up: By booking, you agree to our Terms of Service.\n"
            "We just ask for at least 48 hours’ notice if you ever need to change your schedule.\n"
            "You may get texts or calls about your service—you can opt out anytime.\n"
            "Full terms are at homegnome.com/terms.",
            highlight=(active_step_key == "chk_policy")
        )

        st.checkbox("✔️ Policy Read", key="chk_policy")
        show_step_hint("chk_policy", active_step_key, active_step_label)

        show_active_marker("chk_payment", active_step_key)

        info_card(
            "13. Payment Method / Secure Link",
            "Perfect, all I need is a payment method to schedule you. We accept major credit and debit cards, "
            "and we won’t charge you until 3 days after the service is complete.\n\n"
            "I’m sending over a secure link for you to add your payment info directly, since we don’t have access to that on our end. "
            "This will go through text and email.",
            highlight=(active_step_key == "chk_payment")
        )

        st.checkbox("✔️ Payment Link Sent", key="chk_payment")
        show_step_hint("chk_payment", active_step_key, active_step_label)


        show_active_marker("chk_expectation", active_step_key)

        info_card(
            "14. Expectation Setting / App / Portal",
            "Once the crew adds the job to their route, you’ll receive an email confirming your two-day window "
            "and letting you know a Pro picked the job up. At that point, you can message them directly.\n\n"
            "You’ll also receive a text with a link to our free app and a temporary password — your email will be your username.\n\n"
            "Through the app and web login, you can request additional services, make changes to your account, "
            "and it’s the fastest way to contact our Support Team.\n\n"
            "📋 Once you’re logged in, there are a few important questions about your pool we’d love for you to answer — "
            "things like pool size and filtration details — so your Pro is fully prepared before they arrive.",
            highlight=(active_step_key == "chk_expectation")
        )

        st.checkbox("✔️ Expectation Set", key="chk_expectation")
        show_step_hint("chk_expectation", active_step_key, active_step_label)


        info_card(
            "15. Landline-Only Customers",
            "To log onto the website, enter your email address and click forgot password. "
            "You’ll receive an email with a temporary password. Make sure to change the password once you log in.\n\n"
            "Websites:\n"
            "my.lawnstarter.com\n"
            "my.lawnlove.com\n"
            "my.homegnome.com"
        )

        show_active_marker("chk_nextdoor", active_step_key)

        info_card(
            "16. NextDoor Referral Credit",
            "When you log in to your account, you’ll be able to recommend us on NextDoor. "
            "Do this and receive a $20 credit to your account.",
            highlight=(active_step_key == "chk_nextdoor")
        )

        st.checkbox("✔️ Nextdoor Promo", key="chk_nextdoor")
        show_step_hint("chk_nextdoor", active_step_key, active_step_label)

        info_card(
            "17. Final Closing",
            "Any other questions before I let you go?\n\n"
            "If anything comes up, you can always reach out through the app or portal.\n\n"
            "Thank you for choosing LawnStarter / Lawn Love / Home Gnome, have a great day!"
        )


    st.divider()

    st.subheader("🧠 Quick Call Flow Cheat Sheet")
    st.markdown("""
    1. Ask what the pool looks like  
    2. Verify name, address, and phone early  
    3. Explain deep clean + maintenance  
    4. Say chemicals are included  
    5. Use monthly pricing  
    6. Guide frequency based on condition  
    7. Close confidently  
    8. Verify email  
    9. Ask property details  
    10. Review order  
    11. Send payment link  
    12. Read policy disclosure  
    13. Reinforce 48-hour notice  
    14. Set expectations for confirmation + app
    """)


    missing_steps = []

    if not st.session_state.get("chk_service"):
        missing_steps.append("Service Explained")

    if not st.session_state.get("chk_contact"):
        missing_steps.append("Contact Info")

    if not st.session_state.get("chk_price"):
        missing_steps.append("Pricing")

    if not st.session_state.get("chk_serviceincl"):
        missing_steps.append("What’s Included")

    if not st.session_state.get("chk_close"):
        missing_steps.append("Attempted Close")

    if not st.session_state.get("chk_email"):
        missing_steps.append("Email")

    if not st.session_state.get("chk_recap"):
        missing_steps.append("Recap")

    if not st.session_state.get("chk_policy"):
        missing_steps.append("Policy")

    if not st.session_state.get("chk_payment"):
        missing_steps.append("Payment")

    if not st.session_state.get("chk_expectation"):
        missing_steps.append("Expectation Set")

    if not st.session_state.get("chk_nextdoor"):
        missing_steps.append("Nextdoor Promo")




    if missing_steps:
        st.warning(f"⚠️ Missing steps before close: {', '.join(missing_steps)}")
    else:
        st.success("🎉 All steps completed — ready to close!")

# -----------------------------
# -----------------------------
# TAB 2: OBJECTION ASSISTANT
# -----------------------------
with tab2:
    st.subheader("Objection Assistant")
    st.caption("Use this only when the customer raises a concern. Keep the main flow simple and come here when resistance appears.")

    deep, monthly, visit, freq = get_pricing_strings()

    button_rows = [
        ["Needs Monthly Price", "Flat Monthly Request", "Comparing Lower Price"],
        ["Green Pool / Urgent", "Price Too High", "Just Shopping Around"],
        ["Only Wants One Clean", "Selling Home", "Wants to Think About It"],
        ["Who Is Coming?", "I’ve Been Ghosted Before", "Trust / Wants to Try Us First"],
        ["I Don’t Want Ongoing Service", "Why Do I Need Weekly?", "Can I Skip or Pause?"],
        ["Does That Include Chemicals?", "New Pool Owner / Needs Guidance", "Assumptive Close"],
    ]

    for row in button_rows:
        cols = st.columns(len(row))
        for col, label in zip(cols, row):
            with col:
                if st.button(label, use_container_width=True, key=f"btn_{label}"):
                    st.session_state["selected_response"] = label

    selected = st.session_state.get("selected_response")

    # -----------------------------
    # MONTHLY / PRICING LANGUAGE
    # -----------------------------
    if selected == "Needs Monthly Price":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Most customers are around {monthly} per month for weekly service.\n\n"
            f"It’s billed at {visit} per visit, but that’s typically what it comes out to."
        )

        st.subheader("💡 Why This Works")
        st.info("Answers exactly what they asked for (monthly) without overcomplicating it.")

    elif selected == "Flat Monthly Request":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally get that — ours is billed per visit so you’re only paying for completed service, "
            f"but most customers think of it as about {monthly} per month."
        )

        st.subheader("💡 Why This Works")
        st.info("Acknowledges preference while reinforcing your model as fair and flexible.")

    elif selected == "Comparing Lower Price":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Got it — most customers we work with are around {monthly} per month because everything’s included — "
            f"cleaning, chemicals, and balancing — so there aren’t extra costs popping up."
        )

        st.subheader("💡 Why This Works")
        st.info("Repositions price comparison into value instead of just cost.")

    # -----------------------------
    # CORE OBJECTIONS
    # -----------------------------
    elif selected == "Price Too High":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally fair — most customers we work with are around {monthly} per month for weekly service.\n\n"
            f"It’s billed at {visit} per visit, and that includes cleaning, chemicals, balancing, and filter care — "
            f"so there aren’t extra costs."
        )

        st.subheader("💡 Why This Works")
        st.info("Anchors to monthly, reinforces value, removes hidden cost concern.")

    elif selected == "Only Wants One Clean":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally get that — we’ll start with the deep clean at {deep} to get everything reset.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service, "
            f"just to keep it from going right back."
        )

        st.subheader("💡 Why This Works")
        st.info("Keeps it simple and reframes maintenance as part of solving the problem.")

    elif selected == "Selling Home":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"That makes sense — we hear that a lot with homes getting ready for photos and showings.\n\n"
            f"What we’ll do is get it cleaned up first at {deep}, then keep it show-ready so you don’t have to worry "
            f"about it slipping backward while the home is on the market.\n\n"
            f"Most customers are around {monthly} per month during that time."
        )

        st.subheader("💡 Why This Works")
        st.info("Aligns with the seller’s goal: presentation and convenience.")

    elif selected == "I Don’t Want Ongoing Service":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally get that — we do a few follow-up maintenance visits up front to keep the pool stable after the clean.\n\n"
            f"Most customers are around {monthly} per month for that ongoing service."
        )

        st.subheader("💡 Why This Works")
        st.info("Explains logic without sounding contractual or rigid.")

    elif selected == "Why Do I Need Weekly?":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"The deep clean gets it fixed — the next few visits are what keep it from going right back.\n\n"
            f"Most customers are around {monthly} per month for weekly service, billed at {visit} per visit."
        )

        st.subheader("💡 Why This Works")
        st.info("Explains the why first, then reinforces pricing simply.")

    elif selected == "Can I Skip or Pause?":
        st.subheader("🎯 Suggested Response")
        st.success(
            "Absolutely — you’re not locked in. You can skip or pause anytime as long as you let us know at least 48 hours ahead."
        )

        st.subheader("💡 Why This Works")
        st.info("Gives control and reduces fear of commitment.")

    elif selected == "Trust / Wants to Try Us First":
        st.subheader("🎯 Suggested Response")
        st.success(
            "Totally fair — a lot of people feel that way at first. "
            "If you’re ever not happy, we handle switching you to a new pro so you don’t have to start over."
        )

        st.subheader("💡 Why This Works")
        st.info("Reduces risk and builds trust quickly.")

    elif selected:
        show_response(selected)

    st.divider()

    with st.expander("🧠 When to Use Objection Handling"):
        st.markdown("""
Use this tab only when the customer gives resistance or hesitation.

**Examples:**
- “I only want one clean”
- “I’m still shopping around”
- “That sounds expensive”
- “I don’t want to be locked in”
- “I’ve had bad luck with pool guys before”
- “I just want to see how you do first”

**Do not** front-load these into the main script unless the customer brings them up.
        """)

    with st.expander("🔥 Best Practice for Reps"):
        st.markdown("""
**1. Stay in the main flow first**  
Guide the customer through the service, pricing, and close.

**2. Only pull an objection response when needed**  
Do not introduce concerns they haven’t raised.

**3. Answer briefly, then return to the sale**  
After handling the concern, move right back to closing.
        """)

    with st.expander("⚡ Best 'Return to Close' Lines"):
        st.markdown("""
- **Let’s get that taken care of — I have Thursday or Friday available. Which works better?**
- **That’s exactly why most people get started now — I do have availability this week.**
- **Totally fair — with that in mind, I can get you on the schedule for Thursday or Friday. Which works better?**
- **That makes sense — let’s go ahead and lock in your first window so this is handled.**
        """)

with tab3:
    deep, monthly, visit, freq = get_pricing_strings()

    st.subheader("Scenario Mode")
    st.caption("Real call examples to guide reps through common situations.")

    scenario = st.selectbox(
        "Choose Scenario",
        [
            "Green Pool (Urgent)",
            "Price Shopper",
            "New Pool Owner",
            "Only Wants One Clean",
            "Selling Home"
        ]
    )

    st.divider()

    # -----------------------------
    # GREEN POOL
    # -----------------------------
    if scenario == "Green Pool (Urgent)":
        st.markdown("### 🟢 Green Pool Call")

        st.markdown("**Customer:** My pool is green, I need it cleaned ASAP.")

        st.markdown("**Rep:**")
        st.success(
            "Got it — that’s exactly when most people reach out. "
            "What we’ll do is start with a deep clean to get everything reset and balanced, "
            "then maintain it so it stays clean."
        )

        st.markdown("**Rep:**")
        st.success(
            "Chemicals are included, and our goal is simple — every visit, we leave your pool better than we found it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it’s {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** That’s kind of expensive.")

        st.markdown("**Rep:**")
        st.success(
            f"Totally fair — most customers we work with are around {monthly} per month, "
            "and that includes cleaning, chemicals, and balancing so you’re not dealing with extra costs."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let’s get that taken care of — I have Thursday or Friday available. Which works better?"
        )

    # -----------------------------
    # PRICE SHOPPER
    # -----------------------------
    elif scenario == "Price Shopper":
        st.markdown("### 💰 Price Shopper Call")

        st.markdown("**Customer:** I’m just calling around getting quotes.")

        st.markdown("**Rep:**")
        st.success(
            "Totally makes sense — most people we talk to are comparing options. "
            "I’ll give you a clear picture so you can compare apples to apples."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we do is start with a deep clean if needed, then ongoing maintenance to keep the pool clean and balanced."
        )

        st.markdown("**Rep:**")
        st.success(
            "Each visit includes cleaning, chemicals, balancing, and filter care."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it’s {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** Okay, I’m still looking around.")

        st.markdown("**Rep:**")
        st.success(
            "That makes sense. I do have availability this week if you want to grab a spot while you're comparing."
        )

    # -----------------------------
    # NEW POOL OWNER
    # -----------------------------
    elif scenario == "New Pool Owner":
        st.markdown("### 🏡 New Pool Owner")

        st.markdown("**Customer:** I just moved in and have no idea how to maintain a pool.")

        st.markdown("**Rep:**")
        st.success(
            "Yeah — that’s super common. We handle the cleaning, chemicals, and balancing for you, "
            "so you don’t have to figure it all out yourself."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we’ll do is start with a deep clean if needed, then maintain it so it stays clean and consistent."
        )

        st.markdown("**Rep:**")
        st.success(
            "Our goal is simple — every visit, we leave your pool better than we found it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it’s {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** Okay, that sounds helpful.")

        st.markdown("**Rep (close):**")
        st.success(
            "Perfect — let’s get that taken care of. I have Thursday or Friday available. Which works better?"
        )

    # -----------------------------
    # ONLY WANTS ONE CLEAN
    # -----------------------------
    elif scenario == "Only Wants One Clean":
        st.markdown("### 🧼 Only Wants One Clean")

        st.markdown("**Customer:** I really just want one clean to see how it goes.")

        st.markdown("**Rep:**")
        st.success(
            "Totally get that — a lot of people say that at first."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we do is start with the deep clean to get everything reset, "
            "then do a few maintenance visits so it doesn’t go right back."
        )

        st.markdown("**Customer:** I just don’t want to be locked into something.")

        st.markdown("**Rep:**")
        st.success(
            "Completely fair — that’s really just to stabilize the pool after we clean it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it’s {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let’s get that taken care of — I have Thursday or Friday available. Which works better?"
        )

    # -----------------------------
    # SELLING HOME
    # -----------------------------
    elif scenario == "Selling Home":
        st.markdown("### 🏠 Selling Home")

        st.markdown("**Customer:** I’m selling the house, so I just need the pool cleaned up.")

        st.markdown("**Rep:**")
        st.success(
            "That makes sense — we hear that a lot with homes getting ready for photos and showings."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we’ll do is get it cleaned up first, then keep it show-ready so you don’t have to worry "
            "about it slipping backward while the home is on the market."
        )

        st.markdown("**Customer:** I really don’t need long-term service.")

        st.markdown("**Rep:**")
        st.success(
            "Totally understand — the follow-up visits are really just to keep it looking good while buyers are coming through."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it’s {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let’s get that taken care of so the pool is one less thing on your plate — "
            "I have Thursday or Friday available. Which works better?"
        )

    st.divider()

    with st.expander("🧠 How to Use Scenario Mode"):
        st.markdown("""
- Use these as **confidence builders**, not word-for-word scripts every time.
- Keep the call moving.
- Don’t introduce objections unless the customer raises them.
- Answer briefly, then guide back to the close.
        """)

    with st.expander("🔥 Best Practice"):
        st.markdown("""
**Main script = guide to sale**  
**Tab 2 = handle resistance**  
**Tab 3 = hear how good calls should sound**

The goal is not to sound scripted.
The goal is to sound simple, clear, and confident.
        """)

# -----------------------------
# TAB 4: FAQs
# -----------------------------
with tab4:
    st.subheader("Frequently Asked Questions")
    st.caption("Quick answers to common customer questions — use these verbatim or as a guide.")

    faqs = [
        (
            "Q1: What does the deep clean actually include?",
            "The deep clean includes shocking the pool, skimming, vacuuming, adding algaecide, cleaning the filter and skimmer basket, and adjusting all chemical levels. We take before and after photos so you can see the difference."
        ),
        (
            "Q2: What does weekly maintenance include?",
            "Every visit includes vacuuming, skimming, adjusting chemical levels, cleaning the filter as needed, and before and after photos. Our goal is simple — every visit, we leave your pool better than we found it."
        ),
        (
            "Q3: Are chemicals included? What kind do you use?",
            "Yes — all chemicals are included, we handle everything. That includes shock, algaecide, and whatever balancing agents your pool needs. You don't need to supply anything or know anything about it — that's on us."
        ),
        (
            "Q4: Can I use my own chemicals?",
            "You're welcome to add chemicals yourself between visits, but our pro handles everything during the service — you don't need to."
        ),
        (
            "Q5: Do you offer biweekly or twice-a-week service?",
            "Right now, we start everyone on a weekly schedule because it keeps the pool the most stable. That said, you have full flexibility — if you only want service every other week, you can simply skip any upcoming visit in the app with at least 48 hours' notice, no penalty.\n\nA lot of customers use that to effectively create a biweekly schedule while still having the option to add extra visits anytime if needed."
        ),
        (
            "Q6: Can I just get a one-time deep clean?",
            "The deep clean is always packaged with ongoing maintenance starting one week later — that's what keeps the pool from going right back. That said, you have full flexibility on frequency after that, including every-two-weeks service."
        ),
        (
            "Q7: My pool is green — can you fix it?",
            "Yes — that's exactly what the deep clean is designed for. It includes shocking, algaecide, vacuuming, and full chemical balancing to get it reset. After that, regular maintenance keeps it from going back."
        ),
        (
            "Q8: How does billing work?",
            "You're billed 3–4 days after the service is marked complete — so you never pay until the work is done."
        ),
        (
            "Q9: Is there a contract? Can I cancel?",
            "No contract. The only thing we ask is 48 hours' notice if you need to cancel or reschedule a visit."
        ),
        (
            "Q10: Can I change my frequency later?",
            "We keep service on a weekly schedule to keep your pool in great shape, but you're never locked in — if you need to space things out, you can skip any upcoming visit in the app with 48 hours' notice, no penalty."
        ),
        (
            "Q11: Who is coming to my pool?",
            "We connect you with a vetted local pool pro. Once they pick up the job, you'll see their info and can message them directly through the app."
        ),
        (
            "Q12: Can you service a pool that has no water (empty pool)?",
            "Yes, we can still help — even if the pool is empty and needs a full scrub and clean.\n\n"
            "Just keep in mind this isn't a one-time service — we'd start with a deep clean and then set you up on regular maintenance to keep it in good shape going forward.\n\n"
            "If you're only looking for a one-time scrub with no ongoing service, that's not something we currently offer as a standalone.",
            "For quoting purposes, treat an empty pool like a green or heavily impacted pool depending on how dirty it is — this lets you price the deep clean appropriately. Our current flow isn't specifically designed for empty pools, so make sure to walk the customer through what to expect to avoid confusion on billing or scheduling."
        ),
        (
            "Q13: Can you fix or replace my pool pump / motor?",
            "We focus on cleaning and maintaining the pool itself, so we don't handle equipment repairs like pumps or motors.\n\n"
            "What we can do is get the pool cleaned up, balanced, and back in great shape right away — and if your pro notices anything off with the equipment during the visit, they'll flag it for you so you know exactly what to address.\n\n"
            "A lot of customers will get the water handled first while coordinating repairs separately — that way everything's ready to go as soon as the equipment is sorted."
        ),
        (
            "Q14: Can you install pool rails / steps / hardware I bought on Amazon?",
            "We don't handle installations like rails or steps — we focus on keeping the pool clean, clear, and properly maintained.\n\n"
            "Most customers will have a handyman take care of the install, and then we handle everything on the pool side so it stays looking great and ready to use.\n\n"
            "Once everything's set up, that's where we really take it off your plate."
        ),
        (
            "Q15: Does the weekly maintenance include opening and cleaning the filter housing / pump baskets?",
            "Every visit includes filter cleaning as needed — our pro will check and clean the filter as part of the service.\n\n"
            "If you're asking about full filter housing disassembly or deep internal pump work, that goes beyond our standard maintenance scope. The weekly service covers the cleaning tasks: skimming, vacuuming, chemical testing, and filter cleaning.\n\n"
            "If the pro spots something that needs more attention, they'll let you know."
        ),
        (
            "Q16: Can I pay by check?",
            "We require a card on file to book — we accept all major credit and debit cards.\n\n"
            "The good news is we don't charge you until 3–4 days after the service is completed, so you're never paying upfront."
        ),
        (
            "Q17: What if the deep clean doesn't fully fix my pool?",
            "The deep clean is designed to start the reset — we'll treat the water, remove debris, and begin balancing everything.\n\n"
            "If the pool is really green or hasn't been maintained in a while, it's completely normal for that process to take a few visits over the first week to get it fully cleared up.\n\n"
            "That's exactly why we pair it with weekly maintenance — we stay on it, continue treatments, and make sure it gets all the way to clear and stays that way.\n\n"
            "And if anything ever feels off along the way, you can reach out through the app and we'll take care of it."
        ),
        (
            "Q18: Can I get a free assessment before committing?",
            "We don't do a pre-service assessment visit — the deep clean is how we get started, and it includes a full evaluation of the pool's condition when the pro arrives.\n\n"
            "You're not charged until 3–4 days after the service is complete, so there's no upfront risk. If anything, the before and after photos give you a clear picture of what was done."
        ),
        (
            "Q19: Can you do same-day or next-day service?",
            "Our fastest turnaround is a 48-hour window from when you book — so we can typically get someone out within two days.\n\n"
            "Once you're booked, we'll confirm your scheduled date and you'll be able to see your pro's info through the app."
        ),
    ]

    for faq in faqs:
        question, answer = faq[0], faq[1]
        rep_note = faq[2] if len(faq) > 2 else None
        with st.expander(question):
            st.success(answer)
            if rep_note:
                st.warning(f"🔒 **Rep note (don't read aloud):** {rep_note}")