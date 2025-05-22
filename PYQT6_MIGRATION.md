# PyQt6 迁移记录

此文件记录将项目从 **PyQt5** 迁移到 **PyQt6** 所做的关键修改。

## 主要改动

1. **依赖更新**
   - 所有 `PyQt5` 的导入语句替换为 `PyQt6`。
2. **API 调整**
   - `exec_()` 方法更名为 `exec()`。
   - 枚举值使用新的命名空间，例如 `QDialog.DialogCode`、`QMessageBox.StandardButton`、`QFrame.Shape` 等。
   - `QLineEdit.Password` 改为 `QLineEdit.EchoMode.Password`。
   - `Qt.AlignRight` 改为 `Qt.AlignmentFlag.AlignRight`。
   - `QWebEngineSettings` 的属性调整为 `WebAttribute` 枚举。
3. **其它**
   - 修改了相关代码逻辑以适配新枚举和 API 的调用方式。

以上改动完成后，程序即可在 PyQt6 环境下运行。
