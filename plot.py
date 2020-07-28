import argparse
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

parser = argparse.ArgumentParser()

parser.add_argument(
    '-i', '--input',
    type=str,
    required=True,
    help='input CSV file'
)
parser.add_argument(
    '-w', '--window',
    type=int,
    default=30,
    help='moving average window (default: 30)'
)
parser.add_argument(
    '-n', '--name',
    type=str,
    default='Plant',
    help='specific plant type name (default: Plant)'
)

args = parser.parse_args()

df = pd.read_csv(args.input)

states = df.drop_duplicates(['state'])['state']

final = pd.DataFrame()

for state in states:
    aggregate = df[df['state'] == state].groupby(['date']).sum()
    aggregate = aggregate.rename(columns={
        'weight': state
    })
    final = pd.concat([final, aggregate], axis=1, sort=True)

# Fill missing data points

final = final.interpolate(limit_direction='both')

final = final.rolling(args.window).mean()

# Convert index to date

final.index = pd.to_datetime(final.index)

ax = final.plot()

ax.autoscale(tight=False)
ax.set_title(args.name)
ax.set_ylabel('Phase cumulative weight')

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

ax.set_xlim([datetime.date(2019, 1, 1), datetime.date(2020, 7, 15)])

plt.margins(0)
plt.legend(loc='upper left')
plt.tight_layout()
# plt.gca().get_legend().remove()
plt.show()
