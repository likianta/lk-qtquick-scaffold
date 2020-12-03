function log(...content) {
    /*
     *  References:
     *      js stack trace: https://stackoverflow.com/questions/591857/how-can-i
     *          -get-a-javascript-stack-trace-when-i-throw-an-exception
     *      mutable arguments length: https://blog.csdn.net/m0_37263637/article/
     *          details/83186229
     *
     *  Usage in Qml:
     *      // view.qml
     *      import '~/logger.js' as Logger
     *      Item {
     *          Component.onCompleted: {
     *              Logger.log()
     *              Logger.log('Hello')
     *              Logger.log('Hello', true)  // The arguments length is mutable
     *              //  show out:
     *              //      [view.qml:4]
     *              //      [view.qml:5], [Hello]
     *              //      [view.qml:6], [Hello,true]
     *          }
     *      }
     */

    const err = new Error()

    /*
        console.log(err.stack)
        -> qml: log@file:///~/lk_qtquick_scaffold/debugger/logger.js:23
           onCompleted@file:///~/lk_qtquick_scaffold/tests/qml/view.qml:48
                                                               ^---------^
                                                              This is our target
           reload@file:///~/lk_qtquick_scaffold/debugger/HotReloader.qml:34
           onClicked@file:///~/lk_qtquick_scaffold/debugger/HotReloader.qml:69
     */

    let target_prefix = err.stack.toString().split('\n')[1]
    target_prefix = target_prefix.split('/').pop()

    if (content.length == 0) {
        content = ''
    }
    console.log('[' + target_prefix + ']', content)
}
