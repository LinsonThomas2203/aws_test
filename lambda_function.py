import json
import boto3
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

nltk.data.path.append("/tmp")  # Use /tmp directory for Lambda
nltk.download('stopwords', download_dir="/tmp")
nltk.download('punkt', download_dir="/tmp")

s3 = boto3.client('s3')

def summarize_text(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    
    summary = summarizer(parser.document, sentences_count)
    summarized_text = " ".join([str(sentence) for sentence in summary])
    return summarized_text

def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    file_key = event['file_key']
    
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    
    data = json.loads(file_content)
    
    text_kerala = data.get('text_kerala', '')
    text_rajasthan = data.get('text_rajasthan', '')
    text_assam = data.get('text_assam', '')
    
    combined_text = text_kerala + " " + text_rajasthan + " " + text_assam
    
    summary = summarize_text(combined_text, sentences_count=7)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'summary': summary
        })
    }
