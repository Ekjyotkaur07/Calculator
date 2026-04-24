import streamlit as st
import math
st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)
if "css_loaded" not in st.session_state:
    st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
    st.session_state.css_loaded = True
    st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    /* Display styling */
    .display-box {
        background-color: #000;
        padding: 15px;
        border-radius: 10px;
        text-align: right;
        font-family: monospace;
        margin-bottom: 10px;
    }

    .expr {
        font-size: 18px;
        color: #aaa;
    }

    .result {
        font-size: 32px;
        color: #00ffcc;
    }

    /* Buttons */
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
    
    }
    </style>
    """, unsafe_allow_html=True)
st.title("SCIENTIFIC CALCULATOR")


# ---------------- SESSION STATE ----------------
st.session_state.setdefault("expr", "")
st.session_state.setdefault("result", "")
st.session_state.setdefault("history", [])
st.session_state.setdefault("degree_mod", True)



# ---------------- FUNCTIONS ----------------
def to_rad(x):
    return math.radians(x) if st.session_state.degree_mod else x
def sin(x):
    return math.sin(to_rad(x))
def cos(x):
    return math.cos(to_rad(x))
def tan(x):
    try:
        return math.tan(to_rad(x))
    except:
        return "Error"
def calculate():
    try:
        result = eval(st.session_state.expr, {
            "__builtins__": None,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "sqrt": math.sqrt,
            "log": math.log10,
            "pi": math.pi,
            "e": math.e
        })
        st.session_state.result = str(result)
        st.session_state.history.insert(
            0, f"{st.session_state.expr} = {result}"
        )
    except:
        st.session_state.result = "Error"

def update_expr(val):
    if st.session_state.expr == "Error":
        st.session_state.expr = ""
    if st.session_state.result:
        st.session_state.expr = ""
        st.session_state.result = ""
    st.session_state.expr += val

#------------TOGGLE----------------------
mode ="DEG" if st.session_state.degree_mod else "RAD"
if st.button(f"Mode: {mode}",key="mode"):
    st.session_state.degree_mod=not st.session_state.degree_mod

#--------KEYOBARD INPUT-------------------
user_input = st.text_input(
    "⌨️ Type expression",
    placeholder="e.g. sin(30) + 5*2",
    key="keyboard_input"
)
#------------DISPLAY------------
st.markdown(f"""
<div class="display-box">
    <div class="expr">{st.session_state.expr}</div>
    <div class="result">{st.session_state.result}</div>
</div>
""", unsafe_allow_html=True)

#-----SCIENTIFIC FUNCTIOS---------------
sci_buttons = ["sin(", "cos(", "tan(", "sqrt(", "log(", "pi", "e"]
cols = st.columns(len(sci_buttons))

for i, (col, btn) in enumerate(zip(cols, sci_buttons)):
    with col:
        if st.button(btn, key=f"sci_{i}"):
            update_expr(btn)

#-----------------BUTTONS-------------
st.markdown("---")

buttons = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "x"],
    ["1", "2", "3", "-"],
    ["C", "0", "⌫", "="],
]

for i, row in enumerate(buttons):
    cols = st.columns(4)
    for j, (col, btn) in enumerate(zip(cols, row)):
        with col:
            if st.button(btn, key=f"btn_{i}_{j}", use_container_width=True):

                    if btn == "=":
                        calculate()

                    elif btn == "x":
                        update_expr("*")

                    elif btn == "÷":
                        update_expr("/")

                    elif btn == "C":   # ✅ ADD THIS
                        st.session_state.expr = ""
                        st.session_state.result = ""

                    elif btn == "⌫":   # ✅ ADD THIS
                        st.session_state.expr = st.session_state.expr[:-1]

                    else:
                        update_expr(btn)


st.markdown("---")
#-----HISTORY-------------
if st.session_state.history:
    st.subheader("History")
    for item in st.session_state.history[:5]:
        st.markdown(f"`{item}`")
    if st.button("Clear History",key="clear_history"):
        st.session_state.history=[]
 