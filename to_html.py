import markdown
from bs4 import BeautifulSoup
import copy
with open('patterns.md') as md_file, open('template.html') as templ_file:
    markdown_data = md_file.read()
    html_template = templ_file.read()
html_markdown = markdown.markdown(markdown_data)
soup_markdown = BeautifulSoup(html_markdown, "html.parser")
soup_template = BeautifulSoup(html_template, "html.parser")

start_makrer = soup_template.find('div', id='start-marker')

block_question = copy.copy(soup_template.find('div', class_='wrapper'))


def gen_block_question(bq: BeautifulSoup, quest_block: dict) -> BeautifulSoup:
    start_block = bq.find('div', id='block-q')
    correct_q = bq.find_all('label', class_='option')[0]
    incorrect_q = bq.find_all('label', class_='option')[1]
    quest = bq.find('p', class_='p-quest')

    quest.string.replace_with(quest_block['q'])
    start_block.insert_after(copy.copy(correct_q))
    start_block.insert_after(copy.copy(incorrect_q))
    start_block.insert_after(copy.copy(correct_q))
    start_block.insert_after(copy.copy(incorrect_q))
    correct_q.decompose()
    incorrect_q.decompose()
    return copy.copy(bq)

quest_block = {'q': 'Q1. Wraps !!! an object to provide new behavior', 'ans': [{'correct': True, 'text': 'Visitor'}, {'correct': False, 'text': 'Decorator'}]}
block1 = gen_block_question(block_question, quest_block)
start_makrer.insert_after(block1)

with open('res.html', 'w') as fw:
    fw.write(str(soup_template))
