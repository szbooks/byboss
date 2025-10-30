from fabric import Connection


def deploy():
    # 远程服务器的 IP 地址、用户名和密码
    host = '47.98.255.48'
    user = 'root'
    password = 'todgo123KUANG'

    # 连接到远程服务器
    conn = Connection(host=host, user=user, connect_kwargs={"password": password})

    # 上传文件
    conn.put('requirements.txt', '/usr/local/myproject/bak/byboss/requirements.txt')

    # 执行命令并捕获输出
    result = conn.run('ps aux | grep python | grep run.py', hide=True)

    # 解析输出，提取进程编号
    process_ids = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) > 1:
            temp_process_id = parts[1]
            process_ids.append(temp_process_id)
    process_id=process_ids[1]
    print(process_id)
    #
    # command = f"kill -9 {process_id}"
    # killresult = conn.run(command, hide=True)
    # print(killresult)








    # # 导航到项目目录
    # with conn.cd('/path/to/project'):
    #     # 激活虚拟环境
    #     conn.run('source venv/bin/activate')
    #
    #     # 安装或更新依赖项
    #     conn.run('pip install -r requirements.txt')
    #
    #     # 重启服务（假设使用 systemd）
    #     conn.sudo('systemctl restart your_service', password=password)