import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="D",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f7f8fb;
            --surface: #ffffff;
            --ink: #172033;
            --muted: #667085;
            --line: #e6e9ef;
            --brand: #2563eb;
            --brand-dark: #1d4ed8;
            --good: #0f766e;
            --good-bg: #ecfdf5;
            --risk: #b42318;
            --risk-bg: #fff1f0;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, .08), transparent 28rem),
                linear-gradient(180deg, #ffffff 0%, var(--bg) 42%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1120px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, p {
            letter-spacing: 0;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stVerticalBlock"] {
            gap: 1.05rem;
        }

        .hero {
            border-bottom: 1px solid var(--line);
            margin-bottom: 1.35rem;
            padding-bottom: 1.6rem;
        }

        .eyebrow {
            color: var(--brand);
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .08em;
            margin-bottom: .45rem;
            text-transform: uppercase;
        }

        .hero h1 {
            color: var(--ink);
            font-size: clamp(2.15rem, 4vw, 4.25rem);
            font-weight: 850;
            letter-spacing: 0;
            line-height: 1.02;
            margin: 0;
        }

        .hero p {
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.65;
            margin: .85rem 0 0;
            max-width: 760px;
        }

        .panel,
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, .92);
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 18px 50px rgba(23, 32, 51, .07);
            padding: 1.2rem;
        }

        [data-testid="stForm"] {
            margin-bottom: 0;
        }

        .section-title {
            align-items: center;
            color: var(--ink);
            display: flex;
            font-size: .95rem;
            font-weight: 800;
            gap: .65rem;
            margin: .25rem 0 .2rem;
        }

        .section-title:before {
            background: var(--brand);
            border-radius: 999px;
            content: "";
            display: inline-block;
            height: .55rem;
            width: .55rem;
        }

        .section-note {
            color: var(--muted);
            font-size: .9rem;
            margin: -.15rem 0 .45rem;
        }

        .stNumberInput label,
        .stSelectbox label,
        .stSlider label {
            color: var(--ink) !important;
            font-size: .9rem !important;
            font-weight: 700 !important;
        }

        .stNumberInput input,
        [data-baseweb="select"] > div,
        .stTextInput input {
            background: #ffffff;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            color: var(--ink);
            transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease;
        }

        .stNumberInput input:focus,
        [data-baseweb="select"] > div:focus-within,
        .stTextInput input:focus {
            border-color: rgba(37, 99, 235, .65) !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, .12) !important;
        }

        div[data-testid="stSlider"] [data-baseweb="slider"] > div {
            color: var(--brand);
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background: var(--brand);
            border: 1px solid var(--brand);
            border-radius: 8px;
            box-shadow: 0 12px 26px rgba(37, 99, 235, .22);
            color: #ffffff;
            font-weight: 800;
            min-height: 3rem;
            transition: background .18s ease, border-color .18s ease, box-shadow .18s ease, transform .18s ease;
            width: 100%;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background: var(--brand-dark);
            border-color: var(--brand-dark);
            box-shadow: 0 16px 34px rgba(37, 99, 235, .28);
            color: #ffffff;
            transform: translateY(-1px);
        }

        .stButton > button:active,
        .stFormSubmitButton > button:active {
            box-shadow: 0 8px 18px rgba(37, 99, 235, .22);
            transform: translateY(0);
        }

        .stButton > button:focus,
        .stFormSubmitButton > button:focus {
            box-shadow: 0 0 0 4px rgba(37, 99, 235, .16), 0 12px 26px rgba(37, 99, 235, .22);
        }

        .result {
            border: 1px solid var(--line);
            border-radius: 8px;
            margin-top: 1.1rem;
            overflow: hidden;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 1.1rem 1.2rem;
        }

        .result-title {
            color: var(--ink);
            font-size: 1.4rem;
            font-weight: 850;
            line-height: 1.15;
            margin: 0;
        }

        .result-subtitle {
            color: var(--muted);
            font-size: .95rem;
            margin-top: .35rem;
        }

        .score {
            color: var(--ink);
            font-size: 2.1rem;
            font-weight: 850;
            line-height: 1;
            white-space: nowrap;
        }

        .risk-high {
            background: var(--risk-bg);
            border-color: #ffd5d1;
        }

        .risk-low {
            background: var(--good-bg);
            border-color: #bbf7d0;
        }

        .advice {
            border-top: 1px solid rgba(23, 32, 51, .08);
            color: #344054;
            display: grid;
            font-size: .96rem;
            gap: .65rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            padding: 1rem 1.2rem 1.15rem;
        }

        .advice span {
            background: rgba(255, 255, 255, .72);
            border: 1px solid rgba(23, 32, 51, .08);
            border-radius: 8px;
            padding: .7rem .8rem;
        }

        .small-print {
            color: var(--muted);
            font-size: .82rem;
            line-height: 1.55;
            margin-top: .85rem;
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: .85rem 1rem;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: var(--ink) !important;
        }

        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.3rem;
            }

            .panel {
                padding: 1rem;
            }

            .result-header {
                display: block;
            }

            .score {
                margin-top: .8rem;
            }

            .advice {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    import joblib

    return joblib.load("diabetes_model.pkl")


def binary_choice(label, key, yes_text="Yes", no_text="No"):
    return st.selectbox(
        label,
        options=[0, 1],
        format_func=lambda value: no_text if value == 0 else yes_text,
        key=key,
    )


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Health screening tool</div>
        <h1>Diabetes Risk Predictor</h1>
        <p>
            A focused, ML-powered checker for estimating diabetes risk from everyday
            health indicators. Adjust the details below and get a clear result instantly.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    model = load_model()
except Exception as error:
    st.error(
        "The prediction model could not be loaded. Install the project dependencies "
        "from requirements.txt, then restart the app."
    )
    with st.expander("Technical details"):
        st.code(str(error))
    st.stop()

left, right = st.columns([1.9, 1], gap="large")

with left:
    with st.form("risk_form"):
        st.markdown('<div class="section-title">Personal profile</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">Use the closest option when an exact value is not available.</div>',
            unsafe_allow_html=True,
        )

        age_labels = {
            1: "18-24",
            2: "25-29",
            3: "30-34",
            4: "35-39",
            5: "40-44",
            6: "45-49",
            7: "50-54",
            8: "55-59",
            9: "60-64",
            10: "65-69",
            11: "70-74",
            12: "75-79",
            13: "80+",
        }
        education_labels = {
            1: "No school",
            2: "Elementary",
            3: "Some high school",
            4: "High school graduate",
            5: "Some college",
            6: "College graduate",
        }
        income_labels = {
            1: "Under $10k",
            2: "$10k-$15k",
            3: "$15k-$20k",
            4: "$20k-$25k",
            5: "$25k-$35k",
            6: "$35k-$50k",
            7: "$50k-$75k",
            8: "$75k+",
        }
        health_labels = {
            1: "Excellent",
            2: "Very good",
            3: "Good",
            4: "Fair",
            5: "Poor",
        }

        col1, col2, col3 = st.columns(3)
        with col1:
            Age = st.selectbox(
                "Age range",
                options=list(age_labels.keys()),
                index=4,
                format_func=lambda value: age_labels[value],
            )
        with col2:
            BMI = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
        with col3:
            Sex = st.selectbox(
                "Sex",
                options=[0, 1],
                format_func=lambda value: "Female" if value == 0 else "Male",
            )

        col4, col5, col6 = st.columns(3)
        with col4:
            Education = st.selectbox(
                "Education",
                options=list(education_labels.keys()),
                index=3,
                format_func=lambda value: education_labels[value],
            )
        with col5:
            Income = st.selectbox(
                "Income",
                options=list(income_labels.keys()),
                index=3,
                format_func=lambda value: income_labels[value],
            )
        with col6:
            GenHlth = st.selectbox(
                "General health",
                options=list(health_labels.keys()),
                index=2,
                format_func=lambda value: health_labels[value],
            )

        st.markdown('<div class="section-title">Medical history</div>', unsafe_allow_html=True)
        col7, col8, col9 = st.columns(3)
        with col7:
            HighBP = binary_choice("High blood pressure", "high_bp")
        with col8:
            HighChol = binary_choice("High cholesterol", "high_chol")
        with col9:
            Stroke = binary_choice("Stroke history", "stroke")

        col10, col11, col12 = st.columns(3)
        with col10:
            HeartDiseaseorAttack = binary_choice("Heart disease or attack", "heart")
        with col11:
            MentHlth = st.slider("Mental health bad days", 0, 30, 0)
        with col12:
            PhysHlth = st.slider("Physical health bad days", 0, 30, 0)

        st.markdown('<div class="section-title">Lifestyle</div>', unsafe_allow_html=True)
        col13, col14, col15 = st.columns(3)
        with col13:
            Smoker = binary_choice("Smoker", "smoker")
        with col14:
            PhysActivity = binary_choice("Physically active", "activity")
        with col15:
            DiffWalk = binary_choice("Difficulty walking", "diff_walk")

        col16, col17, spacer = st.columns(3)
        with col16:
            Fruits = binary_choice("Fruit daily", "fruit")
        with col17:
            Veggies = binary_choice("Vegetables daily", "veggies")

        submitted = st.form_submit_button("Check risk", use_container_width=True)

with right:
    st.markdown('<div class="section-title">Quick context</div>', unsafe_allow_html=True)
    st.metric("BMI entered", f"{BMI:.1f}")
    st.metric("Age range", age_labels[Age])
    st.metric("General health", health_labels[GenHlth])
    st.markdown(
        """
        <div class="small-print">
            This tool is for screening support only. It does not diagnose diabetes
            or replace care from a qualified medical professional.
        </div>
        """,
        unsafe_allow_html=True,
    )

if submitted:
    input_data = pd.DataFrame(
        [
            {
                "HighBP": HighBP,
                "HighChol": HighChol,
                "BMI": BMI,
                "Smoker": Smoker,
                "Stroke": Stroke,
                "HeartDiseaseorAttack": HeartDiseaseorAttack,
                "PhysActivity": PhysActivity,
                "Fruits": Fruits,
                "Veggies": Veggies,
                "GenHlth": GenHlth,
                "MentHlth": MentHlth,
                "PhysHlth": PhysHlth,
                "DiffWalk": DiffWalk,
                "Sex": Sex,
                "Age": Age,
                "Education": Education,
                "Income": Income,
            }
        ]
    )

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]
    risk_pct = float(probability[1] * 100)
    confidence_pct = risk_pct if prediction == 1 else float(probability[0] * 100)

    if prediction == 1:
        result_class = "risk-high"
        title = "Higher risk detected"
        subtitle = "Consider scheduling a clinical checkup and reviewing modifiable risk factors."
        advice = [
            "Book a doctor visit for proper testing.",
            "Monitor blood sugar as recommended by a clinician.",
            "Aim for regular movement and gradual weight management.",
            "Limit sugary drinks and highly processed foods.",
        ]
    else:
        result_class = "risk-low"
        title = "Lower risk detected"
        subtitle = "Keep maintaining healthy habits and routine preventive checkups."
        advice = [
            "Stay consistent with activity through the week.",
            "Keep fruit, vegetables, and fiber in regular meals.",
            "Maintain sleep, hydration, and yearly checkups.",
            "Recheck if symptoms or health markers change.",
        ]

    st.markdown(
        f"""
        <div class="result {result_class}">
            <div class="result-header">
                <div>
                    <p class="result-title">{title}</p>
                    <div class="result-subtitle">{subtitle}</div>
                </div>
                <div class="score">{confidence_pct:.1f}%</div>
            </div>
            <div class="advice">
                <span>{advice[0]}</span>
                <span>{advice[1]}</span>
                <span>{advice[2]}</span>
                <span>{advice[3]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Estimated diabetes risk: {risk_pct:.1f}%")
    st.progress(int(round(risk_pct)))
