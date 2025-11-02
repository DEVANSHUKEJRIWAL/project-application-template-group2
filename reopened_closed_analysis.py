from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue, Event

class ReopenedClosedRatioAnalysis:
    def __init__(self):
        pass

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()

        if not issues:
            print("No issues loaded.")
            return

        start_input = input("\nStart date (YYYY-MM-DD) or press Enter to skip: ").strip()
        end_input = input("End date (YYYY-MM-DD) or press Enter to skip: ").strip()

        start_date = pd.to_datetime(start_input, utc=True) if start_input else None
        end_date = pd.to_datetime(end_input, utc=True) if end_input else None

        data = []
        filtered_dates = []

        for issue in issues:
            created = pd.to_datetime(getattr(issue, 'created_date', None), utc=True)
            if pd.isna(created):
                continue
            created_date = created.tz_convert(None)

            if start_date and created_date < start_date.tz_convert(None):
                continue
            if end_date and created_date > end_date.tz_convert(None):
                continue

            filtered_dates.append(created_date)

            state = getattr(issue, 'state', '').lower()
            events: List[Event] = getattr(issue, 'events', [])

            if state == 'open':
                status = 'Open'
            elif state == 'closed':
                reopened_events = [e for e in events if getattr(e, 'event_type', '').lower() == 'reopened']
                status = 'Reopened' if reopened_events else 'Closed'
            else:
                status = 'Unknown'

            data.append({'issue_number': getattr(issue, 'number', 0), 'status': status})

        if not data:
            print("\nNo issues found in this range.\n")
            return

        df = pd.DataFrame(data)
        counts = df['status'].value_counts()
        total_issues = counts.sum()

        print("\nIssue Status Summary")
        print("-" * 40)
        for status, count in counts.items():
            ratio = count / total_issues
            print(f"{status}: {count} issues ({ratio:.2%})")

        if filtered_dates:
            first_date = min(filtered_dates)
            last_date = max(filtered_dates)
            print(f"\nIssue data range: {first_date.date()} -> {last_date.date()}")
        print("-" * 40)

        plt.figure(figsize=(6, 6))
        plt.pie(
            counts,
            labels=counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=['blue', 'orange', 'green', 'grey']
        )
        plt.title("Issue Status Ratio (Open / Closed / Reopened)")
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    ReopenedClosedRatioAnalysis().run()
