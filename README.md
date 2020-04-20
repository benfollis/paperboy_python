Paperboy (python 3.8 version)
---
This is a rough proptype of the Paperboy application that performs NLP similarity on a series of articles downloaded
from with the [paperboy_fetcher](http://github.com/benfollis/paperboy_fetcher) application.

Specifically it requires you pass in the location of a directory with top level names the names of feed providers, 
and second level names the name of the feed within the provider. For example `/BBC/top_stories`
Inside each feed directory (e.g. `top_stories`) there should be one json file per downloaded article,
with the json consisting of the following keys:
1. `title`: the title of the article
2. `article`: the text of the article
3. `link`: the link where the article can be downloaded

Payperboy will also require a config file passed in that contains a list of equivalencies of feeds for comparison.
E.g.  
```json
{
  "equivalencies": [
    {
      "name": "Top Stories",
      "article_sources": [
        "BBC/top_stories",
        "CNN/top_stories",
        "NYT/top_stories",
        "WAPO/world"
      ]
    }
  ]
}
```
These are the sets of directories it will consider containing
equivalent type of stories. This is because it doesn't make a lot of sense to compare stories about English Football,
with Nascar Races.

For each of the equivalency sets it will extract the article text of all articles in the feed directory, and perform
[Google Universal Sentence Encoder](https://arxiv.org/abs/1803.11175) similarity analysis of them, and build an
NxN matrix of the similarities.
It will then scan that matrix and group together articles that are above a threshold (optionally passed in as the `--threshold` parameter,
or defaulted to .80). It will then output those groups, as a JSON file containing a list with one entry per group.
Each group will contain the keys
1. `title`: randomly selected from one member of the group
2. `article`: text of the article we selected the title from 
3. `[links]`: a list of links, one for each member of the group

It is expected that some other process will make that file visible to the web, and that a frontend exists somewhere that
can render that file in a user's browser