from django.conf import settings
from analytics.services import SpendingAnalytics
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class FinancialAdvisor:
    def __init__(self, user):
        self.user = user
        self.analytics = SpendingAnalytics(user)

    def get_advice(self, question):
        report = self.analytics.get_full_report()
        prompt = f"""You are FinBuddy AI, a friendly financial advisor. Here's the user's spending data:

Total Spent: ₹{report['total_spent']}
Monthly Income: ₹{report['monthly_income']}
By Category: {report['by_category']}

User Question: {question}

IMPORTANT: Respond in PLAIN TEXT ONLY. No markdown, no asterisks, no formatting. Just normal sentences with line breaks between paragraphs. Be conversational and friendly."""

        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text

    def get_roast(self):
        report = self.analytics.get_full_report()
        prompt = f"""You are FinBuddy AI's "Roast Mode" - brutally honest and funny.

Total Spent: ₹{report['total_spent']}
Monthly Income: ₹{report['monthly_income']}
Categories: {report['by_category']}

Give a SHORT roast (3-4 sentences) about their spending. Plain text only, no formatting, no asterisks. Be witty and constructive."""

        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
