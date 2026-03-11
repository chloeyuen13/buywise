# BuyWise

Find the right product for you, faster.

BuyWise is an AI-inspired shopping decision assistant for e-commerce scenarios.

It helps users compare products based on personal priorities, understand trade-offs between alternatives, and decide whether now is a good time to buy.

## Overview

Most online shopping comparison tools show product data, but they do not truly help users make a decision.

BuyWise was designed to support three common shopping questions.

1. Which product fits my priorities best
2. Is the current price attractive enough to buy now
3. If I do not choose the top recommendation, what is the next best option

This project turns static product comparison into a more decision-oriented shopping experience.

## Core Features

- Personalized recommendation based on weighted user preferences
- Product comparison cards for quick scanning
- Feature comparison radar for visual comparison
- Price timing insight using recent price history
- Alternative product exploration on demand
- AI-style shopping insight powered by rule-based recommendation logic

## Problem

Online shoppers often compare products across multiple pages, reviews, and price histories.

Most comparison tools focus on showing information, but not on helping users decide.

In real shopping scenarios, users are usually trying to answer three practical questions.

1. Which option fits my needs best
2. Is now the right time to buy
3. If I skip the top recommendation, what should I consider next

## Product Concept

BuyWise combines three layers of decision support.

### Preference-based recommendation

Users can adjust the importance of price, reviews, battery life, noise cancellation, and after-sale support.

### Product comparison

Users can quickly compare a selected set of products through overview cards and a radar chart.

### Buying timing insight

Users can inspect recent price history and determine whether the current price looks attractive.

## Why I Built This

I built BuyWise to explore how an AI-inspired product experience can support decision-making in e-commerce.

Rather than treating AI as a chatbot layer, this project focuses on decision structure. The goal was to help users move from comparing information to making a clearer and more confident choice.

## Design Decisions

### Recommendation comes first

Users usually want an answer before they want a full analysis. That is why the product surfaces the top recommendation early in the experience.

### Price timing is part of the decision

A product may match a user well, but the current price may still make it a poor purchase moment. BuyWise therefore places price timing insight close to the recommendation layer.

### Alternatives are explored only when needed

Showing full analysis for every product at once made the interface feel too heavy. The final design allows users to inspect alternative products on demand.

## Prototype Scope

This version includes:

- product selection
- weighted preference setup
- personalized scoring
- recommendation output
- price timing insight
- product comparison overview
- alternative product inspection
- AI-style summary

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

- Real marketplace data integration
- Promotion timing prediction
- Brand and ecosystem preference modeling
- LLM-generated shopping explanations
- Personalized recommendations based on user history

## Repository

https://github.com/chloeyuen13/buywise
