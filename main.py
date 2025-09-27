import os
import streamlit as st
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# ----------------------------
# Clinic context
# ----------------------------
clinic_name = "Hamza Boss DK Medical Center"
clinic_info = {
    "address": "123 Wellness Street, Springfield",
    "phone": "+1-555-123-4567",
    "email": "info@healthylifeclinic.com",
    "hours": {
        "Mon–Fri": "9:00 AM – 6:00 PM",
        "Sat": "10:00 AM – 2:00 PM",
        "Sun": "Closed"
    }
}

faq_list = [
    ("What are your opening hours?",
     "We are open Mon–Fri (9 AM – 6 PM), Sat (10 AM – 2 PM), closed Sun."),
    ("How can I book an appointment?",
     "Call us at +1-555-123-4567, email info@healthylifeclinic.com, or use our online portal."),
    ("Do you accept walk-ins?",
     "Yes, but appointments are prioritized."),
    ("Which doctors are available?",
     "Dr. Imad  (Kunati Specialist), Dr. Hamza Khatak (Da Damo Sardard), Dr. Emily Davis (Dermatologist)."),
    ("Do you provide emergency services?",
     "No, please call 911 or go to the nearest hospital."),
    ("What insurance do you accept?",
     "HealthCare Plus, MediAssist, Wellness Insurance."),
    ("How can I get my medical records?",
     "Request at reception or email records@healthylifeclinic.com."),
    ("Do you provide vaccinations?",
     "Yes, including flu shots, COVID-19, and travel vaccines."),
    ("How do I cancel or reschedule?",
     "Call us at least 24 hours before at +1-555-123-4567."),
    ("Do you have parking?",
     "Yes, free parking is available for patients.")
]

faq_context = "\n".join([f"Q: {q}\nA: {a}" for q, a in faq_list])

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Clinic Chatbot", page_icon="💬", layout="centered")

# Sidebar with clinic info
st.sidebar.title("🏥 Clinic Info")
st.sidebar.write(f"**{clinic_name}**")
st.sidebar.write(clinic_info["address"])
st.sidebar.write(f"📞 {clinic_info['phone']}")
st.sidebar.write(f"✉️ {clinic_info['email']}")
st.sidebar.subheader("🕒 Hours")
for day, hrs in clinic_info["hours"].items():
    st.sidebar.write(f"{day}: {hrs}")

st.title("💬 HealthyLife Clinic Chatbot")
st.write("Ask me anything about our services, doctors, and hours.")

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "👨‍⚕️"):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    system_prompt = f"""
    You are a polite chatbot for {clinic_name}.
    Use the following FAQ context to answer questions clearly.
    If not in context, say you’re not sure and suggest contacting the clinic.
    Important: you will not write any code or irrelevant answers.
    If a user requests code, respond with: "I am a medical bot, not a coder."
    
    Context:
    {faq_context}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ],
            temperature=0.3,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"⚠️ API error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant", avatar="👨‍⚕️"):
        st.markdown(answer)


