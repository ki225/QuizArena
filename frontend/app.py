import gradio as gr
import requests

# 後端 API 基本 URL
BASE_URL = "http://127.0.0.1:8000"

# 全局變數
user_token = None
game_id = None
question_id = None

# 註冊用戶
def register_user(username, password):
    global user_token
    try:
        response = requests.post(f"{BASE_URL}/users/register", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            user_token = data["token"]
            return f"註冊成功！用戶 ID: {data['user_id']}, Token: {user_token}"
        else:
            return f"註冊失敗: {response.json().get('detail', '未知錯誤')}"
    except Exception as e:
        return f"註冊失敗: {str(e)}"

# 加入遊戲
def join_game(user_id, game_id_input):
    global game_id
    try:
        response = requests.post(f"{BASE_URL}/games/{game_id_input}/join", json={"user_id": user_id})
        if response.status_code == 200:
            game_id = game_id_input
            return f"成功加入遊戲！遊戲 ID: {game_id}, Session ID: {response.json()['session_id']}"
        else:
            return f"加入遊戲失敗: {response.json().get('detail', '未知錯誤')}"
    except Exception as e:
        return f"加入遊戲失敗: {str(e)}"

# 獲取問題
def get_question():
    global question_id
    try:
        response = requests.get(f"{BASE_URL}/games/{game_id}/questions/{question_id}")
        if response.status_code == 200:
            data = response.json()
            question_id = data["id"]
            return f"題目: {data['question']}\n選項: {', '.join(data['options'])}"
        else:
            return f"獲取題目失敗: {response.json().get('detail', '未知錯誤')}"
    except Exception as e:
        return f"獲取題目失敗: {str(e)}"

# 提交答案
def submit_answer(player_id, selected_option):
    try:
        response = requests.post(
            f"{BASE_URL}/games/{game_id}/questions/{question_id}/answer",
            json={"player_id": player_id, "selected_option": selected_option}
        )
        if response.status_code == 200:
            data = response.json()
            return f"答案提交成功！正確: {data['correct']}, 當前分數: {data['current_score']}"
        else:
            return f"提交答案失敗: {response.json().get('detail', '未知錯誤')}"
    except Exception as e:
        return f"提交答案失敗: {str(e)}"

# Gradio 介面
with gr.Blocks() as demo:
    gr.Markdown("# 遊戲前端介面")
    
    # 註冊用戶
    with gr.Row():
        username = gr.Textbox(label="用戶名")
        password = gr.Textbox(label="密碼", type="password")
        register_btn = gr.Button("註冊")
        register_output = gr.Textbox(label="註冊結果")
        register_btn.click(register_user, inputs=[username, password], outputs=register_output)
    
    # 加入遊戲
    with gr.Row():
        user_id = gr.Textbox(label="用戶 ID")
        game_id_input = gr.Textbox(label="遊戲 ID")
        join_btn = gr.Button("加入遊戲")
        join_output = gr.Textbox(label="加入結果")
        join_btn.click(join_game, inputs=[user_id, game_id_input], outputs=join_output)
    
    # 獲取問題
    with gr.Row():
        get_question_btn = gr.Button("獲取題目")
        question_output = gr.Textbox(label="題目內容")
        get_question_btn.click(get_question, outputs=question_output)
    
    # 提交答案
    with gr.Row():
        player_id = gr.Textbox(label="玩家 ID")
        selected_option = gr.Textbox(label="選擇的答案")
        submit_btn = gr.Button("提交答案")
        submit_output = gr.Textbox(label="提交結果")
        submit_btn.click(submit_answer, inputs=[player_id, selected_option], outputs=submit_output)

# 啟動 Gradio 介面
demo.launch()