# BuyWise

Find the right product for you, faster.

BuyWise is an AI-inspired shopping decision assistant for e-commerce scenarios.

It helps users compare products based on personal priorities, understand trade-offs between alternatives, and decide whether now is a good time to buy.

## Core Features

- Personalized recommendation based on weighted user preferences
- Price timing insight using recent price history
- Product comparison cards for quick scanning
- Feature comparison radar
- Alternative product exploration
- AI-style shopping insight with rule-based recommendation logic

## Problem

Online shoppers often compare products across multiple pages, reviews, and price histories.

Most comparison tools show data, but do not truly help users decide.

BuyWise was designed to answer three key questions:

1. Which product fits my priorities best?
2. Is now a good time to buy?
3. If I do not choose the top recommendation, what is the next best option?

## Product Concept

BuyWise combines three layers of decision support:

- Preference-based recommendation  
  Users can adjust the importance of price, reviews, battery life, noise cancellation, and after-sale support.

- Product comparison  
  Users can quickly compare a selected set of products through overview cards and a radar chart.

- Buying timing insight  
  Users can inspect price history and determine whether the current price looks attractive.

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```md

Future Improvements
	•	Real marketplace data integration
	•	Promotion timing prediction
	•	Brand and ecosystem preference modeling
	•	LLM-generated shopping explanations
	•	Personalized recommendations based on user history

Repository

https://github.com/chloeyuen13/buywise
