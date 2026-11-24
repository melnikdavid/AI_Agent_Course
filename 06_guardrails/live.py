from agent import run
from llm import chat
from tools import TOOLS

print(run("Research solar", chat, TOOLS))
