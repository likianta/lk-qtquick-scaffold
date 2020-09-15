"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm_old.py
@Version  : 0.1.2
@Created  : 2019-07-09
@Updated  : 2020-09-15
@Desc     : Communicate machanism between QML and Python.
"""
from lk_logger import lk

""" 模块说明

# 工作流程

1. 广播系统 BroadcastSystem 创建全局唯一实例 broadcast
2. 成员 (Member) 初始化
    1. 所有自定义的成员均需要继承 Member 父类
    2. 成员通过自己的 _open_channels() 方法向 broadcast 开通自己的频道
        1. 对于该频道来说, 成员的身份是 "播主"
        2. 一个频道允许存在多个播主
        3. 播主之间的开通/加入顺序是不确定的
    3. 成员通过自己的 _subscribe_channels() 方法向 broadcast 订阅自己想要的频道
        1. 对于该频道来说, 成员的身份是 "用户"
        2. 一个频道允许存在多个用户
        3. 用户之间的订阅顺序是不确定的
    4. 也就是说, 一个成员既可以成为播主, 也可以成为用户, 可以同时拥有这两个身份
       (但不允许对同一个频道持有两个身份)
3. 播主发布消息
    1. 播主可以向自己开通/加入的频道发布消息
    2. broadcast 会将该频道的消息传递给收听该频道的所有用户
4. 用户消费消息
    1. 用户收到自己订阅的频道的消息后, 可以进行消费
    2. 消费方法由用户自己定义. 例如, 某用户在收听到 "购物" 频道的消息后, 去参加
       购物; 某用户在收听到 "购物" 频道的消息后, 向自己开通的 "团购" 频道转发了
       这个信息 (然后订阅了 "团购" 频道的用户就会继续消费)

# 特殊需求: 用户订阅了复合频道

上述工作流程针对单频道的发布/订阅已足够使用. 但假设有以下需求:

某用户同时订阅了 "购物 A" 频道和 "购物 B" 频道, 他只有从两个频道都收到消息以后,
才会进行比较, 并决定参加哪个购物活动. 其中:

- 购物 A 频道和购物 B 频道之间是不互通的, 两频道的播主互相不认识
- 购物 A 频道和购物 B 频道的消息发布先后顺序是不确定的
- 用户在接收到任何一方的消息后, 需要先把消息储存起来 (因为 broadcast 不负责储存
  消息); 直到等到另一方的消息发过来

为了解决此需求, Member 类增加了一个 compound_subscribes 成员变量和
_check_compound_subscribes() 方法. 详见方法注释.
"""


class PyCommunicator:
    """
    Usage:
        QML Register
            // === SomeComp.qml ===
            Button {
                id: _btn
                onClicked: PyComm.send("launch", _btn)
                
                Popup {
                    id: _popup
                    
                    function updateModel(options) {
                        _list.model = options
                    }
                    
                    ListView {
                        id: _list
                        Component.onCompleted: {
                            PyComm.register("options", _list, updateModel)
                        }
                    }
                }
            }
        Python
            # === some_module.py ===
            def dialog():
                pycomm.send("options", ["Confirm", "Skip", "Exit"])
                user_select = pycomm.recv()
            
    """


class BroadcastSystem:
    """
    NOTE: 如需使用广播系统, 请确保订阅者/频道主具有以下类变量:
        uid: str. 用户名, 请确保自己的用户名是唯一的.
        some_method(**kwargs): 用于注册的方法, 其参数必须是 **kwargs 的形式.
    """
    ADMIN = 'super_administrator'
    
    channels: dict
    datapot: dict
    listen_only_manager: dict
    lock = False
    message_queue: list
    
    def __init__(self):
        # channels
        self.channels = {}
        """ {
                channel_name: {
                    "owners": [...],
                    "followers": {uid: user.mailbox, ...}
                }, ...
            }
        """
        # managers
        self.listen_only_manager = {}  # {username: {None|list}}
        # self.compound_channel_manager = {}  # fmt: {mailbox: list}
        
        # messages and data
        self.message_queue = []
        self.datapot = {}
    
    def __new__(cls):
        """ 维持单例模式. """
        if not hasattr(cls, 'instance'):
            cls.instance = super(BroadcastSystem, cls).__new__(cls)
        return cls.instance

    # --------------------------------------------------------------------------
    
    def open_channel(self, owner_name: str, *channel_names,
                     is_private=False) -> bool:
        """
        IN: owner_name (str): e.g. 'filetree_panel'
            channel_name (str): e.g. 'filetree_item_selected'
            is_private (bool):
                True: this channel can only be used by current owner. even
                    refusing super administrator to control it.
                False: this channel allows other owner to register in it.
        OT: is_succeed (bool): shows opening channel succeed or not.
        """
        lk.loga(channel_names)
        
        for channel_name in channel_names:
            node = self.channels.setdefault(
                channel_name, {'owners': [], 'followers': {}}
            )
            
            owners = node['owners']
            
            if not owners:
                if not is_private:
                    owners.append(self.ADMIN)
                owners.append(owner_name)
                continue
            
            if is_private:
                try:
                    assert len(owners) == 1 and owners[0] == owner_name
                except AssertionError:
                    return self._failed_and_warning(
                        'The private channel ({}) you want to open is occupied '
                        'by someone else: {}. so we cannot provide this '
                        'channel for you'.format(channel_name, owners)
                    )
            
            if owner_name in owners:
                return self._failed_and_warning(
                    'Failed to "re-create" this channel, because you have '
                    'already been this channel\'s owner', channel_name,
                    owner_name, owners
                )
            
            owners.append(owner_name)
            lk.loga(node)
        
        return True
    
    def subscribe_channel(self, user_name, **subscribes) -> bool:
        """
        IN: user_name: str.
            subscibes: {channel_name: user}
                <key channel_name>: str. e.g. 'on_addressbar_updated'
                <value user>: {method|dict}.
                    <method mailbox>: method or classmethod. e.g. Addressbar()
                        .listener()
                    dict: {
                        'mailbox': staticmethod|classmethod,
                        'listen_only': {None|tuple|list},
                        'is_private': bool
                    }
                        (value) mailbox: required; {method|classmethod}.
                        (value) listen_only: optional; default None.
                            <None>: 表示收听目标频道的所有播主发布的内容.
                            <tuple|list>: 表示用户指定了一个列表, 只收听处于该列
                                表中的播主发布的内容.
                            二者的区别在于, 假如 xx 频道由两个播主共同管理, 播主
                            A 喜欢发布科普类知识, 播主 B 主要发布事务与行程安排.
                            而用户只想要看 A 的内容, 那么用户就需要指定一个列表,
                            列表中只包含 A 播主, 这样 BroadcastSystem 只会在 A
                            有更新时才向此用户推送内容.
                            (旧版注释) 这个场景的背景是, 广播台是基于频道进行消
                            息发布的, 而一个频道允许有多个播主共同管理 (就好比
                            "科技美学" 这个频道会有多个评测人一样). 如果我们只对
                            其中某个播主感兴趣, 那么我们可以在这里设置某个或某几
                            个收听对象: listen_only=['NaYan']. (注意类型是列表或
                            元组).
                            比较人性化的是, 我们不需要等新消息提醒后再去检查是不
                            是这个播主的发布, 广播台会自动过滤掉非此播主的同频道
                            发布内容.
                            另外, 您也可以传入一个空元组或空列表, 以表示您不想收
                            听任何播主在此频道发布的消息. (注意: 传入空列表和传
                            入 None 表达的是完全不同的意思). 这是一种小众的需求,
                            也许在您因为某种原因需要彻底封闭自己的视听时会用到
                            (当然超级管理员也可能通过此操作封闭您的活动, 类似于
                            关到 "小黑屋").
                            相关函数: self.filter()
                        (value) is_private: optional; bool; default False.
                            True: 表示这是私人订阅行为, 超级管理员无权访问该用户
                            的订阅列表.
                            False: 表示这是公开订阅行为, 超级管理员有权将自己注
                            册为被订阅方中的一员.
        OT: bool.
                True: 表示订阅成功.
                False: 表示订阅失败.
        """
        for channel_name, subscribe in subscribes.items():
            channel = self.channels.setdefault(
                channel_name, {'owners': [], 'followers': {}}
            )
            
            followers = channel['followers']  # type: dict
            
            if isinstance(subscribe, dict):
                mailbox = subscribe['mailbox']
                listen_only = subscribe.get('listen_only', None)
                is_private = subscribe.get('is_private', False)
            else:
                mailbox = subscribe
                listen_only = None
                is_private = False
            
            followers.update({user_name: mailbox})
            # -> {'sheetlist1': sheetlist1.update_sheetlist}

            # ------------------------------------------------------------------
            
            if listen_only is None:
                self.listen_only_manager[user_name] = None
                """
                NOTICE: None 具有特殊的含义, None 表示的是无限制, 而非谁都不听.
                    具体可在 self.filter() 方法中观看它的逻辑.
                """
            else:
                node = self.listen_only_manager.setdefault(
                    user_name,
                    [] if is_private else [self.ADMIN]
                )
                node.extend(listen_only)
                """
                listen_only = ['filelist1']
                is_private = True:
                    -> self.listen_only = {
                        'filelist1': ['filelist1']
                    }
                is_private = False:
                    -> self.listen_only = {
                        'filelist1': ['super_administrator', 'filelist1']
                    }
                    
                NOTE: 这里有一个小问题, 如果 listen_only 中包含了大量该频道根本
                    不存在的主播, 是否应该把他们剔除掉? 目前 (2019年7月7日) 基于
                    以下两点考虑:
                        1. 剔不剔除都不影响程序正常执行
                        2. 如果后期有新播主加入此频道, 而用户关注的新播主恰好在
                           listen_only 列表, 那么 listen_only 保持不剔除才是正确
                           和安全的
                    因此决定不予剔除.
                """
        return True
    
    def reset(self):  # DEL: this method is not used.
        """ 重置消息盒子和清空消息队列.

        NOTICE: 本操作仅允许第一个触发 push_message() 的人适用 (且适用时机是在
            push_message() 之前). 一般来说, 这个第一触发人永远都是
            WebSocketHandler 的 on_message() 方法.
        """
        self.lock = False
        self.datapot.clear()
        self.message_queue.clear()
    
    def push_message(self, pusher: str, channel_name: str, **message):
        # push into message queue.
        self.message_queue.append((pusher, channel_name, message))
    
    def run(self) -> dict:
        if not self.lock:
            self.lock = True
        else:
            lk.logt('[W4605]', 'the message queue is under locking')
            return {}
        
        # 重置消息盒子
        self.datapot.clear()
        
        for i in self.message_queue:
            pusher, channel_name, message = i
            data = message.get('data')
            lk.loga(pusher, channel_name, data)
            # | lk.loga(pusher, channel_name, message)
            
            if data is not None:  # 方案1
                self.datapot[pusher] = data
            # | self.datapot[pusher] = message  # 方案2
            """
                方案1: 只有在 data 的值不为空的情况下更新. (目前采用)
                方案2: 任何时候都更新 message 的所有键值对到 self.datapot 上.
            """
            
            channel = self.channels.get(channel_name)  # type: dict
            # lk.loga(channel)
            """ channel ('on_addressbar_updated') -> {
                    "owners": ['super_administrator', 'addressbar'],
                    "followers": {
                        'filelist1': filelist1.listener,
                        'filelist2': filelist2.listener, ...
                    }
                }
            """
            
            # check the owner whether has the authority.
            assert pusher in channel['owners'], self._failed_and_warning(
                'The channel refused your delivery because you are not its '
                'owners. Please submit a channel application first (by '
                '`broadcast.open_channel(<your_name>, <channel_name>)`).',
                pusher, channel
            )
            
            followers = channel['followers']  # type: dict
            if not followers:
                continue
            
            # dispatch message to its followers.
            for username, mailbox in followers.items():
                if self._filter(username, pusher):
                    if data is not None:
                        mailbox(data=data)
                    else:
                        # 允许用户的邮箱接收频道主发送的 "空消息"
                        mailbox()
                    # | self.datapot[username] = mailbox(**message)
        
        # 清空消息队列, 以及解开锁
        self.message_queue.clear()
        self.lock = False
        
        return self.datapot
    
    def _filter(self, username, owner):
        """ Filter owner's message by checking user's listen_only
            configuration. """
        if self.listen_only_manager[username] is None:
            # 表示用户收听所有播主.
            return True
        else:
            return bool(owner in self.listen_only_manager[username])
    
    @staticmethod
    def _failed_and_warning(*msg) -> False:
        msg = ';\t'.join(map(str, msg))
        lk.logt('[W3407]', msg, h='parent')
        return False


broadcast = BroadcastSystem()


# ------------------------------------------------------------------------------

class Member:
    member_name = 'lkcs_member'  # must overwrite it in child classes.
    
    channels = None  # type: (list, tuple)
    subscribes = None  # type: dict
    compound_subscribes = None  # type: dict
    # {mailbox_id: {channel_name: <None|channel_message>}}
    
    def __init__(self, member_name=''):
        """
        :param member_name: str. if not empty, will override self.member.
        """
        self.cast = broadcast
        if member_name:
            self.member_name = member_name
        self._init_channels()
        self._open_channels()
        self._subscribe_channels()
    
    def _init_channels(self):
        """
        请覆写这个方法, 并在这里初始化 self.channels, self.subscribes.

        self.channels: None/str/tuple/list.
            str: channel1
            tuple: (channel1, channel2, channel3, ...)
            list: [channel1, channel2, channel3, ...]
        self.subscribes: None/classmethod/dict.
            (classmethod) mailbox
            (dict) {
                'mailbox': mailbox,
                'listen_only': listen_only,
                'is_private': is_private
            }
                (value) mailbox: required, classmethod.
                (value) listen_only: optional, None/tuple/list.
                (value) is_private: optional, bool.
        """
        """
        self.channels = ()
        self.subscribes = {}
        # self.widget.onclick.do()
        """
        raise NotImplementedError
    
    def _open_channels(self):
        if self.channels is None:
            return
        elif isinstance(self.channels, str):
            self.cast.open_channel(
                self.member_name,
                self.channels
            )
        else:  # list
            self.cast.open_channel(
                self.member_name,
                *self.channels
            )
    
    def _subscribe_channels(self):
        if self.subscribes is None:
            return
        elif self.subscribes:  # dict
            self.cast.subscribe_channel(
                self.member_name,
                **self.subscribes
            )
    
    def _check_compould_subscribes(self, mailbox_id, channel, message):
        holder = self.compound_subscribes[mailbox_id]
        holder[channel] = message
        return bool(all(holder.values()))
    
    def push_message(self, channel, **message):
        """ 在这里, 您可以向您所管理的频道推送信息.
        
        NOTICE: 这里的推送是推送到 broadcast 的消息队列里面, 而不是立即被
            broadcast 执行的.
        
        TODO: `**message` 参数未来可能会改为 `data`.
        """
        # you should submit your name, channel name, and message to the
        # broadcast.
        self.cast.push_message(self.member_name, channel, **message)
    
    def push_failed(self, channel, *badnews):
        """ Push a bad message and return a none type value.

        FIXME: 目前该方法暂无使用场景, 未来考虑调整业务或者删除此方法.
        
        E.g. push_failed(official_channels.ON_ADDRESSBAR_UPDATED, filelist)
        """
        if not badnews:
            self.push_message(channel, BADNEWS=True)
        else:
            badnews = dict(zip(badnews, [None] * len(badnews)))
            self.push_message(channel, **badnews, BADNEWS=True)
        """
        If someone is an audience of this channel, he should check the key of
        'BADNEWS' before handling channel message.
        E.g.
            class SomeAudience(ComponentPrototype):

                def on_recv_msg(msg, **kwargs):
                    if kwargs.get(self.BADNEWS, False):
                        return self.push_failed(...)

                    # else then do the normal things.
        """
        return None
    
    def run_pushing_queue(self):
        return self.cast.run()
