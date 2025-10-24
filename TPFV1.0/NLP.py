#!/usr/bin/env python3
"""
Natural Language Processing module using OpenAI API
Run this in env2
"""
import sys
import os
from openai import OpenAI

def generate_response(input_text, api_key=None):
    """
    Generate response using OpenAI API
    """
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("ERROR: No API key provided. Set OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Remove any extra kwargs that might cause issues
        client = OpenAI(api_key=api_key)
        
        print(f"Sending to OpenAI: {input_text}", file=sys.stderr)
        
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:personal::9NbLcpu1:ckpt-step-60",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a loving grandmother speaking to your grandchild. Be warm, caring, and supportive."
                },
                {
                    "role": "user", 
                    "content": input_text
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        print(f"Received response: {answer}", file=sys.stderr)
        return answer
        
    except Exception as e:
        print(f"ERROR: OpenAI API error: {e}", file=sys.stderr)
        # Fallback response
        return "I love you, my dear child."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No input text provided", file=sys.stderr)
        print("Usage: python NLP.py <input_text>", file=sys.stderr)
        sys.exit(1)
    
    input_text = " ".join(sys.argv[1:])
    response = generate_response(input_text)
    
    # Output only the response to stdout (for piping)
    print(response)