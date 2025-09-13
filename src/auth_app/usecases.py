def logout(session) -> bool:
    if session.get("user_id") is None:
        return False
    session.pop("user_id")
    return True
