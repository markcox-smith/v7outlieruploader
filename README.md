# v7outlieruploader

A simple example of uploading and detecting outliers using the V7 platform as part of a Summer Cup challenge with Kevin Chang and James Hudson.

##Why?
Data drift is a common challenge in Computer Vision and can cause model degradation if not detected quickly. This simple script uploads images and stores simple stats about their RGB channels in a sqllite DB. If an item has values 2 \sigma away from the mean then it is uploaded with an 'Outlier' tag to the V7 system. This in turn can trigger a webhook to send a Slack message alerting the team about an outlier image.


##How to use the example
You will need a V7labs account. See our page here[(https://www.v7labs.com/)] for more details.

It is important to already have a batch of images filling your stats table or otherwise you will have too small a sample size.


##Notes
This example makes use of the V7labs V2 API as well as the darwin-py SDK. You can see more details here[(https://docs.v7labs.com/v2.0/reference/introduction)].



