<h1 align="center">🦾 Reddit Insight Agents</h1>
<p align="center">
  <b>AI-powered Reddit Analysis & Engagement Tool</b><br>
  Summarize posts, fact-check comments, analyze sentiment, 
  <b>generate user-style comments</b>, and 
  <b>auto-post directly to Reddit</b> using 
  <a href="https://www.camel-ai.org" target="_blank">Camel AI</a> + 
  <a href="https://streamlit.io" target="_blank">Streamlit</a>.
</p>


<p align="center">
  <a href="https://www.camel-ai.org" target="_blank">
    <img src="https://img.shields.io/badge/Powered%20By-Camel%20AI-00D4B1?style=for-the-badge" alt="Camel AI"/>
  </a>
  <a href="https://streamlit.io" target="_blank">
    <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge" alt="Streamlit"/>
  </a>
  <a href="https://www.reddit.com/dev/api/" target="_blank">
    <img src="https://img.shields.io/badge/API-Reddit-orange?style=for-the-badge&logo=reddit" alt="Reddit API"/>
  </a>
  <a href="https://openai.com" target="_blank">
    <img src="https://img.shields.io/badge/LLM-GPT--4o-blue?style=for-the-badge&logo=openai" alt="GPT-4o"/>
  </a>
</p>


---

## 🌟 Why This Project?

Reddit is one of the **largest knowledge hubs** online — but it’s also cluttered with **endless threads, biased opinions, and misinformation**.  
This project transforms that chaos into **actionable insights** using **AI-powered agents**:  

- 🔎 **Smart Summaries** → Instantly capture the essence of long discussions  
- ✅ **Built-in Fact-Checking** → Spot truth vs. misinformation with AI verdicts  
- 📊 **Sentiment Analysis** → Measure community mood (-1 to +1) in real time  
- 🤖 **AI-Generated Comments** → Reply in a natural Reddit-style tone  
- 🚀 **Direct Posting** → Create & publish posts without leaving the app  

👉 In short: **Turn Reddit’s noise into knowledge.**

---

## ✨ Features
- 📰 **Collector Agent** → Fetches posts & top comments with summaries  
- 😊 **Sentiment Agent** → Rates positivity/negativity (-1.0 → +1.0)  
- 🕵️ **Fact-Checker Agent** → Validates claims (`True`, `False`, `Unverified`)  
- 💬 **Comment Generator Agent** → Mimics top-liked comment styles  
- 📊 **Dashboard** → Charts, metrics & CSV export  
- 📤 **Reddit Poster** → Create new posts (with flair support)  

---

### 🖼️ Visual Workflow Demo

Watch the AI agents in action:  


<p align="center">
  <img src="assets/redditinsight demo 1.gif" alt="demo" width="600"/>
</p>


---

## 🛠 Tech Stack
- **Frontend:** Streamlit (custom dark UI)  
- **Agents & LLM:** Camel AI (`ChatAgent`, `ModelFactory`)  
- **Reddit API:** PRAW + Camel RedditToolkit  
- **Backend:** Python 3.10+  
- **Visualization:** Pandas, Streamlit charts  

---

## 📂 Project Structure

```
RedditToolkit
|
├── app.py # Streamlit UI (dashboard + interactions)
├── agents.py # Multi-agent logic (collector, sentiment, fact-checker, comment gen)
├── api.env # Environment variables (keys & secrets)
├── assets/ # Logos, UI images, screenshots
└── README.md # Documentation
```


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/tushar80rt/RedditToolkit.git
cd RedditToolkit
```
2️⃣ Install Dependencies
```
pip install -r requirements.txt
```
3️⃣ Configure API Keys

Create a .env file (or api.env) in root:

```
OPENAI_API_KEY=your_openai_key
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_app_name
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```
🚀 Usage

Run the app:
```
streamlit run app.py
```
Visit 👉 http://localhost:8501

## Typical Workflow

1. Enter subreddits and keywords

2.  Click Start Analysis

3.  View →

    - Summaries
    
    - Sentiment scores
    
    - Fact-check verdicts
    
    - Top comments
  
4. Generate →

    - New Reddit-style comment
    - Or post directly to Reddit
  
## 📊 Example Output

  #### Collector Summary

       “The post discusses AI’s impact on elections. Users are divided: some worry about bias, others are optimistic...”
       
   #### Sentiment Score → 0.72 (positive)

   #### Fact Verdict → Unverified
   
   #### Generated Comment →
     “Good point! But we should also consider how policies affect smaller communities.”

## 🤝 Contributing

Contributions are welcome 💡
  
   - Fork the repo
    
   - Create a feature branch
    
  - Submit a PR 🚀

## 📜 License

MIT License © 2025 — Built with ❤️ using Camel AI
