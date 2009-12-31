def human_readable(bytes):
    suffixes = ['b', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    current = bytes
    while current > 1024:
        current = current / 1024.0
        suffixes = suffixes[1:]
        assert suffixes, 'non realistic size encountered'
    return '%.1f%s' % (current, suffixes[0])
