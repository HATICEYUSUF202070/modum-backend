class UserChannelRegistry:
    def __init__(self):
        self._user_channel_mapping = {}

    def add_channel_for_user(self, user_id, channel_name):
        self._user_channel_mapping[user_id] = channel_name

    def get_channel_for_user(self, user_id):
        return self._user_channel_mapping.get(user_id)

    def remove_channel_for_user(self, user_id):
        self._user_channel_mapping.pop(user_id)


registry = UserChannelRegistry()
