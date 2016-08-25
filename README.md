# 云数鹰眼车险反欺诈系统

## 1 软件要求

*	Linux 系统： Contos 7  *	Linux 系统 rpm包：sqlite, sqlite-devel   *	Linux 系统软件： Python 3.5。要求在 bash 命令行下执行 python 指令会运行 python3。  *	Python 3 包：pip, setuptools, Django-1.9.5 或以上, djangorestframework-3.2.5 或以上  *	在以下文档中，用 $PROJECT_DIR 指代本项目源代码文件根目录


## 2 安装 django-msa

    $ cd $PROJECT_DIR/django-msa/modules/msa/    $ make install
    
## 3 数据预处理
    $ cd $PROJECT_DIR/data-processing    $ make
    
## 4 安装反欺诈核心模块
    $ cd $PROJECT_DIR/hawk-rest-api    $ make
    
## 5 启动 django 服务
    $ cd $PROJECT_DIR/hawk-rest-api/hawk_rest_api    $ python3 manage.py runserver 0.0.0.0:8000
