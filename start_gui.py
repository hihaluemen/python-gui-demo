from modules.login_dialog import LoginDialog
from modules.crm_viewer import CRMViewer
import PyQt5.QtWidgets as qtWidgets

import sys
import qt_material

def show_login():
    """显示登录窗口，验证成功后显示主窗口"""
    # 创建应用程序实例
    app = qtWidgets.QApplication(sys.argv)
    
    # 应用Material样式
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')
    
    # 显示登录对话框
    login_dialog = LoginDialog()
    if login_dialog.exec_() == qtWidgets.QDialog.Accepted:
        # 登录成功，显示主窗口
        viewer = CRMViewer(login_dialog.sales_id, login_dialog.user_name)
        viewer.show()
        
        # 运行应用程序
        sys.exit(app.exec_())
    else:
        # 登录取消或失败，退出应用
        sys.exit(0)

if __name__ == '__main__':
    show_login()
    