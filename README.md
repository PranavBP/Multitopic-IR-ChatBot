# Multitopic-IR-ChatBot
End-to-End Functional IR chatbot for multi-topic conversations

**Dataset** <br />
Data was scraped from Reddit using pushshift API supported by Python. About 200k submissions and comments from following subreddits were scraped - <br />

1. ExplainLikeImFive <br />
2. FoodForThought <br />
3. ChangeMyView <br />
4. TodayILearned <br />
5. Politics <br />
6. Healthcare <br />
7. Education <br />
8. Environment <br />
9. Technology <br />
 
The dataset was indexed using Apache SOLR and hosted on GCP <br />

**Pre-processing** <br />

Following preprocessing steps were applied - <br />
* NaN values from the indexed data were removed
* Redundant submissions were removed
* Submissions with [removed] or [deleted] subtext were eliminated,
* Comments with [removed] or [deleted] body were eliminated.  
* Submissions/comments with empty strings were removed

**Classification between general conversation and faceted search**

The above dataset was combined with chitchat dataset - https://github.com/BYU-PCCL/chitchat-dataset for generic conversations.
A pre-trained BERT model was further trained on the combined dataset to classify the user query into chitchat data (0) vs reddit data (1).

The Neural Network has a layer that uses the BERTpreprocessor for English vocabulary from the tensorflow_hub library. After preprocessing, this data is further passed to the encoder layer that encodes the data using preprocessed embeddings. This adds a semantic meaning to the data and then we get the embeddings for our data according to the pretrained model. These embeddings are then passed through a dense layer and a sigmoid activation function is used to get final output prediction for the class. If the predicted value is about 0.4 then the data is classified as reddit data else it is chitchat data.

The model was able to get an accuracy of 98% for classifying the training data and a precision of 97%. The loss went from 0.7 to 0.0660 after 10 epochs.

For the test data the model was able to get an accuracy of 97% and precision of 97%.

**Fetching documents**

According to the predicted class from the classifier, we hit the corresponding Solr index and get the top 20 ranked documents from Solr. This list of 20 documents is passed to a re-ranker.

**Reranking**

We used the sentence_transformer library which is a pre-trained library for calculating the similarity between the retrieved document and the user query. The document that has maximum similarity is returned as the response from the chatbot.

**Live demo**

Please find the link to live demo of the project - https://www.youtube.com/watch?v=wxNcdEwtX9M&t=1s 

**Future Scope**

We have hereby completed this End to End IR Chat Bot. The performance can be improved by using a larger and diverse dataset so that the chat can be more coherent. We can try to integrate other models like LSTM to keep the context of the conversation and make the replies more logical.
