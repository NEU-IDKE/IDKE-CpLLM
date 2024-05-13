# IDKE-CpLLM
用于生成C语言试卷的大语言模型

# CPaper

首先进入`CPaperAPI`文件夹，运行各个模型接口后，进入`CPaperUI`运行前端界面


# 0508 更新

* 新增文件夹 `database` 里面包括：

  > 为了和你的文件夹格式命名统一，可以把这个文件夹改名为 `CPaperDB`

  * `contents` 底下是整理的所有的C语言教材资料：

    * `chapterA-B.xlsx` 表示第A章到第B章的文本内容
    * 每个 `chapterA-B.xlsx`  由两个 sheet 组成

  * `papers` 底下是整理的所有试卷题目：

    * `papers-partX.xlsx` 表示一次整理的 20 张试卷
    * 每个 `chapterA-B.xlsx`  由 20 个 sheet 组成

  * `origin_data` 底下是ChatGLM微调用的prompt形式：

    * `训练后的数据.ipynb` 简单看一下每组数据的情况

    * `algorithm` 训练 文本/题目转化成算法题，同理，`choice、completion、implement` 分别表示：训练文本/题目转化成选择题、填空题、应用题

    * 每个文件夹下：

      * `test_lora.csv` 或者 `test_ptuning.csv` 表示通过 lora、ptuing 进行微调

      * 部分文件下有 `test_content.csv` 和 `test_question.csv`，这是未合并前的基于内容转化和基于题型转换的 csv 文件

        > `test_lora.csv` 或者 `test_ptuning.csv` 是通过合并上述两个 csv 得到( 因此，如果使用 `test_lora.csv` 或者 `test_ptuning.csv` 就不需要再使用 `test_content.csv` 和 `test_question.csv` 文件了)

* 更改 `CpaperUI -> cpaper.py` 文件的代码：

  * `paper_gen_page()` 函数：
    * 更新 knowledge_point、uploaded_file参数的设置
    * 更新 content 的读取形式，根据知识点筛选
    * 更新 `gen_question()`的传参形式和参数量的定义
  * `question_gen_page()` 函数：
    * 也需要更新 `gen_question()`的传参形式和参数量的定义

* [可选] 性能优化 `CpaperUI -> util.py -> get_response()`

  * `requests.post(url + 'get_response', data=json.dumps(data))`

    * 将 一次性传回 结果改为通过 文本流的形式传回 (即那边每生成一个字符，这边就获取一个字符)

----

`CPaperAPI`更新了依赖项`sse-starlette`，用于流传输

* 新增协作者
