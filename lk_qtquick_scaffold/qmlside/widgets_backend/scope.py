"""
structure:
    field: {scope: {sid: {kid: fid}}}
"""
import typing as t
from collections import defaultdict

from qtpy.QtCore import Qt

from .__ext__ import QObject
from .__ext__ import signal
from .__ext__ import slot


class T:
    FID = str  # function id
    KID = t.Tuple[int, tuple[bool, bool, bool]]  # key id
    #   (int key_code, (ctrl, shift, alt))
    SID = str  # scope id
    
    Field = str
    FuncName = str
    Scope = str
    
    CurrentState = t.TypedDict('CurrentState', {
        'field'      : Field,  # noqa
        'scope_2_sid': t.Dict[str, SID],
        'active_sids': t.Set[SID],
        'kid_2_fid'  : t.Dict[KID, FID],
    })
    Fid2Qobj = t.Dict[FID, QObject]
    Field2Scopes = t.Dict[Field, t.Set[Scope]]
    Registered = t.Dict[Scope, t.Dict[SID, t.Dict[KID, FID]]]
    Scope2Sids = t.Dict[Scope, t.Set[SID]]


class Scope(QObject):
    triggered = signal(str)  # signal[fid]  # DELETE
    
    _current_state: T.CurrentState = {
        'field'      : 'default',
        'scope_2_sid': {},
        'active_sids': set(),
        'kid_2_fid'  : {},
    }
    _fid_2_qobj: T.Fid2Qobj = {}
    _field_2_scopes: T.Field2Scopes = defaultdict(set)
    # _registered: T.Registered = defaultdict(dict)
    _registered: T.Registered = defaultdict(lambda: defaultdict(dict))
    
    def __init__(self):
        super().__init__()
        self._field_2_scopes['default'].add('global')
        # self.triggered.connect(lambda fid: self._fid_2_qobj[fid]())
    
    @property
    def _current_field(self) -> T.Field:
        return self._current_state['field']
    
    @property
    def _current_scopes(self) -> t.Set[T.Scope]:
        return self._field_2_scopes[self._current_state['field']]
    
    # -------------------------------------------------------------------------
    
    @slot(str)
    @slot(str, str)
    def register_scope(self, scope: T.Scope, field: T.Field = None) -> None:
        self._field_2_scopes[field or self._current_field].add(scope)
    
    @slot(str, str, str, object, int)
    @slot(str, str, str, object, int, int)
    def register_func(
            self, scope: T.Scope, sid: T.SID, fid: T.FID, qobj: QObject,
            key: int, modifier: int = 0
    ) -> None:
        kid = self._compose_kid(key, modifier)
        self._current_scopes.add(scope)
        # self._current_state['kid_2_fid'][kid] = fid
        self._fid_2_qobj[fid] = qobj
        self._registered[scope][sid][kid] = fid
        if sid in self._current_state['active_sids']:
            self._current_state['kid_2_fid'][kid] = fid
        # print(':l', self._registered, self._current_state)
    
    # -------------------------------------------------------------------------
    
    @slot(str)
    def activate_field(self, field: T.Field) -> None:
        self._current_state['field'] = field
        self._current_state['kid_2_fid'].clear()
        for scope in self._current_scopes:
            if sid := self._current_state['scope_2_sid'].get(scope):
                self._current_state['kid_2_fid'].update(
                    self._registered[scope][sid]
                )
    
    @slot(str, str)
    def activate_scope(self, scope: T.Scope, sid: T.SID) -> None:
        if sid in self._current_state['active_sids']:
            return
        
        if last_sid := self._current_state['scope_2_sid'].get(scope):
            for kid in self._registered[scope][last_sid]:
                self._current_state['kid_2_fid'].pop(kid, None)
        
        self._current_state['scope_2_sid'][scope] = sid
        self._current_state['active_sids'].add(sid)
        self._current_state['kid_2_fid'].update(
            self._registered[scope][sid]
        )
        # print(':l', self._current_state)
    
    @slot(str, str)
    def deactivate_scope(self, scope: T.Scope, sid: T.SID) -> None:
        if sid not in self._current_state['active_sids']:
            return
        self._current_state['active_sids'].remove(sid)
        for kid in self._registered[scope][sid]:
            self._current_state['kid_2_fid'].pop(kid, None)
    
    # -------------------------------------------------------------------------
    
    @slot(int, int)
    def on_key(self, key: int, modifier: int) -> None:
        # import lk_logger
        # lk_logger.start_ipython({'key': key})
        kid = self._compose_kid(key, modifier)
        # print(':l', kid, self._current_state)
        if fid := self._current_state['kid_2_fid'].get(kid):
            qobj = self._fid_2_qobj[fid]
            qobj.triggered.emit(fid)
            # self.triggered.emit(fid)
    
    @staticmethod
    def _compose_kid(key: int, modifier: int) -> T.KID:
        return (key, (
            bool(modifier & Qt.ControlModifier),
            bool(modifier & Qt.ShiftModifier),
            bool(modifier & Qt.AltModifier),
        ))
