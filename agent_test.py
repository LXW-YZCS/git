import os
import base64
from openai import OpenAI

# ----------------------1. 将本地图片转为base64----------------------
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf‑8")

img_path=r"C:\Users\34195\Pictures\微信图片_20260710193129_75_70.png"
# 这里填写你的截图本地路径
img_base64 = image_to_base64(img_path)

system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double‑click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple‑click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double‑click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function‑name>, "arguments": <args‑json‑object>}
</tool_call>

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function‑name>, "arguments": <args‑json‑object>}.

Rules:
- Output exactly in the order: Action, <tool_call>.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call."""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": [
            # ==========改动：传入base64图片，不再使用网络URL==========
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
            {"type": "text", "text": "帮我打开QQ"}
        ]
    }
]

client = OpenAI(
    api_key="sk-ws-H.EMYDRIY.LKXk.MEQCIHcRbphIPpP-3_p14Mqn4nVfuEWN18kjZHITr5CIw3DTAiAfR-l69yuo038B1EqesiTiupFSriSJUX-MjCj5L6gGDg",
    base_url="https://ws-fn7n3o88qht5l67h.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="gui-plus-2026-02-26", # 如果你调用标准千问多模态模型改为 "qwen-vl-max"
    messages=messages,
    extra_body={"vl_high_resolution_images": True}
)

print(completion.choices[0].message.content)
