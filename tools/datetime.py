from datetime import datetime
import dateutil.parser

def load_from_config(cfg=None):
    def datetime_tool(query=None):
        """ 
        tool name: datetime
        Arguments
            "now" → returns current datetime
            "%Y-%m-%d" → returns current date in format
            "2025-07-04"  → returns day of the week of the specified date
        """
        if not query or query.lower() == "now":
            return datetime.now().isoformat()

        try:
            # Try parsing as a date string
            parsed = dateutil.parser.parse(query)
            return f"{parsed.strftime('%A, %B %d, %Y')} (Day of week)"
        except Exception:
            pass

        try:
            # Try formatting current date
            return datetime.now().strftime(query)
        except Exception as e:
            return f"[ERROR parsing datetime input: {e}]"

    return datetime_tool
