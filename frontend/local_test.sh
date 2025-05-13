docker build -t kahoot-gradio-frontend:latest .

docker run -p 7860:7860 kahoot-gradio-frontend:latest

# then visit http://localhost:7860