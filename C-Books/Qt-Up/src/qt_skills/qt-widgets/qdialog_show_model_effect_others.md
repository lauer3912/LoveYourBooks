# 弹出对话框，阻止应用程序所有窗口输入，如何做？

QDialog 分为两大类：

- 模态对话框
- 非模态对话框

而，模态对话框又分为两种方式：（1）窗口模态对话框；（2）应用模态对话框。

- **窗口模态对话框**：只能阻止与对话框关联（它的父窗口、所有祖父窗口，以及父窗口和父窗口的所有兄弟姐妹）的窗口的访问，允许用户在应用程序中继续使用其他窗口。
- **应用模态对话框**：阻止应用程序的所有窗口输入。

## 显示模态对话框

- 调用它的 exec()函数。当用户关闭对话框时，exec()将提供一个有用的返回值。通常，为了使对话框关闭后并返回适当的值，我们可以连接一个默认按钮，例如：OK 按钮关联到 accept()槽，Cancle 按钮关联到 reject()槽。或者可以调用 done()槽，返回一个整数值。而根据这个返回值，我们就可以采取下一步动作了。
- 调用 setModal(true)或 setWindowModality()，然后 show()。与 exec()不同，show()弹出对话框后，不需等待用户输入确认，便立即将控制权返回给调用者。

```cpp
//弹出应用模态对话框
void ModelWidget::on_btnApp_clicked()
{
    QDialog* dlg = new QDialog(this);
    dlg->setAttribute(Qt::WA_DeleteOnClose);//设置对话框关闭后，自动销毁
    dlg->setWindowModality(Qt::ApplicationModal);//或者可以使用setModel(true)
    dlg->show();
    qDebug() << "虽然显示模态对话框，但我也不需要等用户操作完就会立马执行";
}
```
