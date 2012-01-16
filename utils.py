import os
import jinja2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

loader = jinja2.FileSystemLoader(TEMPLATE_DIR)
env = jinja2.Environment(loader=loader)


def render(template, context):
    return env.get_template(template).render(context)


def format_size(size):
    cur_size = size

    gigabytes = cur_size / (1024 ** 3)
    cur_size -= (1024 ** 3) * gigabytes

    megabytes = cur_size / (1024 ** 2)
    cur_size -= (1024 ** 2) * megabytes

    kilobytes = cur_size / 1024
    cur_size -= 1024 * kilobytes

    if gigabytes:
        return "%d.%d GB" % (gigabytes, megabytes)

    if megabytes:
        return "%d.%d MB" % (megabytes, kilobytes)

    if kilobytes:
        return "%d.%d kB" % (kilobytes, cur_size)

    return cur_size


def format_speed(speed):
    cur_speed = speed

    megabytes = cur_speed / (1024 ** 2)
    cur_speed = cur_speed % (1024 ** 2)

    kilobytes = cur_speed / 1024
    cur_speed = cur_speed % 1024

    if megabytes:
        return "%d.%d MB/s" % (megabytes, kilobytes)
    if kilobytes:
        return "%d.%d kB/s" % (kilobytes, cur_speed)
    return "%d B/s" % (cur_speed)


def time_remaining(speed, bytes_left):
    if speed == 0:
        return None

    if bytes_left == 0:
        return 0

    seconds = bytes_left / speed

    hours = seconds / (60 * 60)
    seconds = seconds % (60 * 60)

    minutes = seconds / 60
    seconds = seconds % 60

    if hours:
        return "%d hours, %d minutes" % (hours, minutes)
    if minutes:
        return "%d minutes, %d seconds " % (minutes, seconds)
    return "%d seconds " % seconds
