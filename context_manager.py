# context_manager.py
class ConversationContext:
    def __init__(self, window_size=5):
        self.buffer = []
        self.window_size = window_size

    def update(self, user_msg, assistant_msg):
        self.buffer.append(f"You: {user_msg}\nJarvis: {assistant_msg}")
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)

    def get_context(self):
        return "\n".join(self.buffer)
