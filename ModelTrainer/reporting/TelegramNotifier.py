import traceback

import telegram_send


def send_message_via_telegram(message: str, image_path: str = None) -> None:
    """
    Sends a message as TrainingFather.

    Example usage:
        - send_message_via_telegram("Training father is speaking to you!")
        - send_message_via_telegram("Only the *bold* use _italics_")

    Each machine that needs to send a message, should run the following (from command-line):
        telegram-send --configure
        # Connect to the bot, e.g. Alex12345Bot, by adding its Access Token
        # Connect your user-account to the bot and enter the password
    :param image_path: A path to a file on the disk that should optionally be sent along with the message
    :param message: The message to be sent in markdown formatting
    """
    try:
        if image_path is not None:
            with open(image_path, "rb") as f:
                telegram_send.send([message], parse_mode="text", images=[f])
        else:
            telegram_send.send([message], parse_mode="text")
    except Exception as exception:
        print("Error while sending notification via telegram: {0}".format(str(exception)))
        traceback.print_exc()


if __name__ == '__main__':
    send_message_via_telegram("I'm sending you a message with an image attached", "2017-07-10_res_net_3_small_96.7p.png")
