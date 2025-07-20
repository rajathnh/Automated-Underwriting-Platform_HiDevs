import streamlit as st
import os
import base64
from groq import Groq
from pypdf import PdfReader

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Automated Underwriting Platform",
    page_icon="🤖",
    layout="wide"
)

# --- AUTHENTICATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except KeyError:
    st.error("GROQ_API_KEY not found! Please add it to your .streamlit/secrets.toml file.")
    st.stop()

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def encode_image(uploaded_file):
    """Encodes an uploaded image to base64, checking size limits."""
    # Read file bytes
    file_bytes = uploaded_file.getvalue()
    # Check size (Groq limit is 4MB for base64)
    if len(file_bytes) > 4 * 1024 * 1024:
        st.warning(f"Image '{uploaded_file.name}' is too large (>4MB) and will be skipped.")
        return None
    return base64.b64encode(file_bytes).decode('utf-8')

# --- UI & MAIN LOGIC ---

st.title("🤖 Automated Insurance Underwriting Platform")
st.markdown("This tool uses Multimodal AI to analyze property documents and images for risk assessment.")

# --- INSURANCE RULEBOOK (RAG Context) ---
st.subheader("1. Define Underwriting Guidelines")
st.info("These rules will be used by the AI to assess risk (RAG). You can edit them.")
insurance_rules = st.text_area(
    "Insurance Rulebook",
    height=250,
    value="""
=== ROOFING RULES ===
- Any roof with visible sagging, significant curling, or more than 10% of shingles missing is a high risk.
- Roofs older than 20 years are a high risk.
- Metal roofs in good condition are a low risk.

=== ELECTRICAL RULES ===
- Properties with knob-and-tube wiring are an unacceptable risk.
- Electrical panels must be at least 100 amps. Panels below this are a medium risk.
- Visible frayed wires or scorch marks are a high risk.

=== PLUMBING & WATER RULES ===
- Any visible signs of active water leaks or significant water damage stains are a high risk.
"""
)

# --- FILE UPLOADERS ---
st.subheader("2. Upload Property Files")
col1, col2 = st.columns(2)

with col1:
    pdf_file = st.file_uploader("Upload Appraisal Report (PDF)", type="pdf")

with col2:
    image_files = st.file_uploader("Upload Property Images (JPG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)


# --- ANALYSIS BUTTON & LOGIC ---
if st.button("Analyze Property Risk", type="primary", use_container_width=True):
    if not pdf_file or not image_files:
        st.warning("Please upload both a PDF report and at least one image.")
        st.stop()

    analysis_results = []
    
    with st.spinner("Processing files... This may take a moment."):
        
        # 1. Document Analysis (PDF)
        st.write("📄 Analyzing PDF report...")
        report_text = extract_text_from_pdf(pdf_file)
        if report_text:
            analysis_results.append(f"--- APPRAISAL REPORT SUMMARY ---\n{report_text[:2000]}...") # Truncate for brevity

        # 2. Computer Vision (Images)
        st.write("🖼️ Analyzing property images...")
        image_analysis_prompt = """
        You are an expert insurance inspector. Analyze this image of a house.
        Describe its condition in detail, focusing on any potential hazards, damage, or areas of concern relevant to property insurance.
        List any visible issues related to roofing, electrical, plumbing, foundation, or general safety.
        """
        
        for image_file in image_files:
            base64_image = encode_image(image_file)
            if base64_image:
                try:
                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {"role": "user", "content": [
                                {"type": "text", "text": image_analysis_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        max_tokens=512
                    )
                    image_desc = response.choices[0].message.content
                    analysis_results.append(f"--- IMAGE ANALYSIS: {image_file.name} ---\n{image_desc}")
                except Exception as e:
                    st.error(f"Failed to analyze image {image_file.name}: {e}")

        # 3. Final Synthesis & Risk Assessment (RAG)
        st.write("🧠 Performing final risk assessment...")
        evidence = "\n\n".join(analysis_results)
        
        final_assessment_prompt = f"""
        You are a senior insurance underwriter. Your task is to provide a final risk assessment for a property.
        
        You have been provided with two sources of information:
        1. The UNDERWRITING GUIDELINES which you must strictly follow.
        2. The EVIDENCE gathered from an appraisal report and photos of the property.

        **UNDERWRITING GUIDELINES:**
        ---
        {insurance_rules}
        ---

        **EVIDENCE:**
        ---
        {evidence}
        ---

        **YOUR TASK:**
        Based *only* on the evidence and adhering strictly to the guidelines, provide a final risk assessment. Your response should include:
        1.  **Overall Risk Level:** (Low Risk, Medium Risk, High Risk, or Unacceptable Risk).
        2.  **Justification:** A brief, point-by-point explanation for your decision, referencing specific evidence and the rules it violates or adheres to.
        """
        
        try:
            final_response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct", # Using Scout again for consistency
                messages=[{"role": "user", "content": final_assessment_prompt}],
                max_tokens=1024
            )
            
            st.subheader("✅ Final Underwriting Assessment")
            st.markdown(final_response.choices[0].message.content)

        except Exception as e:
            st.error(f"Failed to generate final assessment: {e}")