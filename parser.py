# parser.py
import csv
import re

def parse_raw_output(raw_output, output_path="questions.csv"):
    rows = []
    question_blocks = re.split(r'\n(?=Q\d+\.)', raw_output.strip())

    for idx, block in enumerate(question_blocks, 1):
        question_match = re.search(r'^Q\d+\.\s+(.*?)\n', block)
        options = re.findall(r'^([A-D])\.\s+(.*?)$', block, re.MULTILINE)
        answer_match = re.search(r'Answer:\s+([A-D])', block)

        if not (question_match and options and answer_match):
            continue

        question_text = question_match.group(1).strip()
        correct_label = answer_match.group(1)

        for label, option_text in options:
            rows.append({
                'question_id': idx,
                'question_text': question_text,
                'answer_label': label,
                'answer_text': option_text.strip(),
                'is_correct': str(label == correct_label).upper()
            })

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
