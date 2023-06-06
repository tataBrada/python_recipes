class TimeSeriesFeatureExtractor:
    """
        A class that extracts features from time series using plugins.
    """

    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def process(self, ts):
        """
            Extracts features from a time series using the plugins that have been added.
            Args:
                ts: A list of numeric values representing a time series.
            Returns:
                A dictionary of features extracted from the time series.
        """
        results = {}
        for plugin in self.plugins:
            plugin_features = plugin.process(ts)
            results.update(plugin_features)
        return results


# ----- PLUGINS ------
# 1.Trend
# 2.Moving Average
# 3.Seasonality

class TrendPlugin:
    def process(self, ts):
        trend = ts[-1] - ts[0]
        return {'trend': trend}


class MovingAveragePlugin:
    def __init__(self, window_size):
        self.window_size = window_size

    def process(self, ts):
        moving_average = sum(ts[-self.window_size:]) / self.window_size
        return {'moving_average': moving_average}


class SeasonalityPlugin:
    def process(self, ts):
        max_value = max(time_series)
        min_value = min(time_series)
        seasonality = max_value - min_value
        return {'seasonality': seasonality}


extractor = TimeSeriesFeatureExtractor()

# Add plugins to the extractor
extractor.add_plugin(TrendPlugin())
extractor.add_plugin(MovingAveragePlugin(window_size=5))
extractor.add_plugin(SeasonalityPlugin())

# sample data
time_series = [1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 0, 0, 3, 6, 6, 9]
features = extractor.process(time_series)
print(features)
# {'trend': 8, 'moving_average': 4.8, 'seasonality': 9}
