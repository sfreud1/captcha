from telegram import Update, Bot,ChatMemberAdministrator, ChatMemberOwner,KeyboardButton,KeyboardButtonPollType,Poll,ReplyKeyboardMarkup,ReplyKeyboardRemove,MessageEntity,ChatPermissions
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler,ContextTypes,PollAnswerHandler,PollHandler
import telegram
import time
import json
import logging
import re
import command as c
import otomatikmesaj as o
import captcha as captcha
import deletejoin as deletejoin

ChatPermissions({
    'can_send_messages': False, 
    'can_send_media_messages': False, 
    'can_send_polls': False, 
    'can_send_other_messages': False, 
    'can_add_web_page_previews': False, 
    'can_change_info': False, 
    'can_invite_users': False, 
    'can_pin_messages': False
})

def quiz(update, context):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    user = update.effective_user
    chat = update.effective_chat
    username = update.message.from_user
    first = username.username
    userID=username.id
    user_member = chat.get_member(user.id)
    context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    context.bot.restrict_chat_member(chat_id=update.effective_chat.id,user_id=userID,permissions=ChatPermissions())

    questions = ["\U0001F44A", "\U0001F44A", "\U0001F42E", "\U0001F44A"]
    message =  context.bot.send_poll(update.effective_chat.id,
        "\U0001F449 Please select the different emoji to join the group.(60sec)", questions, type=Poll.QUIZ, correct_option_id=2, is_anonymous=False,open_period=60
    )
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id,"questions": questions,"answers": 0}
    }
    context.bot_data.update(payload)
    context.job_queue.run_once(delete_quiz, 60, context=(update.effective_chat.id,message.message_id))
def receive_quiz_answer(update, context):
        answer = update.poll_answer
        answered_poll = context.bot_data[answer.poll_id]
        soru = answered_poll['questions']
        cow = answered_poll['questions'][2]
        msg_id =  answered_poll["message_id"]
        chat_idd= answered_poll["chat_id"]
        userID=update.effective_user.id
        selected_options = answer.option_ids
        for question_id in selected_options:
                if question_id != 2 :
                    context.bot.delete_message(chat_id=chat_idd,message_id=msg_id)
                elif question_id == 2:
                    context.bot.promote_chat_member(chat_id=chat_idd,user_id=userID,can_post_messages=True)
                    context.bot.delete_message(chat_id=chat_idd,message_id=msg_id)
def delete_quiz(context: telegram.ext.CallbackContext):
    try:
        context.bot.delete_message(chat_id=context.job.context[0],message_id=context.job.context[1])
    except:
        pass