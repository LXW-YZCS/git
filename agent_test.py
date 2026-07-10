# ...existing code...
import requests, base64, json, time
import pyautogui
from PIL import Image
import io

API_URL = "https://api.example.com/v1/chat/completions"  # 替换为厂商 HTTP 接口
API_KEY = "ark-9d2782ea-9e2c-4286-9abf-a853305a5f1a-ca84d"
MODEL = "ep-20260709234613-sh8tg"  # 或 doubao 支持图像的模型名

def image_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def send_model_request(prompt, image_b64):
    functions = [
        {
            "name": "click_ui",
            "description": "在屏幕上点击一个 UI 元素",
            "parameters": {
                "type": "object",
                "properties": {
                    "method": {"type": "string", "enum": ["by_coords", "by_template", "by_text"]},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "template_b64": {"type": "string"},
                    "text": {"type": "string"}
                },
                "required": ["method"]
            }
        }
    ]
    # 下面 payload 根据目标厂商接口调整字段（示例通用结构）
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "user", "name": "screenshot", "content": image_b64}
        ],
        "functions": functions,
        "function_call": "auto"
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def dispatch_function(call):
    # call: {"name": "...", "arguments": "json-string"}
    name = call.get("name")
    args = {}
    if "arguments" in call and call["arguments"]:
        try:
            args = json.loads(call["arguments"])
        except:
            args = {}
    if name == "click_ui":
        click_ui(args)
    else:
        print("未知工具：", name)

def click_ui(args):
    method = args.get("method")
    if method == "by_coords":
        x = int(args.get("x", 0)); y = int(args.get("y", 0))
        pyautogui.click(x, y)
    elif method == "by_template":
        tpl_b64 = args.get("template_b64")
        if not tpl_b64:
            return
        tpl = Image.open(io.BytesIO(base64.b64decode(tpl_b64)))
        tpl.save("tpl.png")
        loc = pyautogui.locateOnScreen("tpl.png", confidence=0.8)
        if loc:
            cx, cy = pyautogui.center(loc)
            pyautogui.click(cx, cy)
    elif method == "by_text":
        # 简单示例：通过 OCR/额外工具定位，这里只示意
        print("by_text 未实现，需要 OCR 支持")
    else:
        print("未知点击方法:", method)

def run_example():
    screenshot_path = "screen.png"
    # 截图（也可以用外部工具截取再保存）
    pyautogui.screenshot(screenshot_path)
    img_b64 = image_to_b64(screenshot_path)
    prompt = "请在截图中找到并点击界面上的“确定”按钮。"
    resp = send_model_request(prompt, img_b64)
    # 根据厂商返回结构调整下面的解析
    # 这里假定 resp['choices'][0]['message']['function_call']
    fc = None
    try:
        fc = resp["choices"][0]["message"].get("function_call")
    except:
        pass
    if fc:
        dispatch_function(fc)
    else:
        print("模型未返回工具调用：", resp)

if __name__ == "__main__":
    run_example()
# ...existing code...