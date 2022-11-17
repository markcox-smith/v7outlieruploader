# v7outlieruploader

A simple example of uploading and detecting outliers using the V7 platform as part of a Summer Cup challenge with Kevin Chang and James Hudson.

## Why?
Data drift is a common challenge in Computer Vision and can cause model degradation if not detected quickly. This simple script uploads images and stores simple stats about their RGB channels in a sqllite DB. If an item has values 2 sigma away from the mean then it is uploaded with an 'Outlier' tag to the V7 system. This in turn can trigger a webhook to send a Slack message alerting the team about an outlier image. We used a [Zapier workflow](https://zapier.com/shared/da5be18e8019d3865ec01b0f106dbf044971455a) in order to do this.

You can see this demonstrated by James Hudson in [this Loom video](https://www.loom.com/share/2a261e2434fc409f9720b910956334b5).

## How to use the example
You will need a V7labs account. See our page [here](https://www.v7labs.com/) for more details.

It is important to already have a batch of images filling your stats table or otherwise you will have too small a sample size.


## Notes
This example makes use of the V7labs V2 API as well as the darwin-py SDK. You can see more details [here](https://docs.v7labs.com/v2.0/reference/introduction).

This script can be easily readapted to detect files that are too similar based on their RGB channel values. Reach out to your V7 Customer Success Manager if you are interested in speaking to a Customer Success Engineer about the range of possibilities and how we can help with your use case.


