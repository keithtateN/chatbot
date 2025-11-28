import streamlit as st
import google.generativeai as genai

# ——— PAGE CONFIG & DARK THEME ———
st.set_page_config(page_title="Polaris AI", page_icon="Compass", layout="centered")
st.markdown("""
<style>
    .main {background-color: #0e0e0e; color: #e0e0e0;}
    .stChatMessage {background-color: #1a1a1a; border-radius: 12px; padding: 12px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.title("Compass Polaris AI")
st.markdown("**Paste her message → get the perfect masculine reply instantly.**")

# ——— YOUR GEMINI KEY ———
genai.configure(api_key="AIzaSyAM2eAdXxMCwLk_oTjT6DvrsblvopGwLMA")
model = genai.GenerativeModel("gemini-2.5-flash")  # ← Updated to current stable model

# ——— POLARIS SYSTEM PROMPT ———
POLARIS_SYSTEM = """
You are Polaris AI — the world's most powerful authentic masculine attraction coach.

Mission: Help men attract high-quality women through confidence, sexual polarity, playfulness, leadership, and unbreakable frame — never manipulation or toxicity.

Strict rules:
• Assume mutual attraction & enthusiastic consent
• Masculine, decisive, teasing, sexually polarized
• Escalate only when she invests
• Outcome-independence: he is the prize
• Never neg, insult, dread, or deceive

Output format (exactly every time):
1. **Primary reply** (bold, ready to copy)
2. Why this works (3–5 short bullets)
3. Alternatives:
   • Lighter: [one option]
   • Bolder: [one option]

Tone: masculine, playful, leading, never needy.

Examples:
Her: "You seem like trouble" → **"Only the kind you'd beg to get into… can you keep up?"**
Her: "What are you doing tonight?" → **"Taking over a rooftop bar in an hour. You should come keep me company — unless you're scared of heights"**
"""

# ——— SESSION STATE ———
if "messages" not in st.session_state:
    st.session_state.messages = []

# ——— DISPLAY CHAT ———
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ——— USER INPUT ———
if prompt := st.chat_input("Paste her exact message here..."):
    her_msg = f"**Her:** {prompt}"
    st.session_state.messages.append({"role": "user", "content": her_msg})
    with st.chat_message("user"):
        st.markdown(her_msg)

    with st.chat_message("assistant"):
        with st.spinner("Polaris is thinking..."):
            full_prompt = POLARIS_SYSTEM + "\n\nMessage from her: " + prompt
            response = model.generate_content(full_prompt, stream=True)

            full_response = ""
            placeholder = st.empty()
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

        # Copy button
        primary = full_response.split("**")[1].split("**")[0] if "**" in full_response else full_response.split("\n")[0]
        st.markdown(f"""
        <div style="text-align: right; margin-top: 12px;">
            <button onclick="navigator.clipboard.writeText('{primary}')">
                Copy Primary Reply
            </button>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("---")
st.caption("Polaris AI • Built for men who lead • Powered by Gemini 2.5 Flash")