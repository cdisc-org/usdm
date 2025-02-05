class Conditons:
    def __init__(self, conditon_info):
        self.items = []
        self.errors = []
        if conditon_info:
            parts = conditon_info.split(",")
            for part in parts:
                name_value = part.split(":")
                if len(name_value) == 2:
                    name = self._remove_unprintable(name_value[0])
                    condition = self._remove_unprintable(name_value[1])
                    self.items.append({"name": name, "condition": condition})
                else:
                    self.errors.append(
                        f"Could not decode a condition, no ':' found in '{part}'"
                    )
        else:
            pass  # Empty, this is OK

    def _remove_unprintable(self, text):
        return "".join(c for c in text if c.isprintable()).strip()
