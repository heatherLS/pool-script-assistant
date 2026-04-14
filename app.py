import streamlit as st

st.set_page_config(page_title="🏊 Pool Sales Call Guide", layout="wide")

# -----------------------------
# RESPONSE LIBRARY
# -----------------------------
RESPONSES = {
    "Green Pool / Urgent": {
        "response": (
            "Yeah — that's exactly when most people call us. "
            "We'll start with a deep clean to get everything reset and balanced, "
            "then maintain it so it stays clean and you don't have to deal with it again."
        ),
        "why": "Matches urgency and clearly explains the reset → maintain model."
    },
    "Only Wants One Clean": {
        "response": (
            "Totally get that — we'll start with the deep clean to get everything cleaned up, "
            "then do a few maintenance visits to keep it from going right back. "
            "After that, you're completely flexible."
        ),
        "why": "Avoids saying no directly while reframing the follow-up visits as part of the solution."
    },
    "Price Too High": {
        "response": (
            "Yeah — totally fair. What most customers like is that everything's included — "
            "cleaning, chemicals, balancing, and filter care — so there are no surprise costs."
        ),
        "why": "Acknowledges the objection and shifts the focus to value."
    },
    "Just Shopping Around": {
        "response": (
            "Totally makes sense — most people we talk to are comparing options. What we focus on is making it simple and consistent" 
             "— everything's included, and you can see exactly what's being done after each visit. "
        ),
        "why": "Keeps the rep calm and confident without sounding pushy."
    },
    "Does That Include Chemicals?": {
        "response": "Yes — chemicals are included. You don't need to provide anything.",
        "why": "Directly removes one of the most common friction points."
    },
    "Who Is Coming?": {
        "response": (
            "We connect you with a vetted local pool pro. Once they pick up the job, "
            "you'll see their info and be able to message them directly."
        ),
        "why": "Builds trust and transparency."
    },
    "I've Been Ghosted Before": {
        "response": (
            "Yeah — we hear that a lot. That's actually one of the biggest reasons customers like using us. "
            "If you're ever not happy for any reason, we handle switching you to a new pro, "
            "so you don't have to start all over again."
        ),
        "why": "Turns a pain point into one of your strongest competitive advantages."
    },
    "I Don't Want Ongoing Service": {
        "response": (
            "Totally get that — we do a few follow-up maintenance visits up front to keep the pool stable "
            "after the clean. After that, you're completely flexible."
        ),
        "why": "Keeps the explanation honest without sounding rigid or contractual."
    },
    "Can I Skip or Pause?": {
        "response": (
            "Absolutely — you're never locked into the schedule. "
            "You can skip or pause anytime as long as you let us know at least 48 hours ahead."
        ),
        "why": "Gives the customer control and reduces fear of overpaying."
    },
    "Trust / Wants to Try Us First": {
        "response": (
            "Totally fair — a lot of people feel that way at first. "
            "That's why we make it simple and consistent, and if you're ever not happy for any reason, "
            "we handle switching you to a new pro so you don't have to start over."
        ),
        "why": "Acknowledges trust hesitation and uses your strongest service advantage to reduce risk."
    },
    "Selling Home": {
        "response": (
            "That actually works really well for this. We'll get it cleaned up, "
            "then keep it maintained while the home is being shown so you don't have to worry about it."
        ),
        "why": "Frames service as a simple solution for sellers."
    },
    "New Pool Owner / Needs Guidance": {
        "response": (
            "Yeah — that's super common. We handle the cleaning, chemicals, and balancing for you, "
            "so you don't have to figure it all out yourself."
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
            "That's what keeps the pool stable."
        ),
        "why": "Explains the logic behind recurring in a simple, confident way."
    },
    "Assumptive Close": {
        "response": (
            "Let's get that taken care of — I have the earliest 2-day window of Thursday or Friday available. "
            "Which works better for you?"
        ),
        "why": "Keeps momentum moving and guides the customer into the next step."
    },
}

TOP_10_LINES = [
    "What's the pool looking like right now?",
    "We start with a deep clean, then maintain it so it stays that way.",
    "Chemicals are included.",
    "Each visit includes cleaning, balancing, and filter care.",
    "Most customers are around $150/month.",
    "We do a few maintenance visits up front to keep everything stable.",
    "You can skip or pause anytime with 48 hours' notice.",
    "If you're not happy, we'll switch you to a new pro.",
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

    # Escape $ so Streamlit's KaTeX renderer doesn't treat $..$ as inline math
    safe_body = body.replace("$", "&#36;")

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
                {safe_body}
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
        f"${deep:,.0f}",
        f"${monthly:,.0f}",
        f"${visit:,.0f}",
        freq.lower()
    )

def show_step_hint(current_key: str, active_key: str, active_label: str) -> None:
    if current_key == active_key and active_label:
        st.caption(f"➡️ Next Step: {active_label}")

def show_active_marker(current_key: str, active_key: str) -> None:
    if current_key == active_key:
        st.info("🔵 Current Step")

def faq_card(question: str, answer: str, what_to_say: str) -> None:
    st.markdown(f"**{question}**")
    st.caption(answer)
    st.success(f'💬 "{what_to_say}"')
    st.markdown("---")

# -----------------------------
# HEADER
# -----------------------------
st.title("🏊 Pool Sales Call Guide")
st.caption("Built for live rep support, objection handling, and fast pool call guidance.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📞 Full Call Flow",
    "⚡ Objection Assistant",
    "🎭 Scenario Mode",
    "🧠 Rep FAQ",
    "❓ FAQs",
    "📖 Pool Terms"
])

# -----------------------------
# TAB 1: FULL CALL FLOW
# -----------------------------
with tab1:
    st.subheader("Full Pool Call Flow")
    st.caption("Simple, trustworthy guide-to-sale from greeting to close.")

    setup_col1, setup_col2, setup_col3 = st.columns([2, 1.5, 2])
    with setup_col1:
        rep_name = st.text_input("Your Name", value="Heather", placeholder="Enter your name...", key="rep_name_input")
        if not rep_name.strip():
            rep_name = "Heather"
    with setup_col2:
        state = st.radio("State", ["FL", "GA", "TX"], horizontal=True, key="state_select")
    with setup_col3:
        pool_condition = st.radio("Pool Condition", ["Clear", "Cloudy", "Green", "Black"], horizontal=True, key="pool_condition")

    # Deep clean decision for clear pools happens mid-flow, after value anchoring
    # For all other conditions it's always required
    needs_deep_clean = True  # default; Clear pools override this via mid-flow radio

    # Pricing defaults driven by state + condition
    _fl = state == "FL"
    _dc_defaults = {
        "Clear":  100.0 if _fl else 200.0,
        "Cloudy": 100.0 if _fl else 200.0,
        "Green":  300.0 if _fl else 500.0,
        "Black":  500.0 if _fl else 1000.0,
    }
    _pv_defaults = {"FL": 38.0, "GA": 82.0, "TX": 60.0}
    _default_dc = _dc_defaults[pool_condition]
    _default_pv = _pv_defaults[state]

    st.info("""
    🔥 Live Call Reminders  •  Mirror first → anchor the value → then price  •  Don't introduce objections early  •  If resistance appears, go to Tab 2

    💙 Human Moment Rule: When a customer shares something personal ("my wife was in the hospital", "she passed away") — pause, acknowledge it, then continue naturally. "I'm really sorry to hear that — let's make this easy for you." Never skip it. Never overdo it.
    """)

    step_order = [
        ("chk_mirror", "Mirrored & Bridged"),
        ("chk_anchor", "Value Anchored"),
        ("chk_contact", "Contact Info"),
        ("chk_price", "Pricing"),
        ("chk_serviceincl", "What's Included"),
        ("chk_close", "Attempted Close"),
        ("chk_email", "Email"),
        ("chk_property", "Property Details Confirmed"),
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
            "Deep Clean Price",
            min_value=0.0,
            step=1.0,
            value=_default_dc,
            key=f"deep_clean_input_{state}_{pool_condition}"
        )

    with q2:
        recurring_visit_input = st.number_input(
            "Recurring Price Per Visit",
            min_value=0.0,
            step=1.0,
            value=_default_pv,
            key=f"recurring_visit_input_{state}"
        )

    with q3:
        recurring_frequency = st.selectbox(
            "Frequency",
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

    st.markdown("### 👋 Start Here")
    gcol1, gcol2 = st.columns(2)
    with gcol1:
        info_card(
            "📞 Inbound Call",
            f"Hey this is {rep_name} with Home Gnome — I can help you get your pool taken care of today.\n\n"
            "What's the pool looking like right now — clear, cloudy, or starting to turn green?"
        )
    with gcol2:
        info_card(
            "💬 Outbound / SMS Follow-Up",
            f"Hey this is {rep_name} with Home Gnome — you were just texting us about pool service.\n\n"
            "I can get you a quote and walk you through everything real quick.\n\n"
            "What's the pool looking like right now — clear, cloudy, or starting to turn green?"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        # --- STEP 1: MIRROR THEIR SITUATION ---
        show_active_marker("chk_mirror", active_step_key)

        mirror_body = (
            "Repeat back exactly what the customer said — in their words, not yours. "
            "This shows you heard them before you start talking.\n\n"
            "They say: \"I just need the floor vacuumed, that's it.\"\n"
            "You say: \"Got it — so you're looking to get the floor cleaned out. "
            "Let me walk you through what we can do for you.\"\n\n"
            "They say: \"I want an acid wash.\"\n"
            "You say: \"Got it — you're looking for an acid wash. "
            "Let me tell you about what we can offer.\"\n\n"
            "They say: \"I just need a one-time clean.\"\n"
            "You say: \"Got it — you're looking for a one-time service. "
            "Here's what that looks like with us.\"\n\n"
            "They say: \"I just need the chemicals balanced.\"\n"
            "You say: \"Got it — you want someone to come balance everything out. "
            "I can get you set up.\"\n\n"
            "We don't offer vacuum-only or acid washes — but you validate FIRST, "
            "then bridge to what we CAN do. Never skip the mirror."
        )

        info_card("1. Mirror Their Request", mirror_body, highlight=(active_step_key == "chk_mirror"))
        st.checkbox("✔️ Mirrored & Bridged", key="chk_mirror")
        show_step_hint("chk_mirror", active_step_key, active_step_label)

        # --- STEPS 2-4: ANCHOR THE VALUE ---
        show_active_marker("chk_anchor", active_step_key)

        if pool_condition == "Clear":
            why_body = (
                "\"So in situations like yours, where the pool is already clear, what we typically recommend is a lighter deep clean first — "
                "not because anything is wrong, but because it resets anything sitting underneath that you can't see yet.\n\n"
                "Even when it looks clean, there's usually buildup starting along the walls, floor, or filter system — "
                "and if we knock that out now, it keeps you from dealing with algae or stains popping up later.\""
            )
            skip_body = (
                "\"If you skip that reset, what usually happens is buildup starts catching up — you get staining, algae spots, "
                "or the chemistry starts drifting — and you end up chasing it instead of just maintaining it.\""
            )
            outcome_body = (
                "\"What the deep clean does is fully reset everything so when we're done, it's clean underneath, not just on the surface. "
                "From there, maintenance keeps it that way without you ever having to fight it.\""
            )
        elif pool_condition == "Cloudy":
            why_body = (
                "\"So the reason we start with a deep clean — even when the water looks like it might just need some chemicals — "
                "is because what's causing the cloudiness is usually sitting in the filter system or walls.\n\n"
                "What happens is people add chemicals, it clears up for a bit, but it keeps coming back because the root cause was never fully addressed.\""
            )
            skip_body = (
                "\"If you skip that step, what usually happens is it either doesn't fully clear, or it comes right back within a couple weeks — "
                "and you end up spending more time and money chasing it.\""
            )
            outcome_body = (
                "\"What the deep clean does is fully reset everything — so when we're done, it's actually clean underneath, not just on the surface. "
                "From there, maintenance keeps it that way without you having to fight it every week.\""
            )
        elif pool_condition == "Green":
            why_body = (
                "\"So the reason we start with a deep clean is because algae doesn't just live in the water — it embeds in the surfaces and filter.\n\n"
                "What happens is people shock it, it turns blue for a day or two, but then it comes right back because it was never fully treated and reset.\""
            )
            skip_body = (
                "\"If you skip that step, it either doesn't fully clear or it comes right back within a couple weeks — "
                "and you end up spending more time and money chasing it.\""
            )
            outcome_body = (
                "\"What the deep clean does is fully reset everything — so when we're done, it's actually clean underneath, not just on the surface. "
                "From there, maintenance keeps it that way.\""
            )
        else:  # Black
            why_body = (
                "\"So black algae is one of the hardest things to remove — it has roots that go into the surface.\n\n"
                "You can add chemicals all day and it won't fully clear because the roots are still there. The deep clean is what actually gets it out.\""
            )
            skip_body = (
                "\"If we skip the deep clean, it comes right back — black algae is relentless. This is the only way to actually solve it.\""
            )
            outcome_body = (
                "\"What the deep clean does is fully reset everything — gets the roots out, treats the surface, balances the water. "
                "From there, weekly maintenance keeps it from ever coming back.\""
            )

        info_card("2. Why a Deep Clean Exists", why_body, highlight=(active_step_key == "chk_anchor"))
        info_card("3. What Happens If They Skip It", skip_body)
        info_card("4. Paint the Outcome", outcome_body)

        # Clear pool only: deep clean decision point (shown AFTER value is anchored)
        if pool_condition == "Clear":
            dc_price = 100 if _fl else 200
            dc_choice = st.radio(
                "How would you like to proceed?",
                [f"Include deep clean — ${dc_price} (recommended)", "Skip deep clean — weekly maintenance only"],
                key="clear_dc_choice"
            )
            needs_deep_clean = "Include deep clean" in dc_choice

            if not needs_deep_clean:
                st.info(
                    "💬 **If they hesitate on the deep clean:**\n\n"
                    "\"Totally fair — honestly a lot of people feel that way when the pool already looks clean.\"\n\n"
                    "*(pause — let that land)*\n\n"
                    "\"We can absolutely start you with just the weekly maintenance and skip that first reset if you'd prefer.\"\n\n"
                    "\"The only difference is we're maintaining what's there instead of fully resetting it — but if everything's been staying clean for you, that can still work just fine.\""
                )

        st.checkbox("✔️ Value Anchored", key="chk_anchor")
        show_step_hint("chk_anchor", active_step_key, active_step_label)

        # --- STEP 5: VERIFY CUSTOMER INFORMATION ---
        show_active_marker("chk_contact", active_step_key)

        info_card(
            "5. Verify Customer Information",
            "Before I pull exact pricing, let me just make sure I've got the right info.\n\n"
            "I have your (NAME) as — did I get that right?\n"
            "And I have the service address as (ADDRESS) — is that correct?\n"
            "And is (PHONE) still the best number for you?",
            highlight=(active_step_key == "chk_contact")
        )

        st.checkbox("✔️ Contact Info Verified", key="chk_contact")
        show_step_hint("chk_contact", active_step_key, active_step_label)

        # --- STEP 6: PRICING ---
        show_active_marker("chk_price", active_step_key)

        _monthly_hint = f"📌 If they ask about monthly: \"Most customers are around ${monthly_display} per month — it's billed per visit so you only pay for what's completed.\""
        if pool_condition == "Clear" and not needs_deep_clean:
            pricing_body = (
                f"It's ${recurring_display} per visit for weekly maintenance — so you're only paying for completed service.\n\n"
                f"{_monthly_hint}"
            )
        elif pool_condition == "Clear":
            pricing_body = (
                f"To get everything dialed in from the start, it's ${deep_clean_display} for the initial deep clean — "
                f"that gets your pro fully calibrated so the ongoing service runs exactly the way it should.\n\n"
                f"After that, it's ${recurring_display} per visit for weekly maintenance — so you're only paying for completed service.\n\n"
                f"{_monthly_hint}"
            )
        elif pool_condition == "Black":
            pricing_body = (
                f"That deep clean is ${deep_clean_display} for the first visit — that's what gets everything properly treated and reset.\n\n"
                f"After that, it's ${recurring_display} per visit for weekly maintenance — so you're only paying for completed service.\n\n"
                f"{_monthly_hint}"
            )
        else:  # Cloudy or Green
            pricing_body = (
                f"That deep clean is ${deep_clean_display} for the first visit.\n\n"
                f"After that, it's ${recurring_display} per visit for weekly maintenance — so you're only paying for completed service.\n\n"
                f"{_monthly_hint}"
            )
        info_card("6. Pricing", pricing_body, highlight=(active_step_key == "chk_price"))

        st.checkbox("✔️ Pricing Clearly Explained", key="chk_price")
        show_step_hint("chk_price", active_step_key, active_step_label)

        show_active_marker("chk_serviceincl", active_step_key)

        info_card(
            "7. What's Included",
            "Every visit — skimming, vacuuming, brushing, chemical balancing, "
            "and the filter cleaned as needed.\n\n"
            "The deep clean is all of that, plus:\n\n"
            "• shocking the pool\n"
            "• algaecide treatment\n"
            "• full filter & skimmer basket cleaning\n"
            "• before & after photos\n\n"
            "And all chemicals are included — nothing extra, ever.",
            highlight=(active_step_key == "chk_serviceincl")
        )
        st.checkbox("✔️ What's Included", key="chk_serviceincl")
        show_step_hint("chk_serviceincl", active_step_key, active_step_label)

        show_active_marker("chk_close", active_step_key)

        info_card(
            "8. Assumptive Close",
            "Let's get that pool taken care of — I have Thursday or Friday available as our first 2-day window. Does that work for you?",
            highlight=(active_step_key == "chk_close")
        )

        st.checkbox("✔️ Attempted Close", key="chk_close")
        show_step_hint("chk_close", active_step_key, active_step_label)

        show_active_marker("chk_email", active_step_key)

        info_card(
            "9. Email Verification",
            "Great — what's the best email for your account?\n\n"
            "I have your email as (PHONETICALLY SPELLED OUT @ ALWAYS.com).\n\n"
            "To confirm, just in case we have it wrong, your phone number is (___) ___-____.",
            highlight=(active_step_key == "chk_email")
        )

        st.checkbox("✔️ Email Verified", key="chk_email")
        show_step_hint("chk_email", active_step_key, active_step_label)
    
    with col2:

        show_active_marker("chk_property", active_step_key)

        info_card(
            "10. Property Details",
            "Are there any pets?\n"
            "If so, during the time of service, pets should be secured.\n\n"
            "Is the property in a gated community?\n"
            "If so, is there a gate code or special instructions for accessing the gate?",
            highlight=(active_step_key == "chk_property")
        )

        st.checkbox("✔️ Property Details Confirmed", key="chk_property")
        show_step_hint("chk_property", active_step_key, active_step_label)


        show_active_marker("chk_recap", active_step_key)

        info_card(
            "11. Order Recap",
            f"To confirm, we're scheduling you for "
            f"{'weekly maintenance only' if not needs_deep_clean else 'deep cleaning + weekly maintenance'}.\n\n"
            f"Your first visit is ${deep_clean_display if needs_deep_clean else recurring_display}, "
            f"and ongoing service is billed at ${recurring_display} per visit.",
            highlight=(active_step_key == "chk_recap")
        )

        st.checkbox("✔️ Recap", key="chk_recap")
        show_step_hint("chk_recap", active_step_key, active_step_label)


        show_active_marker("chk_policy", active_step_key)

        info_card(
            "12. Policy Disclosure (Verbatim)",
            "Quick heads-up: By booking, you agree to our Terms of Service.\n"
            "We just ask for at least 48 hours' notice if you ever need to change your schedule.\n"
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
            "and we won't charge you until 3 days after the service is complete.\n\n"
            "I'm sending over a secure link for you to add your payment info directly, since we don't have access to that on our end. "
            "This will go through text and email.",
            highlight=(active_step_key == "chk_payment")
        )

        st.checkbox("✔️ Payment Link Sent", key="chk_payment")
        show_step_hint("chk_payment", active_step_key, active_step_label)


        show_active_marker("chk_expectation", active_step_key)

        info_card(
            "14. Expectation Setting / App / Portal",
            "Once the crew adds the job to their route, you'll receive an email confirming your two-day window "
            "and letting you know a Pro picked the job up. At that point, you can message them directly.\n\n"
            "You'll also receive a text with a link to our free app and a temporary password — your email will be your username.\n\n"
            "Through the app and web login, you can request additional services, make changes to your account, "
            "and it's the fastest way to contact our Support Team.\n\n"
            "📋 Once you're logged in, there are a few important questions about your pool we'd love for you to answer — "
            "things like pool size and filtration details — so your Pro is fully prepared before they arrive.",
            highlight=(active_step_key == "chk_expectation")
        )

        st.checkbox("✔️ Expectation Set", key="chk_expectation")
        show_step_hint("chk_expectation", active_step_key, active_step_label)


        info_card(
            "15. Landline-Only Customers",
            "To log onto the website, enter your email address and click forgot password. "
            "You'll receive an email with a temporary password. Make sure to change the password once you log in.\n\n"
            "Websites:\n"
            "my.lawnstarter.com\n"
            "my.lawnlove.com\n"
            "my.homegnome.com"
        )

        show_active_marker("chk_nextdoor", active_step_key)

        info_card(
            "16. NextDoor Referral Credit",
            "When you log in to your account, you'll be able to recommend us on NextDoor. "
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
    1. Mirror their situation — show you heard them
    2. Explain why a deep clean exists
    3. What happens if they skip it
    4. Paint the outcome
    5. Verify name, address, and phone
    6. Give pricing (deep clean + per visit)
    7. Explain what's included
    8. Assumptive close
    9. Verify email
    10. Property details
    11. Order recap
    12. Policy disclosure
    13. Send payment link
    14. Set expectations for app + portal
    15. Nextdoor promo
    """)


    missing_steps = []

    if not st.session_state.get("chk_mirror"):
        missing_steps.append("Mirrored & Bridged")

    if not st.session_state.get("chk_anchor"):
        missing_steps.append("Value Anchored")

    if not st.session_state.get("chk_contact"):
        missing_steps.append("Contact Info")

    if not st.session_state.get("chk_price"):
        missing_steps.append("Pricing")

    if not st.session_state.get("chk_serviceincl"):
        missing_steps.append("What's Included")

    if not st.session_state.get("chk_close"):
        missing_steps.append("Attempted Close")

    if not st.session_state.get("chk_email"):
        missing_steps.append("Email")

    if not st.session_state.get("chk_property"):
        missing_steps.append("Property Details Confirmed")

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
        ["Needs Monthly Price", "Flat Monthly Request", "Comparing Lower Price", "Pay in Installments?"],
        ["Green Pool / Urgent", "Price Too High", "Just Shopping Around"],
        ["Only Wants One Clean", "Selling Home", "Wants to Think About It"],
        ["Who Is Coming?", "I've Been Ghosted Before", "Trust / Wants to Try Us First"],
        ["I Don't Want Ongoing Service", "Why Do I Need Weekly?", "Can I Skip or Pause?"],
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
            f"It's billed at {visit} per visit, but that's typically what it comes out to."
        )

        st.subheader("💡 Why This Works")
        st.info("Answers exactly what they asked for (monthly) without overcomplicating it.")

    elif selected == "Flat Monthly Request":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally get that — ours is billed per visit so you're only paying for completed service, "
            f"but most customers think of it as about {monthly} per month."
        )

        st.subheader("💡 Why This Works")
        st.info("Acknowledges preference while reinforcing your model as fair and flexible.")

    elif selected == "Comparing Lower Price":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Got it — most customers we work with are around {monthly} per month because everything's included — "
            f"cleaning, chemicals, and balancing — so there aren't extra costs popping up."
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
            f"It's billed at {visit} per visit, and that includes cleaning, chemicals, balancing, and filter care — "
            f"so there aren't extra costs."
        )

        st.subheader("💡 Why This Works")
        st.info("Anchors to monthly, reinforces value, removes hidden cost concern.")

    elif selected == "Only Wants One Clean":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"Totally get that — we'll start with the deep clean at {deep} to get everything reset.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service, "
            f"just to keep it from going right back."
        )

        st.subheader("💡 Why This Works")
        st.info("Keeps it simple and reframes maintenance as part of solving the problem.")

    elif selected == "Selling Home":
        st.subheader("🎯 Suggested Response")
        st.success(
            f"That makes sense — we hear that a lot with homes getting ready for photos and showings.\n\n"
            f"What we'll do is get it cleaned up first at {deep}, then keep it show-ready so you don't have to worry "
            f"about it slipping backward while the home is on the market.\n\n"
            f"Most customers are around {monthly} per month during that time."
        )

        st.subheader("💡 Why This Works")
        st.info("Aligns with the seller's goal: presentation and convenience.")

    elif selected == "I Don't Want Ongoing Service":
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
            "Absolutely — you're not locked in. You can skip or pause anytime as long as you let us know at least 48 hours ahead."
        )

        st.subheader("💡 Why This Works")
        st.info("Gives control and reduces fear of commitment.")

    elif selected == "Trust / Wants to Try Us First":
        st.subheader("🎯 Suggested Response")
        st.success(
            "Totally fair — a lot of people feel that way at first. "
            "If you're ever not happy, we handle switching you to a new pro so you don't have to start over."
        )

        st.subheader("💡 Why This Works")
        st.info("Reduces risk and builds trust quickly.")

    elif selected == "Pay in Installments?":
        st.subheader("🎯 Choose Your Response")
        st.caption("Pick the one that fits the customer's energy. All four keep momentum without being dismissive.")

        st.markdown("**Option 1 — Simple & confident** *(most calls)*")
        st.success(
            "I totally understand wanting to split that up. The deep clean is a one-time reset to get everything in the right condition, "
            "and after that it's just the smaller weekly maintenance — so it doesn't stay at that higher price."
        )

        st.markdown("**Option 2 — Value + reassurance** *(if they're focused on the total cost)*")
        st.success(
            "I get that. The deep clean is really what gets everything back to a clean, usable state, and then from there it's just the lower "
            "weekly visits to keep it that way — so you're not repeatedly paying that larger amount."
        )

        st.markdown("**Option 3 — Ease + close** *(if they're close to yes)*")
        st.success(
            "I hear you. The good news is that's just a one-time cost to get everything back in shape, and after that it drops down to the "
            "regular weekly service. Once it's done, it's much easier to maintain."
        )

        st.markdown("**Option 4 — If they're hesitating hard**")
        st.success(
            "I completely get wanting to break that up. Most customers go ahead with the deep clean so they don't end up dealing with bigger "
            "issues later, and then it's just the lower weekly visits to maintain it."
        )

        st.subheader("💡 Why This Works")
        st.info(
            "Never shut the door on a cost concern — reframe the deep clean as a one-time reset, not an ongoing expense. "
            "The pivot is always: 'that price doesn't repeat — it drops to the weekly rate after.'"
        )

    elif selected:
        show_response(selected)

    st.divider()

    with st.expander("🧠 When to Use Objection Handling"):
        st.markdown("""
Use this tab only when the customer gives resistance or hesitation.

**Examples:**
- “I only want one clean”
- “I'm still shopping around”
- “That sounds expensive”
- “I don't want to be locked in”
- “I've had bad luck with pool guys before”
- “I just want to see how you do first”

**Do not** front-load these into the main script unless the customer brings them up.
        """)

    with st.expander("🔥 Best Practice for Reps"):
        st.markdown("""
**1. Stay in the main flow first**  
Guide the customer through the service, pricing, and close.

**2. Only pull an objection response when needed**  
Do not introduce concerns they haven't raised.

**3. Answer briefly, then return to the sale**  
After handling the concern, move right back to closing.
        """)

    with st.expander("⚡ Best 'Return to Close' Lines"):
        st.markdown("""
- **Let's get that taken care of — I have Thursday or Friday available. Which works better?**
- **That's exactly why most people get started now — I do have availability this week.**
- **Totally fair — with that in mind, I can get you on the schedule for Thursday or Friday. Which works better?**
- **That makes sense — let's go ahead and lock in your first window so this is handled.**
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
            "Got it — that's exactly when most people reach out. "
            "What we'll do is start with a deep clean to get everything reset and balanced, "
            "then maintain it so it stays clean."
        )

        st.markdown("**Rep:**")
        st.success(
            "Chemicals are included, and our goal is simple — every visit, we leave your pool better than we found it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it's {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** That's kind of expensive.")

        st.markdown("**Rep:**")
        st.success(
            f"Totally fair — most customers we work with are around {monthly} per month, "
            "and that includes cleaning, chemicals, and balancing so you're not dealing with extra costs."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let's get that taken care of — I have Thursday or Friday available. Which works better?"
        )

    # -----------------------------
    # PRICE SHOPPER
    # -----------------------------
    elif scenario == "Price Shopper":
        st.markdown("### 💰 Price Shopper Call")

        st.markdown("**Customer:** I'm just calling around getting quotes.")

        st.markdown("**Rep:**")
        st.success(
            "Totally makes sense — most people we talk to are comparing options. "
            "I'll give you a clear picture so you can compare apples to apples."
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
            f"To get it cleaned up, it's {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** Okay, I'm still looking around.")

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
            "Yeah — that's super common. We handle the cleaning, chemicals, and balancing for you, "
            "so you don't have to figure it all out yourself."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we'll do is start with a deep clean if needed, then maintain it so it stays clean and consistent."
        )

        st.markdown("**Rep:**")
        st.success(
            "Our goal is simple — every visit, we leave your pool better than we found it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it's {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Customer:** Okay, that sounds helpful.")

        st.markdown("**Rep (close):**")
        st.success(
            "Perfect — let's get that taken care of. I have Thursday or Friday available. Which works better?"
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
            "then do a few maintenance visits so it doesn't go right back."
        )

        st.markdown("**Customer:** I just don't want to be locked into something.")

        st.markdown("**Rep:**")
        st.success(
            "Completely fair — that's really just to stabilize the pool after we clean it."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it's {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let's get that taken care of — I have Thursday or Friday available. Which works better?"
        )

    # -----------------------------
    # SELLING HOME
    # -----------------------------
    elif scenario == "Selling Home":
        st.markdown("### 🏠 Selling Home")

        st.markdown("**Customer:** I'm selling the house, so I just need the pool cleaned up.")

        st.markdown("**Rep:**")
        st.success(
            "That makes sense — we hear that a lot with homes getting ready for photos and showings."
        )

        st.markdown("**Rep:**")
        st.success(
            "What we'll do is get it cleaned up first, then keep it show-ready so you don't have to worry "
            "about it slipping backward while the home is on the market."
        )

        st.markdown("**Customer:** I really don't need long-term service.")

        st.markdown("**Rep:**")
        st.success(
            "Totally understand — the follow-up visits are really just to keep it looking good while buyers are coming through."
        )

        st.markdown("**Rep (pricing):**")
        st.success(
            f"To get it cleaned up, it's {deep} for the first visit.\n\n"
            f"After that, most customers are around {monthly} per month for weekly service — "
            f"billed at {visit} per visit."
        )

        st.markdown("**Rep (close):**")
        st.success(
            "Let's get that taken care of so the pool is one less thing on your plate — "
            "I have Thursday or Friday available. Which works better?"
        )

    st.divider()

    with st.expander("🧠 How to Use Scenario Mode"):
        st.markdown("""
- Use these as **confidence builders**, not word-for-word scripts every time.
- Keep the call moving.
- Don't introduce objections unless the customer raises them.
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
# TAB 4: REP FAQ / QUICK ANSWERS
# -----------------------------
with tab4:
    st.subheader("Rep FAQ / Quick Answers")
    st.caption("Fast answers for common rep questions. Check Current Process first on every pool call.")

    st.success("""
✅ **Normal Process — Use This Every Call**

**Use the sales tool → send the payment link. That's it.**
- Book through the sales tool as normal
- Send the customer the payment link
- Keep recording running — no pause needed
""")

    st.error("""
🚨 **Emergency Fallback — Only If Sales Tool Is Down**

If the sales tool is not working, revert to web signup:

1. **Pause** the Five9 recording
2. Use the correct web signup link for the brand:
   - **LawnStarter:** https://signup-web.lawnstarter.com/cart/contact-info?intent=poolCleaning&utm_source=sales
   - **Lawn Love:** https://signup-web.lawnlove.com/cart/contact-info?intent=poolCleaning&utm_source=sales
   - **Home Gnome:** https://signup-web.homegnome.com/cart/contact-info?intent=poolCleaning&utm_source=sales
3. Collect the card over the phone
4. **Resume** recording after card entry is complete
""")

    with st.expander("📋 Call Handling & Payment", expanded=True):
        faq_card(
            "Do I need to pause the recording?",
            "No — not under normal circumstances. Recording runs the whole call when using the sales tool.",
            "No action needed. Just book through the sales tool and send the payment link as usual."
        )
        faq_card(
            "When would I ever pause the recording?",
            "Only if the sales tool goes down and you must revert to web signup. In that case: pause recording → use web signup → collect card by phone → resume recording.",
            "I'm going to go ahead and take your card information now — I'll be entering it securely on my end while we talk."
        )
        faq_card(
            "Sales tool is down — what do I do?",
            "Revert to the emergency fallback process (see red box above). Web signup + card by phone + pause recording.",
            "I'm walking you through this right now — it'll just take a moment."
        )

    with st.expander("💰 Internal Pricing Reference"):
        st.warning("🔒 Internal use only — do not read aloud. Use the sales tool for customer-facing quotes.")
        st.markdown("""
| Condition | Florida | Non-Florida |
|-----------|---------|-------------|
| **Clear** | $100 | $200 |
| **Green** | $300 | $500 |
| **Black** | $500 | $1,000 |
        """)

# -----------------------------
# TAB 5: FAQs
# -----------------------------
with tab5:
    st.subheader("Frequently Asked Questions")
    st.caption("Quick answers to common customer questions — use these verbatim or as a guide.")

    faq_search = st.text_input("🔍 Search FAQs", placeholder="Type a keyword — e.g. chemicals, contract, cover, leak...")

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
        (
            "Q20: What does it mean to shock a pool?",
            "Shocking just means adding a strong dose of chlorine to quickly kill algae and bacteria — it's one of the first steps in turning a green pool back to clear.\n\n"
            "We'll handle all of that during the deep clean so you don't have to worry about it."
        ),
        (
            "Q21: How many deep cleans per year?",
            "Most customers only need a deep clean when the pool gets out of balance or turns green.\n\n"
            "After that, weekly maintenance keeps it in good shape so you don't have to go through that again.\n\n"
            "We'll get you set up so this is the last time you have to deal with it."
        ),
        (
            "Q22: Is there a contract?",
            "We don't have any contracts — you only pay for the service you receive.\n\n"
            "Most customers stick with us because the pool stays clean and it's one less thing they have to think about.\n\n"
            "We'll get you started with the deep clean and weekly service so you can see the difference right away."
        ),
        (
            "Q23: Will my price change after I enter my pool details?",
            "No — the price we quote you is the price you'll pay.\n\n"
            "After booking, you'll just log into the app and add a few pool details so your pro shows up fully prepared.\n\n"
            "It doesn't change your price — it just makes sure everything goes smoothly from the start."
        ),
        (
            "Q24: Are there any extra charges — like a deep clean fee or long grass fee?",
            "No — there are no surprise charges.\n\n"
            "The deep clean price covers getting your pool through that initial reset.\n\n"
            "After booking, you'll just add a few details in the app so your pro has everything they need. That way, everything is handled upfront and there are no unexpected costs."
        ),
        (
            "Q25: Are your pros licensed, bonded, and insured?",
            "Yes — they're vetted and covered, so if anything were to happen, you're protected.\n\n"
            "We make sure you're matched with someone qualified so you can feel confident from day one."
        ),
        (
            "Q26: If it takes multiple visits, does the price change?",
            "No — the deep clean price covers getting your pool through that initial reset.\n\n"
            "Some pools take a few visits to fully clear, and we stay on it until it's right without changing that price.\n\n"
            "That's exactly why we pair it with weekly service so it gets fully cleared and stays that way."
        ),
        (
            "Q27: What if the deep clean doesn't fix it?",
            "Green pools don't turn overnight, but we handle it step-by-step until it's right.\n\n"
            "The deep clean starts the reset, and if needed, we continue treatments over the first week until it fully clears.\n\n"
            "Weekly maintenance is what keeps it on track so it doesn't go back to green.\n\n"
            "We'll get you started so we can begin turning it around right away."
        ),
        (
            "Q28: How long does it take for the pool to turn clear?",
            "Most pools start improving within the first few visits, and depending on the condition, it can take about a week to fully clear.\n\n"
            "Green pools don't turn overnight, but we stay on it until it's where it should be.\n\n"
            "The sooner we start, the sooner you'll see it clear up."
        ),
        (
            "Q29: Will it be clear after the first visit?",
            "You'll usually see a big improvement right away.\n\n"
            "If it's heavily green, it can take a few treatments over that first week to fully clear.\n\n"
            "We stay on it until it gets there, which is why we set it up with weekly service."
        ),
        (
            "Q30: Why do I need weekly maintenance after the deep clean?",
            "The deep clean gets things started, but weekly service is what finishes the job and keeps it that way.\n\n"
            "Without it, pools can slip right back to green.\n\n"
            "We'll get you set up so you don't have to deal with this again."
        ),
        (
            "Q31: What if it turns green again?",
            "That's exactly what we're here to prevent.\n\n"
            "With weekly maintenance, we keep everything balanced and catch issues early before they turn into a bigger problem.\n\n"
            "We'll stay on top of it so it stays clear and ready to use."
        ),
        (
            "Q32: Can I just do the deep clean and then cancel?",
            "I totally get wanting to just knock it out in one visit.\n\n"
            "The way green pools work though — it usually takes a few treatments over that first week to fully clear, and without ongoing care it can come right back.\n\n"
            "So we set it up with weekly service to make sure it actually gets clear and stays that way.\n\n"
            "Let's get you started so we can begin turning it around right away.\n\n"
            "---\n\n"
            "**If they push back:**\n\n"
            "You do have flexibility, but we want to make sure you're not paying for a reset and ending up right back where you started.\n\n"
            "Starting with weekly service is what ensures you actually get the full result."
        ),
        (
            "Q33: Do you offer acid washes?",
            "We don't perform acid washes, but once that's completed, we can take over weekly maintenance to keep your pool clean, balanced, and looking great moving forward."
        ),
        (
            "Q34: Will the pro remove my pool cover?",
            "Yes, the pro will remove your pool cover as part of getting started."
        ),
        (
            "Q35: I need my pool opened — can you do that?",
            "Absolutely. We start with a deep clean to get everything reset, then move into weekly maintenance to keep it in great shape all season."
        ),
        (
            "Q36: I don't know what condition my pool is in.",
            "No problem at all — that's very common, especially if the cover is still on. We'll start with a full deep clean to get everything cleared up, then transition into weekly maintenance to keep it looking its best.",
            "Select **Green** as the pool condition when booking — this routes the job as a deep clean."
        ),
        (
            "Q37: How do I add pool to an existing customer account?",
            "",
            "Use this link to add pool service to an existing account: https://dki.io/10c0daae"
        ),
        (
            "Q38: Will you add water to my pool?",
            "We don't add water to the pool. We focus on cleaning, balancing, and maintaining the water that's there.\n\n"
            "If the pool needs to be filled first, we can absolutely get you set up on maintenance once it's ready."
        ),
        (
            "Q39: Can I use my pool right after you clean it?",
            "It depends on the condition. After a deep clean, the chemicals need a little time to balance out — your pro will let you know when it's safe to swim.\n\n"
            "For routine maintenance visits, you're typically good to go within a few hours."
        ),
        (
            "Q40: What if I can't see the pool because of a cover?",
            "No problem — if the water isn't visible, we treat it like a deeper clean to make sure everything is properly assessed and treated from the start.\n\n"
            "Your pro will take care of the cover and evaluate the condition when they arrive.",
            "Select **Green** as the pool condition when booking if the cover is on and condition is unknown."
        ),
        (
            "Q41: My pool is clear — do I still need a deep clean?",
            "Not necessarily. If your pool is already clear and the water looks good, we can start you directly on regular weekly maintenance — no deep clean required.\n\n"
            "We'll get things set up based on the current condition."
        ),
        (
            "Q42: Do I need to be home for the service?",
            "Nope — as long as the pro has access to the pool area, you're all set. You don't need to be home.\n\n"
            "If there's a gate code or anything we should know about, just add it to your account notes."
        ),
        (
            "Q43: Can the pro come inside my house?",
            "Our pros work entirely from outside — they just need access to the pool area and they're good to go.\n\n"
            "No need to be home or let anyone inside."
        ),
        (
            "Q44: What if I'm not satisfied with the service?",
            "We stand behind every visit. Here's what that looks like:\n\n"
            "- **Re-do or refund** — Tell us within 5 days if anything's off. We'll send your pro back or give you a full refund.\n"
            "- **Pay 3 days after service** — Your card isn't charged until 3 full days after the visit. Time to confirm you're happy.\n"
            "- **$2M property protection** — Every job is backed by $2 million in property damage protection. You're fully covered.\n"
            "- **Cancel or skip anytime** — No contracts. One tap to skip, pause, reschedule, or cancel. No penalty, no awkward calls."
        ),
        (
            "Q45: Do you offer leak detection? I just need that, not maintenance.",
            "We don't offer leak detection — for that, you'd want a pool repair specialist who handles diagnostics and equipment work.\n\n"
            "What we do is keep pools clean, balanced, and maintained. If you get the leak sorted and want someone to take care of the water side going forward, we'd be glad to help at that point."
        ),
    ]

    search_term = faq_search.strip().lower()
    matched = 0

    for faq in faqs:
        question, answer = faq[0], faq[1]
        rep_note = faq[2] if len(faq) > 2 else None

        if search_term:
            searchable = (question + " " + answer + " " + (rep_note or "")).lower()
            if search_term not in searchable:
                continue

        matched += 1
        auto_expand = bool(search_term)
        with st.expander(question, expanded=auto_expand):
            if answer:
                st.success(answer)
            if rep_note:
                st.warning(f"🔒 **Rep note (don't read aloud):** {rep_note}")

    if search_term and matched == 0:
        st.info("No matching questions found. Try a different keyword.")

# -----------------------------
# TAB 6: POOL TERMS
# -----------------------------
with tab6:
    st.subheader("Pool Terms Glossary")
    st.caption("Plain-language definitions and analogies to help reps explain pool concepts with confidence.")

    terms = [
        (
            "Chlorine",
            "Kills bacteria and algae in the water.",
            "It's like soap for your pool — it keeps everything clean and safe."
        ),
        (
            "Shock",
            "A strong dose of chlorine used to quickly clean up a problem.",
            "It's like a deep clean or power wash — used when things get out of control."
        ),
        (
            "Stabilizer (Cyanuric Acid / CYA)",
            "Protects chlorine from being burned off by the sun.",
            "It's like sunscreen for your pool — without it, chlorine disappears fast in the sun."
        ),
        (
            "pH Balance",
            "Measures how acidic or basic the water is.",
            "It's like keeping your skin balanced — too high or too low and things get irritated."
        ),
        (
            "Total Alkalinity",
            "Acts as a buffer that keeps pH from swinging up and down.",
            "It's like the shock absorbers on a car — it keeps pH from bouncing all over the place when you add chemicals."
        ),
        (
            "Calcium Hardness",
            "Measures how much calcium is dissolved in the water.",
            "It's like mineral content in drinking water — too low and the water starts eating away at surfaces; too high and it leaves scale buildup."
        ),
        (
            "Algaecide",
            "Prevents or kills algae growth.",
            "It's like weed killer for your pool."
        ),
        (
            "Clarifier",
            "Causes tiny particles that are too small for the filter to catch to clump together so the filter can remove them.",
            "It's like a magnet for cloudiness — it groups the tiny invisible particles together so the filter can actually grab them. Used when the water is hazy blue but not fully clearing."
        ),
        (
            "Flocculant (Floc)",
            "A heavy-duty version of clarifier — causes particles to sink to the bottom so they can be vacuumed out.",
            "It's like dropping a net through the water — everything clumps and falls to the bottom so you can vacuum it out. Used for really cloudy or green pools."
        ),
        (
            "Metal Sequestrant",
            "Binds metals in the water so they don't stain the pool or discolor the water.",
            "It's like a rust remover — it grabs metals like iron and copper so they can't leave stains on the walls or turn the water a weird color."
        ),
        (
            "Filter",
            "Removes dirt, debris, and particles from the water.",
            "It's like your pool's vacuum or air filter — constantly cleaning in the background."
        ),
        (
            "Saltwater Pool",
            "Uses salt to generate chlorine automatically.",
            "It's like a self-cleaning system — it makes its own chlorine instead of adding it manually."
        ),
        (
            "Chlorine Pool",
            "Traditional pool where chlorine is added manually.",
            "Like adding detergent to a washing machine — it needs to be maintained regularly."
        ),
        (
            "Brushing",
            "Scrubbing pool walls and surfaces.",
            "Like brushing your teeth — prevents buildup before it becomes a problem."
        ),
        (
            "Vacuuming",
            "Removing debris from the bottom of the pool.",
            "Like vacuuming your floors — keeps everything looking clean."
        ),
        (
            "Balancing Chemicals",
            "Keeping all water chemistry levels in the correct range.",
            "Like maintaining a healthy diet — everything needs to be in the right balance."
        ),
    ]

    for term, definition, analogy in terms:
        with st.expander(term):
            st.markdown(f"**What it is:** {definition}")
            st.info(f"💡 **Analogy:** {analogy}")