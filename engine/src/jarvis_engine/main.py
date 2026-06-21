import asyncio
import threading
import json
import sys
import traceback
from pathlib import Path

import sounddevice as sd
from google import genai
from google.genai import types
import websockets

class HeadlessUI:
    def __init__(self):
        self.muted = True
        self.current_file = None
        self.voice = "Charon"
        self.temperature = 0.7
        self.max_tokens = 2048
        self.on_text_command = None
        self._state = "INITIALISING"
        self._websockets = set()
        self.api_key_future = asyncio.get_running_loop().create_future()
        
    async def wait_for_api_key(self):
        return await self.api_key_future
        
    def set_state(self, state: str):
        self._state = state
        self.broadcast(json.dumps({"type": "state", "value": state}))

    def write_log(self, text: str):
        self.broadcast(json.dumps({"type": "log", "value": text}))

    def broadcast(self, message):
        for ws in list(self._websockets):
            try:
                asyncio.run_coroutine_threadsafe(ws.send(message), ws.loop)
            except:
                pass

    async def handle_client(self, websocket):
        self._websockets.add(websocket)
        websocket.loop = asyncio.get_running_loop()
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["type"] == "text_command" and self.on_text_command:
                    self.on_text_command(data["value"])
                elif data["type"] == "set_muted":
                    self.muted = data["value"]
                elif data["type"] == "set_file":
                    self.current_file = data["value"]
                elif data["type"] == "set_voice":
                    self.voice = data["value"]
                elif data["type"] == "set_temperature":
                    self.temperature = float(data["value"])
                elif data["type"] == "set_max_tokens":
                    self.max_tokens = int(data["value"])
                elif data["type"] == "api_key":
                    try:
                        API_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
                        with open(API_CONFIG_PATH, "w", encoding="utf-8") as f:
                            json.dump({"gemini_api_key": data["value"]}, f)
                    except Exception as e:
                        pass
                        
                    if not self.api_key_future.done():
                        self.api_key_future.set_result(data["value"])
        finally:
            self._websockets.remove(websocket)
            if not self._websockets:
                self.muted = True

from jarvis_engine.memory.memory_manager import (
    load_memory, update_memory, format_memory_for_prompt,
    should_extract_memory, extract_memory
)

from jarvis_engine.actions.file_and_document_management.file_processor import file_processor
from jarvis_engine.actions.information_and_research.flight_finder import flight_finder
from jarvis_engine.actions.computer_and_system_control.open_app import open_app
from jarvis_engine.actions.information_and_research.weather_report import weather_action
from jarvis_engine.actions.creative_and_content.send_message import send_message
from jarvis_engine.actions.scheduling_and_productivity.reminder import reminder
from jarvis_engine.actions.computer_and_system_control.computer_settings import computer_settings
from jarvis_engine.actions.computer_and_system_control.screen_processor import screen_process
from jarvis_engine.actions.web_and_browser_automation.youtube_video import youtube_video
from jarvis_engine.actions.computer_and_system_control.desktop import desktop_control
from jarvis_engine.actions.web_and_browser_automation.browser_control import browser_control
from jarvis_engine.actions.file_and_document_management.file_controller import file_controller
from jarvis_engine.actions.coding_and_development.code_helper import code_helper
from jarvis_engine.actions.ai_agent_capabilities.dev_agent import dev_agent
from jarvis_engine.actions.information_and_research.web_search import web_search as web_search_action
from jarvis_engine.actions.computer_and_system_control.computer_control import computer_control
from jarvis_engine.actions.computer_and_system_control.game_updater import game_updater
from jarvis_engine.actions.coding_and_development.terminal_execute import terminal_execute
from jarvis_engine.actions.information_and_research.rag_ingest import ingest_folder
from jarvis_engine.actions.information_and_research.rag_search import semantic_search
from jarvis_engine.actions.data_and_analytics.analytics import data_analytics
from jarvis_engine.actions.scheduling_and_productivity.todo_manager import todo_manager
from jarvis_engine.actions.file_and_document_management.document_generator import document_generator
from jarvis_engine.actions.information_and_research.search_knowledge_base import search_knowledge_base
from jarvis_engine.actions.data_and_analytics.chart_generator import chart_generator
from jarvis_engine.actions.coding_and_development.code_reviewer import code_reviewer
from jarvis_engine.actions.ai_agent_capabilities.task_executor import task_executor
from jarvis_engine.actions.data_and_analytics.sentiment_analyzer import sentiment_analyzer
from jarvis_engine.actions.information_and_research.summarize_documents import summarize_documents
from jarvis_engine.actions.information_and_research.translate_languages import translate_languages
from jarvis_engine.actions.information_and_research.fact_check import fact_check
from jarvis_engine.actions.information_and_research.compile_reports import compile_reports


from jarvis_engine.actions.information_and_research.extract_spreadsheet_data import extract_spreadsheet_data
from jarvis_engine.actions.information_and_research.extract_structured_data import extract_structured_data
from jarvis_engine.actions.information_and_research.generate_research_briefs import generate_research_briefs
from jarvis_engine.actions.information_and_research.summarize_articles import summarize_articles
from jarvis_engine.actions.information_and_research.synthesize_information import synthesize_information
from jarvis_engine.actions.scheduling_and_productivity.alarm_manager import alarm_manager
from jarvis_engine.actions.scheduling_and_productivity.productivity_tracker import productivity_tracker
from jarvis_engine.actions.scheduling_and_productivity.reminder_manager import reminder_manager
from jarvis_engine.actions.scheduling_and_productivity.task_manager import task_manager
from jarvis_engine.actions.web_and_browser_automation.website_navigator import website_navigator
from jarvis_engine.actions.web_and_browser_automation.website_search import website_search
from jarvis_engine.actions.web_and_browser_automation.web_data_extractor import web_data_extractor

from jarvis_engine.actions.ai_agent_capabilities.autonomous_coder import autonomous_coder
from jarvis_engine.actions.ai_agent_capabilities.context_manager import context_manager
from jarvis_engine.actions.ai_agent_capabilities.memory_manager import memory_manager
from jarvis_engine.actions.ai_agent_capabilities.planner import planner
from jarvis_engine.actions.ai_agent_capabilities.tool_manager import tool_manager
from jarvis_engine.actions.ai_agent_capabilities.tool_orchestrator import tool_orchestrator
from jarvis_engine.actions.coding_and_development.automation_script_creator import automation_script_creator
from jarvis_engine.actions.coding_and_development.code_generator import code_generator
from jarvis_engine.actions.coding_and_development.code_optimizer import code_optimizer
from jarvis_engine.actions.coding_and_development.code_writer import code_writer
from jarvis_engine.actions.coding_and_development.debugger import debugger
from jarvis_engine.actions.coding_and_development.documentation_generator import documentation_generator
from jarvis_engine.actions.coding_and_development.error_fixer import error_fixer
from jarvis_engine.actions.coding_and_development.refactor_engine import refactor_engine
from jarvis_engine.actions.coding_and_development.reverse_engineering import reverse_engineering
from jarvis_engine.actions.coding_and_development.unit_test_generator import unit_test_generator
from jarvis_engine.actions.computer_and_system_control.app_launcher import app_launcher
from jarvis_engine.actions.computer_and_system_control.clipboard_manager import clipboard_manager
from jarvis_engine.actions.computer_and_system_control.command_executor import command_executor
from jarvis_engine.actions.computer_and_system_control.filesystem_controller import filesystem_controller
from jarvis_engine.actions.computer_and_system_control.file_system_control import file_system_control
from jarvis_engine.actions.computer_and_system_control.keyboard_controller import keyboard_controller
from jarvis_engine.actions.computer_and_system_control.mouse_controller import mouse_controller
from jarvis_engine.actions.computer_and_system_control.power_manager import power_manager
from jarvis_engine.actions.computer_and_system_control.screenshot_manager import screenshot_manager
from jarvis_engine.actions.computer_and_system_control.screen_analyzer import screen_analyzer
from jarvis_engine.actions.computer_and_system_control.volume_controller import volume_controller
from jarvis_engine.actions.creative_and_content.ad_copy_generator import ad_copy_generator
from jarvis_engine.actions.creative_and_content.article_writer import article_writer
from jarvis_engine.actions.creative_and_content.blog_writer import blog_writer
from jarvis_engine.actions.creative_and_content.marketing_copy_generator import marketing_copy_generator
from jarvis_engine.actions.creative_and_content.product_description_writer import product_description_writer
from jarvis_engine.actions.creative_and_content.script_writer import script_writer
from jarvis_engine.actions.creative_and_content.story_writer import story_writer
from jarvis_engine.actions.data_and_analytics.dataset_analyzer import dataset_analyzer
from jarvis_engine.actions.data_and_analytics.data_cleaner import data_cleaner
from jarvis_engine.actions.data_and_analytics.data_transformer import data_transformer
from jarvis_engine.actions.data_and_analytics.data_visualizer import data_visualizer
from jarvis_engine.actions.data_and_analytics.sql_query_engine import sql_query_engine
from jarvis_engine.actions.data_and_analytics.statistical_analysis import statistical_analysis
from jarvis_engine.actions.data_and_analytics.trend_forecaster import trend_forecaster
from jarvis_engine.actions.file_and_document_management.archive_compressor import archive_compressor
from jarvis_engine.actions.file_and_document_management.archive_extractor import archive_extractor
from jarvis_engine.actions.file_and_document_management.document_editor import document_editor
from jarvis_engine.actions.file_and_document_management.excel_manager import excel_manager
from jarvis_engine.actions.file_and_document_management.file_organizer import file_organizer
from jarvis_engine.actions.file_and_document_management.file_renamer import file_renamer
from jarvis_engine.actions.file_and_document_management.pdf_manager import pdf_manager
from jarvis_engine.actions.file_and_document_management.report_generator import report_generator
from jarvis_engine.actions.file_and_document_management.word_manager import word_manager
from jarvis_engine.actions.information_and_research.answer_questions import answer_questions
from jarvis_engine.actions.information_and_research.deep_research import deep_research
from jarvis_engine.actions.information_and_research.extract_pdf_data import extract_pdf_data

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


BASE_DIR        = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"
PROMPT_PATH     = BASE_DIR / "core" / "prompt.txt"
LIVE_MODEL          = "models/gemini-2.5-flash-native-audio-preview-12-2025"
CHANNELS            = 1
SEND_SAMPLE_RATE    = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE          = 1024


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def _load_system_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except Exception:
        return (
            "You are JARVIS, Tony Stark's AI assistant. "
            "Be concise, direct, and always use the provided tools to complete tasks. "
            "Never simulate or guess results — always call the appropriate tool."
        )
    
_last_memory_input = ""

def _update_memory_async(user_text: str, jarvis_text: str) -> None:
    global _last_memory_input

    user_text   = (user_text   or "").strip()
    jarvis_text = (jarvis_text or "").strip()

    if len(user_text) < 5 or user_text == _last_memory_input:
        return
    _last_memory_input = user_text

    try:
        api_key = _get_api_key()
        if not should_extract_memory(user_text, jarvis_text, api_key):
            return
        data = extract_memory(user_text, jarvis_text, api_key)
        if data:
            update_memory(data)
            print(f"[Memory] ✅ {list(data.keys())}")
    except Exception as e:
        if "429" not in str(e):
            print(f"[Memory] ⚠️ {e}")

TOOL_MAP = {
    "open_app": open_app,
    "web_search": web_search_action,
    "weather_report": weather_action,
    "send_message": send_message,
    "reminder": reminder,
    "youtube_video": youtube_video,
    "screen_process": screen_process,
    "computer_settings": computer_settings,
    "browser_control": browser_control,
    "file_controller": file_controller,
    "desktop_control": desktop_control,
    "code_helper": code_helper,
    "dev_agent": dev_agent,
    "computer_control": computer_control,
    "game_updater": game_updater,
    "terminal_execute": terminal_execute,
    "ingest_folder": ingest_folder,
    "semantic_search": semantic_search,
    "data_analytics": data_analytics,
    "todo_manager": todo_manager,
    "document_generator": document_generator,
    "search_knowledge_base": search_knowledge_base,
    "chart_generator": chart_generator,
    "code_reviewer": code_reviewer,
    "task_executor": task_executor,
    "sentiment_analyzer": sentiment_analyzer,
    "summarize_documents": summarize_documents,
    "translate_languages": translate_languages,
    "fact_check": fact_check,
    "compile_reports": compile_reports
}

TOOL_DECLARATIONS = [
    {
        "name": "open_app",
        "description": (
            "Opens any application on the Windows computer. "
            "Use this whenever the user asks to open, launch, or start any app, "
            "website, or program. Always call this tool — never just say you opened it."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "app_name": {
                    "type": "STRING",
                    "description": "Exact name of the application (e.g. 'WhatsApp', 'Chrome', 'Spotify')"
                }
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "web_search",
        "description": "Searches the web for any information.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query":  {"type": "STRING", "description": "Search query"},
                "mode":   {"type": "STRING", "description": "search (default) or compare"},
                "items":  {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Items to compare"},
                "aspect": {"type": "STRING", "description": "price | specs | reviews"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "weather_report",
        "description": "Gives the weather report to user",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "city": {"type": "STRING", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "send_message",
        "description": "Sends a text message via WhatsApp, Telegram, or other messaging platform.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "receiver":     {"type": "STRING", "description": "Recipient contact name"},
                "message_text": {"type": "STRING", "description": "The message to send"},
                "platform":     {"type": "STRING", "description": "Platform: WhatsApp, Telegram, etc."}
            },
            "required": ["receiver", "message_text", "platform"]
        }
    },
    {
        "name": "reminder",
        "description": "Sets a timed reminder using Windows Task Scheduler.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "date":    {"type": "STRING", "description": "Date in YYYY-MM-DD format"},
                "time":    {"type": "STRING", "description": "Time in HH:MM format (24h)"},
                "message": {"type": "STRING", "description": "Reminder message text"}
            },
            "required": ["date", "time", "message"]
        }
    },
    {
        "name": "youtube_video",
        "description": (
            "Controls YouTube. Use for: playing videos, summarizing a video's content, "
            "getting video info, or showing trending videos."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {"type": "STRING", "description": "play | summarize | get_info | trending (default: play)"},
                "query":  {"type": "STRING", "description": "Search query for play action"},
                "save":   {"type": "BOOLEAN", "description": "Save summary to Notepad (summarize only)"},
                "region": {"type": "STRING", "description": "Country code for trending e.g. TR, US"},
                "url":    {"type": "STRING", "description": "Video URL for get_info action"},
            },
            "required": []
        }
    },
    {
        "name": "screen_process",
        "description": (
            "Captures and analyzes the screen or webcam image. "
            "MUST be called when user asks what is on screen, what you see, "
            "analyze my screen, look at camera, etc. "
            "You have NO visual ability without this tool. "
            "After calling this tool, stay SILENT — the vision module speaks directly."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "angle": {"type": "STRING", "description": "'screen' to capture display, 'camera' for webcam. Default: 'screen'"},
                "text":  {"type": "STRING", "description": "The question or instruction about the captured image"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "computer_settings",
        "description": (
            "Controls the computer: volume, brightness, window management, keyboard shortcuts, "
            "typing text on screen, closing apps, fullscreen, dark mode, WiFi, restart, shutdown, "
            "scrolling, tab management, zoom, screenshots, lock screen, refresh/reload page. "
            "Use for ANY single computer control command. NEVER route to agent_task."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":      {"type": "STRING", "description": "The action to perform"},
                "description": {"type": "STRING", "description": "Natural language description of what to do"},
                "value":       {"type": "STRING", "description": "Optional value: volume level, text to type, etc."}
            },
            "required": []
        }
    },
    {
        "name": "browser_control",
        "description": (
            "Controls the web browser. Use for: opening websites, searching the web, "
            "clicking elements, filling forms, scrolling, any web-based task."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":      {"type": "STRING", "description": "go_to | search | click | type | scroll | fill_form | smart_click | smart_type | get_text | press | close"},
                "url":         {"type": "STRING", "description": "URL for go_to action"},
                "query":       {"type": "STRING", "description": "Search query for search action"},
                "selector":    {"type": "STRING", "description": "CSS selector for click/type"},
                "text":        {"type": "STRING", "description": "Text to click or type"},
                "description": {"type": "STRING", "description": "Element description for smart_click/smart_type"},
                "direction":   {"type": "STRING", "description": "up or down for scroll"},
                "key":         {"type": "STRING", "description": "Key name for press action"},
                "incognito":   {"type": "BOOLEAN", "description": "Open in private/incognito mode"},
            },
            "required": ["action"]
        }
    },
    {
        "name": "file_controller",
        "description": "Manages files and folders: list, create, delete, move, copy, rename, read, write, find, disk usage.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":      {"type": "STRING", "description": "list | create_file | create_folder | delete | move | copy | rename | read | write | find | largest | disk_usage | organize_desktop | info"},
                "path":        {"type": "STRING", "description": "File/folder path or shortcut: desktop, downloads, documents, home"},
                "destination": {"type": "STRING", "description": "Destination path for move/copy"},
                "new_name":    {"type": "STRING", "description": "New name for rename"},
                "content":     {"type": "STRING", "description": "Content for create_file/write"},
                "name":        {"type": "STRING", "description": "File name to search for"},
                "extension":   {"type": "STRING", "description": "File extension to search (e.g. .pdf)"},
                "count":       {"type": "INTEGER", "description": "Number of results for largest"},
            },
            "required": ["action"]
        }
    },
    {
        "name": "desktop_control",
        "description": "Controls the desktop: wallpaper, organize, clean, list, stats.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {"type": "STRING", "description": "wallpaper | wallpaper_url | organize | clean | list | stats | task"},
                "path":   {"type": "STRING", "description": "Image path for wallpaper"},
                "url":    {"type": "STRING", "description": "Image URL for wallpaper_url"},
                "mode":   {"type": "STRING", "description": "by_type or by_date for organize"},
                "task":   {"type": "STRING", "description": "Natural language desktop task"},
            },
            "required": ["action"]
        }
    },
    {
        "name": "code_helper",
        "description": "Writes, edits, explains, runs, or builds code files.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":      {"type": "STRING", "description": "write | edit | explain | run | build | auto (default: auto)"},
                "description": {"type": "STRING", "description": "What the code should do or what change to make"},
                "language":    {"type": "STRING", "description": "Programming language (default: python)"},
                "output_path": {"type": "STRING", "description": "Where to save the file"},
                "file_path":   {"type": "STRING", "description": "Path to existing file for edit/explain/run/build"},
                "code":        {"type": "STRING", "description": "Raw code string for explain"},
                "args":        {"type": "STRING", "description": "CLI arguments for run/build"},
                "timeout":     {"type": "INTEGER", "description": "Execution timeout in seconds (default: 30)"},
            },
            "required": ["action"]
        }
    },
    {
        "name": "dev_agent",
        "description": "Builds complete multi-file projects from scratch: plans, writes files, installs deps, opens VSCode, runs and fixes errors.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "description":  {"type": "STRING", "description": "What the project should do"},
                "language":     {"type": "STRING", "description": "Programming language (default: python)"},
                "project_name": {"type": "STRING", "description": "Optional project folder name"},
                "timeout":      {"type": "INTEGER", "description": "Run timeout in seconds (default: 30)"},
            },
            "required": ["description"]
        }
    },
    {
        "name": "agent_task",
        "description": (
            "Executes complex multi-step tasks requiring multiple different tools. "
            "Examples: 'research X and save to file', 'find and organize files'. "
            "DO NOT use for single commands. NEVER use for Steam/Epic — use game_updater."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "goal":     {"type": "STRING", "description": "Complete description of what to accomplish"},
                "priority": {"type": "STRING", "description": "low | normal | high (default: normal)"}
            },
            "required": ["goal"]
        }
    },
    {
        "name": "computer_control",
        "description": "Direct computer control: type, click, hotkeys, scroll, move mouse, screenshots, find elements on screen.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":      {"type": "STRING", "description": "type | smart_type | click | double_click | right_click | hotkey | press | scroll | move | copy | paste | screenshot | wait | clear_field | focus_window | screen_find | screen_click | random_data | user_data"},
                "text":        {"type": "STRING", "description": "Text to type or paste"},
                "x":           {"type": "INTEGER", "description": "X coordinate"},
                "y":           {"type": "INTEGER", "description": "Y coordinate"},
                "keys":        {"type": "STRING", "description": "Key combination e.g. 'ctrl+c'"},
                "key":         {"type": "STRING", "description": "Single key e.g. 'enter'"},
                "direction":   {"type": "STRING", "description": "up | down | left | right"},
                "amount":      {"type": "INTEGER", "description": "Scroll amount (default: 3)"},
                "seconds":     {"type": "NUMBER",  "description": "Seconds to wait"},
                "title":       {"type": "STRING",  "description": "Window title for focus_window"},
                "description": {"type": "STRING",  "description": "Element description for screen_find/screen_click"},
                "type":        {"type": "STRING",  "description": "Data type for random_data"},
                "field":       {"type": "STRING",  "description": "Field for user_data: name|email|city"},
                "clear_first": {"type": "BOOLEAN", "description": "Clear field before typing (default: true)"},
                "path":        {"type": "STRING",  "description": "Save path for screenshot"},
            },
            "required": ["action"]
        }
    },
    {
        "name": "game_updater",
        "description": (
            "THE ONLY tool for ANY Steam or Epic Games request. "
            "Use for: installing, downloading, updating games, listing installed games, "
            "checking download status, scheduling updates. "
            "ALWAYS call directly for any Steam/Epic/game request. "
            "NEVER use agent_task, browser_control, or web_search for Steam/Epic."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":    {"type": "STRING",  "description": "update | install | list | download_status | schedule | cancel_schedule | schedule_status (default: update)"},
                "platform":  {"type": "STRING",  "description": "steam | epic | both (default: both)"},
                "game_name": {"type": "STRING",  "description": "Game name (partial match supported)"},
                "app_id":    {"type": "STRING",  "description": "Steam AppID for install (optional)"},
                "hour":      {"type": "INTEGER", "description": "Hour for scheduled update 0-23 (default: 3)"},
                "minute":    {"type": "INTEGER", "description": "Minute for scheduled update 0-59 (default: 0)"},
                "shutdown_when_done": {"type": "BOOLEAN", "description": "Shut down PC when download finishes"},
            },
            "required": []
        }
    },
    {
        "name": "flight_finder",
        "description": "Searches Google Flights and speaks the best options.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "origin":      {"type": "STRING",  "description": "Departure city or airport code"},
                "destination": {"type": "STRING",  "description": "Arrival city or airport code"},
                "date":        {"type": "STRING",  "description": "Departure date (any format)"},
                "return_date": {"type": "STRING",  "description": "Return date for round trips"},
                "passengers":  {"type": "INTEGER", "description": "Number of passengers (default: 1)"},
                "cabin":       {"type": "STRING",  "description": "economy | premium | business | first"},
                "save":        {"type": "BOOLEAN", "description": "Save results to Notepad"},
            },
            "required": ["origin", "destination", "date"]
        }
    },
    {
    "name": "file_processor",
    "description": (
        "Processes any file that the user has uploaded or dropped onto the interface. "
        "Use this when the user refers to an uploaded file and wants an action on it. "
        "Supports: images (describe/ocr/resize/compress/convert), "
        "PDFs (summarize/extract_text/to_word), "
        "Word docs & text files (summarize/fix/reformat/translate), "
        "CSV/Excel (analyze/stats/filter/sort/convert), "
        "JSON/XML (validate/format/analyze), "
        "code files (explain/review/fix/optimize/run/document/test), "
        "audio (transcribe/trim/convert/info), "
        "video (trim/extract_audio/extract_frame/compress/transcribe/info), "
        "archives (list/extract), "
        "presentations (summarize/extract_text). "
        "ALWAYS call this tool when a file has been uploaded and the user gives a command about it. "
        "If the user's command is ambiguous, pick the most logical action for that file type."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path": {
                "type": "STRING",
                "description": "Full path to the uploaded file. Leave empty to use the currently uploaded file."
            },
            "action": {
                "type": "STRING",
                "description": (
                    "What to do with the file. Examples by type:\n"
                    "image: describe | ocr | resize | compress | convert | info\n"
                    "pdf: summarize | extract_text | to_word | info\n"
                    "docx/txt: summarize | fix | reformat | translate_hint | word_count | to_bullet\n"
                    "csv/excel: analyze | stats | filter | sort | convert | info\n"
                    "json: validate | format | analyze | to_csv\n"
                    "code: explain | review | fix | optimize | run | document | test\n"
                    "audio: transcribe | trim | convert | info\n"
                    "video: trim | extract_audio | extract_frame | compress | transcribe | info | convert\n"
                    "archive: list | extract\n"
                    "pptx: summarize | extract_text | analyze"
                )
            },
            "instruction": {
                "type": "STRING",
                "description": "Free-form instruction if action doesn't cover it. E.g. 'translate this to Turkish', 'find all email addresses'"
            },
            "format": {
                "type": "STRING",
                "description": "Target format for conversion. E.g. 'mp3', 'pdf', 'csv', 'png'"
            },
            "width":     {"type": "INTEGER", "description": "Target width for image resize"},
            "height":    {"type": "INTEGER", "description": "Target height for image resize"},
            "scale":     {"type": "NUMBER",  "description": "Scale factor for image resize (e.g. 0.5)"},
            "quality":   {"type": "INTEGER", "description": "Quality 1-100 for image/video compress"},
            "start":     {"type": "STRING",  "description": "Start time for trim: seconds or HH:MM:SS"},
            "end":       {"type": "STRING",  "description": "End time for trim: seconds or HH:MM:SS"},
            "timestamp": {"type": "STRING",  "description": "Timestamp for video frame extraction HH:MM:SS"},
            "column":    {"type": "STRING",  "description": "Column name for CSV filter/sort"},
            "value":     {"type": "STRING",  "description": "Filter value for CSV filter"},
            "condition": {"type": "STRING",  "description": "Filter condition: equals|contains|gt|lt"},
            "ascending": {"type": "BOOLEAN", "description": "Sort order for CSV sort (default: true)"},
            "save":      {"type": "BOOLEAN", "description": "Save result to file (default: true)"},
            "destination": {"type": "STRING", "description": "Output folder for archive extract"},
        },
        "required": []
    }
},
    {
    "name": "shutdown_jarvis",
    "description": (
        "Shuts down the assistant completely. "
        "Call this when the user expresses intent to end the conversation, "
        "close the assistant, say goodbye, or stop Jarvis. "
        "The user can say this in ANY language."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
    }
    },
    {
        "name": "data_analytics",
        "description": "Analyzes data files (CSV, JSON, Excel), generates charts, and executes SQL queries.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":     {"type": "STRING", "description": "analyze | chart | sql"},
                "filepath":   {"type": "STRING", "description": "Path to the data file or database"},
                "query":      {"type": "STRING", "description": "SQL query string"},
                "chart_type": {"type": "STRING", "description": "bar | line | scatter | pie"},
                "x_col":      {"type": "STRING", "description": "Column for X axis"},
                "y_col":      {"type": "STRING", "description": "Column for Y axis"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "todo_manager",
        "description": "Manages a local to-do list / task database.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":   {"type": "STRING", "description": "add | remove | check | list | clear_completed"},
                "task":     {"type": "STRING", "description": "Description of the task to add"},
                "priority": {"type": "STRING", "description": "high | normal | low"},
                "task_id":  {"type": "INTEGER", "description": "ID of the task to remove or check off"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "document_generator",
        "description": "Generates Word documents, Excel spreadsheets, and PDFs from scratch.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action":   {"type": "STRING", "description": "word | excel | pdf"},
                "content":  {"type": "STRING", "description": "Text content to put in Word or PDF"},
                "data":     {"type": "STRING", "description": "JSON string of rows for Excel"},
                "filename": {"type": "STRING", "description": "Filename to save as (e.g. report.docx)"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "search_knowledge_base",
        "description": "Searches the global knowledge base (Wikipedia) for detailed information on any specific topic, entity, or historical event.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {"type": "STRING", "description": "The topic or entity to search for (e.g. 'Quantum Computing', 'Eiffel Tower')."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "chart_generator",
        "description": "Generates a beautiful data visualization (Bar, Line, Scatter, Pie, Histogram). The chart is saved to the storage directory.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "chart_type": {"type": "STRING", "description": "bar | line | scatter | pie | hist"},
                "filepath": {"type": "STRING", "description": "Optional: Path to CSV/JSON/Excel file"},
                "raw_data": {"type": "STRING", "description": "Optional: Raw JSON string of data (e.g. [{'x': 1, 'y': 2}, ...])"},
                "x_col": {"type": "STRING", "description": "Name of the X-axis column"},
                "y_col": {"type": "STRING", "description": "Name of the Y-axis column (can be comma-separated for multiple lines/bars)"},
                "title": {"type": "STRING", "description": "Title of the chart"}
            },
            "required": ["chart_type"]
        }
    },
    {
        "name": "code_reviewer",
        "description": "Performs a strict, comprehensive code review of a file or code snippet using AI. Returns a structured markdown report identifying bugs, performance bottlenecks, and style issues.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "file_path": {"type": "STRING", "description": "Absolute path to the file to review (optional if code is provided)"},
                "code": {"type": "STRING", "description": "Raw string of the code to review (optional if file_path is provided)"},
                "language": {"type": "STRING", "description": "Programming language (e.g. 'python', 'typescript')"}
            },
            "required": []
        }
    },
    {
        "name": "task_executor",
        "description": "Acts as an AI Orchestrator to break down a high-level goal into a logical sequence of actionable subtasks. Saves an execution plan to storage.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "goal": {"type": "STRING", "description": "The high-level goal or objective to break down"}
            },
            "required": ["goal"]
        }
    },
    {
        "name": "sentiment_analyzer",
        "description": "Analyzes the emotional tone and sentiment of a provided text block or file. Returns a structured NLP report.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING", "description": "The raw text to analyze (optional if file_path provided)"},
                "file_path": {"type": "STRING", "description": "Absolute path to a text document to analyze (optional if text provided)"}
            },
            "required": []
        }
    },
    {
        "name": "summarize_documents",
        "description": "Summarizes a document or raw text. Returns a short, medium, or long summary and saves it to storage if a file path was provided.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING", "description": "The raw text to summarize (optional if file_path provided)"},
                "file_path": {"type": "STRING", "description": "Absolute path to a text document to summarize (optional if text provided)"},
                "length": {"type": "STRING", "description": "short | medium | long (default: medium)"}
            },
            "required": []
        }
    },
    {
        "name": "translate_languages",
        "description": "Translates a text block or file into any specified target language.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "text": {"type": "STRING", "description": "The raw text to translate (optional if file_path provided)"},
                "file_path": {"type": "STRING", "description": "Absolute path to a text document to translate (optional if text provided)"},
                "target_language": {"type": "STRING", "description": "The language to translate to (e.g. 'Spanish', 'Japanese')"}
            },
            "required": ["target_language"]
        }
    },
    {
        "name": "fact_check",
        "description": "Analyzes a claim or statement and returns a verdict on its accuracy, along with the facts and context.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "claim": {"type": "STRING", "description": "The specific claim or statement to fact-check"}
            },
            "required": ["claim"]
        }
    },
    {
        "name": "compile_reports",
        "description": "Compiles raw data and information into a highly professional, structured markdown report (Executive Summary, Background, Findings, Recommendations).",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "topic": {"type": "STRING", "description": "The main topic or title of the report"},
                "data": {"type": "STRING", "description": "Optional raw data, text, or context to base the report on"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "save_memory",
        "description": (
            "Save an important personal fact about the user to long-term memory. "
            "Call this silently whenever the user reveals something worth remembering: "
            "name, age, city, job, preferences, hobbies, relationships, projects, or future plans. "
            "Do NOT call for: weather, reminders, searches, or one-time commands. "
            "Do NOT announce that you are saving — just call it silently. "
            "Values must be in English regardless of the conversation language."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": (
                        "identity — name, age, birthday, city, job, language, nationality | "
                        "preferences — favorite food/color/music/film/game/sport, hobbies | "
                        "projects — active projects, goals, things being built | "
                        "relationships — friends, family, partner, colleagues | "
                        "wishes — future plans, things to buy, travel dreams | "
                        "notes — habits, schedule, anything else worth remembering"
                    )
                },
                "key":   {"type": "STRING", "description": "Short snake_case key (e.g. name, favorite_food, sister_name)"},
                "value": {"type": "STRING", "description": "Concise value in English (e.g. Fatih, pizza, older sister)"},
            },
            "required": ["category", "key", "value"]
        }
    },
]


class JarvisLive:

    def __init__(self, ui: HeadlessUI):
        self.ui             = ui
        self.session        = None
        self.audio_in_queue = None
        self.out_queue      = None
        self._loop          = None
        self._is_speaking   = False
        self._speaking_lock = threading.Lock()
        self.ui.on_text_command = self._on_text_command

    def _on_text_command(self, text: str):
        if not self._loop or not self.session:
            return
        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"parts": [{"text": text}]},
                turn_complete=True
            ),
            self._loop
        )

    def set_speaking(self, value: bool):
        with self._speaking_lock:
            self._is_speaking = value
        if value:
            self.ui.set_state("SPEAKING")
        elif not self.ui.muted:
            self.ui.set_state("LISTENING")

    def speak(self, text: str):
        if not self._loop or not self.session:
            return
        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"parts": [{"text": text}]},
                turn_complete=True
            ),
            self._loop
        )

    def speak_error(self, tool_name: str, error: str):
        short = str(error)[:120]
        self.ui.write_log(f"ERR: {tool_name} — {short}")
        self.speak(f"Sir, {tool_name} encountered an error. {short}")

    def _build_config(self) -> types.LiveConnectConfig:
        from datetime import datetime

        memory     = load_memory()
        mem_str    = format_memory_for_prompt(memory)
        sys_prompt = _load_system_prompt()

        now      = datetime.now()
        time_str = now.strftime("%A, %B %d, %Y — %I:%M %p")
        time_ctx = (
            f"[CURRENT DATE & TIME]\n"
            f"Right now it is: {time_str}\n"
            f"Use this to calculate exact times for reminders.\n\n"
        )

        parts = [time_ctx]
        if mem_str:
            parts.append(mem_str)
        parts.append(sys_prompt)

        return types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            output_audio_transcription={},
            input_audio_transcription={},
            system_instruction="\n".join(parts),
            tools=[{"function_declarations": TOOL_DECLARATIONS}],
            session_resumption=types.SessionResumptionConfig(),
            generation_config=types.GenerationConfig(
                temperature=self.ui.temperature,
                max_output_tokens=self.ui.max_tokens,
            ),
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.ui.voice
                    )
                )
            ),
        )

    async def _execute_tool(self, fc) -> types.FunctionResponse:
        name = fc.name
        args = dict(fc.args or {})

        print(f"[JARVIS] 🔧 {name}  {args}")
        self.ui.set_state("THINKING")
        if name == "save_memory":
            category = args.get("category", "notes")
            key      = args.get("key", "")
            value    = args.get("value", "")
            if key and value:
                update_memory({category: {key: {"value": value}}})
                print(f"[Memory] 💾 save_memory: {category}/{key} = {value}")
            if not self.ui.muted:
                self.ui.set_state("LISTENING")
            return types.FunctionResponse(
                id=fc.id, name=name,
                response={"result": "ok", "silent": True}
            )

        loop   = asyncio.get_event_loop()
        result = "Done."

        try:
            if name == "open_app":
                r = await loop.run_in_executor(None, lambda: open_app(parameters=args, response=None, player=self.ui))
                result = r or f"Opened {args.get('app_name')}."

            elif name == "weather_report":
                r = await loop.run_in_executor(None, lambda: weather_action(parameters=args, player=self.ui))
                result = r or "Weather delivered."

            elif name == "browser_control":
                r = await loop.run_in_executor(None, lambda: browser_control(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "search_knowledge_base":
                r = await loop.run_in_executor(None, lambda: search_knowledge_base(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "chart_generator":
                r = await loop.run_in_executor(None, lambda: chart_generator(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "code_reviewer":
                r = await loop.run_in_executor(None, lambda: code_reviewer(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "task_executor":
                r = await loop.run_in_executor(None, lambda: task_executor(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "sentiment_analyzer":
                r = await loop.run_in_executor(None, lambda: sentiment_analyzer(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "summarize_documents":
                r = await loop.run_in_executor(None, lambda: summarize_documents(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "translate_languages":
                r = await loop.run_in_executor(None, lambda: translate_languages(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "fact_check":
                r = await loop.run_in_executor(None, lambda: fact_check(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "compile_reports":
                r = await loop.run_in_executor(None, lambda: compile_reports(parameters=args, player=self.ui))
                result = r or "Done."


            elif name in ["extract_spreadsheet_data", "extract_structured_data", "generate_research_briefs", 
                          "summarize_articles", "synthesize_information", "alarm_manager", 
                          "productivity_tracker", "reminder_manager", "task_manager", 
                          "website_navigator", "website_search", "web_data_extractor"]:
                r = await loop.run_in_executor(None, lambda n=name: globals()[n](parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "autonomous_coder":
                r = await loop.run_in_executor(None, lambda: autonomous_coder(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "context_manager":
                r = await loop.run_in_executor(None, lambda: context_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "memory_manager":
                r = await loop.run_in_executor(None, lambda: memory_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "planner":
                r = await loop.run_in_executor(None, lambda: planner(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "tool_manager":
                r = await loop.run_in_executor(None, lambda: tool_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "tool_orchestrator":
                r = await loop.run_in_executor(None, lambda: tool_orchestrator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "automation_script_creator":
                r = await loop.run_in_executor(None, lambda: automation_script_creator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "code_generator":
                r = await loop.run_in_executor(None, lambda: code_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "code_optimizer":
                r = await loop.run_in_executor(None, lambda: code_optimizer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "code_writer":
                r = await loop.run_in_executor(None, lambda: code_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "debugger":
                r = await loop.run_in_executor(None, lambda: debugger(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "documentation_generator":
                r = await loop.run_in_executor(None, lambda: documentation_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "error_fixer":
                r = await loop.run_in_executor(None, lambda: error_fixer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "refactor_engine":
                r = await loop.run_in_executor(None, lambda: refactor_engine(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "reverse_engineering":
                r = await loop.run_in_executor(None, lambda: reverse_engineering(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "unit_test_generator":
                r = await loop.run_in_executor(None, lambda: unit_test_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "app_launcher":
                r = await loop.run_in_executor(None, lambda: app_launcher(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "clipboard_manager":
                r = await loop.run_in_executor(None, lambda: clipboard_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "command_executor":
                r = await loop.run_in_executor(None, lambda: command_executor(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "filesystem_controller":
                r = await loop.run_in_executor(None, lambda: filesystem_controller(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "file_system_control":
                r = await loop.run_in_executor(None, lambda: file_system_control(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "keyboard_controller":
                r = await loop.run_in_executor(None, lambda: keyboard_controller(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "mouse_controller":
                r = await loop.run_in_executor(None, lambda: mouse_controller(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "power_manager":
                r = await loop.run_in_executor(None, lambda: power_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "screenshot_manager":
                r = await loop.run_in_executor(None, lambda: screenshot_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "screen_analyzer":
                r = await loop.run_in_executor(None, lambda: screen_analyzer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "volume_controller":
                r = await loop.run_in_executor(None, lambda: volume_controller(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "ad_copy_generator":
                r = await loop.run_in_executor(None, lambda: ad_copy_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "article_writer":
                r = await loop.run_in_executor(None, lambda: article_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "blog_writer":
                r = await loop.run_in_executor(None, lambda: blog_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "marketing_copy_generator":
                r = await loop.run_in_executor(None, lambda: marketing_copy_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "product_description_writer":
                r = await loop.run_in_executor(None, lambda: product_description_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "script_writer":
                r = await loop.run_in_executor(None, lambda: script_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "story_writer":
                r = await loop.run_in_executor(None, lambda: story_writer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "dataset_analyzer":
                r = await loop.run_in_executor(None, lambda: dataset_analyzer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "data_cleaner":
                r = await loop.run_in_executor(None, lambda: data_cleaner(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "data_transformer":
                r = await loop.run_in_executor(None, lambda: data_transformer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "data_visualizer":
                r = await loop.run_in_executor(None, lambda: data_visualizer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "sql_query_engine":
                r = await loop.run_in_executor(None, lambda: sql_query_engine(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "statistical_analysis":
                r = await loop.run_in_executor(None, lambda: statistical_analysis(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "trend_forecaster":
                r = await loop.run_in_executor(None, lambda: trend_forecaster(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "archive_compressor":
                r = await loop.run_in_executor(None, lambda: archive_compressor(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "archive_extractor":
                r = await loop.run_in_executor(None, lambda: archive_extractor(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "document_editor":
                r = await loop.run_in_executor(None, lambda: document_editor(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "excel_manager":
                r = await loop.run_in_executor(None, lambda: excel_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "file_organizer":
                r = await loop.run_in_executor(None, lambda: file_organizer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "file_renamer":
                r = await loop.run_in_executor(None, lambda: file_renamer(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "pdf_manager":
                r = await loop.run_in_executor(None, lambda: pdf_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "report_generator":
                r = await loop.run_in_executor(None, lambda: report_generator(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "word_manager":
                r = await loop.run_in_executor(None, lambda: word_manager(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "answer_questions":
                r = await loop.run_in_executor(None, lambda: answer_questions(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "deep_research":
                r = await loop.run_in_executor(None, lambda: deep_research(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "extract_pdf_data":
                r = await loop.run_in_executor(None, lambda: extract_pdf_data(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "file_controller":
                r = await loop.run_in_executor(None, lambda: file_controller(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "send_message":
                r = await loop.run_in_executor(None, lambda: send_message(parameters=args, response=None, player=self.ui, session_memory=None))
                result = r or f"Message sent to {args.get('receiver')}."

            elif name == "reminder":
                r = await loop.run_in_executor(None, lambda: reminder(parameters=args, response=None, player=self.ui))
                result = r or "Reminder set."

            elif name == "youtube_video":
                r = await loop.run_in_executor(None, lambda: youtube_video(parameters=args, response=None, player=self.ui))
                result = r or "Done."
            elif name == "file_processor":
                if not args.get("file_path") and self.ui.current_file:
                    args["file_path"] = self.ui.current_file
                r = await loop.run_in_executor(
                    None,
                    lambda: file_processor(parameters=args, player=self.ui, speak=self.speak)
                )
                result = r or "Done."


            elif name == "screen_process":
                threading.Thread(
                    target=screen_process,
                    kwargs={"parameters": args, "response": None,
                            "player": self.ui, "session_memory": None},
                    daemon=True
                ).start()
                result = "Vision module activated. Stay completely silent — vision module will speak directly."

            elif name == "computer_settings":
                r = await loop.run_in_executor(None, lambda: computer_settings(parameters=args, response=None, player=self.ui))
                result = r or "Done."

            elif name == "desktop_control":
                r = await loop.run_in_executor(None, lambda: desktop_control(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "code_helper":
                r = await loop.run_in_executor(None, lambda: code_helper(parameters=args, player=self.ui, speak=self.speak))
                result = r or "Done."

            elif name == "data_analytics":
                r = await loop.run_in_executor(None, lambda: data_analytics(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "todo_manager":
                r = await loop.run_in_executor(None, lambda: todo_manager(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "document_generator":
                r = await loop.run_in_executor(None, lambda: document_generator(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "dev_agent":
                r = await loop.run_in_executor(None, lambda: dev_agent(parameters=args, player=self.ui, speak=self.speak))
                result = r or "Done."

            elif name == "agent_task":
                from jarvis_engine.agents.execution.task_queue import get_queue, TaskPriority
                priority_map = {"low": TaskPriority.LOW, "normal": TaskPriority.NORMAL, "high": TaskPriority.HIGH}
                priority = priority_map.get(args.get("priority", "normal").lower(), TaskPriority.NORMAL)
                task_id  = get_queue().submit(goal=args.get("goal", ""), priority=priority, speak=self.speak)
                result   = f"Task started (ID: {task_id})."

            elif name == "web_search":
                r = await loop.run_in_executor(None, lambda: web_search_action(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "computer_control":
                r = await loop.run_in_executor(None, lambda: computer_control(parameters=args, player=self.ui))
                result = r or "Done."

            elif name == "game_updater":
                r = await loop.run_in_executor(None, lambda: game_updater(parameters=args, player=self.ui, speak=self.speak))
                result = r or "Done."

            elif name == "flight_finder":
                r = await loop.run_in_executor(None, lambda: flight_finder(parameters=args, player=self.ui))
                result = r or "Done."
            elif name == "shutdown_jarvis":
                self.ui.write_log("SYS: Shutdown requested.")
                self.speak("Goodbye, sir.")

                def _shutdown():
                    import time, sys, os
                    time.sleep(1)
                    os._exit(0)

                threading.Thread(target=_shutdown, daemon=True).start()
            else:
                result = f"Unknown tool: {name}"

        except Exception as e:
            result = f"Tool '{name}' failed: {e}"
            traceback.print_exc()
            self.speak_error(name, e)

        if not self.ui.muted:
            self.ui.set_state("LISTENING")

        print(f"[JARVIS] 📤 {name} → {str(result)[:80]}")

        return types.FunctionResponse(
            id=fc.id, name=name,
            response={"result": result}
        )

    async def _send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send_realtime_input(media=msg)

    async def _listen_audio(self):
        print("[JARVIS] 🎤 Mic started")
        loop = asyncio.get_event_loop()

        def callback(indata, frames, time_info, status):
            with self._speaking_lock:
                jarvis_speaking = self._is_speaking
            if not jarvis_speaking and not self.ui.muted:
                data = indata.tobytes()
                
                def _enqueue():
                    try:
                        self.out_queue.put_nowait({"data": data, "mime_type": "audio/pcm"})
                    except asyncio.QueueFull:
                        pass
                
                loop.call_soon_threadsafe(_enqueue)

        try:
            with sd.InputStream(
                samplerate=SEND_SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16",
                blocksize=CHUNK_SIZE,
                callback=callback,
            ):
                print("[JARVIS] 🎤 Mic stream open")
                while True:
                    await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[JARVIS] ❌ Mic: {e}")
            raise

    async def _receive_audio(self):
        print("[JARVIS] 👂 Recv started")
        out_buf, in_buf = [], []

        try:
            while True:
                async for response in self.session.receive():

                    if response.data:
                        self.audio_in_queue.put_nowait(response.data)

                    if response.server_content:
                        sc = response.server_content

                        if sc.output_transcription and sc.output_transcription.text:
                            txt = sc.output_transcription.text
                            if txt:
                                out_buf.append(txt)

                        if sc.input_transcription and sc.input_transcription.text:
                            txt = sc.input_transcription.text
                            if txt:
                                in_buf.append(txt)

                        if sc.turn_complete:

                            full_in = "".join(in_buf).strip()
                            if full_in:
                                self.ui.write_log(f"You: {full_in}")
                            in_buf = []

                            full_out = "".join(out_buf).strip()
                            if full_out:
                                self.ui.write_log(f"Jarvis: {full_out}")
                            out_buf = []

                            if full_in and len(full_in) > 5:
                                threading.Thread(
                                    target=_update_memory_async,
                                    args=(full_in, full_out),
                                    daemon=True
                                ).start()

                    if response.tool_call:
                        fn_responses = []
                        for fc in response.tool_call.function_calls:
                            print(f"[JARVIS] 📞 {fc.name}")
                            fr = await self._execute_tool(fc)
                            fn_responses.append(fr)
                        await self.session.send_tool_response(
                            function_responses=fn_responses
                        )

        except Exception as e:
            print(f"[JARVIS] ❌ Recv: {e}")
            traceback.print_exc()
            raise

    async def _play_audio(self):
        print("[JARVIS] 🔊 Play started")
        loop = asyncio.get_event_loop()

        stream = sd.RawOutputStream(
            samplerate=RECEIVE_SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=CHUNK_SIZE,
        )
        stream.start()
        try:
            while True:
                try:
                    chunk = await asyncio.wait_for(self.audio_in_queue.get(), timeout=0.5)
                    self.set_speaking(True)
                    await asyncio.to_thread(stream.write, chunk)
                except asyncio.TimeoutError:
                    self.set_speaking(False)
                    chunk = await self.audio_in_queue.get()
                    self.set_speaking(True)
                    await asyncio.to_thread(stream.write, chunk)
        except Exception as e:
            print(f"[JARVIS] ❌ Play: {e}")
            raise
        finally:
            self.set_speaking(False)
            stream.stop()
            stream.close()

    async def run(self):
        api_key = await self.ui.wait_for_api_key()
        client = genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1alpha"}
        )
        config = self._build_config()

        while True:
            try:
                print("[JARVIS] 🔌 Connecting...")
                self.ui.set_state("THINKING")

                async with (
                    client.aio.live.connect(model=LIVE_MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session        = session
                    self._loop          = asyncio.get_event_loop()
                    self.audio_in_queue = asyncio.Queue()
                    self.out_queue      = asyncio.Queue(maxsize=10)

                    print("[JARVIS] ✅ Connected.")
                    self.ui.set_state("LISTENING")
                    self.ui.write_log("SYS: JARVIS online.")

                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    tg.create_task(self._play_audio())
                    
            except Exception as e:
                print(f"[JARVIS] ⚠️ {e}")
                traceback.print_exc()

            self.set_speaking(False)
            self.ui.set_state("THINKING")
            print("[JARVIS] 🔄 Reconnecting in 3s...")
            await asyncio.sleep(3)

async def main_server():
    ui = HeadlessUI()
    jarvis = JarvisLive(ui)
    
    # Start Jarvis loop
    asyncio.create_task(jarvis.run())
    
    print("[SERVER] Starting WebSocket server on ws://localhost:8765")
    # Start WebSocket server
    async with websockets.serve(ui.handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main_server())
    except KeyboardInterrupt:
        print("\n🔴 Shutting down...")
