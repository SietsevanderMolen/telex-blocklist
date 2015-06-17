import tgl
from telex.utils.decorators import pm_only, group_only
from telex import plugin
import re


class BlocklistPlugin(plugin.TelexPlugin):
    """
    Blocklist plugin for Telex bot.
    """
    patterns = {
        "^$": "block"
    }

    usage = [
        ":s/pattern/string: substitute pattern for string in the last message"
    ]

    def __init__(self):
        super().__init__()

    def pre_process(self, msg):
        if not hasattr(msg, 'text'):
            return

        if hasattr(msg.src, 'username'):
            username = msg.src.username
        else:
            username = ""

        if msg.src.last_name:
            name = msg.src.first_name + ' ' + msg.src.last_name
        else:
            name = msg.src.first_name

        self.insert(msg_id=msg.id, timestamp=msg.date,
                    uid=msg.src.id, username=username,
                    name=name,
                    chat_id=msg.dest.id, message=msg.text)

    def block(self, msg, matches):
        return ""
