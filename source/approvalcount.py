import time
import os
import json

import euphoria as eu
from euphutils import EuphUtils

class ApprovalCount(eu.ping_room.PingRoom, eu.chat_room.ChatRoom, eu.nick_room.NickRoom):
    def __init__(self, room, password=None, nickname='ApprovalCount', help_text='', short_help_text='', ping_text='Pong!', save_file='save.json'):
        super().__init__(room, password)
        self.default_nickname = nickname
        self.nickname = self.default_nickname

        self.start_time = time.time()

        self.help_text = help_text
        self.short_help_text = short_help_text
        self.ping_text = ping_text

        self.count = 0
        self.save_file = save_file
        self.load_save_file()

    def ready(self):
        super().ready()
        self.send_chat('/me Hello, world!')
        self.update_nick()

    def update_nick(self):
        self.change_nick(str(self.count) + ' :bronze:')
        self.update_save_file()

    def update_save_file(self):
        try:
            with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', self.save_file), 'w') as file:
                json.dump({'count': self.count}, file)
        except (OSError, IOError):
            pass

    def load_save_file(self):
        try:
            with open(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', self.save_file)) as file:
                self.count = json.load(file).get('count', 0)
        except (ValueError, OSError, IOError):
            pass

    def handle_chat(self, message):
        content = message['content']
        new_count = self.count + content.count(':bronze:') + content.count(':bronze?!:') + content.count(':bronze!?:') + content.count(':+1:')
        if content.startswith('!'):
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
            # !reset @ApprovalCount
            match = EuphUtils.command('!reset', self.nickname).match(content) or EuphUtils.command('!reset', self.default_nickname).match(content)
            if match:
                self.count = 0
                new_count = 0
                self.change_nick(self.default_nickname)
                self.send_chat(':bronze: count reset to 0.', message_id)
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
        if self.count != new_count:
            self.count = new_count
            self.update_nick()
