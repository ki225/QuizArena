import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 使用 frontend 模塊中的 app
from frontend import app

class TestKahootFrontend(unittest.TestCase):
    
    def setUp(self):
        # 測試前重置全局變量
        app.user_token = None
        app.game_id = None
        app.question_id = None
        app.BASE_URL = "http://mockapi:8000"  # 測試用 URL
    
    @patch('requests.post')
    def test_register_user_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user_id": 123, "token": "test-token-123"}
        mock_post.return_value = mock_response
        
        result = app.register_user("testuser", "password123")
        
        self.assertIn("註冊成功", result)
        self.assertIn("123", str(result))
        self.assertIn("test-token-123", result)
        self.assertEqual(app.user_token, "test-token-123")
        
        mock_post.assert_called_once_with(
            f"{app.BASE_URL}/users/register", 
            json={"username": "testuser", "password": "password123"}
        )
    
    @patch('requests.post')
    def test_register_user_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "用戶名已存在"}
        mock_post.return_value = mock_response
        
        result = app.register_user("existinguser", "password123")
        
        self.assertIn("註冊失敗", result)
        self.assertIn("用戶名已存在", result)
    
    @patch('requests.post')
    def test_join_game_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"session_id": "sess-xyz-123"}
        mock_post.return_value = mock_response
        
        result = app.join_game("456", "game-789")
        
        self.assertIn("成功加入遊戲", result)
        self.assertIn("game-789", result)
        self.assertIn("sess-xyz-123", result)
        self.assertEqual(app.game_id, "game-789")
        
        mock_post.assert_called_once_with(
            f"{app.BASE_URL}/games/game-789/join", 
            json={"user_id": "456"}
        )
    
    @patch('requests.get')
    def test_get_question(self, mock_get):
        app.game_id = "game-789"
        app.question_id = "q-123"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "q-123",
            "question": "什麼是 Docker?",
            "options": ["容器化平台", "電子郵件服務", "社交媒體應用", "文件存儲系統"]
        }
        mock_get.return_value = mock_response
        
        result = app.get_question()
        
        self.assertIn("什麼是 Docker?", result)
        self.assertIn("容器化平台", result)
        self.assertIn("電子郵件服務", result)
        
        mock_get.assert_called_once_with(f"{app.BASE_URL}/games/game-789/questions/q-123")
    
    @patch('requests.post')
    def test_submit_answer(self, mock_post):
        app.game_id = "game-789"
        app.question_id = "q-123"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "correct": True,
            "current_score": 100
        }
        mock_post.return_value = mock_response
        
        result = app.submit_answer("player-456", "容器化平台")
        
        self.assertIn("答案提交成功", result)
        self.assertIn("正確: True", result)
        self.assertIn("當前分數: 100", result)
        
        mock_post.assert_called_once_with(
            f"{app.BASE_URL}/games/game-789/questions/q-123/answer",
            json={"player_id": "player-456", "selected_option": "容器化平台"}
        )

class TestGradioInterface(unittest.TestCase):
    @patch('gradio.Blocks.launch')
    def test_gradio_interface_structure(self, mock_launch):
        # 需要以特殊方式處理，因為直接導入 app 時 launch 可能已經被調用
        self.assertTrue(hasattr(app, 'demo'))

if __name__ == '__main__':
    unittest.main()