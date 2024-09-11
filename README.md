# ✉️ Cold Mail Generator

**Cold Mail Generator** helps business development professionals create personalized cold emails by matching job postings with relevant portfolio data. It scrapes job descriptions, compares them with your skills, and generates emails with the appropriate links from your portfolio.

## 🚀 Features
- **Real-time Job Posting Scraping**
- **Portfolio Integration**
- **Automated Cold Email Creation**

## 🗂️ Project Files
- **`.env`**: Stores Groq API key.
- **`requirements.txt`**: Lists dependencies.
- **`my_portfolio.csv`**: Contains tech stack and portfolio links.
- **`data_store.py`**: Stores portfolio data using ChromaDB and Pandas.
- **`app.py`**: Main app for scraping job data and generating cold emails.

## 🛠️ Setup Instructions

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/farukh-javed/AI-Cold-Mail-Generator-with-Llama3.1.git
   cd AI-Cold-Mail-Generator-with-Llama3.1
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**:  
   Add your Groq API key in `.env`:
   ```bash
   GROQ_API_KEY=your-groq-api-key-here
   ```

4. **Store Portfolio Data**:
   Run `data_store.py` to store your portfolio:
   ```bash
   python data_store.py
   ```

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## 💡 How It Works
1. **Run `data_store.py`** to store your portfolio.
2. **Run `app.py`** to scrape job postings and generate personalized cold emails.

## 📧 Example Email
```plaintext
Subject: Tailored Solutions for Your Software Engineer Role

Dear [Client],

I noticed your job posting for a Software Engineer. Datics AI specializes in Java and Python, which align perfectly with your needs...

Best regards,  
Farukh  
Business Development Executive  
Datics AI
```