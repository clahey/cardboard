import os
import slack

class SlackClient:
    '''
    This is a wrapper class around the existing slack web client that allows for
    sending messages, creating channels, and joining channels.
    '''
    def __init__(self, token=os.environ.get("SLACK_API_TOKEN", None),
                 root_channel_name="small-board"):
        self._slack_token = token
        self._web_client = slack.WebClient(token=self._slack_token)
        self.root_channel_name = root_channel_name


    def send_message(self, channel_name, message):
        '''
        Sends message to channel_name.
        '''
        self._web_client.chat_postMessage(channel=channel_name, text=message)


    def create_channel(self, puzzle_name):
        '''
        Returns the assigned channel id if able to create a channel.
        Otherwise, raises an exception.
        '''
        try:
            # By setting validate=False, the client will automatically clean up
            # special characters and make it fit under 80 characters.
            response = self._web_client.channels_create(name=puzzle_name,
                                                   validate=False)
            if response["ok"]:
                assigned_channel_name = response["channel"]["name"]
                channel_id = response["channel"]["id"]
                print(response)
                self.send_message(self.root_channel_name, "Channel " +
                                  assigned_channel_name +
                                  " created for puzzle titled " + puzzle_name
                                  + "!")
                return channel_id
        except SlackApiError as e:
            if (e.response['error'] == 'name_taken'):
                raise NameError('Slack channel name already exists.')
            raise e


    def join_channel(self, channel_name):
        '''
        Joins channel with given name. Assumes channel_name is valid and
        exists.
        '''
        self._web_client.channels_join(channel=channel_name)


    @staticmethod
    def create_join_link(channel_id):
        '''
        Given channel_id, create channel join link.
        '''
        return "https://slack.com/app_redirect?channel=" + channel_id