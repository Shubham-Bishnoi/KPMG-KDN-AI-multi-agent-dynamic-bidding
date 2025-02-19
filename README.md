#  AI Multi-Agent Bidding System

## ** Project Overview**
The **AI Multi-Agent Bidding System** is an advanced simulation framework that integrates **reinforcement learning (DQN)** with **multi-agent competitive bidding**. The system features:
- **Autonomous Bidding Agents** 
- **Dynamic Market Thresholds** 
- **Real-time Visualization** 
- **AI-Powered Bid Strategy Optimization** 
- **Deep Q-Learning (DQN) for Smart Agent Decision Making**

## ** Features**
### ** AI-Powered Multi-Agent Bidding**
- Agents bid dynamically based on **market conditions** 
- Implements **Deep Q-Learning (DQN)** for **reinforcement learning** 

### ** Real-Time Bidding Dashboard (Streamlit)**
- Interactive **data visualization** with **Plotly & Seaborn** 
- **Dark Mode & Light Mode** 
- Real-time **bid activity feed** 

### ** Market Threshold Dynamics**
- Market adjusts based on **previous bid trends** 
- Implements a **dynamic function for competitive thresholds**

### ** Agent Performance Tracking**
- Agent leaderboard 🏆
- Performance charts **(win rate, profit, and bid trends)** 

### ** AI Chatbot for Bid Analysis**
- AI chatbot analyzes bid trends and suggests improvements 

### ** Live Bid Heatmaps & Animations**
- **Animated bid history** 
- **Winning bid heatmaps** 

---

## ** Project Structure**
```
AI_MultiAgent_Bidding/
│─── src/
│    ├── agents/
│    │    ├── bidding_agent.py       # Reinforcement Learning Agent
│    │    ├── negotiation_agent.py   # Agent with Negotiation Logic
│    ├── market/
│    │    ├── market_threshold.py    # Market Dynamics
│    ├── core/
│    │    ├── bidding_simulation.py  # Main Simulation Engine
│    ├── utils/
│    │    ├── data_handler.py        # Data Storage & Management
│─── frontend/
│    ├── app.py                      # Streamlit UI Dashboard
│    ├── components/
│    │    ├── visualization.py       # Graphs & Charts
│─── data/
│    ├── bid_history.csv             # Stores past bid data
│─── tests/
│    ├── test_agents.py              # Unit Tests
│─── main.py                         # Entry Point
│─── requirements.txt                 # Dependencies
│─── README.md                        # Documentation
```

---


## Workflow
### ** AI Agent Bidding Process**
1. **Initialize Agents** - Multi-agents (AI-powered) enter the bidding system.
2. **Generate Bids** - Each agent submits a bid based on market conditions.
3. **Apply Reinforcement Learning** - Agents adjust bids based on **rewards & penalties**.
4. **Market Threshold Calculation** - AI models predict market trends.
5. **Winning Bid Selection** - The lowest bid wins the round.
6. **Data Logging & Analysis** - Bid data is stored and analyzed for performance insights.

### ** Streamlit Dashboard Workflow**
1. **Load Bid History** - Fetch real-time data from `data/bid_history.csv`.
2. **Data Filtering & Aggregation** - Process the latest bid values.
3. **Generate Visuals** - Plotly, Seaborn & Matplotlib charts.
4. **Real-Time Updates** - Interactive refresh of bidding insights.
5. **AI Chatbot** - AI-powered Q&A for bidding trends.

---

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
```bash
git clone https://github.com/Shubham-Bishnoi/KPMG-KDN-AI-multi-agent-dynamic-bidding.git
cd AI_MultiAgent_Bidding
```

### **Step 2: Set Up Virtual Environment**
```bash
python3 -m venv myenv
source myenv/bin/activate 
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run the AI Bidding Simulation**
```bash
python main.py
```

### **Step 5: Launch the Dashboard**
```bash
streamlit run frontend/app.py
```

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

###  6. AI Chatbot for Bid Insights
- AI chatbot **answers questions** about bidding trends.




