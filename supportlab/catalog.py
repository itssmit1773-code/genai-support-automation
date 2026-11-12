"""Versioned, fictional knowledge base for RelayDesk."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    category: str
    text: str
    risk: str
    shortcut: str
    phrases: tuple[str, ...]
    weight: int
    minutes: int


CATALOG = {
    "export": Article("Reporting", "Open Reports → Saved reports → Download CSV. Only fields you can view are included.",
                      "Low", "download report", (
        "download report as a csv", "csv export for a saved report", "export the table from reports",
        "save report results to a spreadsheet", "get csv from a saved report",
        "download the current report rows", "report data export as a file",
        "where can I export a report", "need a csv copy of this report",
        "pull report figures into csv", "can I extract report results", "how to get a spreadsheet of the report"), 23, 7),
    "schedule": Article("Reporting", "Open Reports → Schedules → Pause. Existing deliveries stay in the activity log.",
                        "Low", "pause schedule", (
        "pause schedule for a recurring report", "stop scheduled reports from emailing",
        "turn off the report schedule", "cancel future delivery of my report",
        "suspend recurring report emails", "pause automatic report delivery", "stop the report mailing schedule",
        "disable scheduled delivery", "pause tomorrow's report email", "halt recurring reports",
        "can I stop a report subscription", "the report keeps landing in my inbox"), 15, 9),
    "receipt": Article("Billing", "A billing admin can open Settings → Billing → Invoices and download a receipt.",
                       "Low", "download receipt", (
        "download receipt for our last payment", "get the invoice pdf", "find an invoice receipt",
        "download a paid invoice from billing", "need a receipt for accounting", "where can I find paid invoices",
        "get a copy of the receipt", "download the billing invoice", "our finance team needs a receipt",
        "retrieve the pdf invoice", "need a record of what we paid", "where is the payment paperwork"), 17, 8),
    "invite": Article("Workspace access", "Open Settings → Members → Pending invites and select Resend for the intended recipient.",
                      "Low", "resend invite", (
        "resend invite to a teammate", "pending invite needs another email", "send workspace invitation again",
        "member invitation did not arrive", "send the invite email a second time", "retry a pending invite",
        "workspace invitation never came", "resend a pending member invite", "how to reissue the invite",
        "send another invitation to the workspace", "teammate never got the link", "can I renew a member invitation"), 16, 10),
    "sync": Article("Integrations", "Collect the connector name and last successful sync time. Route to Integrations for diagnosis.",
                    "Medium", "", (
        "connector sync stopped", "integration jobs stopped syncing", "sync queue has an error",
        "connector stopped updating records", "latest records missing from the sync", "integration has a stale sync",
        "sync retry is failing", "connector is missing new records", "the sync is stuck",
        "integration data is stale", "linked app hasn't updated since yesterday", "import runs keep hanging"), 11, 24),
    "refund": Article("Billing", "Route the dispute to Billing. An agent checks entitlement and approves any adjustment.",
                      "High", "", (
        "refund for duplicate billing", "reverse the extra payment", "charged twice on the invoice",
        "credit us for an unexpected charge", "billing chargeback after duplicate payment",
        "request refund for this receipt", "invoice has an unauthorized charge", "need to dispute a payment",
        "billing charged us twice", "money back for this payment", "this receipt shows a second debit",
        "want that transaction reversed"), 8, 25),
    "takeover": Article("Workspace access", "Route suspected compromise to Security through the incident queue.",
                        "High", "", (
        "unknown login to workspace", "suspected account takeover", "credentials may have been exposed",
        "suspicious access by another person", "unrecognized login alert", "an attacker accessed our workspace",
        "possible compromise of credentials", "unknown sign-in event", "account hijack suspected",
        "unexpected access from a stranger", "someone else is using our login", "an unfamiliar device took over"), 6, 32),
    "erasure": Article("Data governance", "Route to Privacy for identity verification and a retention review.",
                       "High", "", (
        "permanently delete customer data", "personal data erasure request", "erase a former user's records",
        "request deletion of personal information", "remove all user records permanently", "privacy erasure ticket",
        "delete a person's stored data", "remove personal records under privacy rights",
        "erase this person's data", "irreversible deletion of customer information",
        "wipe this former member from storage", "need someone's profile scrubbed from records"), 4, 36),
}

