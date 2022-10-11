# Scope 设计框架

## 格式及意义

scope 是 str 类型, 形式类似于路径, 以多个斜杠 (/) 分隔不同的层级.

示例: 'homepage/sidebar/settings'

scope 的格式有助于实现 "互斥" 和 "兼容" 两种组织方式. 以一个例子来理解:

假设有两个 scope: 'homepage/sidebar/dashboard' 和 'homepage/sidebar/settings'.

当用户从 dashboard 切换到 settings 页面时, 后一个 scope 被激活, scope 引擎会自动将前一个 scope 的所有状态清除. 即上个 scope 所绑定的快捷键都失效, 按键被重新分配给新的 scope.
