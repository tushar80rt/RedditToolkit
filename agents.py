import os
import time
import traceback
import praw
from camel.agents import ChatAgent
from camel.toolkits import RedditToolkit
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from dotenv import load_dotenv

# ---------------- Load environment variables ---------------- #
load_dotenv("api.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_USERNAME, REDDIT_PASSWORD]):
    raise ValueError("Please set Reddit API credentials (including username & password) in your .env file!")

# ---------------- Initialize OpenAI model ---------------- #
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O,
    model_config_dict=ChatGPTConfig(temperature=0.2).as_dict(),
)

# ---------------- Initialize Reddit Toolkit ---------------- #
reddit_toolkit = RedditToolkit(retries=3, delay=2, timeout=120)

# ---------------- Initialize PRAW for posting ---------------- #
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# ---------------- Collector Agent ---------------- #
collector_agent = ChatAgent(
    """
You are a Reddit Data Collector & Summarizer Agent.  

For each post, generate exactly:

Post Title: <Post title>
Collector Summary: <3-5 sentence summary>
Comments:
1. Comment Body: <first comment>
   Upvotes: <number>
2. Comment Body: <second comment>
   Upvotes: <number>

Overall Discussion Tone: <Neutral / Supportive / Critical / Mixed>

If no data, return: "No relevant data found."
""",
    model=model,
    tools=[reddit_toolkit.collect_top_posts]
)

# ---------------- Sentiment Agent ---------------- #
sentiment_agent = ChatAgent(
    """
You are a Sentiment Analysis Agent.  

Return numeric sentiment score between -1.0 and +1.0
Only the number.
""",
    model=model,
    tools=[]
)

# ---------------- Fact Checker Agent ---------------- #
factchecker_agent = ChatAgent(
    """
You are a Fact-Checking Agent.  

If correct → 'True'
If incorrect → 'False'
If cannot verify → 'Unverified'
Output only one word.
""",
    model=model,
    tools=[]
)

# ---------------- User Comment Generator ---------------- #
comment_agent = ChatAgent(
    """
You are a Reddit Comment Generator Agent.
Given the most liked comment from a post, generate a new comment
that is similar in style but adds value or a different perspective.
Return only the comment text.
""",
    model=model,
    tools=[]
)

def generate_comment_from_best(fetched_comments):
    """
    fetched_comments: list of dicts with 'Comment Body' and 'Upvotes'
    """
    if not fetched_comments:
        return None

    # Most liked comment
    best_comment = max(fetched_comments, key=lambda c: c.get('Upvotes', 0))
    prompt = f"Original Comment: {best_comment['Comment Body']}\nGenerate a new comment in a similar style."

    try:
        resp = comment_agent.step(prompt)
        new_comment = resp.msgs[0].content.strip()
        return new_comment
    except Exception as e:
        print("Error generating comment:", e)
        return None
    


def fetch_posts(subreddits, keywords=None, post_limit=None, comment_limit=None):
    raw_data = []
    try:
        post_limit = post_limit or 2
        comment_limit = comment_limit or 3

        for subreddit in subreddits:
            top_posts = reddit_toolkit.reddit.subreddit(subreddit).top(limit=post_limit)
            for post in top_posts:
                post.comments.replace_more(limit=0)
                all_comments = post.comments.list()

                
                filtered_comments = [
                    {"Comment Body": c.body, "Upvotes": getattr(c, "score", 0)}
                    for c in all_comments
                    if not keywords or any(kw.lower() in c.body.lower() for kw in keywords)
                ]

              
                sorted_comments = sorted(filtered_comments, key=lambda x: x["Upvotes"], reverse=True)

                
                post_comments = sorted_comments[:comment_limit]

                print(f"DEBUG: Post: {post.title}, Top Comments Fetched: {len(post_comments)}")

                try:
                    comments_text = "\n".join(
                        [f"{i+1}. {c['Comment Body']}" for i, c in enumerate(post_comments)]
                    )
                    prompt = f"Subreddit: {subreddit}\nPost: {post.title}\nComments:\n{comments_text}"
                    collector_summary = collector_agent.step(prompt)
                    collector_text = collector_summary.msgs[0].content.strip()
                except Exception:
                    collector_text = "Collector agent failed"

                raw_data.append({
                    "Subreddit": subreddit,
                    "Post Title": post.title,
                    "Post Body": getattr(post, "selftext", "") or "",
                    "Post Link": f"https://reddit.com{post.permalink}",
                    "Post Upvotes": getattr(post, "score", 0),
                    "Post Thumbnail": post.thumbnail if hasattr(post, "thumbnail") and post.thumbnail.startswith("http") else None,
                    "Collector Summary": collector_text,
                    "Comments": post_comments
                })
                time.sleep(1)

        print(f"DEBUG: Total Posts Fetched: {len(raw_data)}")
        return raw_data
    except Exception as e:
        print("Exception in fetch_posts():", e)
        traceback.print_exc()
        return []


# ---------------- Generate Report ---------------- #
def generate_report(posts_data):
    report = []
    for post in posts_data:
        for comment in post.get("Comments", []):
            body = comment.get("Comment Body", "")
            sentiment_score = 0.0
            verdict = "Unverified"

            try:
                sentiment_resp = sentiment_agent.step(
                    f"Analyze sentiment (positive=1, neutral=0, negative=-1). Comment: {body}"
                )
                sentiment_score = float(sentiment_resp.msgs[0].content.strip())
            except Exception as e:
                print("Error in sentiment analysis:", e)
                traceback.print_exc()

            try:
                fact_resp = factchecker_agent.step(
                    f"Fact check this comment. Respond only with True, False, or Unverified:\n{body}"
                )
                verdict = fact_resp.msgs[0].content.strip() if fact_resp.msgs else "Unverified"
            except Exception as e:
                print("Error in fact checking:", e)
                traceback.print_exc()

            report.append({
                "Subreddit": post.get("Subreddit"),
                "Post Title": post.get("Post Title"),
                "Post Link": post.get("Post Link"),
                "Post Upvotes": post.get("Post Upvotes", 0),
                "Collector Summary": post.get("Collector Summary", ""),
                "Comment": body,
                "Comment Upvotes": comment.get("Upvotes", 0),
                "Sentiment": sentiment_score,
                "Fact Verdict": verdict
            })
    return report

def create_post(subreddit, title, body, flair_text=None):
    """
    Create a new Reddit post based on user input using PRAW.
    flair_text: optional, required by some subreddits
    """
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        
        if flair_text:
            flair_id = None
            for ft in subreddit_obj.flair.link_templates:
                if ft['text'].lower() == flair_text.lower():
                    flair_id = ft['id']
                    break
            submission = subreddit_obj.submit(title=title, selftext=body, flair_id=flair_id)
        else:
            submission = subreddit_obj.submit(title=title, selftext=body)
        
        print(f"✅ Post created: https://reddit.com{submission.permalink}")
        return submission
    except Exception as e:
        print("❌ Error while posting:", e)
        return None
