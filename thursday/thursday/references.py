#test

BUSINESS_TYPE = [
    ("ecommerce", "E-commerce / Retail"),
    ("finance", "Banking / Finance / Insurance"),
    ("healthcare", "Healthcare / Wellness"),
    ("education", "Education / E-learning"),
    ("hospitality", "Hospitality / Travel"),
    ("real_estate", "Real Estate"),
    ("food_beverage", "Food & Beverage"),
    ("telecom", "Telecommunications / Utilities"),
    ("government", "Government / Public Services"),
    ("professional", "Professional Services"),
    ("technology", "Technology / IT"),
    ("media", "Media & Entertainment"),
    ("transportation", "Transportation / Logistics"),
    ("automotive", "Automotive"),
    ("nonprofit", "Nonprofit / Community")
]

CHANNEL_TYPES = [
    ("messenger", "Messenger"),
]

CONVERSATION_STATUS = [
    (0, "Active"),
    (1, "Inactive"),
    (2, "Archived"),
]

SENDER_TYPES = [
    (1, "Customer"),
    (2, "Bot"),
    (3, "System"),
    (4, "Agent"),
]

PLAN = {
  "free": {
    "name": "Free Tier",
    "description": "Free tier for small businesses",
    "token_limit": 10000,
    "duration": 604800,  # 7 days in seconds
  },
  "pro": {
    "name": "Pro Tier",
    "description": "Pro tier for medium businesses",
    "token_limit": 100000,
    "duration": 604800,  # 7 days in seconds
  }
}

BILLING_STATUS = [
    (0, "Pending"),
    (1, "Paid"),
    (2, "Failed"),
]