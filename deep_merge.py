def deep_merge(existing, update):
    if update is None:
        return None
    if isinstance(existing, dict) and isinstance(update, dict):
        result = dict(existing)
        for k, v in update.items():
            result[k] = deep_merge(existing.get(k), v)
        return result
    if isinstance(update, list):
        return list(update)
    return update
