import PyQt5.QtWidgets as qtWidgets

class LoginDialog(qtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("登录验证")
        self.setMinimumWidth(300)

        # 创建表单布局
        layout = qtWidgets.QFormLayout(self)

        # 创建用户名和密码输入框
        self.username_input = qtWidgets.QLineEdit()
        self.password_input = qtWidgets.QLineEdit()
        self.password_input.setEchoMode(qtWidgets.QLineEdit.Password)

        layout.addRow("用户名:", self.username_input)
        layout.addRow("密码:", self.password_input)

        # 创建按钮
        button_box = qtWidgets.QDialogButtonBox(qtWidgets.QDialogButtonBox.Ok | qtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.verify_login)
        button_box.rejected.connect(self.reject)

        layout.addRow(button_box)

        # 存储用户的sales_id
        self.sales_id = None
        self.user_name = None

    def verify_login(self):
        # TODO
        # 验证用户信息
        username = self.username_input.text()
        password = self.password_input.text()

        # 示例用户数据 (用户名: 密码)
        valid_users = {
            "admin": {
                "password": "admin123",
                "sales_id": "S001",
                "user_name": "admin"
            },
            "user1": {
                "password": "password1",
                "sales_id": "S002",
                "user_name": "user1"
            },
            "test": {
                "password": "test123",
                "sales_id": "S003",
                "user_name": "test"
            }
        }

        # 验证用户信息
        current_user_info = valid_users.get(username, None)

        if current_user_info and current_user_info["password"] == password:
            # 模拟获取sales_id的过程
            # 实际应用中，这里应该是从服务器获取用户的sales_id
            self.sales_id = current_user_info["sales_id"]
            self.user_name = current_user_info["user_name"]
            self.accept()  # 验证成功
        else:
            qtWidgets.QMessageBox.warning(self, "验证失败", "用户名或密码错误！", qtWidgets.QMessageBox.Ok)