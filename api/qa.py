
from transformers import pipeline
model_name = 'deepset/roberta-base-squad2'

def qa_func(question,context):
    qa = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input2 = [{'question':question,
            'context':context,
            }]
    output_0 = qa(QA_input2[0]['question'], QA_input2[0]['context'])
    return output_0['answer']