1. 使用者註冊
   - 方法：POST
   - 路徑：/users/register
   - 功能說明：用戶註冊，建立帳號與基本資料。
   - 回傳：用戶 ID、認證 token（如 JWT）。
   - 備註：若系統允許匿名或免註冊進入，可視專案需求調整。
2. 使用者設定名稱
   - 方法：PUT 或 PATCH
   - 路徑：/users/{user_id}/nickname
   - 請求體：{ "nickname": "新暱稱" }
   - 備註
     - 此 API 讓用戶更新顯示名稱，方便辨識。
     - 若註冊時已設定名稱，可視為後續修改。
3. 使用者進入答題介面
   - 方法：POST
   - 路徑：/games/{game_id}/join
   - 功能說明：用戶加入指定遊戲，開始答題。
   - 回傳：遊戲房間狀態、用戶在遊戲中的唯一識別（如 session ID）。
   - 備註
     - 可在此階段檢查用戶權限、遊戲狀態。
     - 合併「使用者進入答題介面」與「加入遊戲」概念。
4. 發布題目
   - 方法：POST
   - 路徑：/games/{game_id}/questions
   - 功能說明：主持人發布新題目給遊戲房間。
   - 請求體：題目內容、選項、答題時間等。
   - 備註
     - 可搭配 WebSocket 推送即時題目給玩家。
5. 退出遊戲
   - 方法：POST 或 DELETE
   - 路徑：/games/{game_id}/players/{player_id}/leave
   - 功能說明：用戶離開遊戲房間。
   - 備註
     - 建議使用 DELETE 表示刪除該用戶在遊戲中的連線狀態。
6. 答題並提交（選擇選項）
   - 方法：POST
   - 路徑：/games/{game_id}/questions/{question_id}/answer
   - 請求體：{ "player_id": "...", "selected_option": "A" }
   - 備註
     - 伺服器可即時計算分數，並透過 WebSocket 推送結果。