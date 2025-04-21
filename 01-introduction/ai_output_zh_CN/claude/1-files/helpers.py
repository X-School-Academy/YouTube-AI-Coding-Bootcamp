import os

def ensure_directories_exist(directories):
    """
    如果目录不存在，则创建目录。
    
    参数:
        directories (list): 要创建的目录路径列表
    """
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
