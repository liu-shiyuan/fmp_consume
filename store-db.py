from adsapi import DailyReport


class PersistentDailyReport:
    def __init__(self, access_token=None):
        if access_token is None:
            raise Exception("Parameter 'access_token' is required.")
        self.access_token = access_token