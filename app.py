import streamlit as st
import joblib
import re
import string

# --- Text Preprocessing Function ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), "", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\w*\d\w*", "", text)
    text = re.sub(r"\s+", " ", text)  
    return text.strip()

# --- Load Vectorizer and Model Safely ---
try:
    vectorizer = joblib.load("vectorizer.jb")
    model = joblib.load("lr_model.jb")
except FileNotFoundError as e:
    st.error(f"❌ Model or vectorizer file not found: {e}")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="Fake News Detector", page_icon="📰")
st.title("📰 Fake News Detector")
st.write("Enter a news article below to check whether it's Fake or Real.")

# --- User Input ---
inputn = st.text_area("News Article:", "", height=200)

# --- Prediction ---
if st.button("🔍 Check News"):
    if inputn.strip():
        cleaned_input = clean_text(inputn)
        transformed_input = vectorizer.transform([cleaned_input])
        prediction = model.predict(transformed_input)

        if prediction[0] == 1:
            st.success("✅ This news article is likely *Real*.")
        else:
            st.error("❌ This news article is likely *Fake*.")
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# --- Footer ---
st.markdown("---")

