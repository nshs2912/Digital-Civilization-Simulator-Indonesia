from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    author: str | None = None
    publication: str | None = None
    edition: str | None = None
    language: str | None = None
    publication_year: int | None = None
    citation: str | None = None
    provenance: str | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_id or not str(self.source_id).strip():
            errors.append("source_id is required")
        if not self.title or not str(self.title).strip():
            errors.append("title is required")
        if self.publication_year is not None and not isinstance(self.publication_year, int):
            errors.append("publication_year must be an integer or null")
        return errors
