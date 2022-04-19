from .base import Base


class Motion(Base):
    def _get_abbrs(self, name: str) -> (str, ...):
        if name.endswith('_m'):
            yield name[:-2]
