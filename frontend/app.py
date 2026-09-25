import os

import requests
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/api/change-requests",
)

st.set_page_config(
    page_title="FCRM Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "request_id" not in st.session_state:
    st.session_state.request_id = ""

if "assessment" not in st.session_state:
    st.session_state.assessment = None


# ============================================================
# UI STYLE
# ============================================================

st.markdown(
    """
<style>

/* GLOBAL */

.stApp {
    background:
        radial-gradient(
            circle at 85% 0%,
            rgba(37, 99, 235, 0.08),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #f5f9ff 0%,
            #eef5fc 48%,
            #f8fbff 100%
        );

    color: #14213d;
    font-weight: 600;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    background: rgba(247, 251, 255, 0.92);
}

#MainMenu,
footer {
    visibility: hidden;
}


/* TYPOGRAPHY */

.main h1 {
    color: #0b2545 !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
}

.main h2 {
    color: #102f55 !important;
    font-weight: 850 !important;
}

.main h3 {
    color: #123d68 !important;
    font-weight: 800 !important;
}

.main p {
    color: #253b53 !important;
    font-weight: 600 !important;
}

.main label {
    color: #243b53 !important;
    font-weight: 700 !important;
}

[data-testid="stCaptionContainer"] {
    color: #536b82 !important;
    font-weight: 600 !important;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #071d3b 0%,
            #092a54 55%,
            #071b36 100%
        );

    border-right: 1px solid rgba(8, 45, 85, 0.25);
    box-shadow: 5px 0 30px rgba(15, 50, 90, 0.10);
}

section[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-weight: 900 !important;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #f4f8ff !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"]
[data-testid="stCaptionContainer"] {
    color: #b8cee5 !important;
    font-weight: 650 !important;
}

section[data-testid="stSidebar"]
[data-testid="stRadio"] label {
    padding: 10px;
    border-radius: 10px;
    transition: all 0.15s ease;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"]
[data-testid="stRadio"] label:hover {
    background: rgba(52, 132, 255, 0.16);
    transform: translateX(2px);
}


/* INPUTS */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: #ffffff !important;
    border: 1px solid #cad9e8 !important;
    border-radius: 10px !important;
}

input,
textarea {
    color: #152238 !important;
    background: #ffffff !important;
    font-weight: 600 !important;
}

input::placeholder,
textarea::placeholder {
    color: #8a9bad !important;
}

div[data-baseweb="select"] span {
    color: #152238 !important;
    font-weight: 650 !important;
}

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label {
    font-weight: 750 !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="input"] > div {
    background: #ffffff !important;
}

section[data-testid="stSidebar"] input {
    color: #152238 !important;
}


/* METRIC CARDS */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #ffffff 0%,
            #f7fbff 100%
        );

    border: 1px solid #dce8f4;
    border-radius: 16px;
    padding: 18px 20px;

    box-shadow:
        0 8px 24px rgba(33, 73, 118, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #40566d !important;
    font-size: 0.92rem;
    font-weight: 800 !important;
}

div[data-testid="stMetricValue"] {
    color: #0d3b70 !important;
    font-weight: 900 !important;
}


/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button {
    min-height: 45px;
    border-radius: 10px;
    font-weight: 800 !important;

    background:
        linear-gradient(
            135deg,
            #1769d2,
            #2787ef
        );

    color: #ffffff !important;
    border: 1px solid #1769d2;

    box-shadow:
        0 5px 14px rgba(23, 105, 210, 0.18);

    transition: all 0.15s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px);

    background:
        linear-gradient(
            135deg,
            #115ab8,
            #1e75d4
        );

    color: #ffffff !important;

    box-shadow:
        0 8px 20px rgba(23, 105, 210, 0.24);
}


/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 12px;
    font-weight: 700 !important;
}


/* FORMS */

[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid #dce8f3;
    border-radius: 16px;
    padding: 20px;

    box-shadow:
        0 8px 25px rgba(33, 73, 118, 0.05);
}


/* DATAFRAME */

div[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #dce7f2;
    border-radius: 14px;
    overflow: hidden;
    font-weight: 650 !important;

    box-shadow:
        0 6px 18px rgba(33, 73, 118, 0.05);
}


/* EXPANDERS */

div[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #dce7f2;
    border-radius: 13px;

    box-shadow:
        0 5px 16px rgba(33, 73, 118, 0.05);
}

div[data-testid="stExpander"] summary {
    color: #123f75 !important;
    font-weight: 800 !important;
}


/* TABS */

button[data-baseweb="tab"] {
    color: #536b82 !important;
    font-weight: 750 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #1769d2 !important;
    font-weight: 850 !important;
}


/* CHECKBOX */

[data-testid="stCheckbox"] label {
    color: #34495e !important;
    font-weight: 700 !important;
}


/* DIVIDER */

hr {
    border-color: #dce7f2 !important;
}


/* PLOTLY */

[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.55);
    border-radius: 16px;
}


/* SCROLLBAR */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #eef4fa;
}

::-webkit-scrollbar-thumb {
    background: #b6c9dc;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #91adc8;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# API
# ============================================================

def api_request(method, endpoint, payload=None):

    try:

        response = requests.request(
            method=method,
            url=f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=90,
        )

        if response.status_code >= 400:

            try:
                data = response.json()
                message = data.get(
                    "detail",
                    response.text,
                )

            except Exception:
                message = response.text

            return None, f"{response.status_code}: {message}"

        if response.content:

            try:
                return response.json(), None

            except Exception:
                return {}, None

        return {}, None

    except requests.exceptions.ConnectionError:

        return (
            None,
            "FastAPI backend is not running. "
            "Start it using: uvicorn src.main:app --reload",
        )

    except requests.exceptions.Timeout:

        return None, "Backend request timed out."

    except Exception as exc:

        return None, str(exc)


# ============================================================
# HELPERS
# ============================================================

def current_request_id():
    return st.session_state.request_id.strip()


def get_request(request_id):

    return api_request(
        "GET",
        f"/{request_id}",
    )


def page_title(title, description):

    st.title(title)
    st.caption(description)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ FCRM")

    st.markdown(
        "**Risk Intelligence**"
    )

    st.caption(
        "Financial Crime Risk Management"
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "🏠 Executive Dashboard",
            "➕ New Change Request",
            "✨ AI Risk Assessment",
            "👤 Analyst Review",
            "🏛️ Risk Committee",
            "🕒 Audit Trail",
        ],
    )

    st.divider()

    st.subheader(
        "Active Case"
    )

    entered_id = st.text_input(
        "Request ID",
        value=st.session_state.request_id,
        placeholder="e.g. CR-DEMO-001",
    )

    entered_id = entered_id.strip()

    if entered_id != st.session_state.request_id:

        st.session_state.request_id = entered_id
        st.session_state.assessment = None

    if current_request_id():

        st.success(
            f"● {current_request_id()}"
        )

    else:

        st.info(
            "No case selected"
        )

    st.divider()

    st.caption(
        "SYSTEM STATUS"
    )

    st.success(
        "● Risk Engine"
    )

    st.success(
        "● Groq AI"
    )

    st.success(
        "● Policy Knowledge"
    )

    st.caption(
        "Human decision required"
    )


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "🏠 Executive Dashboard":

    st.caption(
        "WELCOME TO"
    )

    st.title(
        "FCRM Risk Intelligence"
    )

    st.markdown(
        "AI-assisted financial crime risk assessment "
        "workspace for **governed, explainable and "
        "auditable decision making.**"
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info(
            "✨ **AI-Powered Analysis**"
        )

    with c2:
        st.info(
            "📚 **Policy Grounded**"
        )

    with c3:
        st.info(
            "👤 **Human Controlled**"
        )

    with c4:
        st.info(
            "🕒 **Audit Ready**"
        )

    st.write("")

    cases, error = api_request(
        "GET",
        "/",
    )

    if error:

        st.error(error)
        cases = []

    if not isinstance(cases, list):
        cases = []

    total = len(cases)

    submitted = sum(
        1
        for item in cases
        if item.get("status") == "submitted"
    )

    under_review = sum(
        1
        for item in cases
        if item.get("status") == "under_review"
    )

    committee = sum(
        1
        for item in cases
        if item.get("status") == "committee_review"
    )

    decided = sum(
        1
        for item in cases
        if item.get("status") == "decided"
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "📁 Total Cases",
            total,
        )

    with k2:
        st.metric(
            "🔎 Under Review",
            under_review,
        )

    with k3:
        st.metric(
            "🏛️ Committee Review",
            committee,
        )

    with k4:
        st.metric(
            "✅ Decided",
            decided,
        )

    st.write("")

    left, right = st.columns(
        [0.85, 1.4],
        gap="large",
    )

    with left:

        st.subheader(
            "Case Portfolio Overview"
        )

        values = [
            submitted,
            under_review,
            committee,
            decided,
        ]

        labels = [
            "Submitted",
            "Under Review",
            "Committee",
            "Decided",
        ]

        if sum(values) > 0:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.67,
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                    )
                ]
            )

            fig.update_layout(
                height=300,

                margin=dict(
                    l=10,
                    r=10,
                    t=15,
                    b=35,
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#243b53",
                    size=14,
                ),

                legend=dict(
                    orientation="h",
                    y=-0.10,
                    x=0.5,
                    xanchor="center",
                    font=dict(
                        size=13,
                    ),
                ),

                annotations=[
                    dict(
                        text=(
                            f"<b>{total}</b>"
                            "<br><b>Total Cases</b>"
                        ),
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(
                            size=18,
                            color="#123f75",
                        ),
                    )
                ],
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

        else:

            st.info(
                "No cases available yet."
            )

    with right:

        st.subheader(
            "Governed Assessment Lifecycle"
        )

        top = st.columns(4)

        with top[0]:
            st.success(
                "📄 01\n\n"
                "**Change Intake**"
            )

        with top[1]:
            st.success(
                "⚙️ 02\n\n"
                "**Risk Engine**"
            )

        with top[2]:
            st.info(
                "📚 03\n\n"
                "**Policy Retrieval**"
            )

        with top[3]:
            st.info(
                "✨ 04\n\n"
                "**AI Assessment**"
            )

        bottom = st.columns(3)

        with bottom[0]:
            st.warning(
                "👤 05\n\n"
                "**Analyst Review**"
            )

        with bottom[1]:
            st.warning(
                "🏛️ 06\n\n"
                "**Risk Committee**"
            )

        with bottom[2]:
            st.success(
                "✓ 07\n\n"
                "**Decision & Audit**"
            )

        st.write("")

        st.info(
            "🔒 **Human Decision Required** — "
            "AI supports analysis and drafting. "
            "Final decisions remain with authorized "
            "FCRM professionals."
        )

    st.divider()

    # IMPORTANT:
    # Change-request details stay hidden until this is opened.
    with st.expander(
        "📁 View Change Requests",
        expanded=False,
    ):

        st.caption(
            "Case details are hidden from the "
            "executive dashboard by default."
        )

        if cases:

            rows = []

            for item in reversed(
                cases[-10:]
            ):

                rows.append(
                    {
                        "Request ID":
                            item.get(
                                "request_id",
                                "",
                            ),

                        "Change":
                            item.get(
                                "name",
                                "",
                            ),

                        "Type":
                            item.get(
                                "change_type",
                                "",
                            ),

                        "Business Unit":
                            item.get(
                                "business_unit",
                                "",
                            ),

                        "Status":
                            item.get(
                                "status",
                                "",
                            ),

                        "Decision":
                            item.get(
                                "decision"
                            )
                            or "Pending",
                    }
                )

            st.dataframe(
                rows,
                width="stretch",
                hide_index=True,
            )

        else:

            st.info(
                "No change requests available."
            )


# ============================================================
# NEW CHANGE REQUEST
# ============================================================

elif page == "➕ New Change Request":

    page_title(
        "New Change Request",
        "Register a proposed business change "
        "for Financial Crime Risk Management review.",
    )

    st.info(
        "📋 **Submit the proposed change information.** "
        "This becomes the starting context for "
        "the FCRM assessment."
    )

    with st.form(
        "new_change_request_form"
    ):

        left, right = st.columns(2)

        with left:

            request_id = st.text_input(
                "Request ID *",
                placeholder="CR-DEMO-001",
            )

            name = st.text_input(
                "Change Name *",
                placeholder="International Digital Wallet",
            )

            change_type = st.selectbox(
                "Change Type",
                [
                    "new_product",
                    "new_feature",
                    "process_change",
                    "new_vendor",
                    "new_geography",
                    "new_customer_segment",
                ],
            )

            business_unit = st.text_input(
                "Business Unit",
                value="Consumer Banking",
            )

        with right:

            geography = st.text_input(
                "Geography",
                value="United Kingdom",
            )

            customer_segment = st.text_input(
                "Customer Segment",
                value="Retail Customers",
            )

            submitted_by = st.text_input(
                "Submitted By",
                value="product.owner",
            )

            vendor_involved = st.checkbox(
                "Third-party vendor involved",
                value=True,
            )

        description = st.text_area(
            "Business Change Description *",

            value=(
                "Introduce an international digital payment "
                "capability for retail customers using a "
                "third-party payment provider."
            ),

            height=140,
        )

        create_request = st.form_submit_button(
            "Submit for FCRM Assessment",
            type="primary",
            width="stretch",
        )

    if create_request:

        if (
            not request_id.strip()
            or not name.strip()
            or not description.strip()
        ):

            st.error(
                "Request ID, Change Name and "
                "Description are required."
            )

        else:

            payload = {
                "request_id": request_id.strip(),
                "name": name.strip(),
                "description": description.strip(),
                "change_type": change_type,
                "business_unit": business_unit.strip(),
                "geography": geography.strip(),
                "customer_segment": customer_segment.strip(),
                "vendor_involved": vendor_involved,
                "submitted_by": submitted_by.strip(),
            }

            result, error = api_request(
                "POST",
                "/",
                payload,
            )

            if error:

                st.error(error)

            else:

                st.session_state.request_id = request_id.strip()
                st.session_state.assessment = None

                st.success(
                    "✓ Change request created successfully."
                )

                st.info(
                    f"**Active Case:** {request_id.strip()}\n\n"
                    "Next → Open **AI Risk Assessment**."
                )


# ============================================================
# AI RISK ASSESSMENT
# ============================================================

elif page == "✨ AI Risk Assessment":

    page_title(
        "AI Risk Assessment",
        "Run deterministic risk scoring, policy retrieval "
        "and AI-assisted assessment drafting.",
    )

    request_id = current_request_id()

    if not request_id:

        st.warning(
            "Select or create a Request ID first."
        )

    else:

        request_data, error = get_request(
            request_id
        )

        if error:

            st.error(error)

        else:

            status = request_data.get(
                "status",
                "unknown",
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Case",
                    request_id,
                )

            with c2:
                st.metric(
                    "Workflow Status",
                    status.replace(
                        "_",
                        " ",
                    ).title(),
                )

            with c3:
                st.metric(
                    "Business Unit",
                    request_data.get(
                        "business_unit",
                        "N/A",
                    ),
                )

            st.info(
                "🤖 **AI Advisory Boundary** — "
                "AI identifies risk drivers, retrieves "
                "policy context and prepares a draft assessment. "
                "**It cannot approve or reject the change.**"
            )

            if status == "submitted":

                st.warning(
                    "**Start FCRM Review** before "
                    "running the AI assessment."
                )

                if st.button(
                    "▶ Start FCRM Review",
                    type="primary",
                    width="stretch",
                ):

                    result, error = api_request(
                        "PATCH",
                        f"/{request_id}/start-review",
                    )

                    if error:

                        st.error(error)

                    else:

                        st.success(
                            "✓ FCRM review started."
                        )

                        st.rerun()

            if status == "under_review":

                if st.button(
                    "✨ Run AI-Assisted Risk Assessment",
                    type="primary",
                    width="stretch",
                ):

                    with st.spinner(
                        "Risk Engine → Policy Retrieval → Groq AI..."
                    ):

                        result, error = api_request(
                            "POST",
                            f"/{request_id}/run-assessment",
                        )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.assessment = result

                        st.success(
                            "✓ AI assessment completed."
                        )

            assessment = st.session_state.assessment

            if assessment:

                st.divider()

                st.subheader(
                    "Risk Assessment Result"
                )

                risk_score = assessment.get(
                    "risk_score",
                    0,
                )

                risk_rating = assessment.get(
                    "risk_rating",
                    "UNKNOWN",
                )

                r1, r2, r3 = st.columns(3)

                with r1:
                    st.metric(
                        "Risk Rating",
                        risk_rating,
                    )

                with r2:
                    st.metric(
                        "Risk Score",
                        risk_score,
                    )

                with r3:
                    st.metric(
                        "Decision Authority",
                        "Human",
                    )

                left, right = st.columns(
                    [0.8, 1.5],
                    gap="large",
                )

                with left:

                    fig = go.Figure(
                        go.Indicator(
                            mode="gauge+number",

                            value=risk_score,

                            title={
                                "text":
                                    "<b>FCRM Risk Score</b>"
                            },

                            gauge={
                                "axis": {
                                    "range": [0, 100]
                                },

                                "steps": [
                                    {
                                        "range": [0, 30],
                                        "color":
                                            "rgba(34,197,94,.20)",
                                    },
                                    {
                                        "range": [30, 60],
                                        "color":
                                            "rgba(245,158,11,.20)",
                                    },
                                    {
                                        "range": [60, 100],
                                        "color":
                                            "rgba(239,68,68,.20)",
                                    },
                                ],
                            },
                        )
                    )

                    fig.update_layout(
                        height=280,

                        margin=dict(
                            l=20,
                            r=20,
                            t=55,
                            b=15,
                        ),

                        paper_bgcolor="rgba(0,0,0,0)",

                        font=dict(
                            color="#243b53",
                            size=14,
                        ),
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch",
                    )

                    st.markdown(
                        "#### Risk Drivers"
                    )

                    reasons = assessment.get(
                        "risk_reasons",
                        [],
                    )

                    if reasons:

                        for reason in reasons:

                            st.warning(
                                f"⚠️ **{reason}**"
                            )

                    else:

                        st.info(
                            "No risk drivers returned."
                        )

                with right:

                    st.markdown(
                        "### ✨ AI Draft Assessment"
                    )

                    st.caption(
                        "Groq-generated draft grounded "
                        "in retrieved policy context."
                    )

                    st.markdown(
                        assessment.get(
                            "ai_draft",
                            "No AI draft returned.",
                        )
                    )

                st.divider()

                evidence_tab, trace_tab = st.tabs(
                    [
                        "📚 Evidence Sources",
                        "🔄 Orchestration Trace",
                    ]
                )

                with evidence_tab:

                    sources = assessment.get(
                        "retrieved_sources",
                        [],
                    )

                    if sources:

                        for number, source in enumerate(
                            sources,
                            start=1,
                        ):

                            st.success(
                                f"✓ **{number}. {source}**"
                            )

                    else:

                        st.info(
                            "No retrieved sources returned."
                        )

                with trace_tab:

                    steps = assessment.get(
                        "workflow_steps",
                        [],
                    )

                    if steps:

                        for number, step in enumerate(
                            steps,
                            start=1,
                        ):

                            step_name = (
                                step.get(
                                    "step",
                                    "",
                                )
                                .replace(
                                    "_",
                                    " ",
                                )
                                .title()
                            )

                            step_status = step.get(
                                "status",
                                "unknown",
                            )

                            if step_status == "completed":

                                st.success(
                                    f"✓ **Step {number}: "
                                    f"{step_name}**"
                                )

                            else:

                                st.warning(
                                    f"◉ **Step {number}: "
                                    f"{step_name} — "
                                    f"{step_status.title()}**"
                                )

                    else:

                        st.info(
                            "No orchestration trace returned."
                        )


# ============================================================
# ANALYST REVIEW
# ============================================================

elif page == "👤 Analyst Review":

    page_title(
        "FCRM Analyst Review",
        "Human validation of AI-assisted risk findings "
        "and finalization of the FCRM risk rating.",
    )

    request_id = current_request_id()

    if not request_id:

        st.warning(
            "Select or create a Request ID first."
        )

    else:

        request_data, error = get_request(
            request_id
        )

        if error:

            st.error(error)

        else:

            status = request_data.get(
                "status",
                "unknown",
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Case",
                    request_id,
                )

            with c2:
                st.metric(
                    "Status",
                    status.replace(
                        "_",
                        " ",
                    ).title(),
                )

            with c3:
                st.metric(
                    "Analyst Rating",
                    request_data.get(
                        "analyst_risk_rating"
                    )
                    or "Pending",
                )

            st.info(
                "👤 **Human Override Control** — "
                "The analyst may disagree with the AI assessment. "
                "**An override reason must be recorded.**"
            )

            with st.form(
                "analyst_review_form"
            ):

                left, right = st.columns(2)

                with left:

                    analyst_name = st.text_input(
                        "FCRM Analyst",
                        value="analyst.user",
                    )

                    final_rating = st.selectbox(
                        "Final Human Risk Rating",
                        [
                            "HIGH",
                            "MEDIUM",
                            "LOW",
                        ],
                    )

                    override_ai = st.checkbox(
                        "Override AI Assessment"
                    )

                with right:

                    override_reason = st.text_area(
                        "Override Reason",

                        placeholder=(
                            "Required only when "
                            "overriding AI."
                        ),

                        height=120,
                    )

                comments = st.text_area(
                    "Analyst Comments",

                    value=(
                        "Assessment reviewed. Required financial "
                        "crime controls should be confirmed "
                        "before committee decision."
                    ),

                    height=120,
                )

                save_review = st.form_submit_button(
                    "Record Analyst Review",
                    type="primary",
                    width="stretch",
                )

            if save_review:

                if (
                    override_ai
                    and not override_reason.strip()
                ):

                    st.error(
                        "Override reason is required."
                    )

                else:

                    payload = {
                        "analyst_name":
                            analyst_name.strip(),

                        "final_risk_rating":
                            final_rating,

                        "override_ai":
                            override_ai,

                        "override_reason":
                            (
                                override_reason.strip()
                                if override_ai
                                else None
                            ),

                        "comments":
                            comments.strip(),
                    }

                    result, error = api_request(
                        "POST",
                        f"/{request_id}/analyst-review",
                        payload,
                    )

                    if error:

                        st.error(error)

                    else:

                        st.success(
                            "✓ Analyst review recorded."
                        )

            if status == "under_review":

                st.divider()

                st.subheader(
                    "Committee Handoff"
                )

                st.caption(
                    "After completing the analyst review, "
                    "send the case to the Risk Committee."
                )

                if st.button(
                    "🏛️ Send Case to Risk Committee",
                    type="primary",
                    width="stretch",
                ):

                    result, error = api_request(
                        "PATCH",
                        f"/{request_id}/send-to-committee",
                    )

                    if error:

                        st.error(error)

                    else:

                        st.success(
                            "✓ Case sent to Risk Committee."
                        )

                        st.rerun()


# ============================================================
# RISK COMMITTEE
# ============================================================

elif page == "🏛️ Risk Committee":

    page_title(
        "Risk Committee Decision",
        "Final human governance decision "
        "for the FCRM assessment.",
    )

    request_id = current_request_id()

    if not request_id:

        st.warning(
            "Select or create a Request ID first."
        )

    else:

        request_data, error = get_request(
            request_id
        )

        if error:

            st.error(error)

        else:

            status = request_data.get(
                "status",
                "unknown",
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Case",
                    request_id,
                )

            with c2:
                st.metric(
                    "Analyst Rating",
                    request_data.get(
                        "analyst_risk_rating"
                    )
                    or "Pending",
                )

            with c3:
                st.metric(
                    "Workflow",
                    status.replace(
                        "_",
                        " ",
                    ).title(),
                )

            st.info(
                "🏛️ **Final Human Decision** — "
                "The Risk Committee, not the AI system, "
                "owns the final approval or rejection."
            )

            if status == "decided":

                decision = (
                    request_data.get(
                        "decision"
                    )
                    or "Completed"
                )

                st.success(
                    f"✅ **Final Decision: "
                    f"{decision.upper()}**"
                )

            elif status != "committee_review":

                st.warning(
                    "This case is not ready "
                    "for committee decision."
                )

            else:

                with st.form(
                    "committee_decision_form"
                ):

                    committee_member = st.text_input(
                        "Committee Member",
                        value="committee.user",
                    )

                    decision = st.selectbox(
                        "Decision",
                        [
                            "approved",
                            "rejected",
                            "changes_requested",
                        ],
                    )

                    reason = st.text_area(
                        "Decision Rationale",

                        value=(
                            "The FCRM assessment, identified "
                            "risk drivers and required controls "
                            "have been reviewed."
                        ),

                        height=130,
                    )

                    submit_decision = st.form_submit_button(
                        "Record Final Decision",
                        type="primary",
                        width="stretch",
                    )

                if submit_decision:

                    payload = {
                        "committee_member":
                            committee_member.strip(),

                        "decision":
                            decision,

                        "reason":
                            reason.strip(),
                    }

                    result, error = api_request(
                        "POST",
                        f"/{request_id}/committee-decision",
                        payload,
                    )

                    if error:

                        st.error(error)

                    else:

                        st.success(
                            "✓ Committee decision recorded."
                        )

                        st.rerun()


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "🕒 Audit Trail":

    page_title(
        "Governance & Audit Trail",
        "Trace AI activity, human review "
        "and committee decisions.",
    )

    request_id = current_request_id()

    if not request_id:

        st.warning(
            "Select or create a Request ID first."
        )

    else:

        data, error = api_request(
            "GET",
            f"/{request_id}/audit-history",
        )

        if error:

            st.error(error)

        else:

            events = data.get(
                "audit_events",
                [],
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Case",
                    request_id,
                )

            with c2:
                st.metric(
                    "Audit Events",
                    len(events),
                )

            with c3:
                st.metric(
                    "Decision Authority",
                    "Human",
                )

            st.info(
                "🕒 **Traceability** — "
                "Workflow activity is recorded "
                "as application-level audit events."
            )

            if not events:

                st.warning(
                    "No audit events recorded "
                    "for this case."
                )

            else:

                st.subheader(
                    "Case Timeline"
                )

                for number, event in enumerate(
                    reversed(events),
                    start=1,
                ):

                    action = event.get(
                        "action",
                        "EVENT",
                    )

                    actor = event.get(
                        "actor",
                        "Unknown",
                    )

                    with st.expander(
                        f"{number}. {action} • {actor}",
                        expanded=False,
                    ):

                        left, right = st.columns(2)

                        with left:

                            st.write(
                                "**Actor:**",
                                actor,
                            )

                            st.write(
                                "**From Status:**",
                                event.get(
                                    "from_status"
                                )
                                or "—",
                            )

                        with right:

                            st.write(
                                "**Timestamp:**",
                                event.get(
                                    "created_at",
                                    "",
                                ),
                            )

                            st.write(
                                "**To Status:**",
                                event.get(
                                    "to_status"
                                )
                                or "—",
                            )

                        st.write(
                            "**Details**"
                        )

                        st.info(
                            event.get(
                                "details"
                            )
                            or "No additional details."
                        )

            st.divider()

            st.caption(
                "Prototype: audit events are append-only at "
                "the application workflow level. Production "
                "deployment would add stronger immutable "
                "storage, authentication and identity controls."
            )