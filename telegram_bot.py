import os
from ptbot import Bot
from dotenv import load_dotenv
from pytimeparse import parse


def wait(bot, chat_id, question):
    timer = parse(question)
    first_answer = 'Таймер запущен...'
    message_id = bot.send_message(chat_id, first_answer)
    bot.create_countdown(timer, notify_progress, chat_id=chat_id,
                         message_id=message_id, total_time=timer)
    bot.create_timer(timer, timer_finished, chat_id=chat_id,
                     question=question)


def render_progressbar(total, iteration, prefix='', suffix='',
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(bot, secs_left, chat_id, message_id, total_time):
    elapsed_time = total_time - secs_left
    progress_bar = render_progressbar(total=total_time,
                                      iteration=elapsed_time)
    updated_message = 'Осталось: {0} секунд\n{1}'.format(secs_left,
                                                         progress_bar)
    bot.update_message(chat_id, message_id, updated_message)


def timer_finished(bot, chat_id, question):
    answer = 'Время вышло'
    bot.send_message(chat_id, answer)


def main():
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    bot = Bot(token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
