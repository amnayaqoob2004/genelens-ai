def analyze_sequence(sequence):
    """
    Analyze a DNA sequence and return basic statistics:
    length, A/T/G/C counts, base percentages, and GC%.

    'sequence' should be a string of nucleotide letters (e.g. "ATGCGT...").
    """
    sequence = sequence.upper()
    length = len(sequence)

    if length == 0:
        return None

    a_count = sequence.count("A")
    t_count = sequence.count("T")
    g_count = sequence.count("G")
    c_count = sequence.count("C")

    known_bases = a_count + t_count + g_count + c_count
    ambiguous_count = length - known_bases

    # Percentages are calculated based on total sequence length
    a_percent = round((a_count / length) * 100, 2)
    t_percent = round((t_count / length) * 100, 2)
    g_percent = round((g_count / length) * 100, 2)
    c_percent = round((c_count / length) * 100, 2)

    # GC% = (G + C) / total length, a standard bioinformatics measure
    gc_percent = round(((g_count + c_count) / length) * 100, 2)

    return {
        "length": length,
        "a_count": a_count,
        "t_count": t_count,
        "g_count": g_count,
        "c_count": c_count,
        "ambiguous_count": ambiguous_count,
        "a_percent": a_percent,
        "t_percent": t_percent,
        "g_percent": g_percent,
        "c_percent": c_percent,
        "gc_percent": gc_percent,
    }