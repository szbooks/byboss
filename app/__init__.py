import os
from datetime import timedelta

from flask import Flask

from app.scheduler import init_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

    from .routes import main
    app.register_blueprint(main)

    @app.template_filter('format_number')
    def format_number_filter(value):
        """使用Python的内置功能（如locale模块）或简单的字符串操作来格式化数字（仅千位分隔符）"""
        if value is None or not isinstance(value, (int, float)):
            return ''
        # 注意：这个方法不会根据地区设置来处理千位分隔符，它只是一个简单的示例
        # 在实际应用中，你可能需要使用locale模块或其他库来正确处理不同地区的千位分隔符
        # 这里我们仅使用逗号作为分隔符
        if isinstance(value, int):
            return f"{value:,}"
        else:
            return f"{value:,.2f}"

    return app



