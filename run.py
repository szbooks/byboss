from app import create_app
from app.scheduler import init_scheduler

app = create_app()
init_scheduler(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)



        #app.run(debug=True)  # 设置 debug=True 便于调试
