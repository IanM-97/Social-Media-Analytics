from twitter_analytics import ReportDownloader
import csv


reports = ReportDownloader(
    username='themanmahon',
    password='Chocolate1',
)

reports_filepath = reports.run()            # list of filepaths of downloaded csv reports

# Then you can parse the csv simply as follow
tweets = list()
for report in reports_filepath:
    with open(report, 'r') as csvfile:
        r = csv.DictReader(csvfile)
        rows = [row for row in r]
        tweets += rows