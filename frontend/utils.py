from datetime import datetime


# ---------------------------------
# Health Score Color
# ---------------------------------

def health_color(score):

    if score >= 80:
        return "green"

    elif score >= 60:
        return "orange"

    return "red"


# ---------------------------------
# Health Badge
# ---------------------------------

def health_status(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    return "Poor"


# ---------------------------------
# Percentage Formatter
# ---------------------------------

def percentage(value):

    return f"{value:.2f}%"


# ---------------------------------
# Number Formatter
# ---------------------------------

def number(value):

    return f"{value:,}"


# ---------------------------------
# Date Formatter
# ---------------------------------

def format_date(date):

    if date is None:
        return "-"

    return date.strftime("%d %b %Y")


# ---------------------------------
# Repository Age
# ---------------------------------

def repository_age(created_at):

    if created_at is None:
        return 0

    return (datetime.now() - created_at).days


# ---------------------------------
# API Error Handler
# ---------------------------------

def api_error(response):

    try:
        return response.json()["detail"]

    except Exception:
        return "Something went wrong."