from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from .tasks import task_one, task_two, task_three

scheduler = None  # 定义全局调度器变量


def init_scheduler(app):
    global scheduler
    scheduler = BackgroundScheduler(timezone=timezone('Asia/Shanghai'))  # 设置时区

    # hour = '*'：每小时执行一次。
    # day = '*'：每天执行一次。
    # week = '*'：每周执
    # month = '*'：每月执行一次。
    # minute='*' 每分钟


    # trigger = CronTrigger(minute='*')  # 每分钟执行一次
    # trigger = CronTrigger(hour='*')  # 每小时执行一次
    # trigger_one = CronTrigger(month='*')  # 每月执行一次
    # trigger_two = CronTrigger(minute='*/5')
    # trigger_two = CronTrigger(hour=2, minute=0)  # 每天凌晨2点



    trigger_one = CronTrigger(month='*')  # 每月执行一次
    # trigger_two = CronTrigger(month='*')  # 每月执行一次
    trigger_three = CronTrigger(month='*')  # 每月执行一次
    trigger_two = CronTrigger(hour=6, minute=0)  # 每天凌晨2点
    # trigger_two = CronTrigger(minute='*/2')

    # #现网配置
    # trigger_one = CronTrigger(hour='*')  # 每小时执行一次
    # trigger_two = CronTrigger(hour=5, minute=0)  # 每天凌晨2点
    # trigger_three = CronTrigger(hour=3, minute=0)  # 每天凌晨3点

    # 添加多个任务，使用相同的触发器，并传递应用实例
    scheduler.add_job(partial(task_one, app), trigger=trigger_one, id='task_one')
    scheduler.add_job(partial(task_two, app), trigger=trigger_two, id='task_two')
    scheduler.add_job(partial(task_three, app), trigger=trigger_three, id='task_three')

    # 启动调度器
    scheduler.start()