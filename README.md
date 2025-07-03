## 🚀 AI Multi-Agent Bidding System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-1.13%2B-red?style=for-the-badge&logo=pytorch)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-orange?style=for-the-badge&logo=openai)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit)
![Deep Q-Network](https://img.shields.io/badge/Reinforcement%20Learning-DQN-green?style=for-the-badge&logo=deepmind)
![LangChain](https://img.shields.io/badge/LangChain-Multi--Agent-purple?style=for-the-badge)

##  **Project Overview**
The **AI Multi-Agent Bidding System** is a simulation framework that integrates **Deep Q-Network (DQN)** reinforcement learning with **multi-agent competitive bidding**. It enables **AI-powered bidding strategies**, **real-time data visualization**, and **AI chatbot-driven insights** for better decision-making.

### **Core Features**
###  AI-Powered Multi-Agent Bidding
- Agents bid dynamically based on **market trends**.
- Implements **Deep Q-Learning (DQN)** for optimal bid placement.
- AI-powered **bid negotiation & price optimization**.

### Real-Time Bidding Dashboard
- Interactive **Streamlit dashboard**.
- **Live bid monitoring** with **heatmaps & animations**.

### Market Threshold Adaptation
- Market adjusts dynamically using **previous bid patterns**.
- Implements **AI-driven market predictions**.

###  Agent Performance Tracking
- Leaderboard for **top-performing agents**.
- **Win rate, profit tracking, & bid evolution analysis**.

### 💬 AI Chatbot for Bid Analysis
- AI chatbot **analyzes bid trends** and **provides strategy recommendations**.
- Uses **OpenAI GPT-4** for **expert bidding advice**.

### Animated Bidding History
- **Time-lapse visualizations** of bid evolution.
- **Winning bid heatmaps** for strategic analysis.

---

## **Project Structure**
```
AI_MultiAgent_Bidding/
│─── src/
│    ├── agents/
│    │    ├── bidding_agent.py       # AI-powered RL bidding agent
│    │    ├── negotiation_agent.py   # Agent with negotiation strategies
│    ├── market/
│    │    ├── market_threshold.py    # Market threshold logic
│    ├── core/
│    │    ├── bidding_simulation.py  # Core bidding simulation
│    ├── utils/
│    │    ├── data_handler.py        # Data handling & CSV storage
│─── frontend/
│    ├── app.py                      # Streamlit dashboard
│    ├── components/
│    │    ├── visualization.py       # Charts & plots
│─── data/
│    ├── bid_history.csv             # Stores past bid data
│─── tests/
│    ├── test_agents.py              # Unit tests for agents
│─── main.py                         # Main entry point for bidding simulation
│─── requirements.txt                 # Dependencies list
│─── README.md                        # Documentation
```

---
## Workflow
###  AI Agent Bidding Process
1. **Initialize Agents** - Multi-agents (AI-powered) enter the bidding system.
2. **Generate Bids** - Each agent submits a bid based on market conditions.
3. **Apply Reinforcement Learning** - Agents adjust bids based on **rewards & penalties**.
4. **Market Threshold Calculation** - AI models predict market trends.
5. **Winning Bid Selection** - The lowest bid wins the round.
6. **Data Logging & Analysis** - Bid data is stored and analyzed for performance insights.

###  Streamlit Dashboard Workflow
1. **Load Bid History** - Fetch real-time data from data/bid_history.csv.
2. **Data Filtering & Aggregation** - Process the latest bid values.
3. **Generate Visuals** - Plotly, Seaborn & Matplotlib charts.
4. **Real-Time Updates** - Interactive refresh of bidding insights.
5. **AI Chatbot** - AI-powered Q&A for bidding trends.



##  Tech Stack Used
### ** Backend (AI & ML)**
- **Python 3.10+** - Core programming language.
- **PyTorch** - Deep Q-Networks (DQN) for reinforcement learning.
- **NumPy & Pandas** - Data manipulation and processing.
- **LangChain** - Multi-agent communication.
- **OpenAI API** - AI-driven decision-making.

### ** Data Visualization & UI**
- **Streamlit** - Frontend dashboard for insights.
- **Plotly & Seaborn** - Advanced graphs and animations.
- **Matplotlib** - Basic visualizations.
- **Heatmaps & Boxplots** - Statistical insights into agent behaviors.

---

## Key Visualizations in Dashboard
- **Line Charts** - Bidding trends per agent over time.
- **Heatmaps** - Winning bid patterns.
- **Boxplots** - Bid distribution insights.
- **Leaderboard** - Agent success ranking.
- **Animated Scatterplots** - Bid evolution per round.


## ** Installation & Setup**
### **Step 1: Clone the Repository**
bash
git clone https://github.com/Shubham-Bishnoi/KPMG-KDN-AI-multi-agent-dynamic-bidding.git
cd AI_MultiAgent_Bidding


### **Step 2: Set Up Virtual Environment**
bash
python3 -m venv myenv
source myenv/bin/activate


### **Step 3: Install Dependencies**
bash
pip install -r requirements.txt


### **Step 4: Run the AI Bidding Simulation**
bash
python main.py


### **Step 5: Launch the Dashboard**
bash
streamlit run frontend/app.py


---

##  How It Works
### AI Bidding Agents
Each agent makes a bid using **reinforcement learning (DQN)**, where:
1. Agents **learn optimal bidding strategies** over multiple rounds.
2. The **winning bid is the lowest bid** among competitors.
3. **Market conditions** change dynamically.

### Market Thresholds
- The market dynamically adjusts the **bidding threshold** 
- Agents **respond & adapt** to changes.

### Reinforcement Learning (DQN) Training
- Agents **store past actions & rewards**
- Uses **Q-learning** to optimize future bids.

---

## Features & Visualizations
### 1. Bidding Trends Over Rounds
- **Line graph** showing **agent-wise bid progression**.

###  2. Winning Bids Heatmap
- Heatmap of **winning bid patterns**.

### 3. Agent Performance Leaderboard
- Tracks **most successful bidders**.

###  4. Animated Bid Evolution
- **Time-lapse animation** of bid history.

###  5. Q-Value Evolution Tracking
- Tracks **how agents learn bidding strategies**.



## Contributing
Want to improve the **AI bidding system**? Follow these steps:
1. **Fork the repo** 
2. **Create a feature branch** (`git checkout -b feature-branch`)
3. **Commit changes** (`git commit -m "New feature added"`)
4. **Push to GitHub** (`git push origin feature-branch`)
5. **Submit a pull request** 

## Future Enhancements
✔ AI-powered **multi-agent negotiations** 
✔ **Bid sentiment analysis** using **GPT-4** 
✔ **Live bid-streaming** 
✔ **Adaptive market manipulation detection** 

---


