"""
MetadataAgent
- run(text: str) -> dict
Simple regex-based metadata extraction (dates YYYY-MM-DD, customer IDs like CUS-12345, currency amounts)
"""
import re
from core.logger import logger

class MetadataAgent:
    def run(self, text: str):
        md = {}
        # find dates YYYY-MM-DD
        dates = re.findall(r'\b(20\d{2}-\d{2}-\d{2})\b', text)
        if dates:
            md['dates'] = dates
        # customer id like CUS-12345
        cust = re.findall(r'\b(CUS[-_ ]?\d{3,10})\b', text, flags=re.IGNORECASE)
        if cust:
            md['customerId'] = cust[0]
        # amounts like $123,456.78 or 123,456.78
        amt = re.findall(r'(\$\s?\d{1,3}(?:[\d,]*)(?:\.\d{1,2})?)', text)
        if amt:
            md['amounts'] = amt
        return md
