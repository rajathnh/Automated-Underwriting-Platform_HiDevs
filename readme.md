# AI-Powered Automated Underwriting Platform

This project is a fully functional prototype of an AI-powered platform designed to automate property insurance underwriting. It leverages a powerful multimodal Large Language Model (Groq's Llama 4 Scout) to analyze both textual documents and property images, providing a comprehensive risk assessment based on a configurable set of rules.


*(To add a screenshot: run the app, take a picture, upload to a site like [Imgur](https://imgur.com/upload), get the "Direct Link", and replace the URL above.)*

## 🚀 Features

-   **Multimodal Analysis**: Processes both PDF appraisal reports (text) and property photos (images) in a single workflow.
-   **RAG-based Decision Making**: Uses a Retrieval-Augmented Generation (RAG) approach where the AI's final decision is grounded by a user-defined "Insurance Rulebook."
-   **Configurable Rules**: The underwriting guidelines can be edited directly in the UI, allowing for flexible risk assessment criteria.
-   **Interactive UI**: A clean and user-friendly interface built with Streamlit for easy file uploads and clear result presentation.
-   **Blazing Fast Inference**: Powered by the Groq API for near-instant analysis and assessment.

## ⚙️ Technology Stack

-   **Language**: Python
-   **Web Framework**: Streamlit
-   **LLM Provider**: Groq
-   **Multimodal Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
-   **Core Libraries**: `groq`, `pypdf`, `streamlit`

## 🛠️ Setup and Installation

Follow these steps to get the application running on your local machine.


### 1. Clone the Repository

```bash
git clone https://github.com/rajathnh/Build-Your-Own-AI-Clone_HiDevs.git
cd Build-Your-Own-AI-Clone_HiDevs
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

-   **Windows:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

-   **macOS / Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies

All required packages are listed in `requirements.txt`. Install them with a single command:

```bash
pip install -r requirements.txt
```
### 4. Configure API Keys and Secrets (Crucial Step)

This project requires API keys to function. We will store them securely using Streamlit's secrets management.

1.  **Create the secrets folder:** In the root of the project folder, create a new folder named `.streamlit`.

    ```bash
    mkdir .streamlit
    ```

2.  **Create the secrets file:** Inside the `.streamlit` folder, create a new file named `secrets.toml`.

3.  **Add your keys to `secrets.toml`:** Open the file and paste the following content, replacing the placeholder values with your actual keys.

    ```toml
    # .streamlit/secrets.toml

    GROQ_API_KEY = "gsk_YourGroqApiKeyHere"
    
    ```
    -   Get your **Groq API Key** from the [Groq Console](https://console.groq.com/keys).
    -   
    ```

## ▶️ How to Run the Application

Once the setup is complete, you can run the app with a single command:

```bash
streamlit run app.py
```
Your web browser will automatically open with the chatbot interface.
To view the traces and evaluate the RAG pipeline:
Check the terminal where you ran the app. You will see a URL for the Arize Phoenix UI (e.g., http://127.0.0.1:6006).
Open this URL in a new browser tab to see a detailed breakdown of each query.
