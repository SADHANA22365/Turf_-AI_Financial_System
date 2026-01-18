from flask import Flask, render_template, request, jsonify, session
import sqlite3

from ai.ai_summary import generate_ai_summary
from ai.business_metrics import calculate_business_metrics
from ai.chatbot_ai import generate_chatbot_response

app = Flask(__name__)
app.secret_key = "turf-ai-secret"   # required for session storage

# --------------------------------
# FINANCIAL CALCULATION (MONTH-WISE)
# --------------------------------
def get_financial_data(month_number, month_name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) * t.price_per_slot
        FROM bookings b
        JOIN turfs t ON b.turf_id = t.id
        WHERE b.status = 'Confirmed'
        AND strftime('%m', b.date) = ?
    """, (month_number,))
    booking_income = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(amount)
        FROM income
        WHERE month = ?
    """, (month_name,))
    extra_income = cursor.fetchone()[0] or 0

    total_income = booking_income + extra_income

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE month = ?
    """, (month_name,))
    total_expense = cursor.fetchone()[0] or 0

    conn.close()

    profit = total_income - total_expense
    return total_income, total_expense, profit


# --------------------------------
# DASHBOARD ROUTE
# --------------------------------
@app.route("/")
def dashboard():
    current_month_number = "01"
    current_month_name = "January"
    previous_month_number = "12"
    previous_month_name = "December"

    income, expense, profit = get_financial_data(
        current_month_number, current_month_name
    )
    _, _, prev_profit = get_financial_data(
        previous_month_number, previous_month_name
    )

    times_increase = round(profit / prev_profit, 1) if prev_profit else 0

    ai_summary = generate_ai_summary(
        income=income,
        expense=expense,
        profit=profit,
        prev_profit=prev_profit,
        growth=0
    )

    whatsapp_message = f"""
📊 Turf Monthly Summary ({current_month_name})

💰 Income: ₹{income}
💸 Expenses: ₹{expense}
📈 Profit: ₹{profit}

📊 Profit increased ~{times_increase} times compared to last month

🤖 AI Insights:
{ai_summary}
"""

    return render_template(
        "index.html",
        income=income,
        expense=expense,
        profit=profit,
        whatsapp_message=whatsapp_message
    )


# --------------------------------
# CHATBOT ROUTE (WITH MEMORY)
# --------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json.get("message")

    if not user_question:
        return jsonify({"reply": "Please ask a valid question."})

    # Initialize chat history in session
    if "chat_history" not in session:
        session["chat_history"] = []

    # Add user message to history
    session["chat_history"].append({
        "role": "user",
        "content": user_question
    })

    # Keep only last 4 messages
    session["chat_history"] = session["chat_history"][-4:]

    current_month_number = "01"
    current_month_name = "January"
    previous_month_number = "12"
    previous_month_name = "December"

    income, expense, profit = get_financial_data(
        current_month_number, current_month_name
    )
    _, _, prev_profit = get_financial_data(
        previous_month_number, previous_month_name
    )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE status='Confirmed'
        AND strftime('%m', date)=?
    """, (current_month_number,))
    current_bookings = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE status='Confirmed'
        AND strftime('%m', date)=?
    """, (previous_month_number,))
    prev_bookings = cursor.fetchone()[0] or 0

    conn.close()

    metrics = calculate_business_metrics(
        current_income=income,
        current_expense=expense,
        current_profit=profit,
        prev_profit=prev_profit,
        current_bookings=current_bookings,
        prev_bookings=prev_bookings
    )

    financials = {
        "income": income,
        "expense": expense,
        "profit": profit,
        "prev_profit": prev_profit,
        "current_bookings": current_bookings,
        "prev_bookings": prev_bookings
    }

    ai_reply = generate_chatbot_response(
        financials=financials,
        metrics=metrics,
        user_question=user_question,
        chat_history=session["chat_history"]
    )

    # Save AI reply in history
    session["chat_history"].append({
        "role": "assistant",
        "content": ai_reply
    })

    session["chat_history"] = session["chat_history"][-4:]

    return jsonify({"reply": ai_reply})


# --------------------------------
# START SERVER (ALWAYS LAST)
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
