import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from transformers import FSMTForConditionalGeneration, FSMTTokenizer



def ru2eng(input_text: str, device: str) -> str:
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")

    model.to(device)

    input_ids=torch.tensor([tokenizer.encode(input_text)]).to(device)
    outputs=model.generate(input_ids,eos_token_id=tokenizer.eos_token_id,
                        num_beams=5,
                        min_new_tokens=17,
                        max_new_tokens=200,
                        do_sample=True,
                        no_repeat_ngram_size=4,
                        top_p=0.9)
    for out in outputs:
        print(tokenizer.decode(out))
    return tokenizer.decode(outputs[0])





