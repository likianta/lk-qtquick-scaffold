from .base import Base


class Font(Base):
    def _get_abbrs(self, name: str) -> (str, ...):
        if name.endswith('_m'):
            yield name[:-2]
        elif name.endswith('_default'):
            yield name[:-8]
