def build_unique_name(name: str, id: str, prefix: str | None = None) -> tuple[str, str]:
    index = id.split("_")[-1]
    suffix = f"{prefix if prefix else ""}{"." if prefix else ""}{index}"
    return f"{name} ({suffix})", suffix