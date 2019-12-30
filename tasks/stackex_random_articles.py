import xml.etree.ElementTree as ET
import random


def random_questions(count):
    posts_tree = ET.parse('Posts.xml')
    '''
    [
        {
            question_id:
            title: ''
            text: ''
            answers:[
                        {
                            answer_id: 
                            body: ''
                        }
                    ]
        }
    ]
    '''
    question_tags = []
    answer_tags = []
    posts_root = posts_tree.getroot()
    for row in posts_root:
        if row.get('PostTypeId') == "1":
            question_tags.append(row)
        elif row.get('PostTypeId') == "2":
            answer_tags.append(row)

    comment_parent_ids = []
    question_tags = random.choices(question_tags, k=count)
    question_ids = [q.get('Id') for q in question_tags]
    chosen_answers = {q_id: [] for q_id in question_ids}
    for answer in answer_tags:
        if answer.get('ParentId') in question_ids:
            chosen_answers[answer.get('ParentId')].append(answer)
            comment_parent_ids.append(answer.get('Id'))

    comment_parent_ids.extend(question_ids)

    qa_root = ET.Element("root")
    for i in range(len(question_ids)):
        ET.SubElement(qa_root, 'question', {'Id': question_ids[i],
                                            'Title': question_tags[i].get('Title'),
                                            'Body': question_tags[i].get('Body')})
        for j in range(len(chosen_answers[question_ids[i]])):
            ET.SubElement(qa_root[i], 'answer', {'Id': chosen_answers[question_ids[i]][j].get('Id')})
            qa_root[i][j].text = chosen_answers[question_ids[i]][j].get('Body')

    qa_tree = ET.ElementTree(qa_root)

    qa_tree.write("stackex_qa_data.xml")

tree = ET.parse('stackex_qa_data.xml')
root = tree.getroot()
c = 0
for child in root.iter('question'):
    c += 1
print(c)