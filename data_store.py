from datetime import datetime

# Store entries in memory
entries = []

def save_entry(text, analysis):
    entries.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
        **analysis
    })

def get_entries():
    return list(reversed(entries))
