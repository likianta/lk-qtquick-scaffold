# 关于自定义主题的一些意见和建议

## 不同主题之间是否有联系

不同的主题之间没有关联. 因此不必要追求不同主题库之间组件命名风格一致, 组件 API 一致等.

为什么这样做? 最初有考虑过 "用一套代码, 只通过更改 `import ThemeA` 为 `import ThemeB` 就实现主题切换" 这样的实现的可能性. 但稍加验证, 认为这是一个伪需求且不应该被实现.

例如, ThemeA 有 GhostButton 组件, 我们在代码中也用到了 GhostButton 组件, 于是我们的代码和 A 是有关联的.

我们不能保证 ThemeB 也提供了同样的组件, 或者有同名组件也不能保证同样的属性和方法.

想要实现 "主题切换" 并不应该通过改变要导入的主题来实现. 而应该在同主题下 (保证组件 API 不会被更改的前提下) 通过修改属性的值来实现.

与之相关的工作应该由 "stylesheets" 来完成.