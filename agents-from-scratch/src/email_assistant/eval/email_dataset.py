"""Email evaluation dataset with ground truth classifications."""

# Common reply email
STANDARD_EMAIL = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "John Doe <john.doe@company.com>",
    "subject": "Quick question about API documentation",
    "email_thread": """Hi John,

I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

Specifically, I'm looking at:
- /auth/refresh
- /auth/validate

Thanks!
Alice""",
}

# Common notification email
NOTIFICATION_EMAIL = {
    "author": "System Admin <sysadmin@company.com>",
    "to": "Development Team <dev@company.com>",
    "subject": "Scheduled maintenance - database downtime",
    "email_thread": """Hi team,

This is a reminder that we'll be performing scheduled maintenance on the production database tonight from 2AM to 4AM EST. During this time, all database services will be unavailable.

Please plan your work accordingly and ensure no critical deployments are scheduled during this window.

Thanks,
System Admin Team"""
}

# Dataset examples
email_input_1 = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Quick question about API documentation",
    "email_thread": """Hi Lance,

I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

Specifically, I'm looking at:
- /auth/refresh
- /auth/validate

Thanks!
Alice""",
}

email_input_2 = {
    "author": "Marketing Team <marketing@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "New Company Newsletter Available",
    "email_thread": """Hello Lance,

The latest edition of our company newsletter is now available on the intranet. This month features articles on our Q2 results, upcoming team building activities, and employee spotlights.

Check it out when you have a chance!

Best regards,
Marketing Team""",
}

email_input_3 = {
    "author": "System Admin <sysadmin@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Scheduled maintenance - database downtime",
    "email_thread": """Hi Lance,

This is a reminder that we'll be performing scheduled maintenance on the production database tonight from 2AM to 4AM EST. During this time, all database services will be unavailable.

Please plan your work accordingly and ensure no critical deployments are scheduled during this window.

Thanks,
System Admin Team""",
}

email_input_4 = {
    "author": "Project Manager <pm@client.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Tax season let's schedule call",
    "email_thread": """Lance,

It's tax season again, and I wanted to schedule a call to discuss your tax planning strategies for this year. I have some suggestions that could potentially save you money.

Are you available sometime next week? Tuesday or Thursday afternoon would work best for me, for about 45 minutes.

Regards,
Project Manager""",
}

email_input_5 = {
    "author": "HR Department <hr@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Reminder: Submit your expense reports",
    "email_thread": """Hello Lance,

This is a friendly reminder that all expense reports for the previous month need to be submitted by this Friday. Please make sure to include all receipts and proper documentation.

If you have any questions about the submission process, feel free to reach out to the HR team.

Best regards,
HR Department""",
}

email_input_6 = {
    "author": "Conference Organizer <events@techconf.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Do you want to attend this conference?",
    "email_thread": """Hi Lance,

We're reaching out to invite you to TechConf 2025, happening May 15-17 in San Francisco. 

The conference features keynote speakers from major tech companies, workshops on AI and ML, and great networking opportunities. Early bird registration is available until April 30th.

Would you be interested in attending? We can also arrange for group discounts if other team members want to join.

Best regards,
Conference Organizers""",
}

email_input_7 = {
    "author": "Sarah Johnson <sarah.j@partner.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Can you review these docs before submission?",
    "email_thread": """Lance,

I've attached the final version of our proposal for the Henderson project. Could you please review the technical specifications section (pages 15-20) before we submit it to the client on Friday?

Your expertise would really help ensure we've covered all the necessary details.

Thanks in advance,
Sarah""",
}

email_input_8 = {
    "author": "Community Pool <info@cityrecreation.org>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Sign up daughter for swimming class",
    "email_thread": """Dear Lance,

Summer swimming registration is now open! Based on your daughter's participation last year, we wanted to let you know that intermediate level classes are available on Mondays and Wednesdays at 4PM or Tuesdays and Thursdays at 5PM.

Classes begin June 1st and run for 8 weeks. Space is limited, so early registration is recommended.

Please let us know if you'd like to reserve a spot.

Regards,
City Recreation Department""",
}

email_input_9 = {
    "author": "GitHub <notifications@github.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "PR #42: Comment from alex-dev",
    "email_thread": """Hey there!

alex-dev commented on your pull request #42 in langchain-ai/project:

> I've reviewed the changes and everything looks good. Just one small suggestion for the error handling in auth_controller.py. Maybe we should add a timeout parameter to prevent hanging requests?

View the comment: https://github.com/langchain-ai/project/pull/42#comment-12345

---
You're receiving this because you authored the thread.
Reply to this email directly, or view it on GitHub
""",
}

email_input_10 = {
    "author": "Team Lead <teamlead@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Quarterly planning meeting",
    "email_thread": """Hi Lance,

It's time for our quarterly planning session. I'd like to schedule a 90-minute meeting next week to discuss our roadmap for Q3.

Could you let me know your availability for Monday or Wednesday? Ideally sometime between 10AM and 3PM.

Looking forward to your input on the new feature priorities.

Best,
Team Lead""",
}

email_input_11 = {
    "author": "AWS Monitoring <no-reply@aws.amazon.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "System admin alert: Instance CPU utilization exceeds threshold",
    "email_thread": """ALERT: High CPU Utilization

The following EC2 instance has exceeded the CPU utilization threshold of 90% for more than 15 minutes:

Instance ID: i-0b2d3e4f5a6b7c8d9
Region: us-west-2
Current utilization: 95.3%

This message is automatically generated. Please do not reply.
""",
}

email_input_12 = {
    "author": "Client Success <success@vendor.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Your subscription will renew automatically",
    "email_thread": """Hello Lance,

This is a friendly reminder that your annual subscription to our Developer Pro plan will automatically renew on 04/15/2025.

Your payment method ending in **** 4567 will be charged $1,499.00.

If you would like to make any changes to your subscription, please visit your account settings or contact our support team before the renewal date.

Thank you for your continued business!

Client Success Team""",
}

email_input_13 = {
    "author": "Dr. Roberts <droberts@medical.org>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Annual checkup reminder",
    "email_thread": """Hello Lance,

This is a reminder that it's time for your annual checkup. Our records show that your last visit was approximately one year ago.

Please call our office at (555) 123-4567 to schedule an appointment at your earliest convenience.

Best regards,
Dr. Roberts' Office""",
}

email_input_14 = {
    "author": "Social Media Platform <notifications@social.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "5 people liked your post",
    "email_thread": """Hi Lance,

5 people liked your recent post about "Machine Learning Techniques for NLP"

See who liked your post and continue the conversation!

[View activity]

To unsubscribe from these notifications, adjust your settings here.
""",
}

email_input_15 = {
    "author": "Project Team <project@company.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Joint presentation next month",
    "email_thread": """Hi Lance,

The leadership team has asked us to prepare a joint presentation on our recent project successes for the all-hands meeting next month.

I've started putting together some slides and would appreciate your input on the technical architecture section. Could we schedule about 60 minutes sometime in the next week to collaborate on this?

I'm generally free on Tuesdays and Thursdays.

Thanks,
Project Team""",
}

email_input_16 = {
    "author": "Marketing Team <marketing@openai.com>",
    "to": "Lance Martin <lance@company.com>",
    "subject": "Newsletter: New Model from OpenAI",
    "email_thread": """Hi Lance,

We're excited to announce that we've released a new model from OpenAI!

It's called "GPT-5" and it's a successor to GPT-4.

It's available now and you can find more information [here](https://openai.com/gpt-5).

Thanks,
Marketing Team""",
}

# Triage outputs: "ignore", "notify", "respond"
triage_output_1 = "respond"
triage_output_2 = "ignore"
triage_output_3 = "notify"
triage_output_4 = "respond"
triage_output_5 = "notify"
triage_output_6 = "respond"
triage_output_7 = "respond"
triage_output_8 = "respond"
triage_output_9 = "notify"
triage_output_10 = "respond"
triage_output_11 = "notify"
triage_output_12 = "notify"
triage_output_13 = "respond"
triage_output_14 = "ignore"
triage_output_15 = "respond"
triage_output_16 = "notify"

# Response criteria (when applicable)
response_criteria_1 = """
• Send email with write_email tool call to acknowledge the question and confirm it will be investigated  
"""

response_criteria_2 = """
• No response needed
• Ensure this is ignored  
"""

response_criteria_3 = """
• No response needed
• Ensure the user is notified  
"""

response_criteria_4 = """
• Check calendar availability for Tuesday or Thursday afternoon next week with check_calendar_availability tool call 
• Confirm availability for a 45-minute meeting
• Send calendar invite with schedule_meeting tool call 
• Send email with write_email tool call to acknowledge tax planning request and notifying that a meeting has been scheduled  
"""

response_criteria_5 = """
• No response needed
• Ensure the user is notified  
"""

response_criteria_6 = """
• Express interest in attending TechConf 2025
• Ask specific questions about AI/ML workshops
• Inquire about group discount details
• Send email with write_email tool call to express interest in attending TechConf 2025, ask specific questions about AI/ML workshops, and inquire about group discount details
"""

response_criteria_7 = """
• Explicitly agree to review the technical specifications
• Acknowledge Friday deadline
• Send email with write_email tool call to explicitly agree to review the technical specifications and acknowledge Friday deadline
"""

response_criteria_8 = """
• Send email with write_email tool call to express interest in registering daughter for swimming class
"""

response_criteria_9 = """
• No response needed
• Ensure the user is notified  
"""

response_criteria_10 = """
• Check calendar for 90-minute meeting availability for Monday or Wednesday with check_calendar_availability tool call 
• Send email acknowledging the request and providing availability with write_email tool call  
"""

response_criteria_11 = """
• No response needed
• Ensure the user is notified  
"""

response_criteria_12 = """
• No response needed
• Ensure the user is notified  
"""

response_criteria_13 = """
• Acknowledge annual checkup reminder
• Send email with write_email tool call to acknowledge annual checkup reminder
"""

response_criteria_14 = """
• No response needed
• Ensure this is ignored  
"""

response_criteria_15 = """
• Check calendar for 60-minute meeting availability for Tuesday or Thursday with check_calendar_availability tool call 
• Send calendar invite with schedule_meeting tool call 
• Send email agreeing to collaborate on the joint presentation and notifying that a meeting has been scheduled with write_email tool call  
"""

response_criteria_16 = """
• No response needed
• Ensure the user is notified  
"""

examples_triage = [
  {
      "inputs": {"email_input": email_input_1},
      "outputs": {"classification": triage_output_1},
  },
  {
      "inputs": {"email_input": email_input_2},
      "outputs": {"classification": triage_output_2},
  },
  {
      "inputs": {"email_input": email_input_3},
      "outputs": {"classification": triage_output_3},
  },
  {
      "inputs": {"email_input": email_input_4},
      "outputs": {"classification": triage_output_4},
  },
  {
      "inputs": {"email_input": email_input_5},
      "outputs": {"classification": triage_output_5},
  },
  {
      "inputs": {"email_input": email_input_6},
      "outputs": {"classification": triage_output_6},
  },
  {
      "inputs": {"email_input": email_input_7},
      "outputs": {"classification": triage_output_7},
  },
  {
      "inputs": {"email_input": email_input_8},
      "outputs": {"classification": triage_output_8},
  },
  {
      "inputs": {"email_input": email_input_9},
      "outputs": {"classification": triage_output_9},
  },
  {
      "inputs": {"email_input": email_input_10},
      "outputs": {"classification": triage_output_10},
  },
  {
      "inputs": {"email_input": email_input_11},
      "outputs": {"classification": triage_output_11},
  },
  {
      "inputs": {"email_input": email_input_12},
      "outputs": {"classification": triage_output_12},
  },
  {
      "inputs": {"email_input": email_input_13},
      "outputs": {"classification": triage_output_13},
  },
  {
      "inputs": {"email_input": email_input_14},
      "outputs": {"classification": triage_output_14},
  },
  {
      "inputs": {"email_input": email_input_15},
      "outputs": {"classification": triage_output_15},
  },
  {
      "inputs": {"email_input": email_input_16},
      "outputs": {"classification": triage_output_16},
  },
]

email_inputs = [
        email_input_1, email_input_2, email_input_3, email_input_4, email_input_5,
        email_input_6, email_input_7, email_input_8, email_input_9, email_input_10,
        email_input_11, email_input_12, email_input_13, email_input_14, email_input_15,
        email_input_16
    ]

email_names = [
    "email_input_1", "email_input_2", "email_input_3", "email_input_4", "email_input_5",
    "email_input_6", "email_input_7", "email_input_8", "email_input_9", "email_input_10",
    "email_input_11", "email_input_12", "email_input_13", "email_input_14", "email_input_15",
    "email_input_16"
]

response_criteria_list = [
    response_criteria_1, response_criteria_2, response_criteria_3, response_criteria_4, response_criteria_5,
    response_criteria_6, response_criteria_7, response_criteria_8, response_criteria_9, response_criteria_10,
    response_criteria_11, response_criteria_12, response_criteria_13, response_criteria_14, response_criteria_15,
    response_criteria_16
]

triage_outputs_list = [
    triage_output_1, triage_output_2, triage_output_3, triage_output_4, triage_output_5,
    triage_output_6, triage_output_7, triage_output_8, triage_output_9, triage_output_10,
    triage_output_11, triage_output_12, triage_output_13, triage_output_14, triage_output_15,
    triage_output_16
]

# Define expected tool calls for each email response based on content analysis
# Options: write_email, schedule_meeting, check_calendar_availability, done
expected_tool_calls = [
    ["write_email", "done"],                                                 # email_input_1: API documentation question
    [],                                                                      # email_input_2: Newsletter notification - ignore
    [],                                                                      # email_input_3: System maintenance notification - notification only
    ["check_calendar_availability", "schedule_meeting", "write_email", "done"], # email_input_4: Tax call scheduling
    [],                                                                      # email_input_5: Expense report reminder - notification only
    ["write_email", "done"],                                                 # email_input_6: Conference invitation - needs response
    ["write_email", "done"],                                                 # email_input_7: Document review request
    ["write_email", "done"],                                                 # email_input_8: Swimming class registration
    [],                                                                      # email_input_9: GitHub PR comment - notification only
    ["check_calendar_availability", "write_email", "done"], # email_input_10: Planning meeting
    [],                                                                      # email_input_11: AWS alert - notification only
    [],                                                                      # email_input_12: Subscription renewal - ignore
    ["write_email", "done"],                                                 # email_input_13: Doctor appointment reminder
    [],                                                                      # email_input_14: Social media notification - no action needed
    ["check_calendar_availability", "schedule_meeting", "write_email", "done"], # email_input_15: Joint presentation
    [],                                                                      # email_input_16: Newsletter - notification only
]