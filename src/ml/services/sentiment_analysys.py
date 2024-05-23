import torch


class SentimentAnalysysService:
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def predict_sentiment(self, text):
        ids = self.tokenizer(text)["input_ids"]
        tensor = torch.LongTensor(ids).unsqueeze(dim=0).to(self.device)
        prediction = self.model(tensor).squeeze(dim=0)
        probability = torch.softmax(prediction, dim=-1)
        predicted_class = prediction.argmax(dim=-1).item()
        predicted_probability = probability[predicted_class].item()
        return predicted_class, predicted_probability
