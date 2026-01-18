import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ai_summary(income, expense, profit, prev_profit, growth):
    # Calculate times increase safely
    times_increase = round(profit / prev_profit, 1) if prev_profit else 0

    prompt = f"""
You are an AI assistant for a SPORTS TURF BOOKING business.

Context:
- Turf refers to a sports ground booked by the hour
- Revenue mainly comes from turf bookings and small add-ons like snacks

Financial Performance:
- Current Month Income: ₹{income}
- Current Month Expenses: ₹{expense}
- Current Month Profit: ₹{profit}
- Previous Month Profit: ₹{prev_profit}
- Profit Growth: approximately {times_increase} times compared to last month

Instructions:
1. Write a short financial summary (1–2 lines)
2. Clearly state that profit increased or decreased using "times increase" wording
3. Give ONE simple, practical suggestion related ONLY to:
   - increasing bookings
   - pricing strategy
   - time slot utilization
   - offers or discounts

Do NOT mention percentages.
Do NOT suggest consulting or unrelated services.
Keep the explanation simple and business-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
