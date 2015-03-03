This file has text and target from the following datasets. Note that 'text'
is the text of a tweet, and target is 1 if has gendered harassment, 0 otherewise.

The first 157 rows are from femfreq- One Week of Harassment on Twitter - Sheet1.csv.
The target is 1 for all such rows, as they are hand classified by femfreq herself.

The subsequent rows are from femfreq_mentions_300.csv, which is itself
from 300 mentions gotten via the Twitter Search API on March 02, 2015. These
were from the query '@femfreq', English locale only, with the result type
'mixed', the default, which includes both popular and real time results. These
rows have been classified by the developers.