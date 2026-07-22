import pandas as pd
from triage.data.cleaning import (
    filter_english_tickets,
    drop_missing_and_duplicates,
    clean_text,
    build_text_input,
)


def test_filter_english_tickets_keeps_only_english():
    df = pd.DataFrame({
        'language': ['en', 'de', 'en', 'fr'],
        'value': [1, 2, 3, 4]
    })
    result = filter_english_tickets(df)
    assert len(result) == 2
    assert (result['language'] == 'en').all()


def test_drop_missing_and_duplicates_removes_nulls():
    df = pd.DataFrame({
        'subject': ['a', None, 'c'],
        'body': ['x', 'y', 'z'],
        'answer': ['p', 'q', 'r']
    })
    result = drop_missing_and_duplicates(df)
    assert len(result) == 2


def test_drop_missing_and_duplicates_removes_duplicate_bodies():
    df = pd.DataFrame({
        'subject': ['a', 'b'],
        'body': ['same text', 'same text'],
        'answer': ['p', 'q']
    })
    result = drop_missing_and_duplicates(df)
    assert len(result) == 1


def test_clean_text_strips_html_tags():
    result = clean_text("Hello<br><br>World")
    assert '<br>' not in result
    assert 'Hello' in result and 'World' in result


def test_clean_text_handles_nan():
    result = clean_text(float('nan'))
    assert pd.isna(result)


def test_build_text_input_combines_subject_and_body():
    df = pd.DataFrame({
        'subject': ['Issue'],
        'body': ['My device is broken'],
        'answer': ['We will help']
    })
    result = build_text_input(df)
    assert 'Issue' in result['text_input'].iloc[0]
    assert 'broken' in result['text_input'].iloc[0]