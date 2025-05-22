import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import PyQt5.QtWebEngineWidgets as qtWebEngineWidgets
import qt_material
from PyQt5.QtWebEngineWidgets import QWebEnginePage

class MyWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS Console][{level}] {message} (Line: {lineNumber}, Source: {sourceID})")

class CRMViewer(qtWidgets.QMainWindow):
    def __init__(self, sales_id, sales_name):
        super().__init__()
        # 存储用户的sales_id
        self.sales_id = sales_id
        self.sales_name = sales_name
        # 存储当前客户ID和状态
        self.current_customer_id = None
        self.current_customer_name = None
        self.current_status = 0  # 默认为自动状态
        # 定义主页URL
        # TODO
        self.main_url = "http://www.baidu.com"
        # 用户token使用量
        self.token_usage = 0
        # 初始化UI
        self.init_ui()
        # 设置定时器，定期检查状态
        self.timer = qtCore.QTimer(self)
        self.timer.timeout.connect(self.check_current_status)
        self.timer.start(5000)  # 每5秒检查一次
        
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('CRM智能助手')
        # 设置初始窗口大小，后续会根据网页内容自动调整
        self.setGeometry(100, 100, 180, 650)
        
        # 创建中央部件
        self.central_widget = qtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = qtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # 创建顶部标题栏
        self.create_title_bar()
        
        # 创建网页视图
        self.web_view = qtWebEngineWidgets.QWebEngineView()
        self.setup_browser()
        self.web_view.load(qtCore.QUrl(self.main_url))
        
        # 连接网页加载完成信号，用于调整窗口大小
        self.web_view.loadFinished.connect(self.adjust_window_size)
        
        # 将网页视图添加到主布局
        self.main_layout.addWidget(self.web_view)
        
        # 创建底部控制面板
        self.create_control_panel()
        
        # 初始获取状态
        self.check_current_status()
    
    def create_title_bar(self):
        """创建顶部标题栏"""
        title_bar = qtWidgets.QFrame()
        title_bar.setProperty('class', 'card')
        title_bar.setMinimumHeight(60)
        title_bar_layout = qtWidgets.QHBoxLayout(title_bar)
        
        # 标题
        title_label = qtWidgets.QLabel("CRM智能助手")
        title_label.setProperty('class', 'h3')
        title_bar_layout.addWidget(title_label)
        
        # 用户信息
        user_info = qtWidgets.QLabel(f"{self.sales_name}")
        title_bar_layout.addWidget(user_info, alignment=qtCore.Qt.AlignRight)
        
        self.main_layout.addWidget(title_bar)
    
    def create_control_panel(self):
        """创建底部控制面板"""
        control_panel = qtWidgets.QFrame()
        control_panel.setProperty('class', 'card')
        control_panel.setMinimumHeight(70)
        control_layout = qtWidgets.QHBoxLayout(control_panel)
        
        # 创建当前客户名称显示框
        customer_frame = qtWidgets.QFrame()
        customer_layout = qtWidgets.QVBoxLayout(customer_frame)
        customer_layout.setContentsMargins(2, 2, 2, 2)
        
        customer_label = qtWidgets.QLabel("当前客户:")
        customer_layout.addWidget(customer_label)
        
        self.customer_name_label = qtWidgets.QLabel("暂无客户")
        self.customer_name_label.setMinimumWidth(80)
        customer_layout.addWidget(self.customer_name_label)
        
        control_layout.addWidget(customer_frame)
        
        # 创建状态下拉选择框
        status_frame = qtWidgets.QFrame()
        status_layout = qtWidgets.QVBoxLayout(status_frame)
        status_layout.setContentsMargins(2, 2, 2, 2)
        
        self.status_label = qtWidgets.QLabel("状态:")
        status_layout.addWidget(self.status_label)
        
        self.status_combo = qtWidgets.QComboBox()
        self.status_combo.addItems(["自动", "辅助", "关闭"])
        self.status_combo.currentIndexChanged.connect(self.status_changed)
        self.status_combo.setMinimumWidth(80)
        status_layout.addWidget(self.status_combo)
        
        control_layout.addWidget(status_frame)
        
        # 添加间隔
        control_layout.addStretch(1)
        
        # 创建刷新按钮
        self.refresh_button = qtWidgets.QPushButton('刷新')
        self.refresh_button.setProperty('class', 'primary')
        self.refresh_button.clicked.connect(self.refresh_status)
        self.refresh_button.setMinimumWidth(80)
        control_layout.addWidget(self.refresh_button)
        
        # 创建信息按钮
        self.info_button = qtWidgets.QPushButton('我的信息')
        self.info_button.setProperty('class', 'secondary')
        self.info_button.clicked.connect(self.show_user_info)
        self.info_button.setMinimumWidth(80)
        control_layout.addWidget(self.info_button)
        
        # 将控制面板添加到主布局
        self.main_layout.addWidget(control_panel)
        
    def setup_browser(self):
        """配置浏览器设置"""
        # 用自定义的 Page
        self.web_view.setPage(MyWebEnginePage(self.web_view))
        settings = self.web_view.settings()
        settings.setAttribute(qtWebEngineWidgets.QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(qtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        # 清除缓存
        profile = qtWebEngineWidgets.QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()
    
    def get_current(self):
        """
        获取当前客户ID和状态
        实际应用中，这里应该是从服务器获取数据
        """
        # 模拟从服务器获取数据
        # 返回格式：(current_customer_id, current_customer_name, status)
        try:
            # TODO
            # 这里应该是实际的API调用
            # response = requests.get('https://api.example.com/get_current', params={'sales_id': self.sales_id})
            # data = response.json()
            # return data['customer_id'], data['customer_name'], data['status']
            
            # 模拟数据
            customer_id = "C001"
            customer_name = "张三"  # 模拟客户名称
            return customer_id, customer_name, self.current_status
        except Exception as e:
            print(f"获取当前状态失败: {e}")
            return None, None, 0
    
    def update_status(self, status):
        """
        更新状态到服务器
        实际应用中，这里应该是向服务器发送更新请求
        """
        try:
            # TODO
            # 这里应该是实际的API调用
            # response = requests.post('https://api.example.com/update_status', 
            #                         json={
            #                             'sales_id': self.sales_id,
            #                             'customer_id': self.current_customer_id,
            #                             'status': status
            #                         })
            # return response.json()['success']
            
            # 模拟成功更新
            self.current_status = status
            return True
        except Exception as e:
            print(f"更新状态失败: {e}")
            return False
    
    def check_current_status(self):
        """定期检查当前状态"""
        # 获取当前客户ID和状态
        customer_id, customer_name, status = self.get_current()
        
        if customer_id and status is not None:
            # 更新当前客户ID和状态
            self.current_customer_id = customer_id
            self.current_customer_name = customer_name
            if status != self.current_status:
                self.current_status = status
                self.status_combo.setCurrentIndex(status)
            # 更新客户名称标签
            self.customer_name_label.setText(customer_name if customer_name else "暂无客户")
    
    def status_changed(self):
        """状态下拉框选择改变时触发"""
        new_status = self.status_combo.currentIndex()
        if new_status != self.current_status:
            success = self.update_status(new_status)
            if success:
                self.current_status = new_status
                qtWidgets.QMessageBox.information(self, "状态更新", f"状态已更新为: {self.status_combo.currentText()}", qtWidgets.QMessageBox.Ok)
            else:
                # 更新失败，恢复原状态
                self.status_combo.setCurrentIndex(self.current_status)
                qtWidgets.QMessageBox.warning(self, "状态更新", "状态更新失败，请稍后重试", qtWidgets.QMessageBox.Ok)
    
    def refresh_status(self):
        """刷新按钮点击事件"""
        # 获取当前客户ID和状态
        customer_id, customer_name, status = self.get_current()
        
        if customer_id and status is not None:
            # 更新当前客户ID和状态
            self.current_customer_id = customer_id
            self.current_customer_name = customer_name
            self.current_status = status
            self.status_combo.setCurrentIndex(status)
            # 更新客户名称标签
            self.customer_name_label.setText(customer_name if customer_name else "暂无客户")
            qtWidgets.QMessageBox.information(self, "状态刷新", f"当前客户ID: {customer_id}\n当前客户: {customer_name}\n当前状态: {self.status_combo.currentText()}", qtWidgets.QMessageBox.Ok)
        else:
            qtWidgets.QMessageBox.warning(self, "状态刷新", "获取当前状态失败，请稍后重试", qtWidgets.QMessageBox.Ok)
    
    def show_user_info(self):
        """显示用户信息"""
        # 模拟获取用户信息
        # 实际应用中，这里应该是从服务器获取用户信息
        # TODO
        username = "未知用户"

        # 示例用户数据 (用户名: 密码)
        valid_users = {
            "S001": {
                "password": "admin123",
                "sales_id": "S001",
                "user_name": "admin"
            },
            "S002": {
                "password": "password1",
                "sales_id": "S002",
                "user_name": "user1"
            },
            "S003": {
                "password": "test123",
                "sales_id": "S003",
                "user_name": "test"
            }
        }

        username = valid_users.get(self.sales_id, {}).get("user_name", "未知用户")
        
        # 模拟token使用量增加
        self.token_usage += 100
        
        # 创建一个更美观的信息对话框
        info_dialog = qtWidgets.QDialog(self)
        info_dialog.setWindowTitle("用户信息")
        info_dialog.setMinimumWidth(300)
        
        layout = qtWidgets.QVBoxLayout(info_dialog)
        
        # 标题
        title = qtWidgets.QLabel("用户详细信息")
        title.setProperty('class', 'h4')
        layout.addWidget(title)
        
        # 分隔线
        line = qtWidgets.QFrame()
        line.setFrameShape(qtWidgets.QFrame.HLine)
        layout.addWidget(line)
        
        # 用户信息
        info_frame = qtWidgets.QFrame()
        info_layout = qtWidgets.QFormLayout(info_frame)
        
        info_layout.addRow("用户名:", qtWidgets.QLabel(username))
        info_layout.addRow("Sales ID:", qtWidgets.QLabel(self.sales_id))
        info_layout.addRow("当前Token使用量:", qtWidgets.QLabel(str(self.token_usage)))
        
        layout.addWidget(info_frame)
        
        # 确定按钮
        button = qtWidgets.QPushButton("确定")
        button.clicked.connect(info_dialog.accept)
        layout.addWidget(button)
        
        info_dialog.exec_()
    
    def adjust_window_size(self):
        """根据网页内容调整窗口大小"""
        # 获取网页内容大小
        self.web_view.page().runJavaScript("""
            [document.documentElement.scrollWidth, 
             document.documentElement.scrollHeight,
             window.innerWidth / window.innerHeight]
        """, self.on_size_calculated)

    def on_size_calculated(self, result):
        """处理网页尺寸计算结果"""
        if not result or not isinstance(result, list) or len(result) != 3:
            return
        
        content_width, content_height, aspect_ratio = result
        
        # 计算合适的窗口大小，保持网页的宽高比
        # 获取屏幕尺寸，确保窗口不会超出屏幕
        screen_size = qtWidgets.QApplication.primaryScreen().availableGeometry()
        max_width = min(content_width + 40, screen_size.width() * 0.7)  # 添加一些边距，减小最大宽度比例
        max_height = min(content_height + 150, screen_size.height() * 0.9)  # 为标题栏和控制面板留出空间
        
        # 根据网页内容比例调整窗口大小
        if aspect_ratio > 1:  # 宽大于高
            new_width = max_width
            new_height = new_width / aspect_ratio + 150  # 为标题栏和控制面板留出空间
        else:  # 高大于宽
            new_height = max_height
            new_width = (new_height - 150) * aspect_ratio  # 为标题栏和控制面板留出空间
        
        # 确保窗口大小不小于最小值
        new_width = max(new_width, 180)  # 减小最小宽度
        new_height = max(new_height, 600)
        
        # 设置新的窗口大小
        self.resize(int(new_width), int(new_height))
        
        # 居中显示窗口
        self.center_window()

    def center_window(self):
        """将窗口居中显示在屏幕上"""
        frame_geometry = self.frameGeometry()
        screen_center = qtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def closeEvent(self, event):
        """窗口关闭事件，用于释放资源"""
        # TODO

        # 停止定时器
        if self.timer.isActive():
            self.timer.stop()
            
        # 释放浏览器资源
        if hasattr(self, 'web_view'):
            self.web_view.page().deleteLater()
            self.web_view.deleteLater()
            
        # 如果有其他需要释放的资源，可以在这里添加
        
        # 可以在这里记录日志或执行其他清理操作
        print(f"应用退出，用户: {self.sales_id}, Token使用量: {self.token_usage}")
        
        # 接受关闭事件，允许窗口关闭
        event.accept()