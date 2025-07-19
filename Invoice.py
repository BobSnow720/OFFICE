import pdfplumber
import re
import os
import wx
from pathlib import Path

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="主公，请输入发票文件夹地址", size=(400, 130))
        # 创建一个面板（容器）
        panel = wx.Panel(self)
        # 创建一个垂直布局管理器
        sizer = wx.BoxSizer(wx.VERTICAL)
        # 添加文本输入框
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 10)  # 边距10像素
        # 添加按钮
        my_btn = wx.Button(panel, label="打工人互助魔法开启！")
        my_btn.Bind(wx.EVT_BUTTON, self.list_all_files)  # 绑定按钮点击事件
        sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 10)
        # 设置面板布局
        panel.SetSizer(sizer)
        # 显示窗口
        self.Show()

    def extract_invoice_number_plumber(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            # 正则匹配发票号码
            invoice_pattern = r"(?:发票号码|发票号|号码)[：:\s]*([A-Za-z0-9]+)"
            match = re.search(invoice_pattern, text)
            return match.group(1) if match else 'Fail'

    def list_all_files(self, event):
        directory = Path(self.text_ctrl.GetValue())
        SuccessInfo = ''
        FailInfo = ''
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                invoice_number = self.extract_invoice_number_plumber(file_path)
                # print(file_path)  # 打印文件完整路径
                # print("提取的发票号码:", invoice_number)
                if invoice_number == 'Fail':
                    FailInfo = FailInfo + file_path + '\n'
                else:
                    SuccessInfo = SuccessInfo + invoice_number + ';'
        with open('提取出来的发票号码.txt', 'w', encoding='utf-8') as file:
            file.write(SuccessInfo + '\n' + FailInfo)
            # print('文件创建成功')

if __name__ == "__main__":
    app = wx.App()  # 创建应用对象
    frame = MyFrame()  # 创建主窗口
    app.MainLoop()  # 进入事件循环