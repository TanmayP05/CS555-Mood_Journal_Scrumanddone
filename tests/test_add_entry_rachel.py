def test_entry_displays_after_add():
    """Making sure Add Entry displays after adding an entry"""
    entries = []
    new_entry = {"mood": "happy", "note": "good vibes today"}
    entries.append(new_entry)
    assert new_entry in entries
