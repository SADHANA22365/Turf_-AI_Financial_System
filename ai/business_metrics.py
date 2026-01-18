def calculate_business_metrics(
    current_income,
    current_expense,
    current_profit,
    prev_profit,
    current_bookings,
    prev_bookings
):
    # Booking trend
    if current_bookings > prev_bookings:
        booking_trend = "increased"
    elif current_bookings < prev_bookings:
        booking_trend = "decreased"
    else:
        booking_trend = "stable"

    # Utilization logic (dummy but realistic)
    if current_bookings < 20:
        utilization = "Low"
    elif 20 <= current_bookings <= 35:
        utilization = "Medium"
    else:
        utilization = "High"

    # Revenue efficiency
    revenue_per_booking = (
        round(current_income / current_bookings, 2)
        if current_bookings > 0 else 0
    )

    # Profit trend
    if current_profit > prev_profit:
        profit_trend = "Improved"
    elif current_profit < prev_profit:
        profit_trend = "Declined"
    else:
        profit_trend = "Unchanged"

    return {
        "booking_trend": booking_trend,
        "utilization": utilization,
        "revenue_per_booking": revenue_per_booking,
        "profit_trend": profit_trend
    }
