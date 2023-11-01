import csv
import json

def load_tweets(file_path:str='tweets.js')->dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        prefix = 'window.YTD.tweets.part0 = '
        if content.startswith(prefix):
            content = content[len(prefix):]
        data = json.loads(content)
    return data

def get_all_fields(tweets):
    all_fields = set(['link', 'reply_to_link'])
    for tweet in tweets:
        all_fields.update(tweet['tweet'].keys())
    return all_fields

def get_ordered_fields(all_fields):
    specific_fields = ['created_at', 'link', 'reply_to_link', 'full_text']
    return specific_fields + list(all_fields - set(specific_fields))

def generate_link(tweet_id):
    return f"https://twitter.com/user/status/{tweet_id}"

def generate_reply_to_link(reply_to_id):
    return f"https://twitter.com/user/status/{reply_to_id}" if reply_to_id else None

def convert_csv(tweets:list, output_file:str='tweets.csv'):
    all_fields = get_all_fields(tweets)
    ordered_fields = get_ordered_fields(all_fields)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=ordered_fields)
        writer.writeheader()
        
        for tweet in tweets:
            tweet_data = tweet['tweet']
            tweet_data['link'] = generate_link(tweet_data['id_str'])
            tweet_data['reply_to_link'] = generate_reply_to_link(tweet_data.get('in_reply_to_status_id_str'))
            
            row = {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in tweet_data.items()}
            writer.writerow(row)

tweets_dict = load_tweets()
convert_csv(tweets_dict)
