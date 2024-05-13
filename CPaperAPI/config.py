import argparse

def parsers():
    parser = argparse.ArgumentParser(description='C Paper API')
    parser.add_argument('--base_model_path', type=str, default='./model/chatglm3-6b', help='基础模型目录')
    parser.add_argument('--tuning_model_path', type=str, default='./model/tuning', help='微调模型目录')
    args = parser.parse_args()
    return args
