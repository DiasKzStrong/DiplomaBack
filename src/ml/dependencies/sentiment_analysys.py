from datasets import Dataset
import torch
import torch.nn as nn
import transformers

from ..conf import ml_config

import pandas as pd
from sklearn.model_selection import train_test_split

from src.ml.services.sentiment_analysys import SentimentAnalysysService


class Transformer(nn.Module):
    def __init__(self, transformer, output_dim, freeze):
        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.config.hidden_size
        self.fc = nn.Linear(hidden_dim, output_dim)
        if freeze:
            for param in self.transformer.parameters():
                param.requires_grad = False

    def forward(self, ids):
        # ids = [batch size, seq len]
        output = self.transformer(ids, output_attentions=True)
        hidden = output.last_hidden_state
        # hidden = [batch size, seq len, hidden dim]
        attention = output.attentions[-1]
        # attention = [batch size, n heads, seq len, seq len]
        cls_hidden = hidden[:, 0, :]
        prediction = self.fc(torch.tanh(cls_hidden))
        # prediction = [batch size, output dim]
        return prediction


def get_data():
    bad_file_path = "ml/datasets/train_data_bad.txt"
    good_file_path = "ml/datasets/train_data_good.txt"

    # Define the function to read sentences from the dataset
    def read_sentences(file_path, label):
        with open(file_path, "r", encoding="utf-8") as file:
            sentences = file.readlines()
        sentences = [sentence.strip() for sentence in sentences]
        return [(sentence, label) for sentence in sentences]

    # Update these paths if your files are located elsewhere

    # Read the sentences and label them
    good_sentences = read_sentences(good_file_path, 1)
    bad_sentences = read_sentences(bad_file_path, 0)

    # Combine the good and bad sentences
    all_sentences = good_sentences + bad_sentences

    # Create a DataFrame
    df = pd.DataFrame(all_sentences, columns=["text", "label"])

    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)

    return df


def get_train_data():
    def tokenize_and_numericalize_example(example, tokenizer):
        ids = tokenizer(example["text"], truncation=True)["input_ids"]
        return {"ids": ids}

    df = get_data()

    # Split the dataset into training+validation and test sets
    train_val_df, test_df = train_test_split(df, test_size=0.2)

    # Split the training+validation set into training and validation sets
    train_df, val_df = train_test_split(
        train_val_df, test_size=0.25
    )  # Adjust the test_size as per your requirement

    # Convert DataFrames to datasets.Dataset
    train_data = Dataset.from_pandas(train_df)

    tokenizer = get_tokenizer()

    # Apply the tokenization function to datasets
    train_data = train_data.map(
        tokenize_and_numericalize_example, fn_kwargs={"tokenizer": tokenizer}
    )

    # Set the format for PyTorch
    train_data = train_data.with_format(type="torch", columns=["ids", "label"])

    return train_data


def get_tokenizer():
    tokenizer = transformers.AutoTokenizer.from_pretrained(ml_config.transformer_name)
    return tokenizer


def get_device():
    device = torch.device("cpu")
    return device


def get_sentiment_analysis_model():
    transformer = transformers.AutoModel.from_pretrained(ml_config.transformer_name)

    train_data = get_train_data()

    output_dim = len(train_data["label"].unique())
    freeze = False

    model = Transformer(transformer, output_dim, freeze)

    device = get_device()

    model = model.to(device)

    model.load_state_dict(
        torch.load("ml/ml_model/transformer.pt", map_location=torch.device("cpu"))
    )

    return model


def get_sentiment_analysis_service():
    model = get_sentiment_analysis_model()
    device = get_device()
    tokenizer = get_tokenizer()

    return SentimentAnalysysService(model, tokenizer, device)
