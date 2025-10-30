from flask import current_app
from datetime import datetime
from functools import partial


from .analysis_service import AnalysisService
from .model_presales_progress import update_stat_presales
from .utils import updata_operating_sub

def task_one(app):
    with app.app_context():  # 使用传入的应用实例来推送应用上下文
        print(f"更新客户运营人员数据开始执行: {datetime.now()}")
        updata_operating_sub()
        print(f"更新客户运营人员数据执行完成: {datetime.now()}")


def task_two(app):
    with app.app_context():  # 使用传入的应用实例来推送应用上下文
        print(f"更新售前星级开始执行: {datetime.now()}")
        AnalysisService.perform_analysis()
        print(f"更新售前星级执行完成: {datetime.now()}")

def task_three(app):
    with app.app_context():  # 使用传入的应用实例来推送应用上下文
        print(f"更新售前认领统计表开始执行: {datetime.now()}")
        update_stat_presales()
        print(f"更新售前认领统计表执行完成: {datetime.now()}")

