from config import parsers
import os
import json
import torch
from transformers import AutoModel, AutoTokenizer, AutoConfig
from peft import PeftModel
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from sse_starlette.sse import ServerSentEvent, EventSourceResponse

def load_model_and_tokenizer(base_model_path, tuning_model_path):
    if os.path.exists(tuning_model_path + '/adapter_config.json'):
        tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
        model = AutoModel.from_pretrained(base_model_path, trust_remote_code=True).cuda()
        model = PeftModel.from_pretrained(model, model_id=tuning_model_path)
        model = model.eval()
    else:
        tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
        config = AutoConfig.from_pretrained(base_model_path, trust_remote_code=True, pre_seq_len=128)
        model = AutoModel.from_pretrained(base_model_path, config=config, trust_remote_code=True).cuda()
        prefix_state_dict = torch.load(os.path.join(tuning_model_path, "pytorch_model.bin"))
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
    return model, tokenizer

args = parsers()
model, tokenizer = load_model_and_tokenizer(args.base_model_path, args.tuning_model_path)

app = FastAPI()
class Chat_Data(BaseModel):
    content: str
    history: list
    temperature: float
    top_k: int
    top_p: float

@app.post('/get_response')
def get_response(data: Chat_Data):
    response, _ = model.chat(tokenizer, data.content, history=data.history, temperature=data.temperature, top_k=data.top_k, top_p=data.top_p)
    return response

@app.post('/get_stream_response')
def get_stream_response(data: Chat_Data):
    def decorate(generator):
        for res, his in generator:
            yield ServerSentEvent(json.dumps(res, ensure_ascii=False), event='stream_chat')
    return EventSourceResponse(decorate(model.stream_chat(tokenizer, data.content, history=data.history, temperature=data.temperature, top_k=data.top_k, top_p=data.top_p)))

if __name__ == '__main__':
    uvicorn.run(app, host='')