"""
Test Dataset: 10 Unique Email Generation Scenarios
Each scenario includes: intent, key facts, tone, and a human reference email (gold standard).
"""

TEST_SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up after a job interview",
        "facts": [
            "Interview held on May 2nd with hiring manager Priya Sharma",
            "Role: Senior Data Engineer at Nexus Analytics",
            "Discussed the real-time Kafka pipeline migration project",
            "Interviewer mentioned final decision expected by May 10th",
        ],
        "tone": "Professional, enthusiastic, warm",
        "reference_email": """Subject: Thank You — Senior Data Engineer Interview (May 2nd)

Dear Priya,

Thank you so much for taking the time to speak with me on May 2nd. I genuinely enjoyed our conversation about Nexus Analytics' upcoming Kafka pipeline migration — it's exactly the kind of challenge I find most energising.

The more I reflect on the role, the more confident I am that my experience architecting real-time data systems would let me contribute meaningfully from day one. I'm particularly excited about the scale of the problem you're solving.

I look forward to your update by May 10th and remain very enthusiastic about the opportunity to join the Nexus Analytics team.

Thank you again for your time and consideration.

Warm regards,
[Your Name]""",
    },
    {
        "id": 2,
        "intent": "Request a project deadline extension",
        "facts": [
            "Original deadline: July 15th",
            "Requested new deadline: July 30th",
            "Project: CRM Migration for client Apex Solutions",
            "Reason: Unexpected data schema inconsistencies discovered",
            "Manager's name: David Okafor",
        ],
        "tone": "Formal, accountable, solution-oriented",
        "reference_email": """Subject: Extension Request — CRM Migration Deadline (July 15 → July 30)

Dear David,

I am writing to formally request a two-week extension on the CRM Migration project for Apex Solutions, shifting the delivery date from July 15th to July 30th.

During data validation last week, our team identified significant schema inconsistencies in the legacy system that were not surfaced during initial scoping. Addressing these correctly is non-negotiable for data integrity — rushing this phase would create downstream risks for Apex Solutions that far outweigh a two-week delay.

I have already prioritised this work above other tasks and am confident the July 30th date is achievable without further slippage. I am happy to provide a detailed remediation plan if helpful.

Thank you for your understanding, and please let me know if you'd like to discuss this further.

Respectfully,
[Your Name]""",
    },
    {
        "id": 3,
        "intent": "Apologise to a client for a service outage",
        "facts": [
            "Client: Meridian Retail Group",
            "Outage duration: 4 hours on April 28th",
            "Service affected: Order Management Platform",
            "Estimated revenue impact for client: $12,000",
            "Root cause: Database failover misconfiguration",
            "Compensation offered: 20% credit on next invoice",
        ],
        "tone": "Empathetic, accountable, professional",
        "reference_email": """Subject: Sincere Apology — April 28th Service Outage | Meridian Retail Group

Dear Meridian Retail Group Team,

I want to reach out personally to apologise for the four-hour outage to your Order Management Platform on April 28th. We fully understand the operational disruption this caused, and we recognise the estimated $12,000 revenue impact is significant — that is unacceptable, and I am sorry.

Our engineering team has identified the root cause as a database failover misconfiguration that slipped through our deployment validation process. We have since implemented additional safeguards to ensure this class of error cannot recur.

As a gesture of accountability, we will be applying a 20% credit to your next invoice. More importantly, I want to personally assure you that platform reliability is our highest priority going forward.

Please don't hesitate to reach out if you have questions or concerns. We value your partnership greatly and are committed to earning back your trust.

Sincerely,
[Your Name]""",
    },
    {
        "id": 4,
        "intent": "Cold outreach to a potential business partner",
        "facts": [
            "Recipient: James Harlow, CEO of GreenTech Ventures",
            "Sender's company: EcoLoop, a circular economy platform",
            "Common ground: Both spoke at SustainX Summit 2024",
            "Proposal: Explore a joint pilot programme for SME clients",
            "Specific value: EcoLoop's tracking tech + GreenTech's distribution network",
        ],
        "tone": "Confident, concise, collaborative",
        "reference_email": """Subject: EcoLoop x GreenTech — Joint Pilot Opportunity

Hi James,

Your keynote at SustainX Summit 2024 on scaling circular economy solutions for SMEs stuck with me — it maps almost exactly to the problem EcoLoop is built to solve.

EcoLoop is a circular economy platform that gives businesses real-time visibility into their material flows and waste streams. I believe there's a compelling joint opportunity here: pairing our tracking technology with GreenTech Ventures' distribution network could make a meaningful pilot programme for SME clients genuinely feasible.

I'd love to explore whether this is worth a 20-minute conversation. Would you have availability in the next fortnight?

Best,
[Your Name]""",
    },
    {
        "id": 5,
        "intent": "Send a meeting recap and action items",
        "facts": [
            "Meeting: Q2 Marketing Strategy session on May 1st",
            "Attendees: Lisa Wang, Tom Reeves, Anika Patel",
            "Decision 1: Launch paid social campaign by May 20th",
            "Decision 2: Lisa to own influencer shortlist by May 8th",
            "Decision 3: Tom to share revised budget by May 6th",
            "Next meeting: May 15th at 10am",
        ],
        "tone": "Organised, clear, friendly",
        "reference_email": """Subject: Recap & Actions — Q2 Marketing Strategy | May 1st

Hi Lisa, Tom, and Anika,

Thanks for a productive session this morning. Here's a quick recap to keep us aligned:

Key Decisions:
- Paid social campaign to launch by May 20th
- Lisa: Influencer shortlist due by May 8th
- Tom: Revised budget to be shared by May 6th

Our next check-in is confirmed for May 15th at 10am — I'll send the calendar invite shortly.

Please flag anything I've missed or any blockers that come up in the meantime. Looking forward to seeing this come together!

Best,
[Your Name]""",
    },
    {
        "id": 6,
        "intent": "Negotiate a software vendor contract renewal",
        "facts": [
            "Vendor: CloudScale Inc.",
            "Current annual contract: $48,000",
            "Target price: $38,000 (reduced by ~21%)",
            "Justification: Competitor quote of $35,000 from DataStack Pro",
            "Relationship length: 3 years",
            "Key ask: Multi-year discount or added features at same price",
        ],
        "tone": "Assertive, respectful, business-focused",
        "reference_email": """Subject: Contract Renewal Discussion — CloudScale Inc. Partnership

Dear CloudScale Team,

As we approach our annual renewal, I wanted to open a direct conversation about pricing before we move forward.

We have been a loyal CloudScale customer for three years and value the stability your platform provides. However, our procurement review has surfaced a competitive quote from DataStack Pro at $35,000 annually — a meaningful gap from our current $48,000 contract.

Our preference is to continue with CloudScale. To make that straightforward to justify internally, I'd like to explore either a revised rate in the range of $38,000 or a multi-year arrangement with additional features at the existing price point.

I'm available for a call this week if you'd like to discuss. I hope we can find an arrangement that reflects our long-standing relationship.

Best regards,
[Your Name]""",
    },
    {
        "id": 7,
        "intent": "Welcome a new team member",
        "facts": [
            "New hire: Marcus Osei",
            "Role: Product Designer",
            "Start date: May 6th",
            "Team: Digital Product team",
            "Buddy assigned: Camille Nguyen",
            "First day includes: office tour, onboarding docs, team lunch at 12:30pm",
        ],
        "tone": "Warm, enthusiastic, welcoming",
        "reference_email": """Subject: Welcome to the Team, Marcus! 🎉

Hi Marcus,

We're so excited to have you joining the Digital Product team as our new Product Designer on May 6th!

Here's what your first day looks like: we'll kick off with an office tour and get you set up with all your onboarding materials, and then we'll head out for a team lunch at 12:30pm — a great chance to meet everyone in a relaxed setting.

Camille Nguyen will be your buddy as you settle in, so feel free to lean on her for anything — no question is too small.

We've been looking forward to your arrival and can't wait to see what you bring to the team. See you Tuesday!

Warmly,
[Your Name]""",
    },
    {
        "id": 8,
        "intent": "Escalate an unresolved customer support issue",
        "facts": [
            "Customer: Sandra Bell",
            "Original ticket number: #TKT-88423",
            "Issue: Invoice not generated for March subscription",
            "Ticket open for: 14 days with no resolution",
            "Customer impact: Cannot file expense report",
            "Escalating to: Head of Support, Ryan Fletcher",
        ],
        "tone": "Urgent, professional, factual",
        "reference_email": """Subject: Urgent Escalation — Ticket #TKT-88423 | 14 Days Unresolved

Dear Ryan,

I am escalating ticket #TKT-88423 as it has now been open for 14 days without resolution and is directly impacting our customer Sandra Bell.

The issue: Sandra's invoice for her March subscription was never generated. As a result, she is unable to file her expense report — a tangible, ongoing business disruption that grows more serious with each passing day.

Despite the ticket being logged two weeks ago, Sandra has not received a resolution or a substantive update. This is not the service standard we hold ourselves to, and I want to ensure this is personally reviewed and resolved within 24 hours.

I would appreciate your direct involvement. Please let me know how I can assist in expediting this.

Regards,
[Your Name]""",
    },
    {
        "id": 9,
        "intent": "Invite a speaker to a company event",
        "facts": [
            "Event: InnovateTech Annual Conference 2025",
            "Date: September 12th, Bangalore",
            "Invitee: Dr. Meera Iyer, AI Ethics researcher",
            "Talk topic: Responsible AI in enterprise environments",
            "Audience: 500+ tech leaders and executives",
            "Honorarium: ₹75,000 + travel and accommodation covered",
        ],
        "tone": "Flattering, professional, enthusiastic",
        "reference_email": """Subject: Speaker Invitation — InnovateTech 2025 | Dr. Meera Iyer

Dear Dr. Iyer,

I am reaching out on behalf of InnovateTech to extend a personal invitation for you to speak at our Annual Conference 2025, taking place on September 12th in Bangalore.

Your research on AI ethics is exceptionally well-regarded, and we believe your perspective on responsible AI in enterprise environments would be both timely and invaluable for our audience of 500+ technology leaders and executives. This is precisely the conversation our community needs to be having.

We would be honoured to cover travel and accommodation in full, along with an honorarium of ₹75,000.

We understand your schedule is demanding and would be delighted to work around your availability. I would love to hop on a brief call at your convenience to share more about the event.

With great admiration,
[Your Name]""",
    },
    {
        "id": 10,
        "intent": "Decline a partnership proposal politely",
        "facts": [
            "Proposal received from: Bright Media Agency",
            "Proposal: Co-branded content series",
            "Reason for declining: Brand misalignment",
            "Keep door open for future",
            "Contact at Bright Media: Sofia Andrade",
        ],
        "tone": "Polite, gracious, diplomatic",
        "reference_email": """Subject: Re: Co-Branded Content Series Proposal

Dear Sofia,

Thank you for sharing the co-branded content series proposal — it's clear that a great deal of thought went into it, and I appreciate you reaching out.

After careful consideration, we have decided not to move forward with this particular collaboration at this time. This decision comes down to brand fit rather than the quality of your proposal, which was genuinely impressive.

We have a narrow set of criteria for partnership alignment right now, and we want to be respectful of your time rather than enter into something that isn't the right match for both parties.

That said, I'd be glad to stay in touch. As both our organisations evolve, there may well be opportunities for collaboration that make more sense.

Thank you again, Sofia, and I wish Bright Media continued success.

Kind regards,
[Your Name]""",
    },
]


if __name__ == "__main__":
    print(f"Total test scenarios: {len(TEST_SCENARIOS)}")
    for s in TEST_SCENARIOS:
        print(f"  Scenario {s['id']}: {s['intent'][:60]}")
