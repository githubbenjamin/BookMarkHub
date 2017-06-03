# 准备
通过pipenv来管理所需模块, 首先通过pip安装pipenv.
```bash
sudo pip install pipenv
```
安装完以后通过pipenv来构建项目环境, 如果初次使用首先得初始化.
```bash
# 创建python3的环境(本项目使用)
pipenv --three

# 创建python2的环境
pipenv --two
```
构建的项目环境会下载相应版本的python库. 例如下面的命令会下载python3的flask框架

```bash
pipenv install flask
```
pipenv安装python库时会生成相应的pipfile, 我们通过pipfile就可以下载我们需要的库(类似于virtualenv中的requirements.txt)

```bash
pipenv install
```

使用pipenv使用虚拟环境很简单, `shell`命令来启动
```bash
pipenv shell
# 如果有兼容行问题可使用
pipenv shell -c
```

# 项目运行

当所有的虚拟环境和库都准备完成后, 执行以下命令启动应用
```bash
python manage.py runserver
```
