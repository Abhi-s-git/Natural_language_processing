import re
import heapq
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


text = """

Climate change refers to long-term shifts in temperatures and weather patterns, 
mainly caused by human activities, especially the burning of fossil fuels. 
These changes have led to global warming, rising sea levels, extreme weather events, 
and disruptions in ecosystems. Over the past century, the Earth's average temperature has increased 
significantly, resulting in melting glaciers, shrinking ice sheets, and more frequent heatwaves. 
The Intergovernmental Panel on Climate Change (IPCC) has repeatedly warned that immediate action 
is required to limit global temperature rise to 1.5°C above pre-industrial levels. 
Failure to act could result in irreversible damage to the environment and human societies.
Countries worldwide are working towards reducing carbon emissions through renewable energy, 
reforestation, and sustainable practices. Public awareness and individual efforts,
such as conserving energy and reducing waste, also play a crucial role in combating climate change.
While technological innovations and international agreements like the Paris Accord offer hope,
coordinated global action remains essential to mitigate the worst effects of climate change and 
secure a livable future for coming generations.
"""



sentences = re.split(r'(?<=[.!?]) +', text)


clean_text = re.sub(r'\[[0-9]*\]', ' ', text)
clean_text = re.sub(r'\s+', ' ', clean_text)
clean_text = re.sub(f"[{string.punctuation}]", '', clean_text)


words = re.findall(r'\b\w+\b', clean_text.lower())


stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]


word_freq = {}
for word in filtered_words:
    word_freq[word] = word_freq.get(word, 0) + 1

max_freq = max(word_freq.values())
for word in word_freq:
    word_freq[word] /= max_freq


sentence_scores = {}
for sentence in sentences:
    sentence_words = re.findall(r'\b\w+\b', sentence.lower())
    for word in sentence_words:
        if word in word_freq:
            if len(sentence.split(' ')) < 30:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]


summary_sentences = heapq.nlargest(2, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)


print("\n Summary:\n")
print(summary)

