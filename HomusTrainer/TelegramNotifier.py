import telegram_send


def send_message_via_telegram(message: str) -> None:
    """
    Sends a message as TrainingFather.

    Example usage:
        - send_message_via_telegram("Training father is speaking to you!")
        - send_message_via_telegram("Only the *bold* use _italics_")

    Each machine that needs to send a message, should run the following (from command-line):
        telegram-send --configure
        # Connect to the bot, e.g. Alex12345Bot, by adding its Access Token
        # Connect your user-account to the bot and enter the password
    :param message: The message to be sent in markdown formatting
    """
    telegram_send.send([message], parse_mode="Markdown")
