import streamlit as st
import math

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)

# ---------------- CSS ----------------
if "css_loaded" not in st.session_state:
    st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    button {
        width: 100%;
        height: 50px;
        border-radius: 10px;
        font-size: 18px;
        background-color: #1f2937;
        color: white;
        border: none;
    }

    button:hover {
        background-color: #374151;
    }
    </style>
    """, unsafe_allow_html=True)

    st.session_state.css_loaded = True

# ---------------- TITLE ----------------
st.title("SCIENTIFIC CALCULATOR")

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("expr", "")
st.session_state.setdefault("result", "")
st.session_state.setdefault("history", [])
st.session_state.setdefault("degree_mod", True)
st.session_state.setdefault("show_sci", False)

# ---------------- FUNCTIONS ----------------
def to_rad(x):
    return math.radians(x) if st.session_state.degree_mod else x

def sin(x):
    return math.sin(to_rad(x))

def cos(x):
    return math.cos(to_rad(x))

def tan(x):
    return math.tan(to_rad(x))

# ---------------- CALCULATE ----------------
def calculate():
    try:
        expr = st.session_state.expr.replace("x", "*")

        result = eval(expr, {
            "__builtins__": None,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e
        })

        st.session_state.result = str(result)

        st.session_state.history.insert(
            0, f"{st.session_state.expr} = {result}"
        )

    except:
        st.session_state.result = "Error"

# ---------------- MODE TOGGLE ----------------
mode = "DEG" if st.session_state.degree_mod else "RAD"
if st.button(f"Mode: {mode}"):
    st.session_state.degree_mod = not st.session_state.degree_mod

# ---------------- SCIENTIFIC MODE ----------------
if st.button("⚪ Scientific Mode"):
    st.session_state.show_sci = not st.session_state.show_sci

# ---------------- DISPLAY (FIXED — NO LAG) ----------------
st.markdown(
    f"""
    <div style="text-align:right; font-size:40px; color:#00ffcc; padding:10px;">
        {st.session_state.expr if st.session_state.expr else "0"}
    </div>
    <div style="text-align:right; font-size:28px; color:#ffffff;">
        {st.session_state.result}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SCIENTIFIC BUTTONS ----------------
if st.session_state.show_sci:

    sci_buttons = [
        ["sin(", "cos(", "tan(", "log(", "ln("],
        ["sqrt(", "(", ")", "pi", "e"]
    ]

    for i, row in enumerate(sci_buttons):
        cols = st.columns(len(row))

        for j, (col, btn) in enumerate(zip(cols, row)):
            with col:
                if st.button(btn, key=f"sci_{i}_{j}"):

                    st.session_state.expr += btn
                    st.rerun()   

# ---------------- MAIN BUTTON GRID ----------------
st.markdown("---")

buttons = [
    ["C", "⌫", "÷", "x"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", "00", ".", "^"],
    ["exp", "(", ")", ""]
]

# ---------------- BUTTON LOGIC ----------------
for i, row in enumerate(buttons):
    cols = st.columns(len(row))

    for j, (col, btn) in enumerate(zip(cols, row)):
        with col:
            if st.button(btn, key=f"btn_{i}_{j}", use_container_width=True):

                if btn == "=":
                    calculate()

                elif btn == "C":
                    st.session_state.expr = ""
                    st.session_state.result = ""

                elif btn == "⌫":
                    st.session_state.expr = st.session_state.expr[:-1] if st.session_state.expr else ""

                elif btn == "x":
                    st.session_state.expr += "*"

                elif btn == "÷":
                    st.session_state.expr += "/"

                elif btn == "^":
                    st.session_state.expr += "**"

                elif btn == "exp":
                    st.session_state.expr += "exp("

                elif btn == "":
                    pass

                else:
                    st.session_state.expr += btn

                st.rerun()   

# ---------------- HISTORY ----------------
st.markdown("---")

if st.session_state.history:
    st.subheader("History")

    for item in st.session_state.history[:5]:
        st.markdown(f"`{item}`")

    if st.button("Clear History"):
        st.session_state.history = []