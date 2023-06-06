import numpy as np
import pandas as pd
from scipy import stats


class TimeSeriesFeatureEngineering:
    """
        A class that extracts features from time series using plugins.
    """
    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def process(self, dataframe):
        """
            Extracts features from a time series using the plugins that have been added.
            Args:
                dataframe: A pandas dataframe time series data.
            Returns:
                A dataframe of features extracted from the time series.
        """

        plugin_features = []
        for plugin in self.plugins:
            plugin_features.append(plugin.process(dataframe))

        if len(plugin_features) > 0:
            return pd.concat(plugin_features)
        else:
            return pd.DataFrame()


# ----- PLUGINS ------
# 1.Date Time Feature
# 2.Lag Features
# 3.Rolling Windows Statistics
# 4.Expanding Windows Statistics
# 5. Square Root Transform
# 6. Log Transform
# 7. Box-Cox Transform
# 8. Moving Average

class DateTimeFeaturesPlugin:
    def process(self, df):
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['hour'] = df['date'].dt.hour
        return df


class LagFeaturesPlugin:
    def __init__(self, lag):
        self.lag = lag

    def process(self, df):
        for i in range(1, self.lag + 1):
            df[f'lag_{i}'] = df['target'].shift(i)
        return df


class RollingWindowStats:
    def __init__(self, window):
        self.window = window

    def process(self, df):
        df['rolling_mean'] = df['target'].rolling(window=self.window).mean()
        df['rolling_std'] = df['target'].rolling(window=self.window).std()
        return df


class ExpandingWindowStats:

    def process(self, df):
        df['expanding_mean'] = df['target'].expanding().mean()
        df['expanding_std'] = df['target'].expanding().std()
        return df


class SqrtTransform:
    def process(self, df):
        df['sqrt_transform'] = np.sqrt(df['target'])
        return df


class LogTransform:
    def process(self, df):
        df['log_transform'] = np.log(df['target'])
        return df


class BoxCoxTransform:
    def process(self, df):
        df['boxcox_transform'], _ = stats.boxcox(df['target'])
        return df


class MovingAverage:
    def __init__(self, window):
        self.window = window

    def process(self, df):
        df['moving_average'] = df['target'].rolling(window=self.window).mean().shift(1)
        return df


extractor = TimeSeriesFeatureEngineering()

# # Add plugins to the extractor
extractor.add_plugin(DateTimeFeaturesPlugin())
extractor.add_plugin(LagFeaturesPlugin(lag=2))
# extractor.add_plugin(RollingWindowStats(window=7))
# extractor.add_plugin(ExpandingWindowStats())
# extractor.add_plugin(SqrtTransform())
# extractor.add_plugin(LogTransform())
# extractor.add_plugin(BoxCoxTransform())
# extractor.add_plugin(MovingAverage(window=7))

# load time series data
df = pd.read_csv('time_series_data.csv', parse_dates=['date'])
features = extractor.process(df)
features.to_csv('time_series_features.csv', index=False)

