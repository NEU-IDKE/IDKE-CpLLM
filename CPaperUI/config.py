import argparse

def parsers():
    parser = argparse.ArgumentParser(description='C Paper UI')
    parser.add_argument('--model_path', type=dict, default={
        '基于C语言文本内容': {
            '选择题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '填空题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '算法题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '实际应用题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/'
        },
        '基于已有的题目': {
            '选择题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '填空题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '算法题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/',
            '实际应用题': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/'
        },
        '对话模型': 'https://u252464-bdad-52da5de2.westb.seetacloud.com:8443/'
    }, help='各模型接口地址，最后记得加/')
    parser.add_argument('--system_prompt', type=dict, default={
        '基于C语言文本内容': {
            '选择题': [{"role": "system", "content": "你是一个C语言出题专家,你能够根据文本的内容得到该文本的主要信息进行出题。例如：根据文本内容：“C 语言只提供了下列几种基本数据类型： char 字符型,占用一个字节,可以存放本地字符集中的一个字符 int 整型,通常反映了所用机器中整数的最自然长度 float 单精度浮点型 double 双精度浮点型 此外,还可以在这些基本数据类型的前面加上一些限定符。 short 与 long 两个限定符 用于限定整型： short int sh; long int counter; 在上述这种类型的声明中，关键字 int 可以省略。通常很多人也习惯这么做。”你需要出一个选择题如下：在C语言中，short与long两个限定符通常用于限定下列哪种基本数据类型？ A. char类型 B. int类型 C. float类型 D. double类型"}],
            '填空题': [{"role": "system", "content": "你是一个C语言出题专家"}],
            '算法题': [{"role": "system", "content": "你是一个C语言出题专家，你能够根据文本的内容得到该文本的主要信息进行出题。"}],
            '实际应用题': [{"role": "system", "content": "你是一个C语言出题专家，我将会给你一段文本，你能够根据文本的内容得到该文本的主要信息出一道实际应用题。例如：根据文本内容：“变量和常量是程序处理的两种基本数据对象，声明语句说明变量的名字及类型，也可以指定变量的初值，运算符指定将要进行的操作。表达式则把变量与常量组合起来生成新的值。对象的类型决定该对象可取值的集合以及可以对该对象执行的操作。”你需要出一个实际应用题如下：“\n设计一个C程序，用户输入汽车发动机转速和温度，程序根据以下条件评估：\n\n转速<1000rpm：输出\"发动机运行不稳定，请检查\"；\n转速≥1000rpm，温度<80°C：输出\"发动机运行正常\"；\n转速≥1000rpm，温度≥80°C：输出\"发动机运行正常，注意温度过高\"；\n若输入非法数据，输出\"输入数据不合法，请重新输入\"。”"}]
        },
        '基于已有的题目': {
            '选择题': [{"role": "system", "content": "你是一个C语言出题专家，你需要能够根据原来题目的内容，进行题型的转换，例如：编写程序，计算斐波那契数列1，1，2，3，5，8，13，21，……，的前10项之和。你需要出一个包含正确选项的选择题：斐波那契数列1，1，2，3，5，8，13，21，......，的前10项之和是：()\nA. <54>\nB. <88>\nC. <143>\nD. <145>"}],
            '填空题': [{"role": "system", "content": "你是一个C语言出题专家"}],
            '算法题': [{"role": "system", "content": "你是一个C语言出题专家，你需要根据原来题目的内容，首先抽象出这个题目所侧重考察的C语言知识点，接着你会对这个知识点生成一个标准的C语言算法题。"}],
            '实际应用题': [{"role": "system", "content": "你是一个C语言出题专家，我将会给你一道题目，你需要能够根据原来题目的内容，将该题目的题型转换为实际应用题，例如：“甲、乙、丙三位球迷......试编写C语言程序，求A、B、C、D四队的实际名次。”你需要将文本内的算法与函数定义联系到实际生活中，根据文本内容，出一个由C语言编写的实际应用题，只有问题，不包含答案和选项。"}]
        }
    }, help='各题型System Prompt')
    parser.add_argument('--prefix_prompt', type=dict, default={
        '基于C语言文本内容': {
            '选择题': '请根据以下文本内容进行出题：',
            '填空题': '请根据以下文本内容出一道填空题:\r\n',
            '算法题': '请根据以下文本内容进行出题：',
            '实际应用题': '请根据以下文本内容进行出题：'
        },
        '基于已有的题目': {
            '选择题': '请将该题目转化成选择题：',
            '填空题': '请将下列题目转化为填空题:\r\n',
            '算法题': '请将该题目转化成C语言算法题，所给的题目如下：',
            '实际应用题': '请将该题目转化成实际应用题：'
        }
    }, help='各题型输入prompt前的一些提示语句')
    parser.add_argument('--save_doc_path', type=str, default='CPaperUI/output/C_paper.docx', help='导出的word存储路径')
    parser.add_argument('--save_csv_path', type=str, default='CPaperUI/output/C_paper.csv', help='导出的csv存储路径')
    parser.add_argument('--contents_path', type=str, default='CPaperDB/contents/', help='C语言教材资料路径')
    parser.add_argument('--papers_path', type=str, default='CPaperDB/papers/', help='C语言试卷题目路径')
    args = parser.parse_args()
    return args
