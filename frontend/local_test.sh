#!/bin/bash

echo "======================================================"
echo "開始構建 Docker 映像..."
echo "======================================================"
docker build -t kahoot-gradio-frontend:latest .

echo "======================================================"
echo "啟動容器..."
echo "======================================================"

docker rm -f kahoot-frontend 2>/dev/null || true
docker run -d -p 7860:7860 --name kahoot-frontend kahoot-gradio-frontend:latest

echo "======================================================"
echo "容器已成功啟動!"
echo "請在瀏覽器中訪問: http://localhost:7860"
echo "使用 Docker Desktop 時，Windows 與 WSL 都可通過 localhost 訪問"
echo ""
echo "查看容器日誌:"
echo "docker logs -f kahoot-frontend"
echo ""
echo "停止容器:"
echo "docker stop kahoot-frontend"
echo "======================================================"

docker logs -f kahoot-frontend