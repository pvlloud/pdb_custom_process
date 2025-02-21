from datetime import datetime

import torch
from transformers import T5EncoderModel, T5Tokenizer


class T5ModelExecutor:
    MODEL_NAME = "Rostlab/prot_t5_xl_uniref50"

    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained(
            self.MODEL_NAME, do_lower_case=False
        )
        self.model = T5EncoderModel.from_pretrained(self.MODEL_NAME)
        self.prediction_time = datetime.now().isoformat()

    def prepare_inputs(self, sequence: str):
        return self.tokenizer(sequence, return_tensors="pt", add_special_tokens=True)

    def process_sequence(self, sequence: str):
        inputs = self.prepare_inputs(sequence)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        with torch.no_grad():
            outputs = self.model(**inputs)

        output_tensor = outputs.last_hidden_state  # (batch_size, seq_len, hidden_size)
        sequence_embedding = output_tensor.mean(dim=1).squeeze().numpy()

        return {
            "prediction_time": self.prediction_time,
            "original_sequence": sequence,
            "tokens": tokens,
            "output_tensor_shape": list(output_tensor.shape),
            "sequence_embedding": sequence_embedding.tolist(),
            "raw_sequence_embedding": sequence_embedding,
        }
