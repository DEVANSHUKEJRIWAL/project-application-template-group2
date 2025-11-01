from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
from model import Issue


class IssueCreationTrendAnalysis:
    """
    Issue Creation Trend Over Time
    ---------------------------------
    - If a year is entered: shows issues created each month in that year.
    - If no year is entered: shows issues created per year.
    """

    def __init__(self):
        pass

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()

        year_input = input("\nEnter a year to filter by (or press Enter to analyze all years): ").strip()
        year_filter = int(year_input) if year_input else None

        df = pd.DataFrame.from_records([
            {'created_date': issue.created_date} for issue in issues if getattr(issue, 'created_date', None)
        ])

        df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
        df = df.dropna(subset=['created_date'])

        df['year'] = df['created_date'].dt.year
        df['month'] = df['created_date'].dt.month_name()

        if year_filter:
            df = df[df['year'] == year_filter]
            if df.empty:
                print(f"\nNo issues found for year {year_filter}.\n")
                return

            trend = df.groupby('month').size().reset_index(name='issue_count')
            trend['month'] = pd.Categorical(
                trend['month'],
                categories=[
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ],
                ordered=True
            )
            trend = trend.sort_values('month')

            print(f"\nShowing monthly issue trend for year {year_filter}\n")

            plt.figure(figsize=(12, 6))
            plt.plot(trend['month'], trend['issue_count'], marker='o', color='teal', linewidth=2)
            plt.title(f'Issue Creation Trend in {year_filter}')
            plt.xlabel('Month')
            plt.ylabel('Number of Issues Created')
            plt.grid(True, linestyle='--', alpha=0.5)

        else:
            trend = df.groupby('year').size().reset_index(name='issue_count')
            print("\nShowing yearly issue creation trend\n")

            plt.figure(figsize=(10, 5))
            plt.bar(trend['year'].astype(str), trend['issue_count'], color='teal')
            plt.title('Issue Creation Trend by Year')
            plt.xlabel('Year')
            plt.ylabel('Number of Issues Created')
            plt.grid(axis='y', linestyle='--', alpha=0.5)

        total_issues = trend['issue_count'].sum()
        avg_issues = trend['issue_count'].mean() if not trend.empty else 0
        if year_filter:
            print(f"\nSummary for {year_filter}")
            print("-" * 40)
            print(f"Total issues created: {total_issues}")
            print(f"Average issues per month: {avg_issues:.2f}")
            print(f"Number of months with issue activity: {len(trend[trend['issue_count'] > 0])}")

            most_active = trend.loc[trend['issue_count'].idxmax()]
            print(f"Most active month: {most_active['month']} ({int(most_active['issue_count'])} issues)")
        else:
            print("\nOverall Summary (All Years)")
            print("-" * 40)
            print(f"Total issues analyzed: {total_issues}")
            print(f"Average issues per year: {avg_issues:.2f}")
            print(f"Years with recorded issues: {len(trend)}")

            most_active = trend.loc[trend['issue_count'].idxmax()]
            print(f"Most active year: {int(most_active['year'])} ({int(most_active['issue_count'])} issues)")

        first_date = df['created_date'].min().strftime('%Y-%m-%d')
        last_date = df['created_date'].max().strftime('%Y-%m-%d')
        print(f"Issue data range: {first_date} → {last_date}")
        print("-" * 40)


        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    IssueCreationTrendAnalysis().run()
