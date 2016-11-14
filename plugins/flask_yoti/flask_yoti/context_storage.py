from time import time


class ActivityDetailsStorage(object):

    def __init__(self):
        self.storage = {}
        self._timestamps = {}
        self._timeout_sec = 15

    def save(self, activity_details):
        user_id = activity_details.user_id
        self.storage[user_id] = activity_details
        self._timestamps[user_id] = time() + self._timeout_sec

    def get(self, user_id):
        self._clear_outdated()
        return self.storage.pop(user_id, None)

    def _clear_outdated(self):
        current_time = time()
        to_remove = []
        for user_id, timestamp in self._timestamps.items():
            if timestamp <= current_time:
                to_remove.append(user_id)

        for user_id in to_remove:
            del self.storage[user_id]
            del self._timestamps[user_id]


activity_details_storage = ActivityDetailsStorage()
