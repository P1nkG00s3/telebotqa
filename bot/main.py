from pydoc_data.topics import topics

import telebot
import random

from bot import Questions
from bot.Questions import questions

API_TOKEN = '6583416796:AAGVUsfWES-FkZ2_V1rtVtoL1KiF5erLW9A'

bot = telebot.TeleBot(API_TOKEN)

# Хранилище для данных пользователей
user_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi! I am a test bot. Type /test to start the quiz.')

@bot.message_handler(commands=['topic'])
def choose_topic(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for topic in Questions.questions.keys():
        markup.add(topic)
    bot.send_message(message.chat.id, 'Choose a topic:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in Questions.questions.keys())
def handle_topic_selection(message):
    selected_topic = message.text
    bot.send_message(message.chat.id, f"Выбрана тема: {selected_topic}")
    user_id = message.from_user.id
    user_data[user_id] = {"topic": f'{selected_topic}'}
    print(user_data)

# @bot.message_handler(commands=['test'])
# def start_test(message):
#     user_id = message.from_user.id
#     user_data[user_id] = {"asked_questions": [], "score": 0}
#     ask_random_question(message)

@bot.message_handler(commands=['test'])
def start_test(message):
    user_id = message.from_user.id
    if user_id in user_data and "topic" in user_data[user_id]:
        topic = user_data[user_id]["topic"]
        user_data[user_id]["asked_questions"] = []
        user_data[user_id]["score"] = 0
        ask_random_question(message, topic)
    else:
        bot.reply_to(message, 'Please choose a topic first by typing /topic')

def ask_random_question(message, topic):
    user_id = message.from_user.id
    asked_questions = user_data[user_id]["asked_questions"]

    print(f"HUHUHUHHUHU {asked_questions}")
    len_of_question = len(Questions.questions["Теория тестирования"]) + len(Questions.questions["WEB"])

    if len(asked_questions) == len_of_question:
        score = user_data[user_id]["score"]
        bot.send_message(message.chat.id,
                         f'You have answered all the questions! Your final score is {score}/{len_of_question}')
        user_data.pop(user_id)
        return

    # available_questions = [q for i, q in enumerate(Questions.questions[topic]) if i not in asked_questions]
    # print(available_questions)
    # question_data = random.choice(available_questions)
    # print(f"HUH {question_data}")

    question_list = [q for i, q in enumerate(Questions.questions[topic]) if i not in asked_questions]
    question_object = random.choice(question_list)
    print(question_object)

    # question_object = random.choice(Questions.questions.get(question_data))
    # print(question_object)
    question = question_object.get('question')
    dict_for_user_db = {
        f"{topic}":{question}
    }

    user_data[user_id]["asked_questions"].append(dict_for_user_db)
    answers = question_object.get('answers')
    print(user_data)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for ans in answers:
        markup.add(ans)

    bot.send_message(message.chat.id, question, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.reply_to(message, 'Please start the test by typing /test')
        return

    user_answer = message.text
    asked_questions = user_data[user_id]["asked_questions"]

    current_question_index = asked_questions[-1]
    key = list(current_question_index.keys())[0]
    answer = list(current_question_index.get(key))[0]

    for case in Questions.questions[key]:
        print(case)
        if case["question"] == answer:
        #     print('хуй')
            correct_answer = case["correct"]
        #     print(correct_answer)
    # correct_answer = enumerate(Questions.questions[key]["question"][answer])


    if user_answer == correct_answer:
        user_data[user_id]["score"] += 1
        bot.reply_to(message, f'Верно!')
    else:
        bot.reply_to(message, f'Неправильно! Правильный ответ \n\n*{correct_answer}*')

    topic = user_data[user_id]["topic"]

    ask_random_question(message, topic)



    @bot.message_handler(commands="ekzamen")
    def start_ekzamen():

        """Экзамен из 20 упорядоченных вопросов без повторений по выбранной теме"""
        pass
        # user_id = message.from_user.id
        # if user_id in user_data and "topic" in user_data[user_id]:
        #     print(user_data)
        #     user_data[user_id]["asked_questions"] = []
        #     user_data[user_id]["score"] = 0
        #     ask_random_question(message)
        # else:
        #     bot.reply_to(message, 'Please choose a topic first by typing /topic')



# Бесконечный цикл
bot.infinity_polling()
