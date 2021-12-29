import random
from pathlib import Path
from PIL import Image
import time

questions_dir = "/Users/harao/Documents/rithvik_math/"
max_question = {'ch1ch2': -1, 'ch3': -1, 'ch4': -1, 'ch5': -1}


def current_milli_time():
    return round(time.time() * 1000)


def populate_max_questions():
    for path in sorted(Path(questions_dir).iterdir()):
        file_name_without_extension = get_filename_without_extension(path)
        chapter = file_name_without_extension[0:file_name_without_extension.rfind("-")]
        question_number = file_name_without_extension[file_name_without_extension.rfind("-") + 1:]
        question_number_int = 0
        if len(question_number) < 1:
            continue
        try:
            question_number_int = int(file_name_without_extension[file_name_without_extension.rfind("-") + 1:])
        except ValueError:
            print(f'value error ${file_name_without_extension[file_name_without_extension.rfind("-") + 1:]}')
        if (chapter in max_question) and (max_question[chapter] < question_number_int):
            max_question[chapter] = question_number_int


def get_filename_without_extension(path_i):
    str_path = str(path_i)
    file_name = str_path[str_path.rfind("/") + 1:len(str_path)]
    return file_name[0:file_name.rfind(".")]


def pick_5_questions_from_each_chapter():
    question_list = []
    for k, v in max_question.items():
        ch_list = []
        for i in range(1, v):
            ch_list.append(k + '-' + str(i))
        ch_list_selected = random.sample(ch_list, 5)
        question_list.append(ch_list_selected)
    return question_list


def generate_question_file_list(question_list):
    flat_question_list = flatten(question_list)
    question_file_list = []
    for question in flat_question_list:
        question_file_list.append(questions_dir + question + '.png')
    return question_file_list


def flatten(t):
    return [item for sublist in t for item in sublist]


def create_pdf(question_file_list, pdf_name):
    image_list = []
    count = 0
    im1 = None
    for question in question_file_list:
        count = count + 1
        if count == 1:
            image1 = Image.open(question)
            im1 = image1.convert('RGB')
        else:
            image = Image.open(question)
            im = image.convert("RGB")
            image_list.append(im)
    im1.save(questions_dir+'output/' + pdf_name + '_' + str(current_milli_time()) + '.pdf', save_all=True,
             append_images=image_list)


def pick_15_questions_from_a_chapter(ch):
    question_list = []
    for k, v in max_question.items():
        if k == ch:
            ch_list = []
            for i in range(1, v):
                ch_list.append(k + '-' + str(i))
    ch_list_selected = random.sample(ch_list, 15)
    question_list.append(ch_list_selected)
    return question_list


def main():
    populate_max_questions()
    midterm_question_list = pick_5_questions_from_each_chapter()
    midterm_question_file_list = generate_question_file_list(midterm_question_list)
    create_pdf(midterm_question_file_list, 'midterm')
    generate_chapter_test('ch1ch2')
    generate_chapter_test('ch3')
    generate_chapter_test('ch4')
    generate_chapter_test('ch5')
    # print(max_question)
    # print(question_list)
    # print(*midterm_question_file_list, sep="\n")
    # print(*ch5_question_file_list, sep="\n")


def generate_chapter_test(chapter_key):
    ch_question_list = pick_15_questions_from_a_chapter(chapter_key)
    ch_question_file_list = generate_question_file_list(ch_question_list)
    create_pdf(ch_question_file_list, chapter_key)


if __name__ == "__main__":
    main()
