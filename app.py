import streamlit as st
import openai
import smtplib
from email.mime.text import MIMEText

# Title and description
st.title("AI-Powered Outreach Email Generator")
st.markdown("Generate personalized outreach emails for businesses using AI.")

# Input fields
business_name = st.text_input("Business Name")
business_type = st.text_input("Business Type (e.g., bakery, salon)")
business_website = st.text_input("Business Website (optional)")
recipient_email = st.text_input("Recipient Email")

email_body = ""

# Use your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Generate the email
if st.button("Generate Email"):
    with st.spinner("Generating email with AI..."):
        prompt = f"Write a short, friendly email offering AI services to a {business_type} called {business_name}. Mention how AI can save time and improve efficiency."
        if business_website:
            prompt += f" Their website is {business_website}."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            email_body = response.choices[0].message.content
            st.session_state.email_body = email_body  # Save to session for later use
            st.text_area("Generated Email", email_body, height=200)
        except Exception as e:
            st.error(f"Error generating email: {e}")

# Send the email
if st.button("Send Email"):
    email_body = st.session_state.get("email_body", "")
    if not recipient_email or not email_body:
        st.error("Please provide recipient email and generate an email first.")
    else:
        try:
            sender = st.secrets["EMAIL_ADDRESS"]
            password = st.secrets["EMAIL_PASSWORD"]

            msg = MIMEText(email_body)
            msg["Subject"] = "Helping Your Business Use AI"
            msg["From"] = sender
            msg["To"] = recipient_email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, recipient_email, msg.as_string())

            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")

