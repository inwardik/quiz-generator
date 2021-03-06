import markdown
from bs4 import BeautifulSoup as bs
from copy import copy
import random

SHUFFLE_QUESTIONS = True
SHUFFLE_BLOCKS = True


def generate_quest_blocks(tag: bs) -> list:
    quest_blocks = []
    titles_tags = tag.find_all('h4')
    titles = [title.string for title in titles_tags]
    all_variants = []
    uls_tags = tag.find_all('ul')
    for uls_tag in uls_tags:
        li_tags = uls_tag.find_all('li')
        variants = [li_tag.string for li_tag in li_tags]
        dict_variants = []
        for variant in variants:
            if not variant:
                raise ValueError("Variant is empty")
            temp = {}
            if '[ ]' in variant:
                temp['correct'] = False
            elif '[x]' in variant or '[X]' in variant:
                temp['correct'] = True
            else:
                raise ValueError('wrong [] or [x]')
            temp['text'] = variant.replace('[ ]', '').replace('[x]', '').replace('[X]', '').strip()
            dict_variants.append(temp)
        if SHUFFLE_QUESTIONS:
            random.shuffle(dict_variants)
        all_variants.append(dict_variants)
    for i in range(len(titles)-1, -1, -1):
        q_block = {'q': titles[i], 'ans': all_variants[i]}
        quest_blocks.append(q_block)
    if SHUFFLE_BLOCKS:
        random.shuffle(quest_blocks)
    return quest_blocks


def get_title(tag: bs) -> str:
    quiz_title = tag.find('h2')
    return quiz_title.string


def gen_block_question(bq: bs, quest_block: dict, title: str) -> bs:
    start_block = bq.find('div', id='block-q')
    correct_q = bq.find_all('label', class_='option')[0]
    incorrect_q = bq.find_all('label', class_='option')[1]
    quest = bq.find('p', class_='p-quest')
    quiz_title = bq.find('p', class_='title-text')
    quiz_title.string = title

    quest.string.replace_with(quest_block['q'])
    for answer in quest_block['ans']:
        if answer['correct']:
            copy_correct = copy(correct_q)
            copy_correct.find('p').replace_with(answer['text'])
            start_block.insert_after(copy_correct)
        else:
            copy_incorrect = copy(incorrect_q)
            copy_incorrect.find('p').replace_with(answer['text'])
            start_block.insert_after(copy_incorrect)

    correct_q.decompose()
    incorrect_q.decompose()
    return bq


def save_file(filename, tag):
    with open(f'{filename}.html', 'w') as fw:
        fw.write(str(tag))


def main(filename):
    with open(f'{filename}.md') as md_file, open('template.html') as templ_file:
        markdown_data = md_file.read()
        html_template = templ_file.read()
    html_markdown = markdown.markdown(markdown_data)
    soup_markdown = bs(html_markdown, "html.parser")
    soup_template = bs(html_template, "html.parser")
    start_makrer = soup_template.find('div', id='start-marker')
    q_block_template = soup_template.find('div', class_='wrapper')
    quest_blocks = generate_quest_blocks(copy(soup_markdown))
    quiz_title = get_title(copy(soup_markdown))

    for quest_block in quest_blocks:
        fill_ready_block = gen_block_question(copy(q_block_template), quest_block, quiz_title)
        start_makrer.insert_after(fill_ready_block)

    q_block_template.decompose()

    save_file(filename, soup_template)
    save_file(filename+'_ans', soup_markdown)


if __name__ == '__main__':
    main('scrum')