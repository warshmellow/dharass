dHarass

A tool to get nasty gendered harassment out of your Twitter mentions

How to Use
1. In the project directory, type python build_model.py to build the model
2. Type python flask_app.py to run the app
Then you have 3 choices to get Tweets to scan: the mentions of a Twitter user,
a JSON dump from the Twitter API, or you can type your own message directly.
You will then go to a table with Tweets and their labels.

Motivation & Inspiration
Women with a large online presence receive a special type of gendered
harassment on social media (consisting e.g. of slurs against women, manslplaining, threats of corporal and sexual violence, etc.), that male users have reported never receiving. One social media platform on which they
receive this harassment is Twitter. Prominent women writers on Twitter
complain of constant nasty messages left in their mentions (i.e., messages
featuring their name or send to them). They can of course block the users
after reading these messages, but it requires someone to read the message! 

One solution to this a shared block list, but it still requires someone to 
read the message.

dHarass reads the message before the user sees it, flags it and the user who
sent the nasty message, and returns that information in a list to the user. The user can then block all or some of these users, or export to a shared block list.

At its core, dHarass has a classifier that labels the text of a Tweet for 
gendered harassment.

dHarass was designed under the following constraint:
* The text alone of a single message is enough to determine whether to block someone.
That is, no aggregate text information and no extra-textual information (such as account info or geolocation info) is used to 
This is because people can either make accounts for the sole purpose of harassment, and there would be no aggregate or account info to mine, or people from all walks of life can leave nasty messages, so that the study of who leaves and who doesn't leave such messages is too wide.

* Anything is better than Twitter's current Null Classifier
That is, Twitter lets any tweet go without filtering. If we can catch even some of the messages like "Die B*tch", we're doing better than Twitter!

Data
The data consists Tweets pulled from the mentions of a prominent female critic,
@femfreq, over the course of two weeks. We use her data because she has publically said she receives this harassment constantly. Small samples of her mentions suggest that it consists of more than 5% of her mentions.

She has specifically provided a week's worth of what she considers gendered
harassment. We augment this dataset with more of her mentions, hand classified by the developers.

We worked specifically with about 3000 unique tweets, with about 1000 hand-labeled.

Model
We wanted to stick with basic, scalable text analysis techniques. For us, this meant Bag of Words. We found that under the Bag of Words model, 1-grams with Count Vectorization and Multinomial Naive Bayes was most effective. Also competitive with this are TF-IDF vectorization with L1-regularized Logistic Regression or Linear SVM.

Experiments with Semi-Supervised Expectation-Maximization Naive Bayes were done. Performance didn't improve, but was still competitive with Supervised Naive Bayes.

General Technical Issues
* Data Sparsity
Short texts suffer from extreme data sparsity.  They lack the internal redundancy of longer texts, and once they are processed they may consist of
a few mispelled words. A classifier that works with this data has to be extremely sensitive to addition of key words. This may be why a classifier misclassifies on the strangest tweets.

The theme of the investigation of classifiers of short texts is to understand the limits of standard methods on extremely sparse data.

One way to handle this is to go the other way. It is to augment short texts with longer texts and reduce the problem to one more amenable to standard text analysis methods.

* High Expense of Hand Labeling
Hand labeling is very expensive. We should be able to mine user blocking activity to get something close to labeling, perhaps only the distinguished class.

* Class imbalance + expanding larger class
This problem consists of the distinguished class, which covers a few words and
topics, and literally any other topic. We would like to be able to expand the vocabulary periodically and retrain the classifier accordingly.

Next Steps
* Address data sparsity with Text Augmentation
We can try to reduce the (cf. paper "...") by augmenting the short text with
more text. One suggestion from the paper above is to use Wikipedia as an indexed ground truth source, so we can use our short text as a query to find the most relevant articles, and add the text from these articles.

* Address High Expense of Hand Labeling with Crowd Sourcing
We may be able to mine the blocked Tweets by taking a tweet from a user the main user actually blocked as an actual labeling of the positive class, and the other ones as unlabeled. We then run semi-supervised methods to expand the vocabulary and retrain the classifier.

* Address class imbalance and expanding larger class with periodic retraining
and semi-supervised learning
Again, we run semi-supervised methods to expand the vocabulary and retrain the classifier.


Toolkit + Credits:
1. Twitter API
2. MongoDB
3. Flask
4. Scikit-learn
5. OpenPR-NBEM
