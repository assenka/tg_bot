from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentTypes, Message
import os
import PyPDF2

from main import dp

@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    await message.answer("Please add your files and choose what would you like to do")

@dp.message_handler(commands = "help")
async def cmd_start(message: types.Message):
    await message.answer("You can merge or split your files. Just add your files and print '/run'")

@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    if document := message.document:
        await document.download(
            destination_dir="/home/asenka/Desktop/tg_bot")

def Merge():
    pdf_merger = PyPDF2.PdfFileMerger()
    for filename in os.listdir("documents"):
        pdf_file = open(os.path.join("documents", filename), "rb")
        pdf_merger.append(pdf_file)
        pdf_file.close()
        os.remove(os.path.join("documents", filename))
    pdf_file_merged = open(os.path.join("documents", 'merged_files.pdf'), "wb+")
    pdf_merger.write(pdf_file_merged)


def Split():
    os.mkdir("splitted_files")
    for filename in os.listdir("documents"):
        pdf_file = open(os.path.join("documents", filename), "rb")
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for i in range(pdf_reader.numPages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(i))
            output_file_name = f'{filename}_{i}.pdf'
            with open(output_file_name, "wb+") as output_file:
                pdf_writer.write(output_file)
            os.replace(output_file_name, f'splitted_files/{output_file_name}')

@dp.message_handler(commands = "run")
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)
    buttons = [
        types.InlineKeyboardButton(text="merge", callback_data="to_merge"),
        types.InlineKeyboardButton(text="split", callback_data="to_split"),]
    keyboard.add(*buttons)
    await message.answer("What would you like to do?", reply_markup=keyboard)

@dp.callback_query_handler(Text(startswith="to_"))
async def callbacks_to(call: types.CallbackQuery):
    await call.message.answer(text="What would you like to do?")
    action = call.data.split("_")[1]

    if action == "merge":
        await call.message.answer(text="Files were merged successfully")
        Merge()
        await call.message.answer_document(open("/home/asenka/Desktop/tg_bot/documents/merged_files.pdf", "rb"))

    elif action == "split":
        await call.message.answer(text="Files were splitted successfully")
        Split()
        for filename in os.listdir("splitted_files"):
            pdf_file = open(os.path.join("splitted_files", filename), "rb")
            await call.message.answer_document(pdf_file)



