# 更新日志

### 2.1.0 (wip)

- 新增: 完整版自定义焦点处理引擎 (lkscope)

### 2.0.0 (2022-10-11)

- 新增: 重新制作的组件库 LKWidgets
- 新增: pystyle 样式管理器
- 新增: pylayout 布局管理器
- 新增: pyassets 资源管理器
- 变更: 统一启动入口函数为 app.run
- 更新: 更好地集成热加载器到 app.run
- *次要更新*
    - 新增: 增加命令行界面 (基于 argsense)
    - 更新: 增强 pyside (register, eval)

组件库部分说明:

- 新增: 弹性布局
- 新增: 预设的多种按钮
- 新增: 容器组件
- 新增: 进度条

### 1.3.0 (2022-07-14)

- 更新: 扩展 qt backend 支持. 现已支持: pyside6/pyside2/pyqt6/pyqt5
- 新增: 实验性的预设组件和样式管理器, 预计在 2.0 版本中正式推出
- *次要更新*
    - 优化: 信号/槽装饰器优化
    - 优化: 程序关闭时不会产生空引用错误

### 1.2.3 (2022-04-18)

- *次要更新*
    - 优化(model): 为性能考虑, model update 相关的方法不再返回字典 (取而代之的是返回 None)
    - 优化(model): 提升 "更新非完整 item" 的安全性

### 1.2.2 (2022-04-13)

- 更新: model 所有方法均支持传入非完整的 item dict

### 1.2.1 (2022-04-11)

- *次要更新*
    - 修复(model): update 逻辑错误

### 1.2.0 (2022-04-10)

- 新增: 封装增强的 signal, slot
- 更新: 扩展 model 操作
- *次要更新*
    - 修复: 多个 slot 装饰同一个方法报错

### 1.1.1 (2022-02-16)

次要更新

- 修复: macos 上 qtlogger 对信息的路径格式处理

### 0.1.2 (2021-01-20)

- 优化: 自动识别 Qml 端的传参形式
- 新增: 从 pycomm.PyHandler 提取所有注册方法到父类 PyRegister

### 0.1.1 (2020-12-03)

- 新增: logger.js
- 更新: app 在实例化时注册 LKDebugger 和 LKHelper 模块
- 新增: 支持注册实例方法
- 更新: LCTextField 组件尺寸可调
- 新增: logger.py
- 优化: logger.py 显示效果
- 优化: PyHandler.call() 报错提示

### 0.1.0 (2020-11-28)

- 更新: 完善 HotReloader
- 变更: 简化 pycomm 模块
- 变更: 组件库适配新规范
- 更新: LCButton 使用新风格
- 新增: LCBackground 模块
- 移除: LCRectangleBg 组件
- 新增: LCCheckBox 图标
- 新增: LCOval 组件
- 修复: LCCheckList 和 LCRadioList
- 更新: LCText 和 LCEdit p_alignment 属性
- 变更: pycomm.PyHandler.main() 使用更严格的调用策略
- 优化: HotReloader 后端改造为类形式
- 修复: LCFileBrowse 组件
- 移除: LCFileBrowseButton 组件
- 新增: 按钮的 borderless 属性
- 新增: layout_helper.js
- 更新: 强化 LCRow, LCColumn 属性
- 变更: 组件使用 implitcitWidth/Height
- 新增: PyHandler.decoreg() 装饰器
- 更新: LCCheckList 和 LCRadioList 修改代理组件属性的新方案
- 优化: LCListView 仅在内容超出容器时可滑动
- 变更: debugger 模块移到主项目内
- 新增: LCCheckBg 组件
- 移除: LCEdit 和 LCEditField 组件
- 新增: LCTextField 组件
- 更新: 保持 LCRow, LCColumn 的属性动态更新
- 修复: LCRow, LCColumn 的 fillRest 及相关属性
