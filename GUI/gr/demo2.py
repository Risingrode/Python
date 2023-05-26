import os

import gradio as gr

proxy = "127.0.0.1"
port = 8080


# 设置代理
def start_capture(nothing):
    os.system('networksetup -setwebproxy Wi-Fi ' + proxy + ' ' + str(port))
    os.system('networksetup -setsecurewebproxy Wi-Fi ' + proxy + ' ' + str(port))
    # 进行抓包，做一些你想要做的事情
    os.system('nohup mitmweb -s example.py & echo $! > pid')
    print("===start_capture successful===")


# 取消代理
def stop_capture(nothing):
    os.system('networksetup -setwebproxystate "Wi-Fi" off')
    os.system('networksetup -setsecurewebproxystate "Wi-Fi" off')
    print("===stop_capture succeeded===")


def proxy_off(nothing):
    os.system('networksetup -setwebproxystate "Wi-Fi" off')
    os.system('networksetup -setsecurewebproxystate "Wi-Fi" off')
    print("===proxy_off succeeded===")


def api_capture_tab():
    with gr.Tab("API Capture"):
        with gr.Row():
            with gr.Column(scale=6):
                inp = gr.Textbox(placeholder="输入本次录制接口访问名称,例如：http://www.baidu.com", show_label=True)
            with gr.Column(scale=4):
                capture_btn = gr.Button("开始录制接口访问-API Capture", variant="primary")
                stop_capture_btn = gr.Button("停止录制接口访问-Stop API Capture", variant="primary")
                reset_proxy = gr.Button("重置MAC代理-Reset MAC Proxy Setting", variant="primary")
                capture_btn.click(fn=start_capture, inputs=inp)
                stop_capture_btn.click(fn=stop_capture)
                reset_proxy.click(fn=proxy_off)


# def init_ui():
#     with gr.Blocks() as demo:
#         gr.Markdown("# QA toolkits")
#         api_capture_tab()
#         # code_generate_tab()

#     demo.launch()
# if __name__ == '__main__':
#     init_ui()


#   另外一种写法
with gr.Blocks() as demo:
    gr.Markdown("# QA toolkits")
    api_capture_tab()
    # code_generate_tab()

demo.launch()

# gradio app.py    修改代码，页面随之改变