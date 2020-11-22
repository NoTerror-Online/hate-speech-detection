#!/usr/bin/env python
# coding: utf-8

# In[4]:


from hatesonar import Sonar
from flask import Flask, request
import html2text
import aiohttp
import asyncio


# In[7]:

sonar = Sonar()
h = html2text.HTML2Text()
h.ignore_links = True
loop = asyncio.get_event_loop()
app = Flask(__name__)


async def fetch(client, url):
    async with client.get(url) as resp:
        # assert resp.status == 200
        return await resp.text()

async def main(url):
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url)
        return html

@app.route("/is_clean", methods=['GET', 'POST'])
def is_hate():
    if request.method == 'POST':
        url = request.form.get('url')
        html = loop.run_until_complete(main(url))
        clean_html_text = h.handle(html)
        clean_html_text = clean_html_text.split(" ")
        for sentence in clean_html_text:
            not_offensiveness = sonar.ping(text=sentence).get("classes")[2].get("confidence")
            if not_offensiveness < 0.1:
                return "Hate Speech"
        return "Not Hate Speech"
        # html = loop.run_until_complete(main(url))
        # clean_html_text = h.handle(html)
        # return clean_html_text
        # return sonar.ping(text=html)
    else:
        url = request.args.get("url")
        html = loop.run_until_complete(main(url))
        clean_html_text = h.handle(html)
        clean_html_text = clean_html_text.split(" ")
        for sentence in clean_html_text:
            not_offensiveness = sonar.ping(text=sentence).get("classes")[2].get("confidence")
            if not_offensiveness < 0.1:
                return "Hate Speech"
        return "Not Hate Speech"
        # 1%

# In[ ]:




