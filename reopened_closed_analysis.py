import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from data_loader import DataLoader
import config

class ReopenedClosedAnalysis:
    def __init__(self):
        # Load output directory from config
        self.output_dir = config.get_parameter("output_dir")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze(self):
        all_issues = DataLoader().get_issues()
        print(f"Loaded {len(all_issues)} issues from dataset.")

        start_input = input("Start date (YYYY-MM-DD) [press Enter to skip]: ").strip()
        end_input = input("End date (YYYY-MM-DD) [press Enter to skip]: ").strip()

        start_date = pd.to_datetime(start_input, utc=True) if start_input else None
        end_date = pd.to_datetime(end_input, utc=True) if end_input else None

        issue_records = []
        filtered_dates = []

        for issue in all_issues:
            created_time = pd.to_datetime(issue.created_date, utc=True).tz_convert(None)

            if start_date and created_time < start_date.tz_convert(None):
                continue
            if end_date and created_time > end_date.tz_convert(None):
                continue

            filtered_dates.append(created_time)
            status = 'Open' if issue.state.lower() == 'open' else 'Closed'
            if issue.state.lower() == 'closed':
                for ev in getattr(issue, 'events', []):
                    if getattr(ev, 'event_type', '').lower() == 'reopened':
                        status = 'Reopened'
                        break

            issue_records.append({'number': issue.number, 'status': status})

        if not issue_records:
            print("No issues found in the specified range.")
            return

        df_summary = pd.DataFrame(issue_records)
        counts = df_summary['status'].value_counts()
        total = counts.sum()

        print("\nSummary of issue statuses:")
        for st, ct in counts.items():
            print(f"{st}: {ct} ({ct / total:.1%})")

        if filtered_dates:
            print(f"Issue data range: {min(filtered_dates).date()} → {max(filtered_dates).date()}")

        print("-" * 40)

        # Create pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Distribution of Issue Statuses")
        plt.tight_layout()

        save_choice = input("\nDo you want to save this chart as a PNG file? (y/n): ").strip().lower()
        if save_choice == 'y':
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"issue_status_chart_{timestamp}.png"
            file_path = os.path.join(self.output_dir, filename)
            plt.savefig(file_path, dpi=300)
            print(f"✅ Chart saved to: {file_path}")
        else:
            print("Chart not saved. Displaying instead...")

        plt.show()


if __name__ == '__main__':
    ReopenedClosedAnalysis().analyze()