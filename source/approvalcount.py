import time

import euphoria as eu
from euphutils import EuphUtils

class ApprovalCount(eu.ping_room.PingRoom, eu.chat_room.ChatRoom, eu.nick_room.NickRoom):
    def __init__(self, room, password=None, nickname='ApprovalCount', help_text='', short_help_text='', ping_text='Pong!'):
        super().__init__(room, password)
        self.default_nickname = nickname
        self.nickname = self.default_nickname

        self.start_time = time.time()

        self.help_text = help_text
        self.short_help_text = short_help_text
        self.ping_text = ping_text

        self.count = 0
        self.update_nick()

    def ready(self):
        super().ready()
        self.send_chat('/me Hello, world!')

    def update_nick():
        self.change_nick(str(self.count) + ' :bronze:')

    def handle_chat(self, message):
        content = message['content']
        new_count = self.count + content.count(':bronze:') + content.count(':bronze?!:') + content.count(':+1:')
        if self.count != new_count:
            self.count = new_count
            self.update_nick()
        if not content.startswith('!'):
            return
        message_id = message['id']
        # !ping
        match = EuphUtils.command('!ping', '').match(content) or EuphUtils.command('!ping', self.nickname).match(content) or EuphUtils.command('!ping', self.default_nickname).match(content)
        if match:
            self.change_nick(self.default_nickname)
            self.send_chat(self.ping_text, message_id)
            self.update_nick()
            return
        # !uptime @ApprovalCount
        match = EuphUtils.command('!uptime', self.nickname).match(content) or EuphUtils.command('!uptime', self.default_nickname).match(content)
        if match:
            self.change_nick(self.default_nickname)
            self.send_chat(EuphUtils.uptime_str(self.start_time), message_id)
            self.update_nick()
            return
        # !help
        match = EuphUtils.command('!help', '').match(content)
        if match:
            self.change_nick(self.default_nickname)
            self.send_chat(self.short_help_text, message_id)
            self.update_nick()
            return
        # !help @ApprovalCount
        match = EuphUtils.command('!help', self.nickname).match(content) or EuphUtils.command('!help', self.default_nickname).match(content)
        if match:
            self.change_nick(self.default_nickname)
            self.send_chat(self.help_text, message_id)
            self.update_nick()
            return
        # !restart @ApprovalCount
        match = EuphUtils.command('!restart', self.nickname).match(content) or EuphUtils.command('!restart', self.default_nickname).match(content)
        if match:
            self.change_nick(self.default_nickname)
            self.send_chat('/me is restarting...', message_id)
            self.update_nick()
            self.quit()
            return
