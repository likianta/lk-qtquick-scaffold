"""
structure: {scope: {sid: {kid: fid}}}
docs: ~/docs/scope-engine.zh.md
"""
import typing as t
from collections import defaultdict

from qtpy.QtCore import Qt

from .__ext__ import QObject
from .__ext__ import slot


class T:
    KID = t.Tuple[int, tuple[bool, bool, bool]]  # key id
    FID = str  # function id
    #   (int key_code, (ctrl, shift, alt))
    
    Scope = str  # scope url.
    #   the form is '<node>/<node>/<node>/...',
    #   for exmaple 'homepage/sidebar/settings'
    #   the default scope is 'global'
    PScope = str  # parent scope url.
    SID = str  # scope instance id.
    #   it is a random id generated by `uuid.uuid1().hex`.
    Scopes = t.Dict[Scope, t.Dict[SID, t.Dict[KID, FID]]]
    ExclusiveScopes = t.TypedDict('ExclusiveScopes', {
        'direct'  : t.Set[Scope],
        'indirect': t.Set[PScope],
    })
    
    Fid2Qobj = t.Dict[FID, QObject]
    Sid2Scope = t.Dict[SID, Scope]
    
    CurrentState = t.TypedDict('CurrentState', {
        'scope_2_sid'  : t.Dict[Scope, SID],
        'active_sids'  : t.Set[SID],
        'kid_2_sid_fid': t.Dict[KID, t.Tuple[SID, FID]],
    })


class ScopeEngine(QObject):
    _scopes: T.Scopes = defaultdict(lambda: defaultdict(dict))
    _scopes_ex: T.ExclusiveScopes = {'direct': set(), 'indirect': set()}
    _fid_2_qobj: T.Fid2Qobj = {}
    _sid_2_scope: T.Sid2Scope = {}
    _current_state: T.CurrentState = {
        'scope_2_sid'  : {},
        'active_sids'  : set(),
        'kid_2_sid_fid': {},
    }
    
    @slot(str, str)
    def register_sid(self, scope: str, sid: str) -> None:
        print(f'register: [cyan]scope = {scope} [dim]sid = {sid}[/][/]', ':r')
        self._sid_2_scope[sid] = scope
        if scope.rsplit('/', 1)[-1].startswith('!'):
            self._scopes_ex['direct'].add(scope)
            self._scopes_ex['indirect'].add(self._get_parent_scope(scope))
    
    @slot(str, str, str, object, int)
    @slot(str, str, str, object, int, int)
    def register_func(
            self, scope: T.Scope, sid: T.SID, fid: T.FID, qobj: QObject,
            key: int, modifier: int = 0
    ) -> None:
        kid = self._compose_kid(key, modifier)
        self._fid_2_qobj[fid] = qobj
        self._scopes[scope][sid][kid] = fid
        if sid in self._current_state['active_sids']:
            self._current_state['kid_2_sid_fid'][kid] = (sid, fid)
        # print(':l', self._scopes, self._current_state)
    
    # -------------------------------------------------------------------------
    
    @slot(str, str)
    def activate_scope(self, scope: T.Scope, sid: T.SID = None) -> None:
        if sid in self._current_state['active_sids']:
            return
        
        def attach(scope, sid):
            self._current_state['scope_2_sid'][scope] = sid
            self._current_state['active_sids'].add(sid)
            for kid, fid in self._scopes[scope][sid].items():
                self._current_state['kid_2_sid_fid'][kid] = (sid, fid)
        
        def dettach(scope, remove_old_sid: bool):
            # check if is there another sid in the same scope is active.
            if remove_old_sid:
                if old_sid := self._current_state['scope_2_sid'].get(scope):
                    self._current_state['active_sids'].remove(old_sid)
            
            if self._is_exclusive_scope(scope):
                pscope = self._get_parent_scope(scope)
                sid_to_be_removed = []
                for sid_x in self._current_state['active_sids']:
                    scope_x = self._sid_2_scope[sid_x]
                    if scope_x.startswith(pscope) and \
                            not scope_x.startswith(scope):
                        sid_to_be_removed.append(sid_x)
                for sid_x in sid_to_be_removed:
                    self._current_state['active_sids'].remove(sid_x)
        
        if sid:
            dettach(scope, remove_old_sid=True)
            attach(scope, sid)
        else:
            dettach(scope, remove_old_sid=False)
            
            def get_valid_sid(req_scope):
                for scope, sid in self._current_state['scope_2_sid'].items():
                    print(scope, sid, ':v')
                    if scope.startswith(req_scope):
                        yield scope, sid
            
            for scope, sid in get_valid_sid(scope):
                print('attach sub scope', scope, sid, ':v2')
                attach(scope, sid)
    
    @slot(str)
    def cscope(self, scope: T.Scope) -> None:
        print(scope)
        self.activate_scope(scope)
    
    @slot(str, str)
    def deactivate_scope(self, scope: T.Scope, sid: T.SID = None) -> None:
        if sid not in self._current_state['active_sids']:
            return
        if sid:
            # assert sid in self._current_state['active_sids']
            self._current_state['active_sids'].remove(sid)
        else:
            sid_to_be_removed = []
            for sid in self._current_state['active_sids']:
                if self._sid_2_scope[sid].startswith(scope):
                    sid_to_be_removed.append(sid)
            for sid in sid_to_be_removed:
                self._current_state['active_sids'].remove(sid)
    
    @slot(str, str)
    def dscope(self, scope: T.Scope) -> None:
        self.deactivate_scope(scope)
    
    @staticmethod
    def _get_parent_scope(scope: str) -> str:
        if '/' in scope:
            return scope.rsplit('/', 1)[0]
        else:
            return '/'
    
    def _is_exclusive_scope(self, scope: T.Scope) -> bool:
        # what is exclusive scope? a node that starts with '!'.
        # e.g. 'homepage/sidebar/!settings'
        if scope in self._scopes_ex['direct']:
            return True
        elif scope.rsplit('/', 1)[-1].startswith('!'):
            self._scopes_ex['direct'].add(scope)
            self._scopes_ex['indirect'].add(self._get_parent_scope(scope))
            return True
        elif self._get_parent_scope(scope) in self._scopes_ex['indirect']:
            return True
        else:
            return False
    
    # DELETE
    def _find_sub_scopes(self, scope: T.Scope) -> t.Iterator[T.Scope]:
        for scope_x in self._scopes:
            if scope_x.startswith(scope + '/'):
                yield scope_x
    
    # def _is_parent_in_exclusive_scope(self, scope: T.Scope) -> bool:
    #     parent_scope = self._get_parent_scope(scope)
    #     return parent_scope in self._scopes_ex
    
    # -------------------------------------------------------------------------
    
    @slot(int, int)
    def on_key(self, key: int, modifier: int) -> None:
        # import lk_logger
        # lk_logger.start_ipython({'key': key})
        kid = self._compose_kid(key, modifier)
        # print(':l', kid, self._current_state)
        if kid in self._current_state['kid_2_sid_fid']:
            sid, fid = self._current_state['kid_2_sid_fid'][kid]
            if sid in self._current_state['active_sids']:
                qobj = self._fid_2_qobj[fid]
                qobj.triggered.emit(fid)
    
    from enum import Enum
    if isinstance(Qt.ControlModifier, Enum):
        # see a reference at `PySide6 (v6.4.0) > Qt3DRender.pyi > line 1014`
        _pyside6_640_patch = True
    else:
        _pyside6_640_patch = False
    
    def _compose_kid(self, key: int, modifier: int) -> T.KID:
        if self._pyside6_640_patch:
            # https://www.qt.io/blog/qt-for-python-release-6.4-is-finally-here
            #   open this link and search "Modifier" (seen in comment zone).
            return (key, (
                bool(modifier & Qt.ControlModifier.value),
                bool(modifier & Qt.ShiftModifier.value),
                bool(modifier & Qt.AltModifier.value),
            ))
        return (key, (
            bool(modifier & Qt.ControlModifier),
            bool(modifier & Qt.ShiftModifier),
            bool(modifier & Qt.AltModifier),
        ))
