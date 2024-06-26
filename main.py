import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import GigaLogic
import Kandivsky

TELEGRAM_TOKEN = "7450692282:AAFm7Gk29yi22rsAj99eB8KdIBDPLf134ZQ"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelво)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот для помощи преподавателям. Используйте команды для генерации курсов, планов занятий, тестов и обложек. \n /generate_course_description - Генерация описания курса по названию. \n /generate_lesson_plan - Генерация плана по названию занятия и курса. \n /generate_tests - Генерация тестов на проверку пройденного материала по названию занятия. \n /generate_lesson_cover - Генерация обложки по названию занятия.')

async def generate_course_description(update: Update, context: CallbackContext) -> None:
    course_name = ' '.join(context.args)
    answer = GigaLogic.sent_message(f"Сформируй описание курса по названию. Название курса '{course_name}'.")
    await update.message.reply_text(answer)

async def generate_lesson_plan(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        await update.message.reply_text('Пожалуйста, укажите название курса и название занятия.')
        return
    course_name = context.args[0]
    lesson_name = ' '.join(context.args[1:])
    answer = GigaLogic.sent_message(f"Создай план занятия с названием {lesson_name} для курса {course_name}")
    await update.message.reply_text(answer)

async def generate_tests(update: Update, context: CallbackContext) -> None:
    lesson_name = ' '.join(context.args)
    answer = GigaLogic.sent_message(f"Создай тест на понимание материала для занятия с названием {lesson_name}")
    await update.message.reply_text(answer)

async def generate_lesson_cover(update: Update, context: CallbackContext) -> None:
    lesson_name = ' '.join(context.args)
    promt=f"Создай обложку для занятия с названием {lesson_name}"
    answer = Kandivsky.prints(promt)
    if answer:
        await update.message.reply_photo('image.jpg')
    else:
        await update.message.reply_text("Не удалось сгенерировать обложку. Попробуйте позже.")


def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate_course_description", generate_course_description))
    application.add_handler(CommandHandler("generate_lesson_plan", generate_lesson_plan))
    application.add_handler(CommandHandler("generate_tests", generate_tests))
    application.add_handler(CommandHandler("generate_lesson_cover", generate_lesson_cover))

    application.run_polling()

if __name__ == '__main__':
    main()
