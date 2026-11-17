"""Markdown dosyalarını kullanıcının verdiği sırayla tek belgede birleştirir."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Section:
    """Bir markdown dosyasının içeriği."""

    name: str
    text: str


@dataclass
class MergedDocument:
    """Sırayla birleştirilmiş bölümler."""

    sections: list[Section]

    @property
    def markdown(self) -> str:
        return "\n\n---\n\n".join(s.text.strip() for s in self.sections)


def _read(path: Path) -> str:
    """Dosyayı okur; Türkçe karakterler için utf-8, sorun olursa latin-1 dener."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def merge_files(paths: list[str | Path]) -> MergedDocument:
    """Verilen yollardaki dosyaları sırayla okuyup birleştirir."""
    sections: list[Section] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            raise FileNotFoundError(f"Dosya bulunamadı: {path}")
        sections.append(Section(name=path.name, text=_read(path)))
    if not sections:
        raise ValueError("Hiç markdown dosyası verilmedi.")
    return MergedDocument(sections=sections)
