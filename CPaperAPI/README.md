# CPaperAPI

输入以下命令安装git LFS (Ubuntu)

```
sudo apt-get update
sudo apt-get install git-lfs
```

安装依赖

```
pip install -r requirements.txt
```

进入`model`文件夹输入以下命令下载基础模型

```
git clone https://www.modelscope.cn/ZhipuAI/chatglm3-6b.git
```

将模型微调后的权重文件（以下文件）放到`tuning`文件夹下

`adapter_config.json`、`adapter_model.safetensors`、`tokenizer_config.json`、`tokenizer.model`

或

`config.json`、`pytorch_model.bin`、`tokenizer_config.json`、`tokenizer.model`

返回至`CPaperAPI`文件夹下，修改`api.py`中`host`后，输入以下命令运行`api.py`以接口调用模型

```
python api.py
```

每个模型重复上述操作即可
