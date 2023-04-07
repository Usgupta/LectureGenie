import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# example transcript
transcript = "Speaker 1: Good morning, everyone. Today we're going to talk about our new product line. Speaker 2: Can you tell us more about the features of the new product line? Speaker 1: Sure, the new product line includes several new features such as enhanced performance, improved durability, and better user interface. Speaker 3: How does the new product line compare to our competitors' products? Speaker 1: Our product line is superior in terms of performance and durability. Speaker 2: What is the pricing strategy for the new product line? Speaker 1: We're planning to price it competitively to attract more customers."
t2 = "Testosterone is a chemical substance known as a hormone and it can have quite wide-ranging effects through the body and that’s because it’s released into the bloodstream and therefore it can go around the body in the blood circulation and affect a wide range of organs.Testosterone is made in males in Leydig cells in the testes.There’s also a small amount made in the ovaries in females,and in both sexes is made in the adrenal glands which sits on top of the kidneys.Now, the release of testosterone is controlled by a group of structures called the hypothalamic-pituitary-adrenal axis, and these include the hypothalamus in the brain, the pituitary gland at the base of the brain, and the adrenal glands on top of the kidneys.The release of testosterone generally occurs in two quite big surges in the body and these happen at around seven weeks of fetal development,and that’s associated with the development of the male genitalia,and it happens again at around age twelve and that’s associated with puberty.So as well as those physical characteristics, the release of testosterone is also associated with larger body bills,increased muscle mass and more and more bodily hair.But it’s also associated with some interesting psychological characteristics as well,and these include, greater aggression, more dominant behaviour, but also really interesting behaviour known as risk-taking."

# tokenize transcript
sentences = sent_tokenize(t2)
words = word_tokenize(t2.lower())

# remove stop words and lemmatize words
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
filtered_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

# identify key concepts and topics
concepts = set()
topics = set()
for word in filtered_words:
    if word.isupper():
        concepts.add(word)
    elif word.isalpha():
        topics.add(word)

# identify questions
questions = [sentence for sentence in sentences if sentence.endswith('?')]

# print results
print("Concepts:", concepts)
print("Topics:", topics)
print("Questions:", questions)