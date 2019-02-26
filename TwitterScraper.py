from twitter_analytics import ReportDownloader
import csv


reports = ReportDownloader(
    username='themanmahon',
    password='Chocolate1',
    from_date='03/28/2014',         # must be in string format 'mm/dd/yyyy' and nothing before October 2013 (twitter restriction).
    to_date='12/31/2016'
)

reports_filepath = reports.run()            # list of filepaths of downloaded csv reports

# Then you can parse the csv simply as follow
tweets = list()
for report in reports_filepath:
    with open(report, 'r') as csvfile:
        r = csv.DictReader(csvfile)
        rows = [row for row in r]
        tweets += rows